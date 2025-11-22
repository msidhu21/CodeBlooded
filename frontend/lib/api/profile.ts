// frontend/lib/api/profile.ts

export type Profile = {
  id: number;
  email: string;
  name: string;
  role: string;
};

// If you later set NEXT_PUBLIC_API_BASE_URL, this will use that.
// Otherwise it defaults to localhost:8000 which is where your FastAPI runs.
const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function fetchProfile(): Promise<Profile> {
  const res = await fetch(`${API_BASE}/profile`, {
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error(`Failed to load profile (status ${res.status})`);
  }

  return res.json();
}
