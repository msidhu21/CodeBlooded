'use client';

import Link from 'next/link';
import type { Product } from '@/types';

interface ProductCardProps {
  product: Product;
  showDetails?: boolean;
}

export default function ProductCard({ product, showDetails = true }: ProductCardProps) {
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
      {showDetails && (
        <Link
          href={`/items/${product.product_id}`}
          className="btn btn-primary"
          style={{ marginTop: 'auto', textAlign: 'center', display: 'block' }}
        >
          View Details
        </Link>
      )}
    </div>
  );
}

