"use client";

import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import type { Product } from "@/types";

export default function BrowsePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");

  async function handleSearch() {
    try {
      setLoading(true);
      setError(null);

      const result = await apiClient.searchItems({
        q: searchQuery,
        category: selectedCategory || undefined,
      });

      setProducts(result.products || []);
    } catch (err: any) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    async function loadDefault() {
      try {
        const result = await apiClient.searchItems({});
        setProducts(result.products || []);
      } catch {
        setError("Could not load items");
      }
    }

    loadDefault();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Product Catalog</h1>

      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Search products..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="border p-2 flex-1"
        />

        <button
          onClick={handleSearch}
          className="bg-blue-500 text-white px-4"
        >
          Search
        </button>
      </div>

      {error && <p className="text-red-500 mb-4">{error}</p>}
      {loading && <p>Loading...</p>}

      {!loading && products.length === 0 && (
        <p className="text-center mt-10">Start searching for products!</p>
      )}

      <div className="grid grid-cols-3 gap-4 mt-6">
        {products.map((item) => (
          <div key={item.product_id} className="border p-4 rounded">
            <p className="font-semibold">{item.product_name}</p>
            <p className="text-sm">{item.category}</p>
            <p className="mt-2 text-blue-600">₹{item.discounted_price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}


