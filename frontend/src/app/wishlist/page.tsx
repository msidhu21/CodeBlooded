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
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8 pb-6 border-b-2 border-gray-300">
        <div className="flex justify-between items-center">
          <h1 className="text-4xl font-bold">My Wishlist</h1>
          <Link href="/" className="btn btn-secondary">
            Back to Browse
          </Link>
        </div>
      </header>

      {error && <div className="error p-4 mb-6">{error}</div>}

      {loading ? (
        <div className="loading text-center py-12">Loading wishlist...</div>
      ) : (
        <>
          {products.length > 0 ? (
            <>
              <div className="mb-6 text-gray-600">
                {products.length} item{products.length !== 1 ? 's' : ''} in your wishlist
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product) => (
                  <ProductCard key={product.product_id} product={product} />
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-16">
              <h2 className="text-2xl font-bold mb-3">Your wishlist is empty</h2>
              <p className="text-gray-600 mb-6">
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

