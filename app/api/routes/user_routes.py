from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.services.user_services import create_user, is_username_taken, get_all_users, update_user,delete_user
from app.api.dependencies import get_db

router = APIRouter()

# 🔹 Register User
@router.post("/", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if is_username_taken(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    return create_user(db, user_data)

# 🔹 Get All Users
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)

# 🔹 Update User
@router.put("/{id_user}", response_model=UserResponse)
def update_user_data(id_user: int, user_data: UserCreate, db: Session = Depends(get_db)):
    return update_user(db, id_user, user_data)

# 🔹 Delete User
@router.delete("/{id_user}")
def delete_user_data(id_user: int, db: Session = Depends(get_db)):
    return delete_user(db, id_user)
