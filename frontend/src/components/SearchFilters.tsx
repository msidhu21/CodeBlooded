'use client';

import React, { useState, useEffect } from 'react';

export interface FilterState {
  query: string;
  category: string;
  minRating: string;
  maxRating: string;
  minPrice: string;
  maxPrice: string;
  minDiscount: string;
  compact: boolean;
}

interface SearchFiltersProps {
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  onSearch: () => void;
  categories: string[];
  isLoading?: boolean;
}

export default function SearchFilters({
  filters,
  onFiltersChange,
  onSearch,
  categories,
  isLoading = false,
}: SearchFiltersProps) {
  const [localFilters, setLocalFilters] = useState<FilterState>(filters);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  const handleInputChange = (field: keyof FilterState, value: string | boolean) => {
    setLocalFilters({ ...localFilters, [field]: value });
  };

  const handleApplyFilters = () => {
    onFiltersChange(localFilters);
    onSearch();
  };

  const handleReset = () => {
    const resetFilters: FilterState = {
      query: '',
      category: '',
      minRating: '',
      maxRating: '',
      minPrice: '',
      maxPrice: '',
      minDiscount: '',
      compact: false,
    };
    setLocalFilters(resetFilters);
    onFiltersChange(resetFilters);
    onSearch();
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleApplyFilters();
    }
  };

  return (
    <div className="card p-6 mb-6">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between text-xl font-bold mb-4 hover:text-primary transition-colors"
      >
        <span>Search & Filters</span>
        <span className="text-2xl">{isExpanded ? '−' : '+'}</span>
      </button>

      {!isExpanded && (
        <p className="text-sm text-gray-600 mb-4">
          Click to expand filters
        </p>
      )}

      {isExpanded && (
        <div>

      {/* Search Input */}
      <div className="mb-4">
        <label htmlFor="search" className="block text-sm font-medium mb-2">
          Search Products
        </label>
        <input
          id="search"
          type="text"
          value={localFilters.query}
          onChange={(e) => handleInputChange('query', e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Search by name, description, or category..."
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          disabled={isLoading}
        />
      </div>

      {/* Category Filter */}
      <div className="mb-4">
        <label htmlFor="category" className="block text-sm font-medium mb-2">
          Category
        </label>
        <select
          id="category"
          value={localFilters.category}
          onChange={(e) => handleInputChange('category', e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          disabled={isLoading}
        >
          <option value="">All Categories</option>
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {/* Rating Filters */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="minRating" className="block text-sm font-medium mb-2">
            Min Rating
          </label>
          <input
            id="minRating"
            type="number"
            min="0"
            max="5"
            step="0.1"
            value={localFilters.minRating}
            onChange={(e) => handleInputChange('minRating', e.target.value)}
            placeholder="0.0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
        <div>
          <label htmlFor="maxRating" className="block text-sm font-medium mb-2">
            Max Rating
          </label>
          <input
            id="maxRating"
            type="number"
            min="0"
            max="5"
            step="0.1"
            value={localFilters.maxRating}
            onChange={(e) => handleInputChange('maxRating', e.target.value)}
            placeholder="5.0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
      </div>

      {/* Price Filters */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="minPrice" className="block text-sm font-medium mb-2">
            Min Price (₹)
          </label>
          <input
            id="minPrice"
            type="number"
            min="0"
            step="1"
            value={localFilters.minPrice}
            onChange={(e) => handleInputChange('minPrice', e.target.value)}
            placeholder="0"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
        <div>
          <label htmlFor="maxPrice" className="block text-sm font-medium mb-2">
            Max Price (₹)
          </label>
          <input
            id="maxPrice"
            type="number"
            min="0"
            step="1"
            value={localFilters.maxPrice}
            onChange={(e) => handleInputChange('maxPrice', e.target.value)}
            placeholder="No limit"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            disabled={isLoading}
          />
        </div>
      </div>

      {/* Discount Filter */}
      <div className="mb-4">
        <label htmlFor="minDiscount" className="block text-sm font-medium mb-2">
          Min Discount (%)
        </label>
        <input
          id="minDiscount"
          type="number"
          min="0"
          max="100"
          step="1"
          value={localFilters.minDiscount}
          onChange={(e) => handleInputChange('minDiscount', e.target.value)}
          placeholder="0"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          disabled={isLoading}
        />
      </div>

      {/* Compact View Toggle */}
      <div className="mb-6">
        <label className="flex items-center cursor-pointer">
          <input
            type="checkbox"
            checked={localFilters.compact}
            onChange={(e) => handleInputChange('compact', e.target.checked)}
            className="mr-2 w-4 h-4"
            disabled={isLoading}
          />
          <span className="text-sm font-medium">Compact View (Hide Descriptions)</span>
        </label>
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleApplyFilters}
          disabled={isLoading}
          className="btn btn-primary flex-1"
        >
          {isLoading ? 'Searching...' : 'Apply Filters'}
        </button>
        <button
          onClick={handleReset}
          disabled={isLoading}
          className="btn flex-1"
        >
          Reset
        </button>
      </div>
        </div>
      )}
    </div>
  );
}
