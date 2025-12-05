const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `HTTP error! status: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error(`Cannot connect to backend at ${this.baseUrl}. Make sure the backend is running on port 8000.`);
      }
      throw error;
    }
  }

  async searchItems(params: {
    q?: string;
    category?: string;
    min_rating?: number;
    max_rating?: number;
    min_price?: number;
    max_price?: number;
    min_discount?: number;
    page?: number;
    size?: number;
  }) {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        queryParams.append(key, String(value));
      }
    });
    return this.request<import('@/types').SearchResponse>(`/items/search?${queryParams}`);
  }

  async getItemDetails(productId: string) {
    return this.request<import('@/types').ItemDetailsResponse>(`/items/${productId}`);
  }

  async getCategories() {
    return this.request<import('@/types').CategoryResponse>('/items/categories/list');
  }

  async getRecommendations(query: string, limit: number = 10) {
    return this.request<import('@/types').RecommendationResponse>(
      `/items/recommend?query=${encodeURIComponent(query)}&limit=${limit}`
    );
  }

  async getPlaceAutocomplete(input: string) {
    return this.request<import('@/types').PlacesAutocompleteResponse>(
      `/external/places/autocomplete?input=${encodeURIComponent(input)}`
    );
  }

  async adminRequest<T>(endpoint: string, options: RequestInit = {}) {
    return this.request<T>(endpoint, {
      ...options,
      headers: {
        'Authorization': 'Bearer admin',
        ...options.headers,
      },
    });
  }

  async getAllItems() {
    return this.searchItems({ page: 1, size: 1000 });
  }

  async deleteItem(productId: string) {
    return this.adminRequest(`/admin/items/${productId}`, {
      method: 'DELETE',
    });
  }

  async updateItem(productId: string, data: Partial<import('@/types').Product>) {
    return this.adminRequest(`/admin/items/${productId}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async createItem(data: any) {
    return this.adminRequest('/admin/items', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getWishlist() {
    return this.request<{ products: any[]; count: number }>('/wishlist');
  }

  async addToWishlist(productId: string) {
    return this.request<{ message: string; item: any }>(`/wishlist/${productId}`, {
      method: 'POST',
    });
  }

  async removeFromWishlist(productId: string) {
    return this.request<{ message: string }>(`/wishlist/${productId}`, {
      method: 'DELETE',
    });
  }

  async checkWishlist(productId: string) {
    return this.request<{ is_in_wishlist: boolean }>(`/wishlist/${productId}/check`);
  }
}

export const apiClient = new ApiClient(API_URL);

