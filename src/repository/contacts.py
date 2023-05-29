from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.conn_to_db import get_db
from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    """
    The get_contacts function returns a list of contacts from the database.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Skip a certain number of rows in the database
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    """
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on its id.
        Args:
            contact_id (int): The id of the desired contact.
            db (Session): A connection to the database.

    :param contact_id: int: Pass in the id of the contact we want to retrieve
    :param db: Session: Pass in the database session to the function
    :return: The contact with the given id
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create(body: ContactModel, db: Session = Depends(get_db)):
    """
    The create function creates a new contact in the database.
        It takes a ContactModel object as input and returns the newly created contact.

    :param body: ContactModel: Get the contact data from the request body
    :param db: Session: Get a database session
    :return: A contact object
    """
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    """"
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated version of the ContactModel object.

    :param contact_id: int: Get the contact by id
    :param body: ContactModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :return: The updated contact
    """
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
    """
    The delete function deletes a contact from the database.
        Args:
            contact_id (int): The id of the contact to delete.
            db (Session): A connection to the database.

    :param contact_id: int: Specify the id of the contact to be deleted
    :param db: Session: Pass the database session to the function
    :return: The contact that was deleted
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact