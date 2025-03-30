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
            User.username.label("penulis"),
        )
        .join(User, Artikel.id_penulis == User.id_user)
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
        }
        for artikel in artikels
    ]


# get artikel by id
def get_artikel_by_id(db: Session, id_artikel: int):
    return db.query(Artikel).filter(Artikel.id_artikel == id_artikel).first()

# update artikel
async def update_artikel_data(db: Session, id_artikel: int, artikel_data: ArtikelRequestWithFormData):
    # Cari artikel berdasarkan ID
    db_artikel = get_artikel_by_id(db, id_artikel)
    if not db_artikel:
        raise HTTPException(status_code=404, detail="Artikel not found")

    # jika type gambar adalah UploadFile
    if artikel_data.gambar is not None :
        if db_artikel.gambar and os.path.exists(db_artikel.gambar):
            delete_image(db_artikel.gambar)

        # Simpan gambar baru
        image_path = await simpan_gambar_unik(artikel_data.gambar, UPLOAD_FOLDER)
        db_artikel.gambar = image_path

    try:
        # Perbarui data artikel
        db_artikel.judul = artikel_data.judul
        db_artikel.isi = artikel_data.isi
        db_artikel.tipe = artikel_data.tipe
        db_artikel.tags = ",".join(artikel_data.tags) if artikel_data.tags else ""

        # Commit perubahan ke database
        db.commit()
        db.refresh(db_artikel)

        # ✅ Pastikan mengembalikan data yang dapat di-encode JSON
        return db_artikel

    except Exception as e:
        if artikel_data.gambar and os.path.exists(db_artikel.gambar):
            delete_image(db_artikel.gambar)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update artikel: {str(e)}")



# delete artikel
def delete_artikel_data(db: Session, id_artikel: int):
    db_artikel = get_artikel_by_id(db, id_artikel)

    if db_artikel:
        if db_artikel.gambar and os.path.exists(db_artikel.gambar):
            delete_image(db_artikel.gambar)

        db.delete(db_artikel)
        db.commit()
        return {"message": "Artikel deleted"}
    else:
        raise HTTPException(status_code=404, detail="Artikel not found")

