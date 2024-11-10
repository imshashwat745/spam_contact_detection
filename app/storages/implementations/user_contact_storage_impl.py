from typing import List
from ..interfaces.user_contact_storage_interface import UserContactStorageInterface
from ...dtos import SearchInfoDTO, ContactDTO
from ...models import UserContact
from django.db.models import Q


class UserContactStorageImpl(UserContactStorageInterface):

    def get_user_contacts_whose_name_starts_with(
        self, search_query
    ) -> List[SearchInfoDTO]:
        user_contacts = (
            UserContact.objects.filter(name__istartswith=search_query)
            .select_related("contact")
            .only(
                "name", "contact__country_code", "contact__id", "contact__phone_number"
            )
        )

        result = [
            SearchInfoDTO(
                name=user_contact.name,
                contact_id=user_contact.contact.id,
                country_code=user_contact.contact.country_code,
                phone_number=user_contact.contact.phone_number,
            )
            for user_contact in user_contacts
        ]

        return result

    def get_user_contacts_whose_name_contains_but_not_starts_with(
        self, search_query
    ) -> List[SearchInfoDTO]:
        user_contacts = (
            UserContact.objects.filter(name__icontains=search_query)
            .exclude(name__istartswith=search_query)
            .select_related("contact")
            .only(
                "name", "contact__country_code", "contact__id", "contact__phone_number"
            )
        )

        result = [
            SearchInfoDTO(
                name=user_contact.name,
                contact_id=user_contact.contact.id,
                country_code=user_contact.contact.country_code,
                phone_number=user_contact.contact.phone_number,
            )
            for user_contact in user_contacts
        ]

        return result

    def get_user_contacts_having_contact(
        self, contact_dto: ContactDTO
    ) -> List[SearchInfoDTO]:
        user_contacts = UserContact.objects.select_related("contact").filter(
            Q(contact__country_code=contact_dto.country_code)
            & Q(contact__phone_number=contact_dto.phone_number)
        )

        result = [
            SearchInfoDTO(
                name=user_contact.name,
                contact_id=user_contact.contact.id,
                country_code=user_contact.contact.country_code,
                phone_number=user_contact.contact.phone_number,
            )
            for user_contact in user_contacts
        ]

        return result

    def does_contact_list_of_contact_has_current_user(
        self, jwt_contact_id: int, user_id: int
    ) -> bool:
        existence = UserContact.objects.filter(
            contact=jwt_contact_id, user=user_id
        ).exists()

        return existence
