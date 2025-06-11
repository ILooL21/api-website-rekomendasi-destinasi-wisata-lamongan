from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional,Dict

class SosmedItem(BaseModel):
    instagram: str = ""
    facebook: str = ""
    tiktok: str = ""
    youtube: str = ""
    twitter: str = ""

class DestinationBase(BaseModel):
    nama_tempat: str
    alamat: str
    jenis: str
    deskripsi: str

class DestinationRequestWithFormData(BaseModel):
    nama_tempat: str = Form(...)
    alamat: str = Form(...)
    jenis: str = Form(...)
    deskripsi: str = Form(...)
    sosmed: SosmedItem
    deskripsi_tiket: Optional[str] = None
    link_tiket: Optional[str] = None
    gambar: Optional[UploadFile] = File(None)
    latitude: Optional[str] = Form(None)
    longitude: Optional[str] = Form(None)


