from fastapi import APIRouter, HTTPException
from app.models import UserCreate
from app.auth import fake_users_db, get_password_hash, create_access_token

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[user.username] = {
        "username": user.username,
        "password": get_password_hash(user.password)
    }
    token = create_access_token({"sub": user.username})
    return {"username": user.username, "token": token}

@router.post("/login")
def login(user: UserCreate):
    from app.auth import authenticate_user
    db_user = authenticate_user(user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"username": user.username, "token": token}