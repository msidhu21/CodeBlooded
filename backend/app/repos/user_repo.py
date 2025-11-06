import pandas as pd
from pathlib import Path
import threading
from typing import Optional
from ..core.errors import Conflict, NotFound

class UserRepo:
    _lock = threading.Lock()
    
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            base_path = Path(__file__).parent.parent.parent
            csv_path = base_path / "data" / "users.csv"
        self.csv_path = csv_path
        self._reload()
    
    def _reload(self):
        """Reload data from CSV file"""
        self.df = pd.read_csv(self.csv_path)
    
    def _save(self):
        """Save data to CSV file"""
        with self._lock:
            self.df.to_csv(self.csv_path, index=False)
    
    def by_email(self, email: str) -> Optional[dict]:
        """Get user by email"""
        result = self.df[self.df['email'] == email]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def by_id(self, user_id: int) -> dict:
        """Get user by ID"""
        result = self.df[self.df['user_id'] == user_id]
        if result.empty:
            raise NotFound("User not found")
        return result.iloc[0].to_dict()
    
    def create(self, *, email: str, password_hash: str, name: str, role: str = "user") -> dict:
        """Create a new user"""
        with self._lock:
            # Check if email already exists
            if not self.df[self.df['email'] == email].empty:
                raise Conflict("Email already registered")
            
            # Generate new user_id
            max_id = self.df['user_id'].max() if not self.df.empty else 0
            new_user = {
                'user_id': int(max_id) + 1,
                'email': email,
                'password_hash': password_hash,
                'name': name,
                'role': role
            }
            
            new_row = pd.DataFrame([new_user])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self._save()
            return new_user
    
    def update_profile(self, user_id: int, *, name: str | None) -> dict:
        """Update user profile"""
        with self._lock:
            idx = self.df[self.df['user_id'] == user_id].index
            if len(idx) == 0:
                raise NotFound("User not found")
            
            if name is not None:
                self.df.at[idx[0], 'name'] = name
            
            self._save()
            return self.df.iloc[idx[0]].to_dict()

