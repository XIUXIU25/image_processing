from fastapi import APIRouter, HTTPException, Depends, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Dict
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret"  # use env var in prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Fake in-memory database
fake_users_db: Dict[str, Dict] = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # Example placeholder implementation — replace with real logic
    if token != "valid-token":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"username": "testuser"}

# Password utils
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Auth API
@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[username] = {"username": username, "password": get_password_hash(password)}
    return {"message": "User registered"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")