'use client';

import React from 'react';
import { Product } from '@/types';
import ProductCard from './ProductCard';

interface NoResultsSuggestionsProps {
  originalQuery: string;
  similarCategories: string[];
  popularProducts: Product[];
  didYouMean: string[];
  onCategoryClick: (category: string) => void;
  onSuggestionClick: (suggestion: string) => void;
}

export default function NoResultsSuggestions({
  originalQuery,
  similarCategories,
  popularProducts,
  didYouMean,
  onCategoryClick,
  onSuggestionClick,
}: NoResultsSuggestionsProps) {
  return (
    <div className="space-y-8">
      {/* No Results Message */}
      <div className="card p-6 text-center">
        <h2 className="text-2xl font-bold mb-2">No Results Found</h2>
        <p className="text-gray-600">
          We couldn't find any products matching "{originalQuery}"
        </p>
      </div>

      {/* Did You Mean */}
      {didYouMean.length > 0 && (
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-3">Did you mean?</h3>
          <div className="flex flex-wrap gap-2">
            {didYouMean.map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => onSuggestionClick(suggestion)}
                className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Similar Categories */}
      {similarCategories.length > 0 && (
        <div className="card p-6">
          <h3 className="text-lg font-semibold mb-3">Similar Categories</h3>
          <p className="text-sm text-gray-600 mb-4">
            Try browsing these related categories:
          </p>
          <div className="flex flex-wrap gap-2">
            {similarCategories.map((category) => (
              <button
                key={category}
                onClick={() => onCategoryClick(category)}
                className="px-4 py-2 border border-primary text-primary rounded-lg hover:bg-primary hover:text-white transition-colors"
              >
                {category}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Popular Products */}
      {popularProducts.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold mb-4">Popular Products</h3>
          <p className="text-sm text-gray-600 mb-4">
            You might be interested in these trending products:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {popularProducts.map((product) => (
              <ProductCard key={product.product_id} product={product} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
