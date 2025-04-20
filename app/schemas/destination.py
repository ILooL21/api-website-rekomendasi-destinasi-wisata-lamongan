from fastapi import Form, File, UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional,Dict

class SosmedItem(BaseModel):
    instagram: str = ""
    facebook: str = ""
    tiktok: str = ""
    youtube: str = ""
    twitter: str = ""

class TiketItem(BaseModel):
    dewasa: Optional[int] = 0
    anak: Optional[int] = 0

class TiketList(BaseModel):
    hari_kerja: TiketItem
    hari_libur: TiketItem

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
    tiket: TiketList
    gambar: Optional[UploadFile] = File(None)
    latitude: Optional[str] = Form(None)
    longitude: Optional[str] = Form(None)


