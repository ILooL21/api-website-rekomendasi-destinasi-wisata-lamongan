# FastAPI Project

## 📌 Deskripsi
Proyek ini adalah REST API yang dibangun menggunakan **FastAPI**, dengan dukungan **SQLAlchemy**, **Alembic**, dan **JWT Authentication** untuk manajemen pengguna.

## 🚀 Fitur
- 🔐 **Autentikasi JWT** (Login & Register)
- 🗄️ **CRUD (Create, Read, Update, Delete)**
- 🗃️ **Database dengan SQLAlchemy & PostgreSQL**
- 🔄 **Migrations dengan Alembic**
- 📄 **Swagger UI otomatis untuk dokumentasi API**

---

## 🛠 Teknologi yang Digunakan
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Passlib](https://passlib.readthedocs.io/)
- [Python-JOSE](https://github.com/mpdavis/python-jose)
- [Uvicorn](https://www.uvicorn.org/)

---

## 📂 Struktur Direktori
```
project-root/
│-- app/
│   │-- api/           # Endpoint API
│   │-- core/          # Konfigurasi dan setting
│   │-- db/            # Koneksi dan model database
│   │-- schemas/       # Validasi data dengan Pydantic
│   │-- services/      # Manajemen JWT & Hashing Password
│   │-- main.py        # Entry point aplikasi
│-- alembic.ini       # Konfigurasi Alembic
│-- .env.example      # Konfigurasi lingkungan
│-- requirements.txt  # Dependensi proyek
│-- README.md         # Dokumentasi proyek

```

---

## 📦 Instalasi
### 1️⃣ Clone Repository
```bash
git clone https://github.com/ILooL21/api-website-rekomendasi-destinasi-wisata-lamongan.git
cd api-website-rekomendasi-destinasi-wisata-lamongan
```

### 2️⃣ Buat Virtual Environment & Install Dependencies
```bash
# buat virtual environment
python -m venv venv

# aktifkan virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# install dependencies
pip install -r requirements.txt
```

### 3️⃣ Konfigurasi Environment
Copy file `.env.example` ke `.env`, lalu sesuaikan konfigurasi database dan secret key:
```
# Database Configuration
DB_ENGINE=your_database_engine_here
DB_USERNAME=your_username_here
DB_PASSWORD=your_password_here
DB_HOST=your_host_here
DB_PORT=your_port_here
DB_NAME=your_database_name

# Security Settings
SECRET_KEY=your_secret_key_here
ALGORITHM=your_algorithm_here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True

```

### 4️⃣ Jalankan Migrasi Database
```bash
alembic upgrade head
```

### 5️⃣ Jalankan Server FastAPI
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📌 Dokumentasi API
Setelah server berjalan, buka **Swagger UI** untuk melihat dokumentasi API:

📌 **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

📌 **Redoc UI:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

🚀 **Happy Coding!** 🎉

