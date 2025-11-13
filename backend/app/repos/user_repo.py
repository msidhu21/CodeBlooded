import pandas as pd
from pathlib import Path
import os
import threading
from typing import Optional
from ..core.errors import Conflict, NotFound

class UserRepo:
    _lock = threading.Lock()

    def __init__(self, csv_path: str = None):
        env_path = os.environ.get("USERS_CSV")
        if env_path:
            csv_path = Path(env_path)
        if csv_path is None:
            base_path = Path(__file__).parent.parent.parent
            csv_path = base_path / "data" / "users.csv"
        self.csv_path = csv_path
        self._reload()

    def _reload(self):
        """Reload data from CSV file."""
        self.df = pd.read_csv(self.csv_path)

    def _save(self):
        """Save data to CSV file."""
        with self._lock:
            self.df.to_csv(self.csv_path, index=False)

    def by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        result = self.df[self.df['email'] == email]
        if result.empty:
            return None
        return result.iloc[0].to_dict()

    def by_id(self, user_id: int) -> dict:
        """Get user by ID."""
        result = self.df[self.df['user_id'] == user_id]
        if result.empty:
            raise NotFound("User not found")
        return result.iloc[0].to_dict()

    def create(self, *, email: str, password_hash: str, name: str, role: str = "user") -> dict:
        """Create a new user."""
        with self._lock:
            if not self.df[self.df['email'] == email].empty:
                raise Conflict("Email already registered")

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

    def update_profile(
        self,
        user_id: int,
        *,
        name: str | None = None,
        picture: str | None = None,
        contact: dict | None = None,  # {"email": "...", "phone": "..."}
    ) -> dict:
        """
        Partial update of user profile fields (name, picture, contact).
        Creates optional columns if missing: picture, contact_email, contact_phone.
        """
        with self._lock:
            # Always refresh to avoid stale data
            self._reload()

            # Find row
            idx = self.df[self.df['user_id'] == user_id].index
            if len(idx) == 0:
                raise NotFound("User not found")
            row_idx = idx[0]

            # Ensure optional columns exist
            for col in ['picture', 'contact_email', 'contact_phone']:
                if col not in self.df.columns:
                    self.df[col] = None

            # Apply updates
            if name is not None:
                self.df.at[row_idx, 'name'] = name
            if picture is not None:
                self.df.at[row_idx, 'picture'] = picture
            if contact is not None:
                email_val = contact.get('email') if isinstance(contact, dict) else None
                phone_val = contact.get('phone') if isinstance(contact, dict) else None
                if email_val is not None:
                    self.df.at[row_idx, 'contact_email'] = email_val
                if phone_val is not None:
                    self.df.at[row_idx, 'contact_phone'] = phone_val

            # Save and return
            self._save()
            return self.df.iloc[row_idx].to_dict()
