from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.entities import User
from ..core.errors import Conflict, NotFound

class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def by_email(self, email: str) -> Optional[User]:
        return self.db.execute(select(User).where(User.email == email)).scalars().first()

    def create(self, *, email: str, password_hash: str, name: str, role: str = "user") -> User:
        if self.by_email(email):
            raise Conflict("Email already registered")
        u = User(email=email, password_hash=password_hash, name=name, role=role)
        self.db.add(u)
        self.db.flush()
        return u

    def by_id(self, user_id: int) -> User:
        u = self.db.get(User, user_id)
        if not u:
            raise NotFound("User not found")
        return u

    def update_profile(self, user_id: int, *, name: str | None) -> User:
        u = self.by_id(user_id)
        if name is not None:
            u.name = name
        self.db.flush()
        return u

