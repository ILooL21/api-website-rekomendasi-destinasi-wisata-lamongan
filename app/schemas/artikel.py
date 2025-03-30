from fastapi import Form, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional

class ArtikelBase(BaseModel):
    judul: str
    isi: str
    tipe: str
    tags: list[str]

class ArtikelRequestWithFormData(BaseModel):

    judul: str = Form(...)
    isi: str = Form(...)
    tipe: str = Form(...)
    tags: List[str]  # ⬅️ Akan dikumpulkan manual dari form
    gambar: Optional[UploadFile] = File(None)

class ArtikelResponse(BaseModel):
    id_artikel: int
    judul: str
    isi: str
    tanggal: str
    gambar: Optional[str]
    tipe: str
    tags: Optional[str]
    penulis: str

