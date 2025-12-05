'use client';

import Link from 'next/link';
import type { Product } from '@/types';

interface ProductCardProps {
  product: Product;
  showDetails?: boolean;
}

export default function ProductCard({ product, showDetails = true }: ProductCardProps) {
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
      {showDetails && (
        <Link
          href={`/items/${product.product_id}`}
          className="btn btn-primary mt-auto text-center block"
        >
          View Details
        </Link>
      )}
    </div>
  );
}

