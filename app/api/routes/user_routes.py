from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserSchema
from app.services.user_services import create_user, is_username_taken, get_all_users, update_user,delete_user, get_user_by_id
from app.api.dependencies import get_db, get_current_active_user
from app.db.models import User


router = APIRouter()

# 🔹 Register User
@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if is_username_taken(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username sudah digunakan")
    return create_user(db, user_data)

# 🔹 Get All Users
@router.get("/", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_all_users(db, current_user)

# get active user data
@router.get("/me", response_model=UserResponse)
def get_active_user_data(current_user: User = Depends(get_current_active_user)):
    return current_user

# 🔹 Get User by ID
@router.get("/{id_user}", response_model=UserResponse)
def get_user(id_user: int = Path(..., title="User ID", description="Must be an integer"), db: Session = Depends(get_db)):
    user = get_user_by_id(db, id_user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 🔹 Update User
@router.put("/{id_user}", response_model=UserResponse)
def update_user_data(id_user: int, user_data: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return update_user(db, id_user, user_data, current_user)

# 🔹 Delete User
@router.delete("/{id_user}")
def delete_user_data(id_user: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return delete_user(db, id_user, current_user)
