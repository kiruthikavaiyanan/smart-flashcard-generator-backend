from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 🔐 hash password
def hash_password(password):
    return pwd_context.hash(password)


# 🔐 verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# 🔐 create token
def create_token(data: dict):
    payload = data.copy()
    payload.update({
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# 🔐 decode token
def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None