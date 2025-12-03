'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import ProductCard from './ProductCard';
import type { Product } from '@/types';

interface RecommendedListProps {
  query: string;
}

export default function RecommendedList({ query }: RecommendedListProps) {
  const [recommendations, setRecommendations] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!query || query.trim().length === 0) {
      setRecommendations([]);
      return;
    }

    const fetchRecommendations = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await apiClient.getRecommendations(query, 6);
        setRecommendations(response.items);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load recommendations');
        setRecommendations([]);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [query]);

  if (loading) {
    return (
      <section style={{ marginTop: '40px', paddingTop: '30px', borderTop: '2px solid #ddd' }}>
        <h2 style={{ marginBottom: '20px', fontSize: '24px' }}>Recommended for You</h2>
        <div className="loading">Loading recommendations...</div>
      </section>
    );
  }

  if (error || recommendations.length === 0) {
    return null;
  }

  return (
    <section style={{ marginTop: '40px', paddingTop: '30px', borderTop: '2px solid #ddd' }}>
      <h2 style={{ marginBottom: '20px', fontSize: '24px' }}>Recommended for You</h2>
      <p style={{ marginBottom: '20px', color: '#666' }}>
        Based on your search: &quot;{query}&quot;
      </p>
      <div className="grid">
        {recommendations.map((product) => (
          <ProductCard key={product.product_id} product={product} />
        ))}
      </div>
    </section>
  );
}

