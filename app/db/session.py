from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Membuat engine SQLAlchemy
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_db_connection():
    """ Cek apakah koneksi ke database berhasil """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("Database Connected")
    except Exception as e:
        error_msg = f"Database connection error: {str(e)}"
        error_dict = {"status": "Database Connection Failed", "error": error_msg}

        print(error_dict)
