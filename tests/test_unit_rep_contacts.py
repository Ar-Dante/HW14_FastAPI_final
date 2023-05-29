import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.repository.contacts import get_contacts, get_contact_by_id, create, update, delete
from src.schemas import ContactModel


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact() for _ in range(5)]
        self.session.query(Contact()).limit().offset().all.return_value = contacts
        result = await get_contacts(limit=limit, offset=offset, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id_found(self):
        contact_id = 1
        contact = Contact(name="John", email="john@example.com")
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_id(contact_id=contact_id, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_id_not_found(self):
        contact_id = 1
        self.session.query().filter_by().first.return_value = None
        result = await get_contact_by_id(contact_id=contact_id, db=self.session)
        self.assertIsNone(result)

    async def test_create(self):
        body = ContactModel(name='Bob',
                            sure_name='Dilan',
                            email='bob@gmail.com',
                            phone_number='+38087111233',
                            birthday='1814-03-09',
                            additional_data='blalavav')
        result = await create(body=body, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertTrue(hasattr(result, 'id'))

    async def test_update(self):
        contact_id = 1
        updated_data = ContactModel(name='Updated',
                                    sure_name='Updated',
                                    email='updated@example.com',
                                    phone_number='+38087111234',
                                    birthday='1990-01-01',
                                    additional_data='Updated data')
        contact = Contact(id=contact_id,
                          name='Bob',
                          sure_name='Dilan',
                          email='bob@gmail.com',
                          phone_number='+38087111233',
                          birthday='1814-03-09',
                          additional_data='blalavav')

        self.session.query().filter_by().first.return_value = contact
        result = await update(contact_id=contact_id, body=updated_data, db=self.session)

        self.assertEqual(result.name, updated_data.name)
        self.assertEqual(result.sure_name, updated_data.sure_name)
        self.assertEqual(result.email, updated_data.email)
        self.assertEqual(result.phone_number, updated_data.phone_number)
        self.assertEqual(result.birthday, updated_data.birthday)
        self.assertEqual(result.additional_data, updated_data.additional_data)

    async def test_delete(self):
        contact_id = 1
        contact = Contact(id=contact_id,
                          name='Bob',
                          sure_name='Dilan',
                          email='bob@gmail.com',
                          phone_number='+38087111233',
                          birthday='1814-03-09',
                          additional_data='blalavav')

        self.session.query().filter_by().first.return_value = contact
        result = await delete(contact_id=contact_id, db=self.session)

        self.assertEqual(result, contact)


if __name__ == '__main__':
    unittest.main()
