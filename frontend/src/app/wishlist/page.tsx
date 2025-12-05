'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import type { Product } from '@/types';

export default function WishlistPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchWishlist = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.getWishlist();
      setProducts(response.products);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load wishlist');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWishlist();
  }, []);

  return (
    <div className="container">
      <header style={{ marginBottom: '30px', paddingBottom: '20px', borderBottom: '2px solid #ddd' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '32px' }}>My Wishlist</h1>
          <Link href="/" className="btn btn-secondary">
            Back to Browse
          </Link>
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      {loading ? (
        <div className="loading">Loading wishlist...</div>
      ) : (
        <>
          {products.length > 0 ? (
            <>
              <div style={{ marginBottom: '20px', color: '#666' }}>
                {products.length} item{products.length !== 1 ? 's' : ''} in your wishlist
              </div>
              <div className="grid">
                {products.map((product) => (
                  <ProductCard key={product.product_id} product={product} />
                ))}
              </div>
            </>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <h2 style={{ fontSize: '24px', marginBottom: '10px' }}>Your wishlist is empty</h2>
              <p style={{ color: '#666', marginBottom: '20px' }}>
                Start adding products to your wishlist to save them for later!
              </p>
              <Link href="/" className="btn btn-primary">
                Browse Products
              </Link>
            </div>
          )}
        </>
      )}
    </div>
  );
}

