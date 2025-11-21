"use client";

export default function ProfilePage() {
  return (
    <main className="max-w-2xl mx-auto mt-10 space-y-6 px-4">
      <header className="space-y-1">
        <h1 className="text-3xl font-semibold">My Profile</h1>
        <p className="text-sm text-gray-500">
          View and update your account details.
        </p>
      </header>

      <section className="space-y-4">
        <div className="rounded-lg border border-gray-200 p-4">
          <h2 className="text-lg font-medium mb-2">Basic info</h2>
          <p className="text-sm text-gray-500">
            This page will show your name, email, phone and profile picture once
            the backend is fully wired.
          </p>
        </div>

        <div className="rounded-lg border border-dashed border-gray-300 p-4 text-sm text-gray-400">
          Profile form coming soon…
        </div>
      </section>
    </main>
  );
}
