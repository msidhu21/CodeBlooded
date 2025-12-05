// API Response Types
export interface Product {
  product_id: string;
  product_name: string;
  category: string;
  discounted_price?: string;
  actual_price?: string;
  discount_percentage?: string;
  rating?: string;
  rating_count?: string;
  about_product?: string;
  img_link?: string;
  product_link?: string;
  relevance_score?: number;
  score?: number; // For recommendations
  highlighted_fields?: string[]; // Fields containing search query matches
}

export interface SearchResponse {
  products: Product[];
  pagination: {
    page: number;
    size: number;
    total_results: number;
    total_pages: number;
    has_more: boolean;
  };
  filters_applied: {
    search_query?: string;
    category?: string;
    min_rating?: number;
    max_rating?: number;
    min_price?: number;
    max_price?: number;
    min_discount?: number;
  };
  meta: {
    search_time_ms: number;
    results_on_page: number;
  };
  suggestions?: {
    original_query: string;
    similar_categories: string[];
    popular_products: Product[];
    did_you_mean: string[];
  };
}

export interface ItemDetailsResponse {
  product: Product;
  related: Product[];
}

export interface RecommendationResponse {
  items: Product[];
  query: string;
  total_found: number;
}

export interface CategoryResponse {
  categories: string[];
}

export interface PlacePrediction {
  description: string;
  place_id: string;
}

export interface PlacesAutocompleteResponse {
  predictions: PlacePrediction[];
}

export interface AuthUser {
  id: number;
  email: string;
  name: string;
  role: string;
}

