import pandas as pd
import csv
from pathlib import Path
import threading
from typing import List, Optional
from ..core.errors import NotFound

class WishlistRepo:
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            base_path = Path(__file__).parent.parent.parent
            csv_path = base_path / "data" / "wishlists.csv"
        
        self.csv_path = Path(csv_path)
        self._lock = threading.RLock()
        self._ensure_file_exists()
        self._reload()
    
    def _ensure_file_exists(self):
        if not self.csv_path.exists():
            with self._lock:
                with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['user_id', 'product_id', 'added_at'])
                    writer.writeheader()
    
    def _reload(self):
        try:
            self.df = pd.read_csv(self.csv_path)
            if self.df.empty:
                self.df = pd.DataFrame(columns=['user_id', 'product_id', 'added_at'])
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.df = pd.DataFrame(columns=['user_id', 'product_id', 'added_at'])
    
    def _save(self):
        with self._lock:
            records = self.df.to_dict('records')
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                if records:
                    writer = csv.DictWriter(f, fieldnames=records[0].keys())
                    writer.writeheader()
                    writer.writerows(records)
                else:
                    writer = csv.DictWriter(f, fieldnames=['user_id', 'product_id', 'added_at'])
                    writer.writeheader()
    
    def add_to_wishlist(self, user_id: int, product_id: str) -> dict:
        with self._lock:
            existing = self.df[
                (self.df['user_id'] == user_id) & 
                (self.df['product_id'] == product_id)
            ]
            
            if not existing.empty:
                return existing.iloc[0].to_dict()
            
            import datetime
            new_item = {
                'user_id': user_id,
                'product_id': product_id,
                'added_at': datetime.datetime.now().isoformat()
            }
            
            new_row = pd.DataFrame([new_item])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self._save()
            
            return new_item
    
    def remove_from_wishlist(self, user_id: int, product_id: str) -> bool:
        with self._lock:
            initial_len = len(self.df)
            self.df = self.df[
                ~((self.df['user_id'] == user_id) & (self.df['product_id'] == product_id))
            ]
            
            if len(self.df) < initial_len:
                self._save()
                return True
            return False
    
    def get_user_wishlist(self, user_id: int) -> List[str]:
        result = self.df[self.df['user_id'] == user_id]
        return result['product_id'].tolist()
    
    def is_in_wishlist(self, user_id: int, product_id: str) -> bool:
        result = self.df[
            (self.df['user_id'] == user_id) & 
            (self.df['product_id'] == product_id)
        ]
        return not result.empty
    
    def get_wishlist_count(self, user_id: int) -> int:
        return len(self.df[self.df['user_id'] == user_id])

