from django.test import TestCase
from .models import Contact

# Create your tests here.
class ContactTestCase(TestCase):
    def create_contact(self,
              email="michael@mail.com",
              email_type=Contact.HOME,
              phone_number="345-675-2536",
              phone_type=Contact.HOME,
              address="Neverland Ranch Sacramento, CA",
              name = "MichaelJackson"):
        return Contact.objects.create(
            email=email,
            email_type=email_type,
            phone_number=phone_number,
            phone_type=phone_type,
            address=address,
            name = name
        )

    def test_contact_create(self):
        contactItem = self.create_contact()
        self.assertTrue(isinstance(contactItem, Contact))
        self.assertEqual(contactItem.__str__(), '%s lives on %s' % (contactItem.name, contactItem.address))
