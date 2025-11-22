"use client";

import { useEffect, useState } from "react";
import { fetchProfile, type Profile } from "@/lib/api/profile";

export default function ProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProfile()
      .then((data) => {
        setProfile(data);
        setError(null);
      })
      .catch((err) => {
        console.error(err);
        setError("Could not load profile");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <main className="max-w-xl mx-auto mt-10 space-y-4">
        <h1 className="text-2xl font-semibold">My Profile</h1>
        <p>Loading...</p>
      </main>
    );
  }

  if (error || !profile) {
    return (
      <main className="max-w-xl mx-auto mt-10 space-y-4">
        <h1 className="text-2xl font-semibold">My Profile</h1>
        <p>{error ?? "No profile data"}</p>
      </main>
    );
  }

  return (
    <main className="max-w-xl mx-auto mt-10 space-y-4">
      <h1 className="text-2xl font-semibold">My Profile</h1>

      <div className="space-y-1">
        <p>
          <span className="font-medium">Email:</span> {profile.email}
        </p>
        <p>
          <span className="font-medium">Name:</span> {profile.name}
        </p>
        <p>
          <span className="font-medium">Role:</span> {profile.role}
        </p>
      </div>
    </main>
  );
}
