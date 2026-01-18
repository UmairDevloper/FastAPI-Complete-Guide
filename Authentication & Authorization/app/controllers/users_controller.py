from fastapi import HTTPException
from pathlib import Path
import json
from pydantic import EmailStr
from typing import List, Dict
from app.models.users_model import User
from app.utilis.utilis_helper import hash_password, verify_password, create_access_token

DATA_FILE = Path(__file__).parent.parent / "data" / "users.json"

def get_all_users() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users: Dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

def add_users(user: User) -> Dict:
    users = get_all_users()
    if any(u["email"] == user.email for u in users):
        raise ValueError("User already exists")
    hashed_pwd = hash_password(user.password)
    new_user = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password":hashed_pwd,
    }
    users.append(new_user)
    save_users(users)
    return new_user


def verify_user(email: EmailStr, password: str) -> dict:
    old_users = get_all_users()
    try:
        for u in old_users:
            if u["email"] == email:
                if verify_password(password, u["password"]):
                    token_data = {"sub": email}
                    token = create_access_token(token_data)
                    return {
                        "data": u,
                        "token": token,
                        "message": "Logged in successfully."
                    }
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )



