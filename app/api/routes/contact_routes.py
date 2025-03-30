from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_services import create_mail_log, get_all_mail_logs, get_mail_log_by_id, delete_mail_log
from app.api.dependencies import get_db


router = APIRouter()

# 🔹 Create Mail Log
@router.post("/", response_model=ContactResponse)
def create_contact_log(contact_data: ContactCreate, db: Session = Depends(get_db)):
    return create_mail_log(db, contact_data)

# 🔹 Get All Mail Logs
@router.get("/", response_model=list[ContactResponse])
def list_mail_logs(db: Session = Depends(get_db)):
    return get_all_mail_logs(db)

@router.get("/{id_contact}", response_model=ContactResponse)
def get_mail_log(id_contact: int = Path(..., title="Contact ID", description="Must be an integer"), db: Session = Depends(get_db)):
    return get_mail_log_by_id(db, id_contact)

# 🔹 Reply Mail
@router.post("/{id_contact}/reply", response_model=ContactResponse)
def reply_mail_log(id_contact: int = Path(..., title="Contact ID", description="Must be an integer"), db: Session = Depends(get_db), message: str = Path(..., title="Message", description="Message to be sent")):
    return reply_mail(db, id_contact, message)

@router.delete("/{id_contact}/delete")
def delete_mail(id_contact: int = Path(..., title="Contact ID", description="Must be an integer"), db: Session = Depends(get_db)):
    return delete_mail_log(db, id_contact)