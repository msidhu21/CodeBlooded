"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import styles from "./dashboard.module.css";

interface User {
  user_id: string;
  email: string;
  name: string;
  role: string;
  picture: string;
  contact_email: string;
  contact_phone: string;
  location: string;
}

interface SystemStats {
  totalUsers: number;
  totalProducts: number;
  activeUsers: number;
}

export default function AdminDashboard() {
  const [users, setUsers] = useState<User[]>([]);
  const [searchEmail, setSearchEmail] = useState("");
  const [wishlistEmail, setWishlistEmail] = useState("");
  const [wishlistStats, setWishlistStats] = useState<any>(null);
  const [systemStats, setSystemStats] = useState<SystemStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    // Check if admin is logged in
    const admin = localStorage.getItem('admin');
    if (!admin) {
      window.location.href = '/admin/login';
      return;
    }

    fetchUsers();
    fetchSystemStats();
  }, []);

  async function fetchUsers() {
    try {
      const res = await fetch('http://127.0.0.1:8000/admin/users');
      if (res.ok) {
        const data = await res.json();
        setUsers(data.users || []);
      }
    } catch (err) {
      console.error('Failed to fetch users:', err);
    }
    setLoading(false);
  }

  async function fetchSystemStats() {
    try {
      const res = await fetch('http://127.0.0.1:8000/admin/stats');
      if (res.ok) {
        const data = await res.json();
        setSystemStats(data);
      }
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  }

  async function handleDeleteUser() {
    if (!searchEmail) {
      setMessage("Please enter an email");
      return;
    }

    if (!confirm(`Are you sure you want to delete user: ${searchEmail}?`)) {
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/admin/users/${searchEmail}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        setMessage(`User ${searchEmail} deleted successfully`);
        setSearchEmail("");
        fetchUsers();
        fetchSystemStats();
      } else {
        const error = await res.text();
        setMessage(`Failed to delete: ${error}`);
      }
    } catch (err: any) {
      setMessage(`Error: ${err.message}`);
    }
  }

  async function handleGetWishlistStats() {
    if (!wishlistEmail) {
      setMessage("Please enter an email for wishlist stats");
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/admin/wishlist/${wishlistEmail}`);
      if (res.ok) {
        const data = await res.json();
        setWishlistStats(data);
        setMessage("");
      } else {
        setMessage("User not found or no wishlist data");
        setWishlistStats(null);
      }
    } catch (err: any) {
      setMessage(`Error: ${err.message}`);
    }
  }

  function handleLogout() {
    localStorage.removeItem('admin');
    window.location.href = '/admin/login';
  }

  if (loading) return <div className={styles.container}>Loading...</div>;

  return (
    <main className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Admin Dashboard</h1>
        <div className={styles.headerButtons}>
          <Link href="/">
            <button className={styles.backButton}>← Home</button>
          </Link>
          <button onClick={handleLogout} className={styles.logoutButton}>
            Logout
          </button>
        </div>
      </div>

      {message && <div className={styles.message}>{message}</div>}

      {/* System Stats */}
      {systemStats && (
        <div className={styles.statsGrid}>
          <div className={styles.statCard}>
            <h3>Total Users</h3>
            <p className={styles.statNumber}>{systemStats.totalUsers}</p>
          </div>
          <div className={styles.statCard}>
            <h3>Total Products</h3>
            <p className={styles.statNumber}>{systemStats.totalProducts}</p>
          </div>
          <div className={styles.statCard}>
            <h3>Active Users</h3>
            <p className={styles.statNumber}>{systemStats.activeUsers}</p>
          </div>
        </div>
      )}

      {/* Admin Actions */}
      <div className={styles.actionsGrid}>
        {/* Delete User */}
        <div className={styles.actionCard}>
          <h2>Delete User</h2>
          <input
            type="email"
            placeholder="Enter user email"
            value={searchEmail}
            onChange={(e) => setSearchEmail(e.target.value)}
            className={styles.input}
          />
          <button onClick={handleDeleteUser} className={styles.deleteButton}>
            Delete User
          </button>
        </div>

        {/* Wishlist Stats */}
        <div className={styles.actionCard}>
          <h2>Wishlist Stats</h2>
          <input
            type="email"
            placeholder="Enter user email"
            value={wishlistEmail}
            onChange={(e) => setWishlistEmail(e.target.value)}
            className={styles.input}
          />
          <button onClick={handleGetWishlistStats} className={styles.primaryButton}>
            Get Wishlist Stats
          </button>
          
          {wishlistStats && (
            <div className={styles.wishlistStats}>
              <p><strong>User:</strong> {wishlistStats.email}</p>
              <p><strong>Items in Wishlist:</strong> {wishlistStats.count}</p>
              {wishlistStats.items && wishlistStats.items.length > 0 && (
                <div>
                  <p><strong>Items:</strong></p>
                  <ul>
                    {wishlistStats.items.map((item: string, idx: number) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Users Table */}
      <div className={styles.tableSection}>
        <h2>All Users ({users.length})</h2>
        <div className={styles.tableWrapper}>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Phone</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.user_id}>
                  <td>{user.user_id}</td>
                  <td>{user.name || 'N/A'}</td>
                  <td>{user.email}</td>
                  <td>{user.role}</td>
                  <td>{user.contact_phone || 'N/A'}</td>
                  <td>{user.location || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
