from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from sqlalchemy.orm import Session

from src.database.conn_to_db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, )
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return None
