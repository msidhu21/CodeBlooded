'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

interface CategoryDropdownProps {
  onSelect: (category: string | null) => void;
  selectedCategory?: string | null;
}

export default function CategoryDropdown({ onSelect, selectedCategory }: CategoryDropdownProps) {
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await apiClient.getCategories();
        setCategories(response.categories);
      } catch (error) {
        console.error('Error fetching categories:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  if (loading) {
    return <div>Loading categories...</div>;
  }

  return (
    <select
      value={selectedCategory || ''}
      onChange={(e) => onSelect(e.target.value || null)}
      className="input"
      style={{ minWidth: '200px' }}
    >
      <option value="">All Categories</option>
      {categories.map((category) => (
        <option key={category} value={category}>
          {category}
        </option>
      ))}
    </select>
  );
}

