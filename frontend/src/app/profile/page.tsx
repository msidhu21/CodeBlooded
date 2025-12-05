"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import styles from "./profile.module.css";

// Extend Window interface for Google Maps
declare global {
  interface Window {
    google?: any;
  }
}

// Load Google Places API
const loadGoogleMapsScript = () => {
  return new Promise<void>((resolve, reject) => {
    if (window.google && window.google.maps) {
      resolve();
      return;
    }
    
    const script = document.createElement('script');
    const apiKey = 'AIzaSyDiwWRhEUkSmyW4K1js9SBURtLcKlafFaw';
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`;
    script.async = true;
    script.defer = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Google Maps'));
    document.head.appendChild(script);
  });
};

export default function ProfilePage() {
  const [form, setForm] = useState({
    user_id: 1,
    name: "",
    email: "",
    password_hash: "",
    role: "",
    picture: "",
    phone: "",
    location: "",
  });

  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const locationInputRef = useRef<HTMLInputElement>(null);

  // Load profile from backend
  useEffect(() => {
    async function fetchProfile() {
      try {
        // Get user from localStorage
        const userStr = localStorage.getItem('user');
        if (!userStr) {
          // Redirect to login if not logged in
          window.location.href = '/login';
          return;
        }

        const user = JSON.parse(userStr);
        
        // Fetch full profile data from backend (user.id is returned from login)
        const res = await fetch(`http://127.0.0.1:8000/profile/${user.id}`);
        const data = await res.json();
        
        // Pre-fill form with user data
        setForm({
          user_id: data.user_id || user.id,
          name: data.name || user.name || "",
          email: data.email || user.email || "",
          password_hash: data.password_hash || "",
          role: data.role || user.role || "",
          picture: data.picture || user.picture || "",
          phone: data.phone || user.phone || "",
          location: data.location || user.location || "",
        });
      } catch (err) {
        console.error(err);
      }
      setLoading(false);
    }
    fetchProfile();
  }, []);

  // Initialize Google Places Autocomplete after form data is loaded
  useEffect(() => {
    // Only initialize after loading is complete
    if (loading) return;
    
    let autocomplete: any;
    
    async function initAutocomplete() {
      try {
        await loadGoogleMapsScript();
        
        if (locationInputRef.current && (window as any).google) {
          autocomplete = new (window as any).google.maps.places.Autocomplete(
            locationInputRef.current,
            { types: ['(cities)'] }
          );
          
          autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            if (place.formatted_address) {
              setForm(prev => ({ ...prev, location: place.formatted_address }));
            }
          });
        }
      } catch (err) {
        console.error('Failed to initialize Google Places:', err);
      }
    }
    
    initAutocomplete();
  }, [loading]);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSave() {
    setMessage("");

    try {
      // Get user_id from localStorage as fallback (login returns user.id)
      const userStr = localStorage.getItem('user');
      const userId = form.user_id || (userStr ? JSON.parse(userStr).id : null);
      
      if (!userId) {
        setMessage("User ID not found. Please log in again.");
        return;
      }

      const res = await fetch(
        `http://127.0.0.1:8000/profile/${userId}`,
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

  function handleLogout() {
    // Clear user session
    localStorage.removeItem('user');
    // Redirect to home page
    window.location.href = '/';
  }

  if (loading) return <p>Loading...</p>;

  return (
    <main className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>Account Settings</h2>
        <div className={styles.headerButtons}>
          <Link href="/">
            <button className={styles.backButton}>← Back to Home</button>
          </Link>
          <button onClick={handleLogout} className={styles.logoutButton}>
            Logout
          </button>
        </div>
      </div>

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
              <label>Location</label>
              <input
                ref={locationInputRef}
                name="location"
                value={form.location}
                onChange={handleChange}
                placeholder="Start typing a city name..."
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
