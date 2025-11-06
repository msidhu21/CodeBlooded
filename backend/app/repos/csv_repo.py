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
    
    def search_products(self, 
                       query: str = None, 
                       category: str = None, 
                       min_rating: float = None,
                       max_price: float = None,
                       limit: int = 100,
                       offset: int = 0) -> List[dict]:
        """Search products with filters"""
        filtered_df = self.df.copy()
        
        # Text search in product name
        if query:
            filtered_df = filtered_df[
                filtered_df['product_name'].str.contains(query, case=False, na=False)
            ]
        
        # Filter by category
        if category:
            filtered_df = filtered_df[
                filtered_df['category'].str.contains(category, case=False, na=False)
            ]
        
        # Filter by minimum rating
        if min_rating is not None:
            filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
        
        # Filter by maximum price
        if max_price is not None:
            # Clean price string and convert to float
            filtered_df['price_clean'] = filtered_df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float)
            filtered_df = filtered_df[filtered_df['price_clean'] <= max_price]
        
        return filtered_df.iloc[offset:offset+limit].to_dict('records')
    
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
