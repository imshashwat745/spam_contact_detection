from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
import bcrypt
from app.models import (
    User,
    Contact,
    UserContact,
    SpamDetails,
)


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):

        if not Contact.objects.exists():
            contact_data = [
                {"country_code": 1, "phone_number": 1234567890},
                {"country_code": 91, "phone_number": 9876543210},
                {"country_code": 44, "phone_number": 7894561230},
                {"country_code": 33, "phone_number": 4567891230},
                {"country_code": 61, "phone_number": 4321567890},
                {"country_code": 91, "phone_number": 4321567867},
            ]

            for contact in contact_data:
                Contact.objects.create(**contact)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created Contact: {contact["country_code"]} - {contact["phone_number"]}'
                    )
                )

        if not User.objects.exists():
            user_data = [
                {
                    "name": "Alice",
                    "email": "alice@example.com",
                    "contact": Contact.objects.get(
                        country_code=1, phone_number=1234567890
                    ),
                },
                {
                    "name": "Bob",
                    "email": "bob@example.com",
                    "contact": Contact.objects.get(
                        country_code=91, phone_number=9876543210
                    ),
                },
                {
                    "name": "Charlie",
                    "email": "charlie@example.com",
                    "contact": Contact.objects.get(
                        country_code=44, phone_number=7894561230
                    ),
                },
                {
                    "name": "David",
                    "email": "david@example.com",
                    "contact": Contact.objects.get(
                        country_code=33, phone_number=4567891230
                    ),
                },
                {
                    "name": "Eve",
                    "email": "eve@example.com",
                    "contact": Contact.objects.get(
                        country_code=61, phone_number=4321567890
                    ),
                },
            ]

            for user in user_data:
                password = bcrypt.hashpw(b"test", bcrypt.gensalt())

                try:
                    user_obj = User.objects.create(
                        name=user["name"],
                        email=user["email"],
                        contact=user["contact"],
                        password=password,
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Created User: {user_obj.name}")
                    )
                except IntegrityError as e:
                    self.stdout.write(
                        self.style.WARNING(f'User {user["name"]} already exists.')
                    )
        if not UserContact.objects.exists():
            user_contact_data = [
                {
                    "user": User.objects.get(name="Alice"),
                    "contact": Contact.objects.get(
                        country_code=44, phone_number=7894561230
                    ),
                    "name": "Taplu",
                },
                {
                    "user": User.objects.get(name="Bob"),
                    "contact": Contact.objects.get(
                        country_code=1, phone_number=1234567890
                    ),
                    "name": "Taplu",
                },
                {
                    "user": User.objects.get(name="Charlie"),
                    "contact": Contact.objects.get(
                        country_code=33, phone_number=4567891230
                    ),
                    "name": "Amar",
                },
                {
                    "user": User.objects.get(name="David"),
                    "contact": Contact.objects.get(
                        country_code=91, phone_number=9876543210
                    ),
                },
                {
                    "user": User.objects.get(name="Eve"),
                    "contact": Contact.objects.get(
                        country_code=61, phone_number=4321567890
                    ),
                },
                {
                    "user": User.objects.get(name="David"),
                    "contact": Contact.objects.get(
                        country_code=61, phone_number=4321567890
                    ),
                    "name": "Ramu Kaka",
                },
                {
                    "user": User.objects.get(name="David"),
                    "contact": Contact.objects.get(
                        country_code=91, phone_number=4321567867
                    ),
                    "name": "Sage",
                },
                {
                    "user": User.objects.get(name="Eve"),
                    "contact": Contact.objects.get(
                        country_code=91, phone_number=4321567867
                    ),
                    "name": "Jett",
                },
            ]

            for user_contact in user_contact_data:
                try:
                    user_contact_obj = UserContact.objects.create(**user_contact)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created UserContact: {user_contact["user"].name} - {user_contact["contact"].phone_number}'
                        )
                    )
                except IntegrityError as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'UserContact for {user_contact["user"].name} and {user_contact["contact"].phone_number} already exists.'
                        )
                    )

        if not SpamDetails.objects.exists():
            spam_details_data = [
                {
                    "marked_by": User.objects.get(name="Alice"),
                    "contact": Contact.objects.get(
                        country_code=91, phone_number=9876543210
                    ),
                },
                {
                    "marked_by": User.objects.get(name="Bob"),
                    "contact": Contact.objects.get(
                        country_code=33, phone_number=4567891230
                    ),
                },
                {
                    "marked_by": User.objects.get(name="Charlie"),
                    "contact": Contact.objects.get(
                        country_code=61, phone_number=4321567890
                    ),
                },
                {
                    "marked_by": User.objects.get(name="David"),
                    "contact": Contact.objects.get(
                        country_code=44, phone_number=7894561230
                    ),
                },
                {
                    "marked_by": User.objects.get(name="Eve"),
                    "contact": Contact.objects.get(
                        country_code=1, phone_number=1234567890
                    ),
                },
            ]

            for spam in spam_details_data:
                try:
                    spam_obj = SpamDetails.objects.create(**spam)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Marked contact {spam["contact"].phone_number} as spam by {spam["marked_by"].name}'
                        )
                    )
                except IntegrityError as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'SpamDetails for contact {spam["contact"].phone_number} by {spam["marked_by"].name} already exists.'
                        )
                    )
