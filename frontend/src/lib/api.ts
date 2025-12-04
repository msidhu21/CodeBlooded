const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

import type {
  SearchResponse,
  ItemDetailsResponse,
  RecommendationResponse,
  CategoryResponse,
  PlacesAutocompleteResponse,
  Product,
} from "@/types";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
    console.log("ApiClient using base URL:", baseUrl);
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    console.log("Request:", url);

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      console.log("Response status:", response.status);

      const data = await response.json().catch(() => null);
      console.log("Response JSON:", data);

      if (!response.ok) {
        throw new Error(data?.detail || "Request failed");
      }

      return data;
    } catch (err) {
      console.log("Fetch error:", err);
      throw err;
    }
  }

  async searchItems(params: any): Promise<SearchResponse> {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        queryParams.append(key, String(value));
      }
    });

    const query = queryParams.toString();
    return this.request<SearchResponse>(`/items/search?${query}`);
  }

  async getItemDetails(productId: string): Promise<ItemDetailsResponse> {
    return this.request<ItemDetailsResponse>(`/items/${productId}`);
  }

  async getCategories(): Promise<CategoryResponse> {
    return this.request<CategoryResponse>("/items/categories/list");
  }

  async getRecommendations(query: string, limit: number = 10): Promise<RecommendationResponse> {
    return this.request<RecommendationResponse>(
      `/items/recommend?query=${encodeURIComponent(query)}&limit=${limit}`
    );
  }

  async getPlaceAutocomplete(input: string): Promise<PlacesAutocompleteResponse> {
    return this.request<PlacesAutocompleteResponse>(
      `/external/places/autocomplete?input=${encodeURIComponent(input)}`
    );
  }

  async registerUser(data: { name: string; email: string; password: string }) {
    return this.request("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async adminRequest<T>(endpoint: string, options: RequestInit = {}) {
    return this.request<T>(endpoint, {
      ...options,
      headers: {
        Authorization: "Bearer admin",
        ...options.headers,
      },
    });
  }

  async getAllItems(): Promise<SearchResponse> {
    return this.searchItems({ page: 1, size: 1000 });
  }

  async deleteItem(productId: string) {
    return this.adminRequest(`/admin/items/${productId}`, {
      method: "DELETE",
    });
  }

  async updateItem(productId: string, data: Partial<Product>) {
    return this.adminRequest(`/admin/items/${productId}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  async createItem(data: any) {
    return this.adminRequest("/admin/items", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }
}

export const apiClient = new ApiClient(API_URL);