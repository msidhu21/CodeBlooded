'use client';

import { useState, useEffect, useRef } from 'react';
import { apiClient } from '@/lib/api';
import type { PlacePrediction } from '@/types';

interface LocationAutocompleteProps {
  onSelect: (place: PlacePrediction) => void;
  placeholder?: string;
}

export default function LocationAutocomplete({ 
  onSelect, 
  placeholder = "Enter location..." 
}: LocationAutocompleteProps) {
  const [input, setInput] = useState('');
  const [predictions, setPredictions] = useState<PlacePrediction[]>([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (input.length < 2) {
      setPredictions([]);
      setShowDropdown(false);
      return;
    }

    const fetchPredictions = async () => {
      setLoading(true);
      try {
        const response = await apiClient.getPlaceAutocomplete(input);
        setPredictions(response.predictions);
        setShowDropdown(response.predictions.length > 0);
      } catch (error) {
        console.error('Error fetching places:', error);
        setPredictions([]);
        setShowDropdown(false);
      } finally {
        setLoading(false);
      }
    };

    const debounceTimer = setTimeout(fetchPredictions, 300);
    return () => clearTimeout(debounceTimer);
  }, [input]);

  const handleSelect = (place: PlacePrediction) => {
    setInput(place.description);
    setShowDropdown(false);
    onSelect(place);
  };

  return (
    <div style={{ position: 'relative', width: '100%' }} ref={dropdownRef}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={placeholder}
        className="input"
        onFocus={() => predictions.length > 0 && setShowDropdown(true)}
      />
      {loading && (
        <div style={{ position: 'absolute', right: '10px', top: '50%', transform: 'translateY(-50%)' }}>
          Loading...
        </div>
      )}
      {showDropdown && predictions.length > 0 && (
        <div
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            right: 0,
            background: 'white',
            border: '1px solid #ddd',
            borderRadius: '4px',
            marginTop: '4px',
            maxHeight: '200px',
            overflowY: 'auto',
            zIndex: 1000,
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          }}
        >
          {predictions.map((prediction, index) => (
            <div
              key={prediction.place_id}
              onClick={() => handleSelect(prediction)}
              style={{
                padding: '12px',
                cursor: 'pointer',
                borderBottom: index < predictions.length - 1 ? '1px solid #eee' : 'none',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#f5f5f5';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = 'white';
              }}
            >
              {prediction.description}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

