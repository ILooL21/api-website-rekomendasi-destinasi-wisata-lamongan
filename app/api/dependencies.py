from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import get_current_user
from app.db.models import User
from app.services.user_services import get_user_by_id

# 🔹 Dependency untuk mendapatkan session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Dependency untuk mendapatkan pengguna yang sedang login
def get_current_active_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id_user == current_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user

# 🔹 Dependency untuk mengecek apakah user adalah admin
def get_admin_user(
    current_user: User = Depends(get_current_active_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak, hanya untuk admin")
    return current_user
