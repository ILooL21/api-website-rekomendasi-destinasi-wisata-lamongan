from sqlalchemy import Column, Integer, String,DateTime,Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum("admin","user",name="role"), default="user",nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke rekomendasi wisata (one to one)
    rekomendasi_wisata = relationship("RekomendasiWisata", back_populates="user")

    # Relasi ke Artikel (one to many)
    artikel = relationship("Artikel", back_populates="user")

class TempatWisata(Base):
    __tablename__ = "tempat_wisata"

    id_tempat_wisata = Column(Integer, primary_key=True, index=True)
    nama_tempat = Column(String, unique=True, index=True)
    alamat = Column(Text)
    jenis = Column(Enum("Alam","Religi","Buatan",name="jenis_tempat"), default="Alam",nullable=False)
    deskripsi = Column(Text)
    gambar = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke tiket wisata (one to many)
    tiket = relationship("TiketWisata", back_populates="tempat", cascade="all, delete-orphan")

    # Relasi ke sosmed wisata (one to many)
    sosmed = relationship("SosmedWisata", back_populates="tempat" , cascade="all, delete-orphan")

class TiketWisata(Base):
    __tablename__ = "tiket_wisata"

    id_tiket = Column(Integer, primary_key=True, index=True)
    id_tempat_wisata = Column(Integer, ForeignKey("tempat_wisata.id_tempat_wisata", ondelete="CASCADE"))
    umur = Column(Enum("Dewasa", "Anak-anak", name="umur"), default="Dewasa", nullable=False)
    hari = Column(Enum("Hari Kerja", "Hari Libur", name="hari"), default="Weekday", nullable=False)
    harga = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke tempat wisata (one to many)
    tempat = relationship("TempatWisata", back_populates="tiket")

class SosmedWisata(Base):
    __tablename__ = "sosmed_wisata"

    id_sosmed = Column(Integer, primary_key=True, index=True)
    id_tempat_wisata = Column(Integer, ForeignKey("tempat_wisata.id_tempat_wisata", ondelete="CASCADE"))
    sosmed = Column(Enum("Facebook","Instagram","Twitter","Youtube","Tiktok",name="sosial_media"), nullable=False)
    link = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke tempat wisata (one to many)
    tempat = relationship("TempatWisata", back_populates="sosmed")

class RekomendasiWisata(Base):
    __tablename__ = "rekomendasi_wisata"

    id_rekomendasi = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id_user"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke user (one to one)
    user = relationship("User", back_populates="rekomendasi_wisata")

    # Relasi ke tempat wisata (one ke banyak)
    wisata = relationship("RekomendasiWisataDetail", back_populates="rekomendasi", cascade="all, delete-orphan")

class RekomendasiWisataDetail(Base):
    __tablename__ = "rekomendasi_wisata_detail"

    id = Column(Integer, primary_key=True, index=True)
    id_rekomendasi = Column(Integer, ForeignKey("rekomendasi_wisata.id_rekomendasi"))
    nama_tempat_wisata = Column(String)

    # Relasi ke rekomendasi
    rekomendasi = relationship("RekomendasiWisata", back_populates="wisata")

class Artikel(Base):
    __tablename__ = "artikel"

    id_artikel = Column(Integer, primary_key=True, index=True)
    id_penulis = Column(ForeignKey("users.id_user"))
    judul = Column(String, index=True)
    isi = Column(String)
    tanggal = Column(String)
    gambar = Column(String)
    tipe = Column(Enum("Berita","Promo",name="tipe-artikel"), default="Berita",nullable=False)
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke penulis
    user = relationship("User", back_populates="artikel")

class MailLog(Base):
    __tablename__ = "mail_log"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    subject = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)