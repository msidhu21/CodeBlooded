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
  totalCategories: number;
  cartStats: {
    totalItems: number;
    usersWithCarts: number;
  };
  wishlistStats: {
    totalItems: number;
    usersWithWishlists: number;
  };
}

interface SystemHealth {
  status: string;
  timestamp: number;
  checks: {
    [key: string]: {
      status: string;
      records?: number;
      size_kb?: number;
      error?: string;
    };
  };
}

export default function AdminDashboard() {
  const [searchEmail, setSearchEmail] = useState("");
  const [searchedUser, setSearchedUser] = useState<User | null>(null);
  const [wishlistEmail, setWishlistEmail] = useState("");
  const [wishlistStats, setWishlistStats] = useState<any>(null);
  const [systemStats, setSystemStats] = useState<SystemStats | null>(null);
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [recentUsers, setRecentUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [searchMessage, setSearchMessage] = useState("");

  useEffect(() => {
    // Check if admin is logged in
    const admin = localStorage.getItem('admin');
    if (!admin) {
      window.location.href = '/admin/login';
      return;
    }

    fetchSystemStats();
    fetchSystemHealth();
    fetchRecentUsers();
    setLoading(false);
  }, []);

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

  async function fetchSystemHealth() {
    try {
      const res = await fetch('http://127.0.0.1:8000/admin/health');
      if (res.ok) {
        const data = await res.json();
        setSystemHealth(data);
      }
    } catch (err) {
      console.error('Failed to fetch health:', err);
    }
  }

  async function fetchRecentUsers() {
    try {
      const res = await fetch('http://127.0.0.1:8000/admin/recent-users');
      if (res.ok) {
        const data = await res.json();
        setRecentUsers(data.recent_users || []);
      }
    } catch (err) {
      console.error('Failed to fetch recent users:', err);
    }
  }

  async function handleSearchUser() {
    if (!searchEmail) {
      setSearchMessage("Please enter an email");
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/admin/users/search/${encodeURIComponent(searchEmail)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.user) {
          setSearchedUser(data.user);
          setSearchMessage("");
        } else {
          setSearchedUser(null);
          setSearchMessage("User not found");
        }
      } else {
        setSearchedUser(null);
        setSearchMessage("User not found");
      }
    } catch (err: any) {
      setSearchMessage(`Error: ${err.message}`);
      setSearchedUser(null);
    }
  }

  async function handleDeleteUser() {
    if (!searchedUser) {
      setMessage("Please search for a user first");
      return;
    }

    if (!confirm(`Are you sure you want to delete user: ${searchedUser.email}?`)) {
      return;
    }

    try {
      const res = await fetch(`http://127.0.0.1:8000/admin/users/${searchedUser.email}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        setMessage(`User ${searchedUser.email} deleted successfully`);
        setSearchedUser(null);
        setSearchEmail("");
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

      {/* System Health Status */}
      {systemHealth && (
        <div className={styles.healthSection}>
          <div className={styles.healthHeader}>
            <h2>System Health</h2>
            <span className={`${styles.healthBadge} ${styles[systemHealth.status]}`}>
              {systemHealth.status === 'healthy' ? '✓ Healthy' : '⚠ Degraded'}
            </span>
          </div>
          <div className={styles.healthGrid}>
            {Object.entries(systemHealth.checks).map(([name, check]: [string, any]) => (
              <div key={name} className={styles.healthCard}>
                <div className={styles.healthCardHeader}>
                  <span className={styles.healthCardTitle}>
                    {name.replace('_', ' ').toUpperCase()}
                  </span>
                  <span className={`${styles.healthStatus} ${styles[check.status]}`}>
                    {check.status === 'healthy' ? '●' : '●'}
                  </span>
                </div>
                {check.records !== undefined && (
                  <p className={styles.healthDetail}>
                    <strong>{check.records}</strong> records
                  </p>
                )}
                {check.size_kb !== undefined && (
                  <p className={styles.healthDetail}>
                    {check.size_kb} KB
                  </p>
                )}
                {check.error && (
                  <p className={styles.healthError}>{check.error}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* System Stats */}
      {systemStats && (
        <>
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
            <div className={styles.statCard}>
              <h3>Categories</h3>
              <p className={styles.statNumber}>{systemStats.totalCategories}</p>
            </div>
          </div>
          
          <div className={styles.statsGrid}>
            <div className={styles.statCard}>
              <h3>Cart Items</h3>
              <p className={styles.statNumber}>{systemStats.cartStats.totalItems}</p>
              <p className={styles.statSubtext}>{systemStats.cartStats.usersWithCarts} users</p>
            </div>
            <div className={styles.statCard}>
              <h3>Wishlist Items</h3>
              <p className={styles.statNumber}>{systemStats.wishlistStats.totalItems}</p>
              <p className={styles.statSubtext}>{systemStats.wishlistStats.usersWithWishlists} users</p>
            </div>
          </div>
        </>
      )}

      {/* Recent User Logins */}
      {recentUsers.length > 0 && (
        <div className={styles.recentUsersSection}>
          <h2>Recent User Registrations</h2>
          <div className={styles.recentUsersGrid}>
            {recentUsers.map((user) => (
              <div key={user.user_id} className={styles.userCard}>
                <div className={styles.userCardHeader}>
                  <strong>{user.name || 'N/A'}</strong>
                  <span className={styles.userId}>ID: {user.user_id}</span>
                </div>
                <p className={styles.userEmail}>{user.email}</p>
                <div className={styles.userMeta}>
                  <span>{user.role}</span>
                  {user.location && <span>📍 {user.location}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Admin Actions */}
      <div className={styles.actionsGrid}>
        {/* Search and Manage User */}
        <div className={styles.actionCard}>
          <h2>Search User</h2>
          <input
            type="email"
            placeholder="Enter user email"
            value={searchEmail}
            onChange={(e) => setSearchEmail(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearchUser()}
            className={styles.input}
          />
          <button onClick={handleSearchUser} className={styles.primaryButton}>
            Search User
          </button>
          
          {searchMessage && (
            <div className={styles.searchMessage}>{searchMessage}</div>
          )}
          
          {searchedUser && (
            <div className={styles.userDetails}>
              <h3>User Details</h3>
              <p><strong>ID:</strong> {searchedUser.user_id}</p>
              <p><strong>Name:</strong> {searchedUser.name || 'N/A'}</p>
              <p><strong>Email:</strong> {searchedUser.email}</p>
              <p><strong>Role:</strong> {searchedUser.role}</p>
              <p><strong>Phone:</strong> {searchedUser.contact_phone || 'N/A'}</p>
              <p><strong>Location:</strong> {searchedUser.location || 'N/A'}</p>
              
              <button onClick={handleDeleteUser} className={styles.deleteButton}>
                Delete This User
              </button>
            </div>
          )}
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
    </main>
  );
}
