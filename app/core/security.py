from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from app.core.config import settings
from typing import Optional

# Inisialisasi hashing password menggunakan bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 untuk autentikasi dengan token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Secret key dan algoritma JWT
SECRET_KEY = settings.SECRET_KEY  # Pastikan ini diatur di konfigurasi (core/config.py)
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Fungsi untuk hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Fungsi untuk memverifikasi password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Fungsi untuk membuat token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Fungsi untuk memverifikasi token JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token tidak valid")

# Dependency untuk mendapatkan pengguna dari token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Tidak dapat memvalidasi token")
    payload = verify_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    return payload["sub"]
