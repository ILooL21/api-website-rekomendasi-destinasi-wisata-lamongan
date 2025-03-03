from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routes import auth_routes, user_routes

# Inisialisasi database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User Authentication")

# Memasukkan routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
