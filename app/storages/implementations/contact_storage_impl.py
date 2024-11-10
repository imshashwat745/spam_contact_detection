from ..interfaces.contact_storage_interface import ContactStorageInterface
from ...dtos import ContactDTO
from ...models import Contact


class ContactStorageImpl(ContactStorageInterface):

    def does_contact_exist(self, contact_dto: ContactDTO) -> bool:
        existence = Contact.objects.filter(
            phone_number=contact_dto.phone_number, country_code=contact_dto.country_code
        ).exists()

        return existence

    def create_contact(self, contact_dto: ContactDTO) -> Contact:
        contact = Contact.objects.create(
            country_code=contact_dto.country_code, phone_number=contact_dto.phone_number
        )

        return contact

    def get_contact(self, contact_dto: ContactDTO) -> Contact:
        contact = Contact.objects.get(
            country_code=contact_dto.country_code, phone_number=contact_dto.phone_number
        )

        return contact
