"use client";

import { useState } from "react";
import Link from "next/link";
import "@/styles/auth.css";

export default function AdminLoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    // Simple hardcoded admin credentials for demo
    if (username === "admin" && password === "admin123") {
      // Save admin session
      localStorage.setItem("admin", JSON.stringify({ username, role: "admin" }));
      
      // Redirect to admin dashboard
      window.location.href = "/admin/dashboard";
    } else {
      setMessage("Invalid admin credentials");
      setLoading(false);
    }
  }

  return (
    <main className="auth-container">
      <h1 className="auth-title">Admin Login</h1>
      <p style={{ textAlign: 'center', marginBottom: '1.5rem', color: '#666' }}>
        Admin access only
      </p>

      <form onSubmit={handleSubmit}>
        <input
          className="auth-input"
          placeholder="Admin Username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <input
          className="auth-input"
          placeholder="Admin Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="auth-button"
        >
          {loading ? "Logging in..." : "Login as Admin"}
        </button>
      </form>

      {message && <p className="auth-message" style={{ color: 'red' }}>{message}</p>}

      <div className="auth-link">
        <Link href="/">
          <button className="auth-secondary-button">← Back to Home</button>
        </Link>
      </div>
    </main>
  );
}
