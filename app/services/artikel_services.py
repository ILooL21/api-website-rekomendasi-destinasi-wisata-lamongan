import os
import time

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Artikel,User
from app.schemas.artikel import ArtikelRequestWithFormData
from app.core.image import delete_image,simpan_gambar_unik


UPLOAD_FOLDER = "public/artikel/"

async def create_artikel(
    db: Session,
    artikel_data: ArtikelRequestWithFormData,
    current_user: User
):
    image_path = await simpan_gambar_unik(artikel_data.gambar,UPLOAD_FOLDER)

    try:
        # Simpan artikel ke database
        db_artikel = Artikel(
            id_penulis=current_user.id_user,
            judul=artikel_data.judul,
            isi=artikel_data.isi,
            tanggal=time.strftime("%Y-%m-%d %H:%M:%S"),
            gambar=image_path,
            tipe=artikel_data.tipe,
            tags=",".join(artikel_data.tags) if artikel_data.tags else "",
        )

        db.add(db_artikel)
        db.commit()
        db.refresh(db_artikel)
        return db_artikel

    except Exception as e:
        if image_path and os.path.exists(image_path):
            delete_image(image_path)
        raise HTTPException(status_code=500, detail=f"Failed to create artikel: {str(e)}")

# get all artikel
def get_all_artikel(db: Session):
    artikels = (
        db.query(
            Artikel.id_artikel,
            Artikel.judul,
            Artikel.isi,
            Artikel.tanggal,
            Artikel.gambar,
            Artikel.tipe,
            Artikel.tags,
            Artikel.created_at,
            User.username.label("penulis"),
        )
        .join(User, Artikel.id_penulis == User.id_user)
        .order_by(Artikel.id_artikel.desc())
        .all()
    )

    # Konversi hasil query ke list of dict
    return [
        {
            "id_artikel": artikel.id_artikel,
            "judul": artikel.judul,
            "isi": artikel.isi,
            "tanggal": artikel.tanggal,
            "gambar": artikel.gambar,
            "tipe": artikel.tipe,
            "tags": artikel.tags,
            "penulis": artikel.penulis,
            "created_at": artikel.created_at,
        }
        for artikel in artikels
    ]


def get_artikel_by_id(db: Session, id_artikel: int):
    response = (
        db.query(
            Artikel.id_artikel,
            Artikel.judul,
            Artikel.isi,
            Artikel.tanggal,
            Artikel.gambar,
            Artikel.tipe,
            Artikel.tags,
            Artikel.created_at,
            User.username.label("penulis"),
        )
        .join(User, Artikel.id_penulis == User.id_user)
        .filter(Artikel.id_artikel == id_artikel)
        .order_by(Artikel.id_artikel)
        .first()
    )

    return [
        {
            "id_artikel": response.id_artikel,
            "judul": response.judul,
            "isi": response.isi,
            "tanggal": response.tanggal,
            "gambar": response.gambar,
            "tipe": response.tipe,
            "tags": response.tags,
            "penulis": response.penulis,
            "created_at": response.created_at,
        }
    ]

def get_latest_artikel_data(db: Session, limit: int = 5):
    latest_artikels = (
        db.query(
            Artikel.id_artikel,
            Artikel.judul,
            Artikel.isi,
            Artikel.tanggal,
            Artikel.gambar,
            Artikel.tipe,
            Artikel.tags,
            Artikel.created_at,
            User.username.label("penulis"),
        )
        .join(User, Artikel.id_penulis == User.id_user)
        .order_by(Artikel.id_artikel.desc())
        .limit(limit)  # 2. Batasi hasilnya HANYA sebanyak `limit`
        .all()  # 3. Eksekusi query
    )

    # Konversi hasil query ke list of dict, sama seperti fungsi Anda yang lain
    return [
        {
            "id_artikel": artikel.id_artikel,
            "judul": artikel.judul,
            "isi": artikel.isi,
            "tanggal": artikel.tanggal,
            "gambar": artikel.gambar,
            "tipe": artikel.tipe,
            "tags": artikel.tags,
            "penulis": artikel.penulis,
            "created_at": artikel.created_at,
        }
        for artikel in latest_artikels
    ]

async def update_artikel_data(db: Session, id_artikel: int, artikel_data: ArtikelRequestWithFormData):
    # Ambil data artikel dari fungsi yang return list of dict
    artikel_result = get_artikel_by_id(db, id_artikel)
    if not artikel_result:
        raise HTTPException(status_code=404, detail="Artikel not found")

    artikel_dict = artikel_result[0]  # Ambil dict dari list

    # Ambil objek SQLAlchemy asli untuk update
    db_artikel = db.query(Artikel).filter(Artikel.id_artikel == id_artikel).first()
    if not db_artikel:
        raise HTTPException(status_code=404, detail="Artikel object not found in DB")

    # jika ada gambar baru
    if artikel_data.gambar is not None:
        if artikel_dict["gambar"] and os.path.exists(artikel_dict["gambar"]):
            delete_image(artikel_dict["gambar"])

        # Simpan gambar baru
        image_path = await simpan_gambar_unik(artikel_data.gambar, UPLOAD_FOLDER)
        db_artikel.gambar = image_path

    try:
        # Update data
        db_artikel.judul = artikel_data.judul
        db_artikel.isi = artikel_data.isi
        db_artikel.tipe = artikel_data.tipe
        db_artikel.tags = ",".join(artikel_data.tags) if artikel_data.tags else ""

        db.commit()
        db.refresh(db_artikel)

        return db_artikel

    except Exception as e:
        if db_artikel.gambar and os.path.exists(db_artikel.gambar):
            delete_image(db_artikel.gambar)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update artikel: {str(e)}")




# delete artikel
def delete_artikel_data(db: Session, id_artikel: int):
    db_artikel_list = get_artikel_by_id(db, id_artikel)

    if db_artikel_list:
        db_artikel = db_artikel_list[0]

        print(db_artikel["gambar"])

        if db_artikel["gambar"] and os.path.exists(db_artikel["gambar"]):
            delete_image(db_artikel["gambar"])

        # Hapus dari tabel Artikel (pakai model aslinya)
        artikel_obj = db.query(Artikel).filter(Artikel.id_artikel == id_artikel).first()
        if artikel_obj:
            db.delete(artikel_obj)
            db.commit()
            return {"message": "Artikel deleted"}
        else:
            raise HTTPException(status_code=404, detail="Artikel object not found in DB")
    else:
        raise HTTPException(status_code=404, detail="Artikel not found")


