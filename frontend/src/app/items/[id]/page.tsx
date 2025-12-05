'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import type { Product } from '@/types';

export default function ItemDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const productId = params.id as string;

  const [product, setProduct] = useState<Product | null>(null);
  const [related, setRelated] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isInWishlist, setIsInWishlist] = useState(false);
  const [wishlistLoading, setWishlistLoading] = useState(false);

  useEffect(() => {
    const fetchItemDetails = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await apiClient.getItemDetails(productId);
        setProduct(response.product);
        setRelated(response.related);
        
        const wishlistCheck = await apiClient.checkWishlist(productId);
        setIsInWishlist(wishlistCheck.is_in_wishlist);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load product details');
      } finally {
        setLoading(false);
      }
    };

    if (productId) {
      fetchItemDetails();
    }
  }, [productId]);

  const handleWishlistToggle = async () => {
    if (!product) return;
    setWishlistLoading(true);
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
      setWishlistLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading product details...</div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="container">
        <div className="error">{error || 'Product not found'}</div>
        <Link href="/" className="btn btn-secondary" style={{ marginTop: '20px', display: 'inline-block' }}>
          Back to Search
        </Link>
      </div>
    );
  }

  return (
    <div className="container">
      <Link href="/" className="btn btn-secondary" style={{ marginBottom: '20px', display: 'inline-block' }}>
        ← Back to Search
      </Link>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '30px', marginBottom: '40px' }}>
        <div>
          {product.img_link && (
            <img
              src={product.img_link}
              alt={product.product_name}
              style={{
                width: '100%',
                borderRadius: '8px',
                boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
              }}
              onError={(e) => {
                (e.target as HTMLImageElement).src = 'https://via.placeholder.com/400x400?text=No+Image';
              }}
            />
          )}
        </div>

        <div>
          <h1 style={{ fontSize: '32px', marginBottom: '15px' }}>{product.product_name}</h1>
          
          <div style={{ marginBottom: '20px', padding: '15px', background: '#f8f9fa', borderRadius: '4px' }}>
            <div style={{ marginBottom: '10px' }}>
              <strong>Category:</strong> {product.category}
            </div>
            <div style={{ marginBottom: '10px' }}>
              {product.rating && (
                <>
                  <strong>Rating:</strong> {product.rating}
                  {product.rating_count && (
                    <span style={{ color: '#666', marginLeft: '5px' }}>
                      ({product.rating_count} reviews)
                    </span>
                  )}
                </>
              )}
            </div>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#0070f3' }}>
              {product.discounted_price && (
                <>
                  {product.discounted_price}
                  {product.actual_price && product.actual_price !== product.discounted_price && (
                    <>
                      <span style={{ marginLeft: '10px', fontSize: '18px', textDecoration: 'line-through', color: '#999', fontWeight: 'normal' }}>
                        {product.actual_price}
                      </span>
                      {product.discount_percentage && (
                        <span style={{ marginLeft: '10px', color: '#28a745', fontSize: '18px' }}>
                          {product.discount_percentage} off
                        </span>
                      )}
                    </>
                  )}
                </>
              )}
            </div>
          </div>

          {product.about_product && (
            <div style={{ marginBottom: '20px' }}>
              <h2 style={{ fontSize: '20px', marginBottom: '10px' }}>Description</h2>
              <p style={{ lineHeight: '1.6', color: '#555' }}>{product.about_product}</p>
            </div>
          )}

          <div style={{ display: 'flex', gap: '10px', marginTop: '20px', flexWrap: 'wrap' }}>
            <button
              onClick={handleWishlistToggle}
              disabled={wishlistLoading}
              style={{
                padding: '12px 24px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                background: isInWishlist ? '#ff6b6b' : '#fff',
                color: isInWishlist ? '#fff' : '#333',
                cursor: wishlistLoading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                fontWeight: '500',
              }}
            >
              {wishlistLoading ? '...' : isInWishlist ? '❤️ Remove from Wishlist' : '🤍 Add to Wishlist'}
            </button>
            {product.product_link && (
              <a
                href={product.product_link}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
                style={{ display: 'inline-block' }}
              >
                Open Product Link
              </a>
            )}
          </div>
        </div>
      </div>

      {related.length > 0 && (
        <section style={{ marginTop: '40px', paddingTop: '30px', borderTop: '2px solid #ddd' }}>
          <h2 style={{ marginBottom: '20px', fontSize: '24px' }}>Related Products</h2>
          <div className="grid">
            {related.map((relatedProduct) => (
              <ProductCard key={relatedProduct.product_id} product={relatedProduct} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}

