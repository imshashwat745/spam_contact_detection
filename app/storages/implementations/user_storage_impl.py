from typing import List
from ..interfaces.user_storage_interface import UserStorageInterface
from ...dtos import SearchInfoDTO, UserDTO, ContactDTO
from ...models import User
from django.core.exceptions import ObjectDoesNotExist


class UserStorageImpl(UserStorageInterface):

    def create_user(self, user_dto: UserDTO, contact_id: int) -> User:
        user = User.objects.create(
            name=user_dto.name,
            password=user_dto.password,
            contact=contact_id,
            email=user_dto.email,
        )

        return user

    def does_user_exist(self, contact_id):
        existence = User.objects.filter(contact=contact_id).exists()

        return existence

    def get_user(self, contact_id: int) -> User:
        user = User.objects.get(contact_id=contact_id)
        return user

    def get_users_whose_name_starts_with(self, search_query) -> List[SearchInfoDTO]:
        users = (
            User.objects.filter(name__istartswith=search_query)
            .select_related("contact")
            .only(
                "id",
                "name",
                "contact__country_code",
                "contact__id",
                "contact__phone_number",
            )
        )

        result = [
            SearchInfoDTO(
                name=user.name,
                user_id=user.id,
                email=user.email,
                contact_id=user.contact.id,
                country_code=user.contact.country_code,
                phone_number=user.contact.phone_number,
            )
            for user in users
        ]

        return result

    def get_users_whose_name_contains_but_not_starts_with(
        self, search_query
    ) -> List[SearchInfoDTO]:
        users = (
            User.objects.filter(name__icontains=search_query)
            .exclude(name__istartswith=search_query)
            .select_related("contact")
            .only(
                "id",
                "name",
                "contact__country_code",
                "contact__id",
                "contact__phone_number",
            )
        )

        result = [
            SearchInfoDTO(
                name=user.name,
                user_id=user.id,
                email=user.email,
                contact_id=user.contact.id,
                country_code=user.contact.country_code,
                phone_number=user.contact.phone_number,
            )
            for user in users
        ]

        return result

    def get_user_having_contact(self, contact_dto: ContactDTO) -> SearchInfoDTO:
        try:
            user = User.objects.select_related("contact").get(
                contact__phone_number=contact_dto.phone_number,
                contact__country_code=contact_dto.country_code,
            )

            result = SearchInfoDTO(
                name=user.name,
                user_id=user.id,
                email=user.email,
                contact_id=user.contact.id,
                country_code=user.contact.country_code,
                phone_number=user.contact.phone_number,
            )

        except ObjectDoesNotExist:
            result = None

        return result
