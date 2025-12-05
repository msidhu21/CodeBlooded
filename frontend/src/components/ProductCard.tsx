'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import type { Product } from '@/types';

interface ProductCardProps {
  product: Product;
  showDetails?: boolean;
}

export default function ProductCard({ product, showDetails = true }: ProductCardProps) {
  const [isInWishlist, setIsInWishlist] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const checkWishlist = async () => {
      try {
        const response = await apiClient.checkWishlist(product.product_id);
        setIsInWishlist(response.is_in_wishlist);
      } catch (error) {
        console.error('Error checking wishlist:', error);
      }
    };
    checkWishlist();
  }, [product.product_id]);

  const handleWishlistToggle = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setLoading(true);
    try {
      if (isInWishlist) {
        await apiClient.removeFromWishlist(product.product_id);
        setIsInWishlist(false);
      } else {
        await apiClient.addToWishlist(product.product_id);
        setIsInWishlist(true);
      }
    } catch (error) {
      console.error('Error updating wishlist:', error);
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="bg-white rounded-lg p-5 shadow-sm mb-5 h-full flex flex-col">
      {product.img_link && (
        <img
          src={product.img_link}
          alt={product.product_name}
          className="w-full h-[200px] object-cover rounded mb-4"
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://via.placeholder.com/300x200?text=No+Image';
          }}
        />
      )}
      <h3 className="mb-2.5 text-lg font-semibold">
        {product.product_name}
      </h3>
      <div className="mb-2.5 text-gray-600 text-sm">
        <strong>Category:</strong> {product.category}
      </div>
      <div className="mb-2.5">
        {product.discounted_price && (
          <span className="text-xl font-bold text-primary">
            {product.discounted_price}
          </span>
        )}
        {product.actual_price && product.actual_price !== product.discounted_price && (
          <span className="ml-2.5 line-through text-gray-400">
            {product.actual_price}
          </span>
        )}
        {product.discount_percentage && (
          <span className="ml-2.5 text-success font-bold">
            {product.discount_percentage} off
          </span>
        )}
      </div>
      {product.rating && (
        <div className="mb-4 text-sm">
          <strong>Rating:</strong> {product.rating}
          {product.rating_count && (
            <span className="text-gray-600 ml-1">
              ({product.rating_count} reviews)
            </span>
          )}
        </div>
      )}
      <div className="mt-auto flex flex-col gap-2.5">
        <button
          onClick={handleWishlistToggle}
          disabled={loading}
          className={`px-4 py-2 border rounded text-sm font-medium transition-colors ${
            isInWishlist 
              ? 'bg-red-500 text-white border-red-500 hover:bg-red-600' 
              : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
          } ${loading ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}`}
        >
          {loading ? '...' : isInWishlist ? '❤️ Remove from Wishlist' : '🤍 Add to Wishlist'}
        </button>
        {showDetails && (
          <Link
            href={`/items/${product.product_id}`}
            className="btn btn-primary text-center block"
          >
            View Details
          </Link>
        )}
      </div>
    </div>
  );
}

