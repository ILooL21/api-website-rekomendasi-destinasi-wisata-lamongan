from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.schemas.user import UserCreate
from app.services.auth_services import authenticate_user,get_access_token
from app.schemas.auth import Token, LoginRequest
from app.api.dependencies import get_db
from app.core.config import settings
from app.db.models import User
from app.services.user_services import create_user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email atau password salah")

    access_token = get_access_token(
        data={"sub": str(user.id_user)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login/social-media", response_model=Token)
def login_social_media(request: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    # jika user ada langsung berikan token jika tidak ada buat user baru
    if not user:
        user = create_user(db, request)

    access_token = get_access_token(
        data={"sub": str(user.id_user)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}

