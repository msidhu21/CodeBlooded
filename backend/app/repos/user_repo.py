import pandas as pd
import csv
from pathlib import Path
import threading
from typing import Optional
from ..core.errors import Conflict, NotFound


class UserRepo:
    # Instance-level lock for each repository instance
    
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            base_path = Path(__file__).parent.parent.parent
            csv_path = base_path / "data" / "users.csv"

        self.csv_path = Path(csv_path)
        self._lock = threading.RLock()  # Use RLock for reentrant locking
        self._reload()
    
    def _reload(self):
        """Reload data from CSV file"""
        self.df = pd.read_csv(self.csv_path)
        for col in ["phone", "avatar_url"]:
            if col not in self.df.columns:
                self.df[col] = ""
    
    def _save(self):
        """Save data to CSV file - optimized for performance using built-in csv module"""
        with self._lock:
            # Convert DataFrame to list of dicts for faster writing
            records = self.df.to_dict('records')
            if not records:
                return
            
            # Use Python's built-in csv module for faster writes
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
    
    def by_email(self, email: str) -> Optional[dict]:
        result = self.df[self.df["email"] == email]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def by_id(self, user_id: int) -> dict:
        result = self.df[self.df["user_id"] == user_id]
        if result.empty:
            raise NotFound("User not found")
        return result.iloc[0].to_dict()
    
    def create(
        self,
        *,
        email: str,
        password_hash: str,
        name: str,
        role: str = "user",
        phone: str | None = None,
        avatar_url: str | None = None,
    ) -> dict:
        with self._lock:
            if not self.df[self.df["email"] == email].empty:
                raise Conflict("Email already registered")
            
            max_id = self.df["user_id"].max() if not self.df.empty else 0
            new_user = {
                "user_id": int(max_id) + 1,
                "email": email,
                "password_hash": password_hash,
                "name": name,
                "role": role,
                "phone": phone or "",
                "avatar_url": avatar_url or "",
            }
            
            new_row = pd.DataFrame([new_user])
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self._save()

            return new_user
    
    def update_profile(
        self,
        user_id: int,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        avatar_url: str | None = None,
    ) -> dict:
        with self._lock:
            idx = self.df[self.df["user_id"] == user_id].index
            if len(idx) == 0:
                raise NotFound("User not found")

            row_index = idx[0]

            if email is not None:
                email_conflict = self.df[
                    (self.df["email"] == email)
                    & (self.df["user_id"] != user_id)
                ]
                if not email_conflict.empty:
                    raise Conflict("Email already registered")
                self.df.at[row_index, "email"] = email

            if name is not None:
                self.df.at[row_index, "name"] = name

            if phone is not None:
                self.df.at[row_index, "phone"] = phone

            if avatar_url is not None:
                self.df.at[row_index, "avatar_url"] = avatar_url
            
            self._save()
            return self.df.iloc[row_index].to_dict()
