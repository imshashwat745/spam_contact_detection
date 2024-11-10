import bcrypt
from app.dtos import UserDTO, ContactDTO
from app.exceptions import UserAlreadyExistsException
from app.storages.interfaces.user_storage_interface import UserStorageInterface
from app.storages.implementations.user_storage_impl import UserStorageImpl
from app.storages.interfaces.contact_storage_interface import ContactStorageInterface
from app.storages.implementations.contact_storage_impl import ContactStorageImpl
from app.presenters.interfaces.register_user_presenter_interface import (
    RegisterUserPresenterInterface,
)
from app.presenters.implementations.register_user_presenter_impl import (
    RegisterUserPresenterImpl,
)
from rest_framework.response import Response


class RegisterUserInteractor:

    def _interact(self, data):
        email = data["email"] if "email" in data else None
        phone_number = data["phone_number"]
        country_code = data["country_code"]
        name = data["name"]

        bycrypt_salt = bcrypt.gensalt()
        password = bcrypt.hashpw(data["password"].encode("utf-8"), bycrypt_salt)

        contact_dto = ContactDTO(country_code=country_code, phone_number=phone_number)

        contact_storage: ContactStorageInterface = ContactStorageImpl()
        user_storage: UserStorageInterface = UserStorageImpl()

        contact = None
        if contact_storage.does_contact_exist(contact_dto=contact_dto):
            contact = contact_storage.get_contact(contact_dto=contact_dto)

        else:
            contact = contact_storage.create_contact(contact_dto=contact_dto)

        if user_storage.does_user_exist(contact_id=contact.id):
            raise UserAlreadyExistsException

        user_dto = UserDTO(
            name=name, password=password, contact_id=contact.id, email=email
        )

        user_id = user_storage.create_user(user_dto=user_dto, contact_id=contact).id

        user_dto.user_id = user_id

        return user_dto, contact_dto

    def wrapper(self, data) -> Response:
        presenter = RegisterUserPresenterImpl()
        try:
            user_dto, contact_dto = self._interact(data=data)
            return presenter.user_created_successfully_presenter_response(
                user_dto=user_dto, contact_dto=contact_dto
            )

        except UserAlreadyExistsException as e:
            return presenter.user_already_exist_response()
