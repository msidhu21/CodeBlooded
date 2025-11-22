"use client";

type ItemCategoryFilterProps = {
  selected: string;
  onChange: (value: string) => void;
};

function ItemCategoryFilter({ selected, onChange }: ItemCategoryFilterProps) {
  const categories = ["all", "venue", "service", "equipment"];

  return (
    <div className="flex gap-2 flex-wrap">
      {categories.map((cat) => (
        <button
          key={cat}
          type="button"
          onClick={() => onChange(cat)}
          className={`px-3 py-1 rounded-full text-sm border ${
            selected === cat ? "bg-black text-white" : "bg-white"
          }`}
        >
          {cat.toUpperCase()}
        </button>
      ))}
    </div>
  );
}

export default function ItemsPage() {
  const selectedCategory = "all";

  return (
    <main className="max-w-4xl mx-auto mt-10 space-y-6">
      <header className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Items</h1>
          <p className="text-sm text-gray-500">
            Browse items available in the system. Data wiring will be added later.
          </p>
        </div>
        <span className="text-xs text-gray-400">User Story 4 support</span>
      </header>

      <ItemCategoryFilter selected={selectedCategory} onChange={() => {}} />

      <section className="grid gap-4 md:grid-cols-2">
        <article className="border rounded-xl p-4 space-y-2">
          <h2 className="font-medium">Example Item</h2>
          <p className="text-sm text-gray-500">
            This is a placeholder card. It will later be populated from the backend /items API.
          </p>
          <span className="inline-block text-xs px-2 py-1 rounded-full bg-gray-100">
            category: venue
          </span>
        </article>
      </section>
    </main>
  );
}
