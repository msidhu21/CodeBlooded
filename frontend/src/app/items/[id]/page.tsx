'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { apiClient } from '@/lib/api';
import ProductCard from '@/components/ProductCard';
import ThemeToggle from '@/components/ThemeToggle';
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
  const [isInCart, setIsInCart] = useState(false);
  const [cartLoading, setCartLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const user = localStorage.getItem('user');
    setIsLoggedIn(!!user);
    
    const fetchItemDetails = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const response = await apiClient.getItemDetails(productId);
        setProduct(response.product);
        setRelated(response.related);
        
        const wishlistCheck = await apiClient.checkWishlist(productId);
        setIsInWishlist(wishlistCheck.is_in_wishlist);
        
        const cartCheck = await apiClient.checkCart(productId);
        setIsInCart(cartCheck.is_in_cart);
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

  const handleCartToggle = async () => {
    if (!product) return;
    setCartLoading(true);
    try {
      if (isInCart) {
        await apiClient.removeFromCart(product.product_id);
        setIsInCart(false);
      } else {
        await apiClient.addToCart(product.product_id);
        setIsInCart(true);
      }
    } catch (error) {
      console.error('Error updating cart:', error);
    } finally {
      setCartLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen dark:bg-gray-900">
        {/* Top Navigation Bar */}
        <nav className="bg-blue-600 dark:bg-blue-800 shadow-lg sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between gap-4">
              <Link href="/">
                <h1 className="text-2xl font-bold text-white cursor-pointer">Shopping Website</h1>
              </Link>
              <div className="flex gap-3 items-center">
                <ThemeToggle />
                {isLoggedIn ? (
                  <>
                    <Link href="/wishlist">
                      <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Wishlist">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                      </button>
                    </Link>
                    <Link href="/cart">
                      <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Cart">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </button>
                    </Link>
                    <Link href="/profile">
                      <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Profile">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </button>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link href="/login">
                      <button className="px-4 py-2 text-white border-2 border-white rounded-lg hover:bg-white hover:text-blue-600 transition-colors font-medium">
                        Login
                      </button>
                    </Link>
                    <Link href="/register">
                      <button className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-gray-100 transition-colors font-medium">
                        Sign Up
                      </button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </nav>
        <div className="container mx-auto px-4 py-8">
          <div className="loading dark:text-white">Loading product details...</div>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen dark:bg-gray-900">
        {/* Top Navigation Bar */}
        <nav className="bg-blue-600 dark:bg-blue-800 shadow-lg sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between gap-4">
              <Link href="/">
                <h1 className="text-2xl font-bold text-white cursor-pointer">Shopping Website</h1>
              </Link>
              <div className="flex gap-3 items-center">
                <ThemeToggle />
                {isLoggedIn ? (
                  <>
                    <Link href="/wishlist">
                      <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Wishlist">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                      </button>
                    </Link>
                    <Link href="/cart">
                      <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Cart">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                        </svg>
                      </button>
                    </Link>
                    <Link href="/profile">
                      <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Profile">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                        </svg>
                      </button>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link href="/login">
                      <button className="px-4 py-2 text-white border-2 border-white rounded-lg hover:bg-white hover:text-blue-600 transition-colors font-medium">
                        Login
                      </button>
                    </Link>
                    <Link href="/register">
                      <button className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-gray-100 transition-colors font-medium">
                        Sign Up
                      </button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
        </nav>
        <div className="container mx-auto px-4 py-8">
          <div className="error dark:text-white">{error || 'Product not found'}</div>
          <Link href="/" className="btn btn-secondary" style={{ marginTop: '20px', display: 'inline-block' }}>
            Back to Search
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen dark:bg-gray-900">
      {/* Top Navigation Bar */}
      <nav className="bg-blue-600 dark:bg-blue-800 shadow-lg sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between gap-4">
            <Link href="/">
              <h1 className="text-2xl font-bold text-white cursor-pointer">Shopping Website</h1>
            </Link>
            <div className="flex gap-3 items-center">
              <ThemeToggle />
              {isLoggedIn ? (
                <>
                  <Link href="/wishlist">
                    <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Wishlist">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                      </svg>
                    </button>
                  </Link>
                  <Link href="/cart">
                    <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Cart">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                      </svg>
                    </button>
                  </Link>
                  <Link href="/profile">
                    <button className="p-2 rounded-lg bg-white bg-opacity-20 hover:bg-opacity-30 transition-colors" aria-label="Profile">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    </button>
                  </Link>
                </>
              ) : (
                <>
                  <Link href="/login">
                    <button className="px-4 py-2 text-white border-2 border-white rounded-lg hover:bg-white hover:text-blue-600 transition-colors font-medium">
                      Login
                    </button>
                  </Link>
                  <Link href="/register">
                    <button className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-gray-100 transition-colors font-medium">
                      Sign Up
                    </button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>
      <div className="container mx-auto px-4 py-8">
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
              onClick={handleCartToggle}
              disabled={cartLoading}
              style={{
                padding: '12px 24px',
                border: 'none',
                borderRadius: '4px',
                background: isInCart ? '#28a745' : '#0070f3',
                color: '#fff',
                cursor: cartLoading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                fontWeight: '600',
              }}
            >
              {cartLoading ? '...' : isInCart ? '✓ In Cart' : '🛒 Add to Cart'}
            </button>
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
    </div>
  );
}

