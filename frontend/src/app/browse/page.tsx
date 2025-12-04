"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api";
import type { Product } from "@/types";

export default function BrowsePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [query, setQuery] = useState("");


  const loadDefault = async () => {
    try {
      console.log("Loading default items...");
      const res = await apiClient.searchItems({ page: 1, size: 20 });

   
      setProducts(res.products || []);
    } catch (err) {
      console.log("Default load failed:", err);
    }
  };

  useEffect(() => {
    loadDefault();
  }, []);

  const handleSearch = async () => {
    try {
      console.log("Searching:", query);
      const res = await apiClient.searchItems({ query });


      setProducts(res.products || []);
    } catch (err) {
      console.log("Search error:", err);
    }
  };

  return (
    <div>
      <h1>Product Catalog</h1>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search products..."
      />
      <button onClick={handleSearch}>Search</button>

      <div style={{ marginTop: "20px" }}>
        {products.length === 0 ? (
          <p>No items found.</p>
        ) : (
          products.map((p) => (
            <div key={p.product_id} style={{ marginBottom: "20px" }}>
              <strong>{p.product_name}</strong>
              <div>{p.category}</div>
              <div>{p.discounted_price}</div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
