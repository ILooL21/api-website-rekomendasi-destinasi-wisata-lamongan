from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate, UserSchema
from app.core.security import hash_password, verify_password
from typing import List


# Membuat user baru
def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role = user_data.role if user_data.role else "user"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Mendapatkan user berdasarkan username
def get_user_by_username(db: Session, username: int):
    return db.query(User).filter(User.username == username).first()

# Mendapatkan user berdasarkan id
def get_user_by_id(db: Session, id_user: int):
    return db.query(User).filter(User.id_user == id_user).first()

def get_all_users(db: Session, current_user: User) -> List[UserSchema]:
    users = db.query(User).all()
    return [
        UserSchema(
            id_user=user.id_user,
            username=user.username,
            email=user.email,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active_user=(current_user.id_user == user.id_user)
        )
        for user in users
    ]

def is_username_taken(db: Session, username: str, exclude_id: int = None) -> bool:
    user = get_user_by_username(db, username)

    if user and (exclude_id is None or user.id_user != exclude_id):
        return True

    return False

# Menghapus user
def delete_user(db: Session, id_user: int, current_user: User):
    if current_user.role != "admin" or current_user.id_user == id_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    db.query(User).filter(User.id_user == id_user).delete()
    db.commit()

    return {"message": "User berhasil dihapus"}

# Mengupdate user
def update_user(db: Session, id_user: int, user_data: UserCreate, current_user: User):
    db_user = db.query(User).filter(User.id_user == id_user).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if is_username_taken(db, user_data.username, exclude_id=id_user):
        raise HTTPException(status_code=400, detail="Username sudah digunakan")

    db_user.username = user_data.username
    db_user.email = user_data.email
    db_user.role = user_data.role
    if user_data.password:
        if current_user.id_user == id_user:
            is_valid = verify_password(user_data.oldPassword, db_user.password)
            if not is_valid:
                raise HTTPException(status_code=400, detail="Password lama salah")

        if current_user.id_user != id_user and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")

        db_user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(db_user)

    return db_user


