from typing import Optional

from fastapi import APIRouter, Depends, Path,Form,File,UploadFile
from sqlalchemy.orm import Session

from app.schemas.artikel import ArtikelRequestWithFormData
from app.api.dependencies import get_db, get_current_active_user
from app.services.artikel_services import create_artikel, get_all_artikel, get_artikel_by_id, update_artikel_data, \
    delete_artikel_data, get_latest_artikel_data
from app.db.models import User

import json

router = APIRouter()

@router.post("/")
async def add_artikel(judul: str = Form(...),
    isi: str = Form(...),
    tipe: str = Form(...),
    tags: str = Form(...),
    gambar: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)):

    list_tags = json.loads(tags)
    artikel_data = ArtikelRequestWithFormData(
        judul=judul,
        isi=isi,
        tipe=tipe,
        tags=list_tags  ,
        gambar=gambar
    )
    result = await create_artikel(db, artikel_data,current_user)

    return result

@router.get("/")
def list_artikel(db: Session = Depends(get_db)):
    return get_all_artikel(db)

@router.get("/{id_artikel}")
def get_artikel(id_artikel: int = Path(..., title="Artikel ID", description="Must be an integer"), db: Session = Depends(get_db)):
    return get_artikel_by_id(db, id_artikel)

@router.get("/data/latest")
def get_latest_artikel(db: Session = Depends(get_db)):
    return get_latest_artikel_data(db)

@router.put("/{id_artikel}/update")
async def update_artikel(
    id_artikel: int = Path(..., title="Artikel ID", description="Must be an integer"),
    judul: str = Form(...),
    isi: str = Form(...),
    tipe: str = Form(...),
    tags: str = Form(...),
    gambar: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)):

    list_tags = json.loads(tags)
    artikel_data = ArtikelRequestWithFormData(
        judul=judul,
        isi=isi,
        tipe=tipe,
        tags=list_tags,
        gambar=gambar
    )

    return await update_artikel_data(db, id_artikel, artikel_data)

@router.delete("/{id_artikel}/delete")
def delete_artikel(id_artikel: int = Path(..., title="Artikel ID", description="Must be an integer"), db: Session = Depends(get_db)):
    return delete_artikel_data(db, id_artikel)
