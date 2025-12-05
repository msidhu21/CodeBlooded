// frontend/lib/api/auth.ts

const API_BASE_URL = "http://127.0.0.1:8000";

export type RegisterPayload = {
  email: string;
  password: string;
  name: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type AuthUser = {
  id: number;        // mapped from user_id in backend
  email: string;
  name: string;
  role: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export async function register(payload: RegisterPayload): Promise<AuthUser> {
  const res = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Register failed: ${res.status} - ${text}`);
  }

  return res.json();
}

export async function login(payload: LoginPayload): Promise<AuthUser> {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Login failed: ${res.status} - ${text}`);
  }

  // Backend directly returns AuthUser
  return res.json();
}

export async function updateProfile(userId: number, payload: any, token: string) {
  const res = await fetch(`${API_BASE_URL}/profile/${userId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Update failed: ${text}`);
  }

  return res.json();
}


// Small helper to store token in localStorage after login
// export function saveToken(token: string) {
//   if (typeof window === "undefined") return;
//   localStorage.setItem("auth_token", token);
// }

// export function getToken(): string | null {
//   if (typeof window === "undefined") return null;
//   return localStorage.getItem("auth_token");
// }

// export function clearToken() {
//   if (typeof window === "undefined") return;
//   localStorage.removeItem("auth_token");
// }
