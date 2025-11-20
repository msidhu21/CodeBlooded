import pandas as pd
from typing import List, Optional
from pathlib import Path
import os
import threading

class CSVRepository:
    _lock = threading.Lock()  # Thread-safe file operations
    
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            base_path = Path(__file__).parent.parent.parent
            csv_path = base_path / "data" / "amazon.csv"
        self.csv_path = csv_path
        self._reload()
    
    def _reload(self):
        """Reload data from CSV file"""
        self.df = pd.read_csv(self.csv_path)
    
    def _save(self):
        """Save data to CSV file"""
        with self._lock:
            self.df.to_csv(self.csv_path, index=False)
    
    def get_all_products(self, limit: int = 100, offset: int = 0) -> List[dict]:
        """Get all products with pagination"""
        return self.df.iloc[offset:offset+limit].to_dict('records')
    
    def get_product_by_id(self, product_id: str) -> Optional[dict]:
        """Get a single product by ID"""
        result = self.df[self.df['product_id'] == product_id]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def get_products_by_ids(self, product_ids: List[str]) -> List[dict]:
        """Get multiple products by their IDs"""
        if not product_ids:
            return []
        result = self.df[self.df['product_id'].isin(product_ids)]
        return result.to_dict('records')
    
    def search_products(self, 
                       query: str = None, 
                       category: str = None, 
                       min_rating: float = None,
                       max_rating: float = None,
                       min_price: float = None,
                       max_price: float = None,
                       min_discount: float = None,
                       limit: int = 100,
                       offset: int = 0,
                       return_total: bool = False) -> List[dict] | tuple[List[dict], int]:
        """Search products with multiple filters - searches across name, description, and category
        
        Args:
            return_total: If True, returns (results, total_count) tuple
        """
        filtered_df = self.df.copy()
        
        # Enhanced text search across multiple fields
        if query:
            # Search in product name, description (about_product), and category
            # Handle NaN values by filling with empty string
            name_match = filtered_df['product_name'].fillna('').str.contains(query, case=False, na=False)
            desc_match = filtered_df['about_product'].fillna('').str.contains(query, case=False, na=False)
            cat_match = filtered_df['category'].fillna('').str.contains(query, case=False, na=False)
            
            # Combine matches with OR logic - product matches if found in any field
            text_match = name_match | desc_match | cat_match
            filtered_df = filtered_df[text_match]
            
            # Add relevance score for ranking (higher score = better match)
            if len(filtered_df) > 0:
                # Recalculate matches for the filtered dataframe
                filtered_name_match = filtered_df['product_name'].fillna('').str.contains(query, case=False, na=False)
                filtered_desc_match = filtered_df['about_product'].fillna('').str.contains(query, case=False, na=False)
                filtered_cat_match = filtered_df['category'].fillna('').str.contains(query, case=False, na=False)
                
                filtered_df['relevance_score'] = (
                    filtered_name_match.astype(int) * 3 +  # Name matches are most important
                    filtered_desc_match.astype(int) * 1 +  # Description matches are less important
                    filtered_cat_match.astype(int) * 2      # Category matches are moderately important
                )
                
                # Sort by relevance score (highest first)
                filtered_df = filtered_df.sort_values('relevance_score', ascending=False)
        
        # Filter by category (exact or partial match)
        if category:
            filtered_df = filtered_df[
                filtered_df['category'].str.contains(category, case=False, na=False)
            ]
        
        # Filter by minimum rating
        if min_rating is not None:
            # Convert rating to float, handling errors
            filtered_df['rating_float'] = pd.to_numeric(filtered_df['rating'], errors='coerce')
            filtered_df = filtered_df[filtered_df['rating_float'] >= min_rating]
            filtered_df = filtered_df.drop(columns=['rating_float'])
        
        # Filter by maximum rating
        if max_rating is not None:
            filtered_df = filtered_df[filtered_df['rating'] <= max_rating]
        
        # Filter by price range
        if min_price is not None or max_price is not None:
            # Clean price string and convert to float
            filtered_df['price_clean'] = filtered_df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)
            
            if min_price is not None:
                filtered_df = filtered_df[filtered_df['price_clean'] >= min_price]
            
            if max_price is not None:
                filtered_df = filtered_df[filtered_df['price_clean'] <= max_price]
            
            filtered_df = filtered_df.drop(columns=['price_clean'])
        
        # Filter by minimum discount percentage
        if min_discount is not None:
            # Clean discount string and convert to float
            filtered_df['discount_clean'] = filtered_df['discount_percentage'].str.replace('%', '').astype(float)
            filtered_df = filtered_df[filtered_df['discount_clean'] >= min_discount]
            filtered_df = filtered_df.drop(columns=['discount_clean'])
        
        # Get total count before pagination
        total_count = len(filtered_df)
        
        # Apply pagination
        paginated_df = filtered_df.iloc[offset:offset+limit]
        
        # Remove temporary columns before returning
        columns_to_drop = ['relevance_score', 'price_clean', 'discount_clean']
        paginated_df = paginated_df.drop(columns=[col for col in columns_to_drop if col in paginated_df.columns], errors='ignore')
        
        results = paginated_df.to_dict('records')
        
        if return_total:
            return results, total_count
        return results
    
    def get_related_products(self, product_id: str, limit: int = 4) -> List[dict]:
        """Get related products based on category"""
        product = self.get_product_by_id(product_id)
        if not product:
            return []
        
        category = product.get('category', '')
        # Get products in same category, excluding the current product
        related = self.df[
            (self.df['category'] == category) & 
            (self.df['product_id'] != product_id)
        ]
        
        return related.head(limit).to_dict('records')
    
    def get_categories(self) -> List[str]:
        """Get unique categories"""
        return self.df['category'].unique().tolist()
    
    def add_product(self, product_data: dict) -> dict:
        """Add a new product to the CSV"""
        with self._lock:
            # Generate new product_id if not provided
            if 'product_id' not in product_data or not product_data['product_id']:
                # Generate ID based on max existing ID
                max_id = len(self.df)
                product_data['product_id'] = f"P{max_id + 1:08d}"
            
            # Add the new row
            new_row = pd.DataFrame([product_data])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self._save()
            return product_data
    
    def update_product(self, product_id: str, update_data: dict) -> Optional[dict]:
        """Update an existing product"""
        with self._lock:
            idx = self.df[self.df['product_id'] == product_id].index
            if len(idx) == 0:
                return None
            
            # Update only provided fields
            for key, value in update_data.items():
                if value is not None and key in self.df.columns:
                    self.df.at[idx[0], key] = value
            
            self._save()
            return self.df.iloc[idx[0]].to_dict()
    
    def delete_product(self, product_id: str) -> bool:
        """Delete a product from the CSV"""
        with self._lock:
            initial_len = len(self.df)
            self.df = self.df[self.df['product_id'] != product_id]
            
            if len(self.df) < initial_len:
                self._save()
                return True
            return False
