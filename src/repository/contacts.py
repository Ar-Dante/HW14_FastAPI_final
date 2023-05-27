from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.conn_to_db import get_db
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create(body: ContactModel, db: Session = Depends(get_db)):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.name = body.name
        contact.sure_name = body.sure_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def delete(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact