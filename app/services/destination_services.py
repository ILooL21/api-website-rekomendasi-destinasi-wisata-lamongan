import os
import json

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.db.models import TempatWisata, SosmedWisata, TiketWisata
from app.core.image import delete_image,simpan_gambar_unik
from app.schemas.destination import DestinationRequestWithFormData

UPLOAD_FOLDER = "public/wisata/"

async def create_destination(
    db: Session,
    destination_data: DestinationRequestWithFormData,
):
    image_path = await simpan_gambar_unik(destination_data.gambar, UPLOAD_FOLDER)

    try:
        db_destination = TempatWisata(
            nama_tempat=destination_data.nama_tempat,
            alamat=destination_data.alamat,
            jenis=destination_data.jenis,
            deskripsi=destination_data.deskripsi,
            gambar=image_path,
            latitude=destination_data.latitude,
            longitude=destination_data.longitude,
        )
        db.add(db_destination)
        db.commit()  # Commit dulu supaya ID bisa dipakai
        db.refresh(db_destination)

        if destination_data.sosmed:
            for platform, link in destination_data.sosmed.model_dump(exclude_none=True).items():
                db_sosmed = SosmedWisata(
                    id_tempat_wisata=db_destination.id_tempat_wisata,
                    sosmed=platform.capitalize(),
                    link=link
                )
                db.add(db_sosmed)

        db.commit()

        if destination_data.tiket:
            for hari, harga in destination_data.tiket.model_dump(exclude_none=True).items():
                for umur, harga_value in harga.items():
                    db_tiket = TiketWisata(
                        id_tempat_wisata=db_destination.id_tempat_wisata,
                        hari=hari.replace("_", " ").title(),
                        # jika dewasa maka umur = Dewasa, jika anak maka umur = Anak-anak
                        umur= "Anak-anak" if umur == "anak" else "Dewasa",
                        harga=harga_value
                    )

                    db.add(db_tiket)

        db.commit()

        return db_destination
    except Exception as e:
        if image_path and os.path.exists(image_path):
            delete_image(image_path)
        raise HTTPException(status_code=500, detail=f"Failed to create destination: {str(e)}")


# get all destination
def get_all_destination(db: Session):
    # urutkan dari yang terbaru
    return db.query(TempatWisata).order_by(TempatWisata.id_tempat_wisata).all()

def build_destination_response(destination):
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")

    sosmed_dict = {key: None for key in ["instagram", "facebook", "tiktok", "youtube", "twitter"]}
    for s in destination.sosmed:
        sosmed_dict[s.sosmed.lower()] = s.link

    tiket_dict = {
        "hari_kerja": {"dewasa": 0, "anak": 0},
        "hari_libur": {"dewasa": 0, "anak": 0}
    }
    for t in destination.tiket:
        hari = "hari_kerja" if t.hari == "Hari Kerja" else "hari_libur"
        umur = "dewasa" if t.umur == "Dewasa" else "anak"
        tiket_dict[hari][umur] = t.harga

    return {
        "id_tempat_wisata": destination.id_tempat_wisata,
        "nama_tempat": destination.nama_tempat,
        "alamat": destination.alamat,
        "jenis": destination.jenis,
        "deskripsi": destination.deskripsi,
        "gambar": destination.gambar,
        "sosmed": json.dumps(sosmed_dict),
        "tiket": json.dumps(tiket_dict),
        "latitude": destination.latitude,
        "longitude": destination.longitude,
    }

def get_destination_data_by_name(db: Session, nama_tempat: str):
    # Gantilah karakter "-" dengan spasi
    nama_tempat = nama_tempat.replace("-", " ")

    # Query dengan `ilike()` untuk pencarian case-insensitive
    destination = db.query(TempatWisata).options(joinedload(TempatWisata.sosmed)).filter(
        func.lower(TempatWisata.nama_tempat) == nama_tempat.lower()
    ).first()

    return build_destination_response(destination)

def get_destination_by_id(db: Session, id_tempat_wisata: int):
    destination = db.query(TempatWisata).options(joinedload(TempatWisata.sosmed)).filter(
        TempatWisata.id_tempat_wisata == id_tempat_wisata
    ).first()
    return build_destination_response(destination)


# update destination
async def update_destination_data(db: Session, id_tempat_wisata: int, destination_data: DestinationRequestWithFormData):
    db_destination = db.query(TempatWisata).filter(TempatWisata.id_tempat_wisata == id_tempat_wisata).first()

    if not db_destination:
        raise HTTPException(status_code=404, detail="Destination not found")

    if destination_data.gambar is not None:
        image_path = await simpan_gambar_unik(destination_data.gambar, UPLOAD_FOLDER)

        if db_destination.gambar and os.path.exists(db_destination.gambar):
            delete_image(db_destination.gambar)

        db_destination.gambar = image_path

    try:
        db_destination.nama_tempat = destination_data.nama_tempat
        db_destination.alamat = destination_data.alamat
        db_destination.jenis = destination_data.jenis
        db_destination.deskripsi = destination_data.deskripsi
        db_destination.latitude = destination_data.latitude
        db_destination.longitude = destination_data.longitude

        db.commit()
        db.refresh(db_destination)

        # Cari sosmed dari database
        existing_sosmed = db.query(SosmedWisata).filter(SosmedWisata.id_tempat_wisata == id_tempat_wisata).all()
        existing_sosmed_dict = {s.sosmed.lower(): s for s in existing_sosmed}

        # Update link sosmed yang ada di database
        for platform, link in destination_data.sosmed.model_dump(exclude_none=True).items():
            existing_sosmed_dict[platform.lower()].link = link

        db.commit()

        # update tiket
        existing_tiket = db.query(TiketWisata).filter(TiketWisata.id_tempat_wisata == id_tempat_wisata).all()
        existing_tiket_dict = {(t.hari, t.umur): t for t in existing_tiket}

        # Update tiket yang ada di database
        for hari, harga in destination_data.tiket.model_dump(exclude_none=True).items():
            for umur, harga_value in harga.items():
                existing_tiket_dict[(hari.replace("_", " ").title(), "Anak-anak" if umur == "anak" else "Dewasa")].harga = harga_value
        db.commit()

        return db_destination
    except Exception as e:
        if destination_data.gambar and os.path.exists(db_destination.gambar):
            delete_image(db_destination.gambar)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update destination: {str(e)}")


# delete destination
def delete_destination_data(db: Session, id_tempat_wisata: int):
    try:
        destination = db.query(TempatWisata).filter(TempatWisata.id_tempat_wisata == id_tempat_wisata).first()
        if not destination:
            raise HTTPException(status_code=404, detail="Destination not found")

        # Delete image file if it exists
        if destination.gambar and os.path.exists(destination.gambar):
            delete_image(destination.gambar)

        db.delete(destination)
        db.commit()
        return {"message": "Destination deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete destination: {str(e)}")

