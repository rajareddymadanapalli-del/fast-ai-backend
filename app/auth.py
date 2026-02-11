from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext

# 1. Configuration for Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Configuration for JWT
SECRET_KEY = "your-super-secret-key-change-this" # In production, use an environment variable!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
