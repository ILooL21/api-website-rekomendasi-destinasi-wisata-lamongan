from typing import Optional

from fastapi import APIRouter, Depends, Path, Form, File, UploadFile
from sqlalchemy.orm import Session

from app.schemas.destination import DestinationRequestWithFormData, SosmedItem, TiketList
from app.api.dependencies import get_db
from app.services.destination_services import create_destination, get_all_destination, get_destination_by_id, \
    update_destination_data, delete_destination_data, get_destination_data_by_name

import json

router = APIRouter()

@router.post("/")
async def add_destination(
    db: Session = Depends(get_db),
    deskripsi: str = Form(...),
    nama_tempat: str = Form(...),
    alamat: str = Form(...),
    jenis: str = Form(...),
    tiket: Optional[str] = Form(...),
    sosmed: Optional[str] = Form(...),
    gambar: UploadFile = File(...),
):
    list_tiket = TiketList(**json.loads(tiket))
    list_sosmed =  SosmedItem(**json.loads(sosmed))

    destination_data = DestinationRequestWithFormData(
        deskripsi=deskripsi,
        nama_tempat=nama_tempat,
        alamat=alamat,
        jenis=jenis,
        gambar=gambar,
        tiket=list_tiket,
        sosmed=list_sosmed,
    )
    result = await create_destination(db, destination_data)

    return result

@router.get("/")
def list_destination(db: Session = Depends(get_db)):
    return get_all_destination(db)

@router.get("/{id_tempat_wisata}")
def get_destination(id_tempat_wisata: int = Path(..., title="Destination ID", description="Must be an integer"), db: Session = Depends(get_db)):
    return get_destination_by_id(db, id_tempat_wisata)

@router.get("/details/{nama_tempat}")
def get_destination_by_name(nama_tempat: str = Path(..., title="Destination Name", description="Must be a string"), db: Session = Depends(get_db)):
    return get_destination_data_by_name(db, nama_tempat=nama_tempat)

@router.put("/{id_tempat_wisata}/update")
async def update_destination(
    id_tempat_wisata: int = Path(..., title="Destination ID", description="Must be an integer"),
    db: Session = Depends(get_db),
    deskripsi: str = Form(...),
    nama_tempat: str = Form(...),
    alamat: str = Form(...),
    jenis: str = Form(...),
    tiket: Optional[str] = Form(...),
    sosmed: Optional[str] = Form(...),
    gambar: Optional[UploadFile] = File(None),
):
    list_tiket = TiketList(**json.loads(tiket))
    list_sosmed = SosmedItem(**json.loads(sosmed))

    destination_data = DestinationRequestWithFormData(
        deskripsi=deskripsi,
        nama_tempat=nama_tempat,
        alamat=alamat,
        jenis=jenis,
        gambar=gambar,
        tiket=list_tiket,
        sosmed=list_sosmed,
    )

    return await update_destination_data(db, id_tempat_wisata, destination_data)

@router.delete("/{id_tempat_wisata}/delete")
def delete_destination(id_tempat_wisata: int = Path(..., title="Destination ID", description="Must be an integer"), db: Session = Depends(get_db)):
    return delete_destination_data(db, id_tempat_wisata)

