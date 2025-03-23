from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import MailLog
from app.schemas.contact import ContactCreate
from app.core.config import settings

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Membuat log email
def create_mail_log(db: Session, contact_data: ContactCreate):
    db_contact = MailLog(
        email=contact_data.email,
        subject=contact_data.subject,
        message=contact_data.message,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Mendapatkan semua log email
def get_all_mail_logs(db: Session):
    return db.query(MailLog).all()

# Mendapatkan log email berdasarkan id
def get_mail_log_by_id(db: Session, id_contact: int):
    return db.query(MailLog).filter(MailLog.id == id_contact).first()

# send reply email
def send_reply_mail(db: Session, id_contact: int, contact_data: ContactCreate):
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_ADDRESS
        msg['To'] = contact_data.email
        msg['Subject'] = contact_data.subject

        msg.attach(MIMEText(contact_data.message))

        with smtplib.SMTP(settings.SMTP_SERVER,settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_ADDRESS, contact_data.email, msg.as_string())
            server.quit()

        # hapus email dari database
        # db_contact = get_mail_log_by_id(db, id_contact)
        # db.delete(db_contact)
        # db.commit()
        return HTTPException(status_code=204, detail="Email sent")
    except:
        raise HTTPException(status_code=500, detail="Failed to send email")

# membalas email
def reply_mail(db: Session, id_contact: int, message: str):
    db_contact = get_mail_log_by_id(db, id_contact)
    contact_data = ContactCreate(email=db_contact.email, subject="Re: "+db_contact.subject, message=message)
    return send_reply_mail(db, id_contact, contact_data)

