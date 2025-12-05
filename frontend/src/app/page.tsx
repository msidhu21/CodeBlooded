'use client';

import React, { useState, useEffect } from 'react';
import { SearchResponse, Product } from '@/types';
import SearchFilters, { FilterState } from '@/components/SearchFilters';
import NoResultsSuggestions from '@/components/NoResultsSuggestions';
import ProductCard from '@/components/ProductCard';
import RecommendedList from '@/components/RecommendedList';
import ThemeToggle from '@/components/ThemeToggle';
import Link from 'next/link';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

export default function HomePage() {
  const [searchResponse, setSearchResponse] = useState<SearchResponse | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [suggestedProducts, setSuggestedProducts] = useState<Product[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  
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

  // Fetch categories and initial products on mount
  useEffect(() => {
    fetchCategories();
    performSearch(1); // Load all products by default
    
    // Check if user is logged in
    const user = localStorage.getItem('user');
    setIsLoggedIn(!!user);
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

  const fetchSuggestedProducts = async () => {
    try {
      // Fetch popular products (high rating, good discount)
      const params = new URLSearchParams();
      params.append('min_rating', '4.0');
      params.append('size', '8');
      params.append('page', '1');
      
      const response = await fetch(`${API_BASE_URL}/items/search?${params.toString()}`);
      if (response.ok) {
        const data: SearchResponse = await response.json();
        setSuggestedProducts(data.products);
      }
    } catch (err) {
      console.error('Failed to fetch suggested products:', err);
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
      
      // Fetch suggested products if no results found
      if (data.products.length === 0) {
        fetchSuggestedProducts();
      }
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
    const newCategories = filters.categories?.filter((cat: string) => cat !== categoryToRemove) || [];
    const newFilters = { ...filters, categories: newCategories, category: '' };
    setFilters(newFilters);
    setCurrentPage(1);
    performSearch(1, newFilters);
  };

  return (
    <div className="container mx-auto px-4 py-8 dark:bg-gray-900 min-h-screen transition-colors">
      <header className="mb-8 pb-6 border-b-2 border-gray-300 dark:border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold mb-2 dark:text-white">Product Catalog</h1>
            <p className="text-gray-600 dark:text-gray-400">Search and discover products with advanced filtering</p>
          </div>
          <div className="flex gap-3 items-center">
            <ThemeToggle />
            {isLoggedIn ? (
              <Link href="/profile">
                <button className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors" aria-label="Profile">
                  <svg className="w-6 h-6 text-gray-800 dark:text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </button>
              </Link>
            ) : (
              <>
                <Link href="/login">
                  <button className="px-6 py-2 text-blue-600 dark:text-blue-400 border-2 border-blue-600 dark:border-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900 transition-colors font-medium">
                    Login
                  </button>
                </Link>
                <Link href="/register">
                  <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    Sign Up
                  </button>
                </Link>
              </>
            )}
          </div>
        </div>
        
        {/* Search Bar */}
        <div className="flex gap-4 mb-4">
          <div className="flex-1">
            <input
              type="text"
              value={filters.query}
              onChange={(e) => {
                const newFilters = { ...filters, query: e.target.value };
                setFilters(newFilters);
              }}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSearch();
                }
              }}
              placeholder="Search by name, description, or category..."
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-lg"
            />
          </div>
          <button
            onClick={() => handleSearch()}
            disabled={isLoading}
            className="btn btn-primary px-8"
          >
            Search
          </button>
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

          {/* Browse All Products Heading */}
          {searchResponse && searchResponse.products.length > 0 && !filters.query && getActiveFiltersCount() === 0 && (
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Browse All Products</h2>
              <p className="text-gray-600 dark:text-gray-400 mt-1">Explore our complete catalog of {searchResponse.pagination.total_results} products</p>
            </div>
          )}

          {/* Search Metadata */}
          {searchResponse && searchResponse.products.length > 0 && (
            <div className="card p-4 mb-6">
              <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                <span>
                  Showing {searchResponse.pagination.total_results} results
                  {searchResponse.meta.search_time_ms && (
                    <span className="ml-2">
                      ({searchResponse.meta.search_time_ms.toFixed(2)}ms)
                    </span>
                  )}
                </span>
                {filters.compact && (
                  <span className="text-xs bg-gray-100 dark:bg-gray-700 dark:text-gray-300 px-2 py-1 rounded">
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

          {/* No Results Message */}
          {!isLoading && searchResponse && searchResponse.products.length === 0 && (
            <>
              <div className="card p-8 text-center mb-8">
                <div className="mb-4">
                  <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">No products found</h3>
                <p className="text-gray-600 mb-6">
                  {filters.query ? (
                    <>We couldn't find any products matching "<strong>{filters.query}</strong>"</>
                  ) : (
                    <>No products match your current filters</>
                  )}
                </p>
                <div className="space-y-4">
                  <p className="text-sm text-gray-500">Try:</p>
                  <ul className="text-sm text-gray-600 space-y-2">
                    <li>• Using different keywords</li>
                    <li>• Checking your spelling</li>
                    <li>• Using more general search terms</li>
                    {(filters.categories.length > 0 || filters.minRating || filters.minPrice || filters.maxPrice || filters.minDiscount) && (
                      <li>• Removing some filters</li>
                    )}
                  </ul>
                </div>
                {(filters.query || filters.categories.length > 0 || filters.minRating) && (
                  <button
                    onClick={() => {
                      setFilters({
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
                      performSearch(1, {
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
                    }}
                    className="btn mt-6"
                  >
                    Clear all filters
                  </button>
                )}
              </div>

              {/* Suggested Products */}
              {suggestedProducts.length > 0 && (
                <div className="mb-8">
                  <h3 className="text-xl font-semibold mb-4">You might also be interested in...</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {suggestedProducts.map((product: Product) => (
                      <ProductCard key={product.product_id} product={product} />
                    ))}
                  </div>
                </div>
              )}
            </>
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
        </div>

      <footer className="mt-12 pt-6 border-t-2 border-gray-300 text-center">
        <Link href="/admin" className="btn inline-block">
          Admin Dashboard
        </Link>
      </footer>
    </div>
  );
}

