from fastapi import APIRouter
import json, os

router = APIRouter(prefix="/auth")

DATA_PATH = "app/data/users.json"

@router.post("/register")
def register(user: dict):
    os.makedirs("app/data", exist_ok=True)

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            users = json.load(f)
    else:
        users = []

    if any(u["email"] == user.get("email") for u in users):
        return {"error": "User already exists"}

    users.append(user)

    with open(DATA_PATH, "w") as f:
        json.dump(users, f, indent=2)

    return {"message": "User created successfully"}


