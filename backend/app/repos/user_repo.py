import pandas as pd
from pathlib import Path
import threading
from typing import Optional
from ..core.errors import Conflict, NotFound


class UserRepo:
    # one lock for the whole class so reads/writes don't overlap
    _lock = threading.Lock()

    def __init__(self, csv_path: str | None = None):
        # if no path is given, use backend/data/users.csv
        if csv_path is None:
            base_path = Path(__file__).parent.parent.parent  # goes up to backend/
            csv_path = base_path / "data" / "users.csv"

        self.csv_path = Path(csv_path)
        self._reload()

    def _reload(self) -> None:
        # load CSV into a DataFrame. If CSV is missing, create it.
        cols = ["user_id", "email", "password_hash", "name", "role"]

        # make sure the folder exists
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

        # if file doesn't exist, create an empty one with the correct headers
        if not self.csv_path.exists():
            pd.DataFrame(columns=cols).to_csv(self.csv_path, index=False)

        # try reading the file
        try:
            df = pd.read_csv(self.csv_path)
        except pd.errors.EmptyDataError:
            # sometimes pandas treats a blank file as "empty"
            df = pd.DataFrame(columns=cols)

        # make sure all needed columns exist (just in case)
        for c in cols:
            if c not in df.columns:
                df[c] = pd.Series(dtype="string")

        # turn user_id into a numeric column so we can do max(), +1, etc.
        df["user_id"] = pd.to_numeric(df["user_id"], errors="coerce").astype("Int64")

        # store the DataFrame on the repo
        self.df = df

    def _save(self) -> None:
        # writes the DataFrame back to the CSV file
        # we assume the lock is already held when this is called
        self.df.to_csv(self.csv_path, index=False)

    def by_email(self, email: str) -> Optional[dict]:
        # find a user using their email (case-insensitive)
        with self._lock:
            match = self.df["email"].str.casefold() == email.casefold()
            result = self.df[match]

            if result.empty:
                return None

            return result.iloc[0].to_dict()

    def by_id(self, user_id: int) -> dict:
        # find a user by their id
        with self._lock:
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
    ) -> dict:
        # create a new user in the CSV file
        with self._lock:

            # check if the email already exists
            existing = self.df[
                self.df["email"].str.casefold() == email.casefold()
            ]
            if not existing.empty:
                raise Conflict("Email already registered")

            # figure out what the next user_id should be
            max_id = self.df["user_id"].max()
            next_id = int(max_id) + 1 if pd.notna(max_id) else 1

            # build the new row
            new_user = {
                "user_id": next_id,
                "email": email,
                "password_hash": password_hash,
                "name": name or "",
                "role": role or "user",
            }

            # add the row to the DataFrame
            self.df = pd.concat(
                [self.df, pd.DataFrame([new_user])],
                ignore_index=True,
            )

            # save updated CSV
            self._save()

            return new_user

    def update_profile(self, user_id: int, *, name: str | None) -> dict:
        # update the name of the user with this id
        with self._lock:

            # find the row that matches the user
            idx = self.df[self.df["user_id"] == user_id].index

            if len(idx) == 0:
                raise NotFound("User not found")

            # only change name if something was given
            if name is not None:
                self.df.at[idx[0], "name"] = name

            # save the CSV
            self._save()

            # return the updated user info
            return self.df.iloc[idx[0]].to_dict()

