'use client';

import React, { useState, useEffect } from 'react';
import { SearchResponse, Product } from '@/types';
import SearchFilters, { FilterState } from '@/components/SearchFilters';
import NoResultsSuggestions from '@/components/NoResultsSuggestions';
import ProductCard from '@/components/ProductCard';
import RecommendedList from '@/components/RecommendedList';
import Link from 'next/link';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export default function HomePage() {
  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  
  const [filters, setFilters] = useState<FilterState>({
    query: '',
    category: '',
    categories: [],
    minRating: '',
    maxRating: '',
    minPrice: '',
    maxPrice: '',
    minDiscount: '',
    compact: false,
  });

  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/items/categories/list`);
      if (response.ok) {
        const data = await response.json();
        setCategories(data.categories || []);
      }
    } catch (err) {
      console.error('Failed to fetch categories:', err);
    }
  };

  const performSearch = async (page: number = 1, customFilters?: FilterState) => {
    setIsLoading(true);
    setError(null);
    
    // Use provided filters or current state
    const searchFilters = customFilters || filters;
    
    try {
      const params = new URLSearchParams();
      
      // Add search query
      if (searchFilters.query) params.append('q', searchFilters.query);
      
      // Add category filter - handle both single category (backward compat) and multiple categories
      if (searchFilters.categories && searchFilters.categories.length > 0) {
        // For multiple categories, we'll filter by joining them
        // The backend will match if any of these categories are found in the product's category string
        // We'll send the first category and the others will be filtered client-side for now
        // TODO: Update backend to support multiple category filters
        params.append('category', searchFilters.categories[0]);
      } else if (searchFilters.category) {
        params.append('category', searchFilters.category);
      }
      
      // Add rating filters
      if (searchFilters.minRating) params.append('min_rating', searchFilters.minRating);
      if (searchFilters.maxRating) params.append('max_rating', searchFilters.maxRating);
      
      // Add price filters
      if (searchFilters.minPrice) params.append('min_price', searchFilters.minPrice);
      if (searchFilters.maxPrice) params.append('max_price', searchFilters.maxPrice);
      
      // Add discount filter
      if (searchFilters.minDiscount) params.append('min_discount', searchFilters.minDiscount);
      
      // Add pagination
      params.append('page', page.toString());
      params.append('size', '20');
      
      // Add compact mode
      if (searchFilters.compact) params.append('compact', 'true');
      
      const response = await fetch(`${API_BASE_URL}/items/search?${params.toString()}`);
      
      if (!response.ok) {
        throw new Error(`Search failed: ${response.status}`);
      }
      
      const data: SearchResponse = await response.json();
      setSearchResponse(data);
      setCurrentPage(page);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
      console.error('Search error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = (customFilters?: FilterState) => {
    setCurrentPage(1);
    performSearch(1, customFilters);
  };

  const handlePageChange = (newPage: number) => {
    performSearch(newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCategoryClick = (category: string) => {
    const newFilters = { ...filters, category, query: '' };
    setFilters(newFilters);
    setCurrentPage(1);
    performSearch(1, newFilters);
  };

  const handleSuggestionClick = (suggestion: string) => {
    const newFilters = { ...filters, query: suggestion };
    setFilters(newFilters);
    setCurrentPage(1);
    performSearch(1, newFilters);
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (filters.query) count++;
    if (filters.categories && filters.categories.length > 0) count += filters.categories.length;
    else if (filters.category) count++;
    if (filters.minRating) count++;
    if (filters.maxRating) count++;
    if (filters.minPrice) count++;
    if (filters.maxPrice) count++;
    if (filters.minDiscount) count++;
    return count;
  };

  const clearFilter = (filterKey: keyof FilterState) => {
    const newFilters = { ...filters, [filterKey]: filterKey === 'categories' ? [] : '' };
    setFilters(newFilters);
    setCurrentPage(1);
    performSearch(1, newFilters);
  };

  const removeCategoryFromFilter = (categoryToRemove: string) => {
    const newCategories = filters.categories?.filter(cat => cat !== categoryToRemove) || [];
    const newFilters = { ...filters, categories: newCategories, category: '' };
    setFilters(newFilters);
    setCurrentPage(1);
    performSearch(1, newFilters);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8 pb-6 border-b-2 border-gray-300">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold mb-2">Product Catalog</h1>
            <p className="text-gray-600">Search and discover products with advanced filtering</p>
          </div>
          <SearchFilters
            filters={filters}
            onFiltersChange={setFilters}
            onSearch={handleSearch}
            categories={categories}
            isLoading={isLoading}
          />
        </div>
      </header>
      
      <div>
        {/* Active Filters Display */}
          {getActiveFiltersCount() > 0 && searchResponse && (
            <div className="card p-4 mb-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold">Active Filters ({getActiveFiltersCount()})</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {filters.query && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                    Search: {filters.query}
                    <button
                      onClick={() => clearFilter('query')}
                      className="ml-2 hover:text-gray-200"
                    >
                      ×
                    </button>
                  </span>
                )}
                {/* Show multiple categories as chips */}
                {filters.categories && filters.categories.length > 0 ? (
                  filters.categories.map((cat) => {
                    const displayName = cat.split('|').pop() || cat;
                    return (
                      <span key={cat} className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                        {displayName}
                        <button
                          onClick={() => removeCategoryFromFilter(cat)}
                          className="ml-2 hover:text-gray-200"
                        >
                          ×
                        </button>
                      </span>
                    );
                  })
                ) : filters.category ? (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                    Category: {filters.category}
                    <button
                      onClick={() => clearFilter('category')}
                      className="ml-2 hover:text-gray-200"
                    >
                      ×
                    </button>
                  </span>
                ) : null}
                {filters.minRating && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                    Min Rating: {filters.minRating}
                    <button
                      onClick={() => clearFilter('minRating')}
                      className="ml-2 hover:text-gray-200"
                    >
                      ×
                    </button>
                  </span>
                )}
                {filters.maxRating && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                    Max Rating: {filters.maxRating}
                    <button
                      onClick={() => clearFilter('maxRating')}
                      className="ml-2 hover:text-gray-200"
                    >
                      ×
                    </button>
                  </span>
                )}
                {filters.minPrice && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                    Min Price: ₹{filters.minPrice}
                    <button
                      onClick={() => clearFilter('minPrice')}
                      className="ml-2 hover:text-gray-200"
                    >
                      ×
                    </button>
                  </span>
                )}
                {filters.maxPrice && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                    Max Price: ₹{filters.maxPrice}
                    <button
                      onClick={() => clearFilter('maxPrice')}
                      className="ml-2 hover:text-gray-200"
                    >
                      ×
                    </button>
                  </span>
                )}
                {filters.minDiscount && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary text-white">
                    Min Discount: {filters.minDiscount}%
                    <button
                      onClick={() => clearFilter('minDiscount')}
                      className="ml-2 hover:text-gray-200"
                    >
                      ×
                    </button>
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Search Metadata */}
          {searchResponse && searchResponse.products.length > 0 && (
            <div className="card p-4 mb-6">
              <div className="flex items-center justify-between text-sm text-gray-600">
                <span>
                  Showing {searchResponse.pagination.total_results} results
                  {searchResponse.meta.search_time_ms && (
                    <span className="ml-2">
                      ({searchResponse.meta.search_time_ms.toFixed(2)}ms)
                    </span>
                  )}
                </span>
                {filters.compact && (
                  <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                    Compact View
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="error p-4 mb-6">
              <p>{error}</p>
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="loading text-center py-12">
              <p>Searching...</p>
            </div>
          )}

          {/* No Results with Suggestions */}
          {!isLoading && searchResponse && searchResponse.products.length === 0 && searchResponse.suggestions && (
            <NoResultsSuggestions
              originalQuery={searchResponse.suggestions.original_query}
              similarCategories={searchResponse.suggestions.similar_categories}
              popularProducts={searchResponse.suggestions.popular_products}
              didYouMean={searchResponse.suggestions.did_you_mean}
              onCategoryClick={handleCategoryClick}
              onSuggestionClick={handleSuggestionClick}
            />
          )}

          {/* Results Grid */}
          {!isLoading && searchResponse && searchResponse.products.length > 0 && (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-6">
                {searchResponse.products.map((product: Product) => (
                  <ProductCard key={product.product_id} product={product} />
                ))}
              </div>

              {/* Pagination */}
              {searchResponse.pagination.total_pages > 1 && (
                <div className="card p-4 mb-6">
                  <div className="flex items-center justify-between">
                    <button
                      onClick={() => handlePageChange(currentPage - 1)}
                      disabled={currentPage === 1}
                      className="btn disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Previous
                    </button>
                    
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-gray-600">
                        Page {currentPage} of {searchResponse.pagination.total_pages}
                      </span>
                    </div>
                    
                    <button
                      onClick={() => handlePageChange(currentPage + 1)}
                      disabled={!searchResponse.pagination.has_more}
                      className="btn disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      Next
                    </button>
                  </div>
                </div>
              )}

              {/* Recommendations Section */}
              {filters.query && (
                <RecommendedList query={filters.query} />
              )}
            </>
          )}

          {/* Initial State */}
          {!isLoading && !searchResponse && (
            <div className="card p-12 text-center">
              <h2 className="text-xl font-semibold mb-2">Welcome to Product Catalog</h2>
              <p className="text-gray-600 mb-4">
                Use the filters on the left to find products, or browse all items
              </p>
              <button
                onClick={() => performSearch(1)}
                className="btn btn-primary"
              >
                Browse All Products
              </button>
            </div>
          )}
        </div>

      <footer className="mt-12 pt-6 border-t-2 border-gray-300 text-center">
        <Link href="/admin" className="btn inline-block">
          Admin Dashboard
        </Link>
      </footer>
    </div>
  );
}

