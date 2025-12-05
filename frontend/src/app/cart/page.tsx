'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import type { Product } from '@/types';

export default function CartPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCart = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.getCart();
      // The cart API returns an array directly
      setProducts(response as any);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load cart');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const calculateTotal = () => {
    return products.reduce((total, product) => {
      const priceStr = product.discounted_price || product.actual_price || '0';
      const price = parseFloat(priceStr.replace(/[^0-9.]/g, ''));
      return total + (isNaN(price) ? 0 : price);
    }, 0);
  };

  return (
    <div className="container mx-auto px-4 py-8 dark:bg-gray-900 min-h-screen">
      <header className="mb-8 pb-6 border-b-2 border-gray-300 dark:border-gray-700">
        <div className="flex justify-between items-center">
          <h1 className="text-4xl font-bold dark:text-white">Shopping Cart</h1>
          <Link href="/" className="btn btn-secondary">
            Back to Browse
          </Link>
        </div>
      </header>

      {error && <div className="error p-4 mb-6">{error}</div>}

      {loading ? (
        <div className="loading text-center py-12 dark:text-white">Loading cart...</div>
      ) : (
        <>
          {products.length > 0 ? (
            <>
              <div className="mb-6 text-gray-600 dark:text-gray-400 flex justify-between items-center">
                <span>
                  {products.length} item{products.length !== 1 ? 's' : ''} in your cart
                </span>
                <div className="text-2xl font-bold dark:text-white">
                  Total: ${calculateTotal().toFixed(2)}
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {products.map((product) => (
                  <ProductCard key={product.product_id} product={product} />
                ))}
              </div>
              <div className="mt-8 flex justify-end">
                <button className="btn btn-primary text-lg px-8 py-4">
                  Proceed to Checkout
                </button>
              </div>
            </>
          ) : (
            <div className="text-center py-16">
              <h2 className="text-2xl font-bold mb-3 dark:text-white">Your cart is empty</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                Add some products to your cart to get started!
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
