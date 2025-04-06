import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.core.config import settings
from app.api.routes import auth_routes, user_routes, contact_routes,artikel_routes,destination_routes

# Inisialisasi database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User Authentication")

# cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins= settings.ALLOWED_HOSTS,
    allow_credentials=settings.ALLOWED_CREDENTIALS,
    allow_methods= settings.ALLOWED_METHODS,
    allow_headers= settings.ALLOWED_HEADERS,
    max_age=3600,
)

# Memasukkan routes
app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/api/users", tags=["Users"])
app.include_router(contact_routes.router, prefix="/api/contact", tags=["Contact"])
app.include_router(artikel_routes.router, prefix="/api/articles", tags=["Artikel"])
app.include_router(destination_routes.router, prefix="/api/destinations", tags=["Destinations"])

# mount static files public
app.mount("/public", StaticFiles(directory="public"), name="public")

if __name__ == "__main__":
    uvicorn.run(app, host= settings.APP_HOST, port= settings.APP_PORT)
