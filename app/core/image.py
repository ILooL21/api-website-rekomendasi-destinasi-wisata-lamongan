import os
import io
import uuid
import hashlib
import time
from PIL import Image
from fastapi import UploadFile

# Compress image while ensuring compatibility
async def compress_image(image: UploadFile, quality=60):
    try:
        image_bytes = await image.read()
        img_io = io.BytesIO(image_bytes)
        img = Image.open(img_io)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        compressed_io = io.BytesIO()
        img.save(compressed_io, format="JPEG", quality=quality, optimize=True)
        compressed_io.seek(0)

        return compressed_io
    except Exception as e:
        print(f"Error compressing image: {e}")
        return None

# Save compressed image to a specific path
async def save_image(image: UploadFile, path: str, quality=60):
    try:
        img_io = await compress_image(image, quality)

        if img_io is None:
            return None

        # Buat direktori jika belum ada
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "wb") as f:
            f.write(img_io.getvalue()) # gunakan getvalue()

        return path
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

# Delete image from storage
def delete_image(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            print(f"File {path} not found")
            return False
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False

async def simpan_gambar_unik(gambar: UploadFile, direktori_tujuan: str ):
    try:
        if not gambar:
            return None

        original_name = gambar.filename.encode('utf-8')
        unique_hash = hashlib.sha256(original_name + str(time.time()).encode()).hexdigest()[:16]
        filename = f"{unique_hash}_{uuid.uuid4().hex}.jpg"

        path_gambar = os.path.join(direktori_tujuan, filename)

        # Asumsi save_image adalah fungsi asinkron yang telah Anda definisikan sebelumnya
        image_path = await save_image(gambar, path_gambar)

        return image_path

    except Exception as e:
        print(f"Error menyimpan gambar unik: {e}")
        return None