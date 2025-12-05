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
        """Search products with filters - searches across name, description, and category
        
        Args:
            return_total: If True, returns (results, total_count) tuple
        """
        filtered_df = self.df.copy()
        
        # Enhanced text search across multiple fields
        if query:
            import re
            
            # Search in product name, description (about_product), and category
            name_match = filtered_df['product_name'].str.contains(query, case=False, na=False)
            desc_match = filtered_df['about_product'].str.contains(query, case=False, na=False)
            cat_match = filtered_df['category'].str.contains(query, case=False, na=False)
            
            # Check for exact word matches (e.g., "TV" as a whole word, not just "TV" in "Television")
            word_boundary_pattern = r'\b' + re.escape(query) + r'\b'
            name_exact_word = filtered_df['product_name'].str.contains(word_boundary_pattern, case=False, na=False, regex=True)
            cat_exact_word = filtered_df['category'].str.contains(word_boundary_pattern, case=False, na=False, regex=True)
            
            # Combine matches with OR logic - product matches if found in any field
            filtered_df = filtered_df[name_match | desc_match | cat_match]
            
            # Only add relevance scoring if we have matches
            if len(filtered_df) > 0:
                # Filter the boolean series to match the filtered dataframe indices
                filtered_name_exact = name_exact_word[filtered_df.index]
                filtered_name_match = name_match[filtered_df.index]
                filtered_cat_exact = cat_exact_word[filtered_df.index]
                filtered_cat_match = cat_match[filtered_df.index]
                filtered_desc_match = desc_match[filtered_df.index]
                
                # Detect if it's a main product category (Laptops, Smartphones, Tablets, etc) vs accessories
                # Check if category contains main product keywords
                main_product_keywords = r'\|(Laptops|Smartphones|Tablets|Televisions|Cameras|Monitors|Desktops|SmartWatches)\|'
                is_main_product = filtered_df['category'].str.contains(main_product_keywords, case=False, na=False, regex=True)
                
                # Detect accessory subcategories
                accessory_subcategories = r'LaptopAccessories|MobileAccessories|Chargers|Cables|Bags|Sleeves|Covers|Cases|Stands|Mounts|Adapters'
                is_accessory = filtered_df['category'].str.contains(accessory_subcategories, case=False, na=False, regex=True)
                
                # Boost main products over accessories
                product_boost = (is_main_product & ~is_accessory).astype(int) * 5  # +5 points for main products
                
                # Add relevance score for ranking (higher score = better match)
                # Prioritize exact word matches over partial matches
                filtered_df['relevance_score'] = (
                    filtered_name_exact.astype(int) * 10 +  # Exact word in name is most important
                    filtered_name_match.astype(int) * 3 +   # Any name match is important
                    filtered_cat_exact.astype(int) * 5 +    # Exact word in category
                    filtered_cat_match.astype(int) * 2 +    # Category matches are moderately important
                    filtered_desc_match.astype(int) * 1 +   # Description matches are less important
                    product_boost                           # Boost actual products over accessories
                )
                
                # Sort by relevance score (highest first), then by rating
                filtered_df = filtered_df.sort_values(['relevance_score', 'rating'], ascending=[False, False])
        
        # Filter by category (exact or partial match)
        if category:
            filtered_df = filtered_df[
                filtered_df['category'].str.contains(category, case=False, na=False)
            ]
        
        # Filter by minimum rating
        if min_rating is not None:
            filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
        
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
        
        # Filter by minimum discount
        if min_discount is not None:
            # Clean discount string and convert to float
            filtered_df['discount_clean'] = filtered_df['discount_percentage'].str.replace('%', '').astype(float)
            filtered_df = filtered_df[filtered_df['discount_clean'] >= min_discount]
        
        # Get total count before pagination
        total_count = len(filtered_df)
        
        # Apply pagination
        paginated_df = filtered_df.iloc[offset:offset+limit]
        
        # Remove temporary columns before returning
        columns_to_drop = ['relevance_score', 'price_clean']
        paginated_df = paginated_df.drop(columns=[col for col in columns_to_drop if col in paginated_df.columns], errors='ignore')
        
        results = paginated_df.to_dict('records')
        
        if return_total:
            return results, total_count
        return results
    
    def format_for_display(self, products: List[dict], query: str = None, compact: bool = False) -> List[dict]:
        """Format products for display with highlighted search terms
        
        Args:
            products: List of product dictionaries
            query: Search query to highlight
            compact: If True, return only essential fields
        
        Returns:
            List of formatted product dictionaries
        """
        formatted_products = []
        
        for product in products:
            formatted = {
                'product_id': product.get('product_id'),
                'product_name': product.get('product_name'),
                'category': product.get('category'),
                'discounted_price': product.get('discounted_price'),
                'actual_price': product.get('actual_price'),
                'discount_percentage': product.get('discount_percentage'),
                'rating': product.get('rating'),
                'rating_count': product.get('rating_count'),
                'img_link': product.get('img_link'),
                'product_link': product.get('product_link')
            }
            
            # Add highlighted fields if query provided
            if query:
                formatted['highlighted_fields'] = []
                
                # Check which fields match the query
                if product.get('product_name') and query.lower() in str(product.get('product_name', '')).lower():
                    formatted['highlighted_fields'].append('product_name')
                
                if product.get('category') and query.lower() in str(product.get('category', '')).lower():
                    formatted['highlighted_fields'].append('category')
                
                if product.get('about_product') and query.lower() in str(product.get('about_product', '')).lower():
                    formatted['highlighted_fields'].append('about_product')
            
            # Add full description if not compact
            if not compact:
                formatted['about_product'] = product.get('about_product')
            
            formatted_products.append(formatted)
        
        return formatted_products
    
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
