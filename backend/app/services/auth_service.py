from fastapi import HTTPException

from ..repos.user_repo import UserRepo
from ..core.security import hash_password, verify_password
from ..models.dto import RegisterRequest, LoginRequest, AuthUser
from ..core.errors import Unauthorized, Conflict


# we just make our own IntegrityError so the code still works
class IntegrityError(Exception):
    pass


class AuthService:
    def __init__(self) -> None:
        # our service always talks to the UserRepo (CSV file)
        self.repo = UserRepo()

    # turns whatever the repo gives us into a clean dictionary for AuthUser
    def _to_user_dict(self, u, fallback_name: str | None = None) -> dict:
        # if it's already a dictionary just copy it
        if isinstance(u, dict):
            data = u.copy()
        else:
            # otherwise try getting values from the object
            data = {
                "id": getattr(u, "id", None) or getattr(u, "user_id", None),
                "email": getattr(u, "email", None),
                "name": getattr(u, "name", None)
                        or getattr(u, "username", None)
                        or fallback_name,
                "role": getattr(u, "role", None),
            }

        # if repo returned "user_id" instead of "id"
        if "id" not in data and "user_id" in data:
            data["id"] = data["user_id"]

        # make sure id is always an int
        try:
            data["id"] = int(data.get("id", 0) or 0)
        except Exception:
            data["id"] = 0

        # default role is "user"
        if not data.get("role"):
            data["role"] = "user"

        # default name if nothing was provided
        if not data.get("name"):
            data["name"] = fallback_name

        return data

    # register a brand new user
    def register(self, req: RegisterRequest) -> AuthUser:
        # check if someone already used this email
        existing = self.repo.by_email(req.email)
        if existing is not None:
            raise HTTPException(status_code=400, detail="Email already registered")

        # hash their password so we never store plain text
        pwd_hash = hash_password(req.password)
        display_name = req.name or ""

        # try saving the new user to the CSV
        try:
            created = self.repo.create(
                email=req.email,
                password_hash=pwd_hash,
                name=display_name,
            )
        except (IntegrityError, Conflict):
            # email already existed according to repo
            raise HTTPException(status_code=400, detail="Email already registered")
        except Exception:
            # basically if anything weird happens
            raise HTTPException(status_code=500, detail="Could not register user")

        # convert the repo result back into an AuthUser model
        user_dict = self._to_user_dict(created, fallback_name=display_name)
        return AuthUser(**user_dict)

    # login existing user
    def login(self, req: LoginRequest) -> AuthUser:
        # check if the email is in our CSV
        user = self.repo.by_email(req.email)
        if user is None:
            # same message so attackers can't guess valid emails
            raise Unauthorized("Invalid email or password")

        # check if the password matches the stored hash
        if not verify_password(req.password, user.get("password_hash", "")):
            raise Unauthorized("Invalid email or password")

        # return clean user data
        user_dict = self._to_user_dict(user)
        return AuthUser(**user_dict)

    # get profile by id
    def get_profile(self, user_id: int) -> AuthUser:
        # pull the data from the CSV
        user = self.repo.by_id(user_id)
        user_dict = self._to_user_dict(user)
        return AuthUser(**user_dict)

    # update only the name for now
    def update_profile(self, user_id: int, *, name: str | None = None) -> AuthUser:
        # ask repo to update the CSV entry
        updated = self.repo.update_profile(user_id=user_id, name=name)

        # convert result into model
        user_dict = self._to_user_dict(updated, fallback_name=name)
        return AuthUser(**user_dict)
