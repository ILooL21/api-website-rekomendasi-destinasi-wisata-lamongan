from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.security import verify_password,create_access_token,verify_token
from app.db.models import User

# ambil token JWT
def get_access_token(data: dict, expires_delta: timedelta | None = None):
    return create_access_token(data, expires_delta)

# cek token JWT
def check_access_token(token: str):
    return verify_token(token)

# Autentikasi user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password):
        return user
    return None
