"use client";

import { useState, useEffect } from "react";
import styles from "./profile.module.css";

export default function ProfilePage() {
  const [form, setForm] = useState({
    user_id: 1,
    name: "",
    email: "",
    password_hash: "",
    role: "",
    picture: "",
    phone: "",
  });

  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  // Load profile from backend
  useEffect(() => {
    async function fetchProfile() {
      try {
        const res = await fetch("http://127.0.0.1:8000/profile/me");
        const data = await res.json();
        setForm({ ...form, ...data });
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    }
    fetchProfile();
  }, []);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSave() {
    setMessage("");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/profile/${form.user_id}`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        }
      );

      if (!res.ok) {
        const error = await res.text();
        throw new Error(error);
      }

      setMessage("Profile updated successfully!");
    } catch (err: any) {
      setMessage(err.message);
    }
  }

  if (loading) return <p>Loading...</p>;

  return (
    <main className={styles.container}>
      <h2 className={styles.title}>Account Settings</h2>

      <div className={styles.card}>
        <div className={styles.photoSection}>
          <img
            src={form.picture || "/default-avatar.png"}
            className={styles.avatar}
            alt="Profile Picture"
          />

          <input
            type="text"
            placeholder="Profile picture URL"
            name="picture"
            value={form.picture}
            onChange={handleChange}
            className={styles.input}
          />

          <p className={styles.hint}>Paste an image link to change avatar</p>
        </div>

        <div className={styles.formSection}>
          <div className={styles.row}>
            <div className={styles.field}>
              <label>Name</label>
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
              />
            </div>

            <div className={styles.field}>
              <label>Role</label>
              <input
                name="role"
                value={form.role}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className={styles.row}>
            <div className={styles.field}>
              <label>Email</label>
              <input
                name="email"
                value={form.email}
                onChange={handleChange}
              />
            </div>

            <div className={styles.field}>
              <label>Phone</label>
              <input
                name="phone"
                value={form.phone}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className={styles.row}>
            <div className={styles.field}>
              <label>Password Hash (read-only)</label>
              <input
                name="password_hash"
                value={form.password_hash}
                disabled
              />
            </div>
          </div>

          <button onClick={handleSave} className={styles.saveButton}>
            Save Changes
          </button>

          {message && <p className={styles.message}>{message}</p>}
        </div>
      </div>
    </main>
  );
}
