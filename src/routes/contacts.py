from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.conn_to_db import get_db
from src.database.models import User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ContactResponse
from src.services.auth import auth_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=2, seconds=5))],
            description="Two request on 5 second")
async def get_contacts(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db)):
    """
    The get_contacts function returns a list of contacts.

    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of contacts returned to 300
    :param offset: int: Specify the number of records to skip
    :param db: Session: Pass the database session to the repository
    :return: A list of contacts
    """
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    """
    The get_contact function returns a contact by its id.

    :param contact_id: int: Get the contact id from the url path
    :param db: Session: Pass the database session to the function
    :return: A contact object
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, )
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Get the database session
    :param _: User: Get the current user from the auth_service
    :return: The contact object that was created
    """
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    """
    The update_contact function updates a contact in the database.

    :param body: ContactModel: Validate the json body of the request
    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: Session: Pass the database session to the repository layer
    :param _: User: Get the current user from the auth_service
    :return: The updated contact
    """
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    """
    The delete_contact function deletes a contact from the database.
        It takes in an integer representing the id of the contact to be deleted, and returns None.

    :param contact_id: int: Get the contact id from the path
    :param db: Session: Pass the database session to the repository layer
    :param _: User: Get the current user from the auth_service
    :return: None
    """
    contact = await repository_contacts.delete(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    return None
