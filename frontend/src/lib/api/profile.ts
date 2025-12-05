const API_BASE_URL = "http://127.0.0.1:8000";

export async function updateProfile(userId: number, name: string) {
  const res = await fetch(`${API_BASE_URL}/profile/${userId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });

  if (!res.ok) throw new Error("Failed to update profile");

  return res.json();
}
