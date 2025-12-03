'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import type { Product } from '@/types';
import Link from 'next/link';
import AdminLogin from '@/components/AdminLogin';

export default function AdminDashboard() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [items, setItems] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState({
    totalItems: 0,
    mostCommonCategory: '',
    totalCategories: 0,
  });
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<Partial<Product>>({});

  useEffect(() => {
    const token = localStorage.getItem('adminToken');
    if (token === 'admin') {
      setIsAuthenticated(true);
      fetchItems();
      fetchStats();
    }
  }, []);

  if (!isAuthenticated) {
    return (
      <div className="container">
        <AdminLogin onLogin={(token) => {
          setIsAuthenticated(true);
          fetchItems();
          fetchStats();
        }} />
      </div>
    );
  }

  const fetchItems = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getAllItems();
      setItems(response.products);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load items');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await apiClient.getAllItems();
      const products = response.products;
      
      const categoryCount: Record<string, number> = {};
      products.forEach((product) => {
        const cat = product.category || 'Uncategorized';
        categoryCount[cat] = (categoryCount[cat] || 0) + 1;
      });
      
      const mostCommon = Object.entries(categoryCount).sort((a, b) => b[1] - a[1])[0];
      
      setStats({
        totalItems: products.length,
        mostCommonCategory: mostCommon ? mostCommon[0] : 'N/A',
        totalCategories: Object.keys(categoryCount).length,
      });
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handleDelete = async (productId: string) => {
    if (!confirm('Are you sure you want to delete this item?')) {
      return;
    }

    try {
      await apiClient.deleteItem(productId);
      setItems(items.filter((item) => item.product_id !== productId));
      fetchStats(); // Refresh stats
    } catch (err) {
      alert('Failed to delete item: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  const handleEdit = (product: Product) => {
    setEditingId(product.product_id);
    setEditForm({
      product_name: product.product_name,
      category: product.category,
    });
  };

  const handleSaveEdit = async (productId: string) => {
    try {
      await apiClient.updateItem(productId, editForm);
      setEditingId(null);
      setEditForm({});
      fetchItems();
    } catch (err) {
      alert('Failed to update item: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setEditForm({});
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">Loading admin dashboard...</div>
      </div>
    );
  }

  return (
    <div className="container">
      <header style={{ marginBottom: '30px', paddingBottom: '20px', borderBottom: '2px solid #ddd' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '32px' }}>Admin Dashboard</h1>
          <Link href="/" className="btn btn-secondary">
            Back to Browse
          </Link>
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      {/* System Monitoring Section */}
      <section className="card" style={{ marginBottom: '30px' }}>
        <h2 style={{ marginBottom: '20px', fontSize: '24px' }}>System Monitoring</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
          <div>
            <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>Total Items</div>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#0070f3' }}>
              {stats.totalItems}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>Total Categories</div>
            <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#28a745' }}>
              {stats.totalCategories}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '14px', color: '#666', marginBottom: '5px' }}>Most Common Category</div>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#333' }}>
              {stats.mostCommonCategory}
            </div>
          </div>
        </div>
      </section>

      {/* Items Table */}
      <section className="card">
        <h2 style={{ marginBottom: '20px', fontSize: '24px' }}>Items Management</h2>
        
        {items.length === 0 ? (
          <div className="loading">No items found</div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #ddd', textAlign: 'left' }}>
                  <th style={{ padding: '12px' }}>ID</th>
                  <th style={{ padding: '12px' }}>Name</th>
                  <th style={{ padding: '12px' }}>Category</th>
                  <th style={{ padding: '12px' }}>Price</th>
                  <th style={{ padding: '12px' }}>Rating</th>
                  <th style={{ padding: '12px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.product_id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '12px' }}>{item.product_id}</td>
                    <td style={{ padding: '12px' }}>
                      {editingId === item.product_id ? (
                        <input
                          type="text"
                          value={editForm.product_name || ''}
                          onChange={(e) => setEditForm({ ...editForm, product_name: e.target.value })}
                          className="input"
                          style={{ width: '100%' }}
                        />
                      ) : (
                        item.product_name
                      )}
                    </td>
                    <td style={{ padding: '12px' }}>
                      {editingId === item.product_id ? (
                        <input
                          type="text"
                          value={editForm.category || ''}
                          onChange={(e) => setEditForm({ ...editForm, category: e.target.value })}
                          className="input"
                          style={{ width: '100%' }}
                        />
                      ) : (
                        item.category
                      )}
                    </td>
                    <td style={{ padding: '12px' }}>
                      {item.discounted_price || item.actual_price || 'N/A'}
                    </td>
                    <td style={{ padding: '12px' }}>
                      {item.rating || 'N/A'}
                    </td>
                    <td style={{ padding: '12px' }}>
                      {editingId === item.product_id ? (
                        <div style={{ display: 'flex', gap: '5px' }}>
                          <button
                            onClick={() => handleSaveEdit(item.product_id)}
                            className="btn btn-primary"
                            style={{ fontSize: '12px', padding: '5px 10px' }}
                          >
                            Save
                          </button>
                          <button
                            onClick={handleCancelEdit}
                            className="btn btn-secondary"
                            style={{ fontSize: '12px', padding: '5px 10px' }}
                          >
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <div style={{ display: 'flex', gap: '5px' }}>
                          <button
                            onClick={() => handleEdit(item)}
                            className="btn btn-primary"
                            style={{ fontSize: '12px', padding: '5px 10px' }}
                          >
                            Edit
                          </button>
                          <button
                            onClick={() => handleDelete(item.product_id)}
                            className="btn btn-danger"
                            style={{ fontSize: '12px', padding: '5px 10px' }}
                          >
                            Delete
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}

