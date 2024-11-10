import json
import bcrypt
from app.dtos import UserDTO, ContactDTO
from app.exceptions import UserDoesNotExist, InvalidPasswordException
from app.storages.interfaces.user_storage_interface import UserStorageInterface
from app.storages.implementations.user_storage_impl import UserStorageImpl
from app.storages.interfaces.contact_storage_interface import ContactStorageInterface
from app.storages.implementations.contact_storage_impl import ContactStorageImpl
from app.presenters.interfaces.login_user_presenter_interface import (
    LoginUserPresenterInterface,
)
from app.presenters.implementations.login_user_presenter_impl import (
    LoginUserPresenterImpl,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import jwt

import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


class LoginUserInteractor:

    def _interact(self, data):
        phone_number = data["phone_number"]
        country_code = data["country_code"]

        bycrypt_salt = bcrypt.gensalt()
        password = data["password"]

        contact_dto = ContactDTO(country_code=country_code, phone_number=phone_number)

        contact_storage: ContactStorageInterface = ContactStorageImpl()
        user_storage: UserStorageInterface = UserStorageImpl()

        if contact_storage.does_contact_exist(contact_dto=contact_dto) is False:
            raise UserDoesNotExist

        contact = contact_storage.get_contact(contact_dto=contact_dto)

        if user_storage.does_user_exist(contact_id=contact.id) is False:
            raise UserDoesNotExist

        user = user_storage.get_user(contact_id=contact.id)

        if bcrypt.checkpw(password.encode("utf-8"), user.password) is False:
            raise InvalidPasswordException

        jwt_payload = {
            "user_id": user.id,
            "contact_id": contact.id,
            "name": user.name,
            "email": user.email,
            "country_code": contact.country_code,
            "phone_number": contact.phone_number,
            "password": str(user.password),
        }

        jwt_access_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm="HS256")

        return jwt_access_token

    def wrapper(self, data):
        presenter: LoginUserPresenterInterface = LoginUserPresenterImpl()
        try:
            access_token = self._interact(data=data)
            return presenter.user_logged_in_successfully_presenter_response(
                access_token=access_token
            )

        except UserDoesNotExist as e:
            return presenter.invalid_user_presenter_response()

        except InvalidPasswordException as e:
            return presenter.invalid_password_presenter_response()
