import uvicorn
from app.core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.api.routes import auth_routes, user_routes, contact_routes

# Inisialisasi database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User Authentication")

# cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f'{settings.ALLOWED_HOSTS}'],
    allow_credentials=settings.ALLOWED_CREDENTIALS,
    allow_methods=[f'{settings.ALLOWED_METHODS}'],
    allow_headers=[f'{settings.ALLOWED_HEADERS}'],
    max_age=3600,
)

# Memasukkan routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(contact_routes.router, prefix="/api/contact", tags=["Contact"])

if __name__ == "__main__":
    uvicorn.run(app, host= settings.APP_HOST, port= settings.APP_PORT)
