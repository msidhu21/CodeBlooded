"use client";

import { useState } from "react";
import { register } from "@/lib/api/auth";
import Link from "next/link";
import "@/styles/auth.css";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const user = await register({ email, password, name });

      // Save session
      localStorage.setItem("user", JSON.stringify(user));

      // Redirect to home
      window.location.href = "/";
    } catch (err: any) {
      setMessage(err.message ?? "Registration failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-container">
      <h1 className="auth-title">Create an Account</h1>

      <form onSubmit={handleSubmit}>
        <input
          className="auth-input"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

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
          {loading ? "Registering..." : "Register"}
        </button>
      </form>

      {message && <p className="auth-message">{message}</p>}

      <div className="auth-link">
        <p>Already have an account?</p>
        <Link href="/login">
          <button className="auth-secondary-button">Login</button>
        </Link>
      </div>
    </main>
  );
}
