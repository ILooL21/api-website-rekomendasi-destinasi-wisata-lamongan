from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased
from app.db.models import MailLog
from app.schemas.contact import ContactCreate

# Membuat log email
def create_mail_log(db: Session, contact_data: ContactCreate):
    db_contact = MailLog(
        email=contact_data.email,
        subject=contact_data.subject,
        message=contact_data.message,
        status="Belum Dibalas",
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Mendapatkan semua log email
def get_all_mail_logs(db: Session):
    results = (
        db.query(MailLog)
        .order_by(
            (MailLog.status != 'Selesai').desc(),  # "Belum Selesai" di atas
            MailLog.updated_at.desc(),  # akan berpengaruh untuk "Selesai"
            MailLog.id.desc()  # akan berpengaruh untuk "Belum Selesai"
        )
        .all()
    )

    return results

# Mendapatkan log email berdasarkan id
def get_mail_log_by_id(db: Session, id_contact: int):
    return db.query(MailLog).filter(MailLog.id == id_contact).first()

# hapus log email
def delete_mail_log(db: Session, id_contact: int):
    db_contact = get_mail_log_by_id(db, id_contact)
    if db_contact:
        db_contact.status = "Selesai"
        db.commit()
        return {"message": "Mail berhasil dibalas"}
    else:
        raise HTTPException(status_code=404, detail="Mail log not found")

