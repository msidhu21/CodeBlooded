"use client";

import { useState } from "react";
import { login } from "@/lib/api/auth";
import Link from "next/link";
import "@/styles/auth.css";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const user = await login({ email, password });

      // Save session
      localStorage.setItem("user", JSON.stringify(user));

      // Redirect to profile
      window.location.href = "/profile";
    } catch (err: any) {
      setMessage(err.message ?? "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-container">
      <h1 className="auth-title">Welcome Back</h1>

      <form onSubmit={handleSubmit}>
        <input
          className="auth-input"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          className="auth-input"
          placeholder="Password"
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
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>

      {message && <p className="auth-message">{message}</p>}

      <div className="auth-link">
        <p>Don't have an account?</p>
        <Link href="/register">
          <button className="auth-secondary-button">Sign Up</button>
        </Link>
      </div>
    </main>
  );
}
