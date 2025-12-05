import pandas as pd
import csv
from pathlib import Path
import threading
from typing import Optional
from ..core.errors import Conflict, NotFound


EDITABLE_FIELDS = [
    "name",
    "email",
    "role",
    "picture",
    "contact_email",
    "contact_phone",
]


class UserRepo:
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            base_path = Path(__file__).parent.parent.parent
            csv_path = base_path / "data" / "users.csv"

        self.csv_path = Path(csv_path)
        self._lock = threading.RLock()
        self._reload()

    def _reload(self):
        self.df = pd.read_csv(self.csv_path)

        # Create columns if missing
        for col in EDITABLE_FIELDS:
            if col not in self.df.columns:
                self.df[col] = ""

    def _save(self):
        with self._lock:
            records = self.df.to_dict("records")
            if not records:
                return
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)

    def by_id(self, user_id: int) -> dict:
        result = self.df[self.df["user_id"] == user_id]
        if result.empty:
            raise NotFound("User not found")
        return result.iloc[0].to_dict()

    def by_email(self, email: str) -> Optional[dict]:
        result = self.df[self.df["email"] == email]
        if result.empty:
            return None
        return result.iloc[0].to_dict()

    def update_profile(self, user_id: int, **updates) -> dict:
        """Dynamically update ANY editable field."""
        with self._lock:
            idx = self.df[self.df["user_id"] == user_id].index
            if len(idx) == 0:
                raise NotFound("User not found")

            row = idx[0]

            # Apply only fields that are editable
            for field, value in updates.items():
                if field in EDITABLE_FIELDS and value is not None:
                    self.df.at[row, field] = value

            self._save()
            return self.df.iloc[row].to_dict()
