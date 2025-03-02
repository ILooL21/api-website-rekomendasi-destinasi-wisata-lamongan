from sqlalchemy import Column, Integer, String,DateTime,Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke rekomendasi wisata (one to one)
    rekomendasi = relationship("RekomendasiWisata", back_populates="user")

class TempatWisata(Base):
    __tablename__ = "tempat_wisata"

    id_tempat_wisata = Column(Integer, primary_key=True, index=True)
    nama_tempat = Column(String, unique=True, index=True)
    alamat = Column(String)
    kategori = Column(Enum("Alam","Religi","Buatan",name="kategori_tempat"), default="Alam",nullable=False)
    deskripsi = Column(String)
    gambar = Column(String)
    kontak = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke koordinat wisata (one to one)
    koordinat = relationship("KoordinatWisata", back_populates="tempat", uselist=False)

    # Relasi ke tiket wisata (one to many)
    tiket = relationship("TiketWisata", back_populates="tempat", cascade="all, delete-orphan")

    # Relasi ke sosmed wisata (one to many)
    sosmed = relationship("SosmedWisata", back_populates="tempat" , cascade="all, delete-orphan")

    # Relasi ke rekomendasi wisata (one ke banyak)
    rekomendasi = relationship("RekomendasiWisataDetail", back_populates="wisata", cascade="all, delete-orphan")

class KoordinatWisata(Base):
    __tablename__ = "koordinat_wisata"

    id_koordinat = Column(Integer, primary_key=True, index=True)
    id_tempat_wisata = Column(Integer, ForeignKey("tempat_wisata.id_tempat_wisata", ondelete="CASCADE"))
    latitude = Column(String)
    longitude = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke tempat wisata (one to one)
    tempat = relationship("TempatWisata", back_populates="koordinat")

class TiketWisata(Base):
    __tablename__ = "tiket_wisata"

    id_tiket = Column(Integer, primary_key=True, index=True)
    id_tempat_wisata = Column(Integer, ForeignKey("tempat_wisata.id_tempat_wisata", ondelete="CASCADE"))
    kategori = Column(Enum("Reguler", "VIP", name="kategori_tiket"), default="Reguler", nullable=False)
    umur = Column(Enum("Dewasa", "Anak-anak", name="umur_tiket"), default="Dewasa", nullable=False)
    hari = Column(Enum("Weekday", "Weekend/Hari Libur", name="hari_tiket"), default="Weekday", nullable=False)
    harga = Column(Integer)
    keterangan = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    # Relasi ke tempat wisata (one to many)
    tempat = relationship("TempatWisata", back_populates="tiket")

class SosmedWisata(Base):
    __tablename__ = "sosmed_wisata"

    id_sosmed = Column(Integer, primary_key=True, index=True)
    id_tempat_wisata = Column(Integer, ForeignKey("tempat_wisata.id_tempat_wisata", ondelete="CASCADE"))
    sosmed = Column(Enum("Facebook","Instagram","Twitter","Youtube","Tiktok",name="sosmed"), nullable=False)
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

    # Relasi ke tempat wisata (one ke banyak)
    wisata = relationship("RekomendasiWisataDetail", back_populates="rekomendasi", cascade="all, delete-orphan")

class RekomendasiWisataDetail(Base):
    __tablename__ = "rekomendasi_wisata_detail"

    id = Column(Integer, primary_key=True, index=True)
    id_rekomendasi = Column(Integer, ForeignKey("rekomendasi_wisata.id_rekomendasi"))
    id_tempat_wisata = Column(Integer, ForeignKey("tempat_wisata.id_tempat_wisata"))

    # Relasi ke rekomendasi
    rekomendasi = relationship("RekomendasiWisata", back_populates="wisata")

    # Relasi ke tempat wisata
    wisata = relationship("TempatWisata", back_populates="rekomendasi")

class Artikel(Base):
    __tablename__ = "artikel"

    id_artikel = Column(Integer, primary_key=True, index=True)
    judul = Column(String, index=True)
    isi = Column(String)
    penulis = Column(String)
    tanggal = Column(String)
    gambar = Column(String)
    tipe = Column(Enum("Berita","Promosi",name="tipe_artikel"), default="Berita",nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
