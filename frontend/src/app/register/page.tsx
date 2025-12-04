"use client";
import { useState } from "react";

export default function RegisterPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async (e: any) => {
    e.preventDefault();

    try {
      console.log("FETCH URL:", process.env.NEXT_PUBLIC_API_URL + "/auth/register");

   const res = await fetch("http://127.0.0.1:8000/auth/register", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    email,
    password,
  }),
});


      const data = await res.json();
      setMessage(JSON.stringify(data));
    } catch (err) {
      console.log(err);
      setMessage("Could not connect to backend.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Create Account</h1>

      <form onSubmit={handleRegister}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <br />

        <button type="submit">Register</button>
      </form>

      {message && <p> {message}</p>}
    </div>
  );
}

