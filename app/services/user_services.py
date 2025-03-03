from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate
from app.core.security import hash_password
from app.api.dependencies import get_current_active_user

# Membuat user baru
def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role = user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Mendapatkan user berdasarkan username
def get_user_by_username(db: Session, username: int):
    return db.query(User).filter(User.username == username).first()

# Mendapatkan semua user
def get_all_users(db: Session):
    return db.query(User).all()

def is_username_taken(db: Session, username: str, exclude_id: int = None) -> bool:
    user = get_user_by_username(db, username)

    # Jika `exclude_id` diberikan, pastikan username yang ditemukan bukan milik user tersebut
    if user and (exclude_id is None or user.id_user != exclude_id):
        return True

    return False

# Menghapus user
def delete_user(db: Session, id_user: int):
    # cek apakah role admin
    current_user = get_current_active_user(db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    db.query(User).filter(User.id_user == id_user).delete()
    db.commit()
    return {"message": "User berhasil dihapus"}

# Mengupdate user
def update_user(db: Session, id_user: int, user_data: UserCreate):
    db_user = db.query(User).filter(User.id_user == id_user).first()

    current_user = get_current_active_user(db)
    if current_user.id_user != id_user and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Gunakan fungsi is_username_taken untuk validasi
    if is_username_taken(db, user_data.username, exclude_id=id_user):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Update data user
    db_user.username = user_data.username
    db_user.email = user_data.email
    db_user.role = user_data.role
    db.commit()
    db.refresh(db_user)
    return {"message": "User berhasil diupdate", "data": db_user}

