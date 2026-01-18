from fastapi import FastAPI, HTTPException, Depends
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordBearer

from app.models.users_model import User, LoginRequest
from app.controllers.users_controller import get_all_users, add_users, verify_user
from app.utilis.utilis_helper import get_current_user
from app.utilis.utilis_helper import create_access_token
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI."}

@app.get("/list-user")
def get_users() -> list[dict]:
    return get_all_users()

@app.post("/register")
def create_users(user: User):
    try:
        return add_users(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.post("/login")
def validate_user(user: LoginRequest) -> dict:
    return verify_user(user.email, user.password)



@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, you are authenticated!"}

