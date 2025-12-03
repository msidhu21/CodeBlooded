'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import SearchBar from '@/components/SearchBar';
import LocationAutocomplete from '@/components/LocationAutocomplete';
import CategoryDropdown from '@/components/CategoryDropdown';
import ProductCard from '@/components/ProductCard';
import RecommendedList from '@/components/RecommendedList';
import { apiClient } from '@/lib/api';
import type { Product, PlacePrediction } from '@/types';
import Link from 'next/link';

export default function BrowsePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(
    searchParams.get('category') || null
  );
  const [selectedLocation, setSelectedLocation] = useState<PlacePrediction | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    total_pages: 1,
    total_results: 0,
  });

  const performSearch = async (query: string, category: string | null, page: number = 1) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.searchItems({
        q: query || undefined,
        category: category || undefined,
        page,
        size: 12,
      });
      
      setProducts(response.products);
      setPagination({
        page: response.pagination.page,
        total_pages: response.pagination.total_pages,
        total_results: response.pagination.total_results,
      });
      
      // Update URL
      const params = new URLSearchParams();
      if (query) params.set('q', query);
      if (category) params.set('category', category);
      if (page > 1) params.set('page', String(page));
      router.push(`/?${params.toString()}`, { scroll: false });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search products');
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    performSearch(searchQuery, selectedCategory, 1);
  }, []);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    performSearch(query, selectedCategory, 1);
  };

  const handleCategoryChange = (category: string | null) => {
    setSelectedCategory(category);
    performSearch(searchQuery, category, 1);
  };

  const handleLocationSelect = (place: PlacePrediction) => {
    setSelectedLocation(place);
    // Location is selected but doesn't affect search - just for demo
    console.log('Selected location:', place);
  };

  const handlePageChange = (newPage: number) => {
    performSearch(searchQuery, selectedCategory, newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="container">
      <header style={{ marginBottom: '30px', paddingBottom: '20px', borderBottom: '2px solid #ddd' }}>
        <h1 style={{ fontSize: '32px', marginBottom: '20px' }}>Product Catalog</h1>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <SearchBar onSearch={handleSearch} initialQuery={searchQuery} />
          
          <div style={{ display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
            <div style={{ flex: '1', minWidth: '200px' }}>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
                Location:
              </label>
              <LocationAutocomplete onSelect={handleLocationSelect} />
            </div>
            
            <div style={{ flex: '1', minWidth: '200px' }}>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
                Category:
              </label>
              <CategoryDropdown 
                onSelect={handleCategoryChange} 
                selectedCategory={selectedCategory}
              />
            </div>
          </div>
        </div>
      </header>

      {selectedLocation && (
        <div style={{ marginBottom: '20px', padding: '10px', background: '#e7f3ff', borderRadius: '4px' }}>
          <strong>Selected Location:</strong> {selectedLocation.description}
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {loading ? (
        <div className="loading">Loading products...</div>
      ) : (
        <>
          {products.length > 0 ? (
            <>
              <div style={{ marginBottom: '20px', color: '#666' }}>
                Found {pagination.total_results} product{pagination.total_results !== 1 ? 's' : ''}
              </div>
              
              <div className="grid">
                {products.map((product) => (
                  <ProductCard key={product.product_id} product={product} />
                ))}
              </div>

              {pagination.total_pages > 1 && (
                <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '30px' }}>
                  <button
                    onClick={() => handlePageChange(pagination.page - 1)}
                    disabled={pagination.page === 1}
                    className="btn btn-secondary"
                  >
                    Previous
                  </button>
                  <span style={{ padding: '10px 20px', display: 'flex', alignItems: 'center' }}>
                    Page {pagination.page} of {pagination.total_pages}
                  </span>
                  <button
                    onClick={() => handlePageChange(pagination.page + 1)}
                    disabled={pagination.page >= pagination.total_pages}
                    className="btn btn-secondary"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="loading">
              {searchQuery ? 'No products found. Try a different search.' : 'Start searching for products!'}
            </div>
          )}

          {/* Recommendations Section - Individual Feature */}
          {searchQuery && (
            <RecommendedList query={searchQuery} />
          )}
        </>
      )}

      <footer style={{ marginTop: '40px', paddingTop: '20px', borderTop: '2px solid #ddd', textAlign: 'center' }}>
        <Link href="/admin" className="btn btn-secondary" style={{ display: 'inline-block' }}>
          Admin Dashboard
        </Link>
      </footer>
    </div>
  );
}

