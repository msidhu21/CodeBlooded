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
    <div className="card" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {product.img_link && (
        <img
          src={product.img_link}
          alt={product.product_name}
          style={{
            width: '100%',
            height: '200px',
            objectFit: 'cover',
            borderRadius: '4px',
            marginBottom: '15px',
          }}
          onError={(e) => {
            (e.target as HTMLImageElement).src = 'https://via.placeholder.com/300x200?text=No+Image';
          }}
        />
      )}
      <h3 style={{ marginBottom: '10px', fontSize: '18px', fontWeight: '600' }}>
        {product.product_name}
      </h3>
      <div style={{ marginBottom: '10px', color: '#666', fontSize: '14px' }}>
        <strong>Category:</strong> {product.category}
      </div>
      <div style={{ marginBottom: '10px' }}>
        {product.discounted_price && (
          <span style={{ fontSize: '20px', fontWeight: 'bold', color: '#0070f3' }}>
            {product.discounted_price}
          </span>
        )}
        {product.actual_price && product.actual_price !== product.discounted_price && (
          <span style={{ marginLeft: '10px', textDecoration: 'line-through', color: '#999' }}>
            {product.actual_price}
          </span>
        )}
        {product.discount_percentage && (
          <span style={{ marginLeft: '10px', color: '#28a745', fontWeight: 'bold' }}>
            {product.discount_percentage} off
          </span>
        )}
      </div>
      {product.rating && (
        <div style={{ marginBottom: '15px', fontSize: '14px' }}>
          <strong>Rating:</strong> {product.rating}
          {product.rating_count && (
            <span style={{ color: '#666', marginLeft: '5px' }}>
              ({product.rating_count} reviews)
            </span>
          )}
        </div>
      )}
      <div style={{ marginTop: 'auto', display: 'flex', gap: '10px', flexDirection: 'column' }}>
        <button
          onClick={handleWishlistToggle}
          disabled={loading}
          style={{
            padding: '8px 16px',
            border: '1px solid #ddd',
            borderRadius: '4px',
            background: isInWishlist ? '#ff6b6b' : '#fff',
            color: isInWishlist ? '#fff' : '#333',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '14px',
            fontWeight: '500',
          }}
        >
          {loading ? '...' : isInWishlist ? '❤️ Remove from Wishlist' : '🤍 Add to Wishlist'}
        </button>
        {showDetails && (
          <Link
            href={`/items/${product.product_id}`}
            className="btn btn-primary"
            style={{ textAlign: 'center', display: 'block' }}
          >
            View Details
          </Link>
        )}
      </div>
    </div>
  );
}

