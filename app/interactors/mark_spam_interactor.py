import json
import bcrypt
from app.dtos import UserDTO, ContactDTO, SpamDetailsDTO
from app.exceptions import (
    UserDoesNotExist,
    InvalidPasswordException,
    UserHasAlreadyMarkedThisContactAsSpamException,
    UserCannotMarkItselfAsSpamException,
)
from app.storages.interfaces.user_storage_interface import UserStorageInterface
from app.storages.implementations.user_storage_impl import UserStorageImpl
from app.storages.interfaces.contact_storage_interface import ContactStorageInterface
from app.storages.implementations.contact_storage_impl import ContactStorageImpl
from app.presenters.interfaces.mark_spam_presenter_interface import (
    MarkSpamPresenterInterface,
)
from app.presenters.implementations.mark_spam_presenter_impl import (
    MarkSpamPresenterImpl,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from app.storages.interfaces.spam_details_storage_interface import (
    SpamDetailsStorageInterface,
)
from app.storages.implementations.spam_details_storage_impl import (
    SpamDetailsStorageImpl,
)
import jwt

import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


class MarkSpamInteractor:
    def _interact(self, data):
        phone_number = data["phone_number"]
        country_code = data["country_code"]

        user_id = data["jwt_user"]["user_id"]
        user_country_code = data["jwt_user"]["country_code"]
        user_phone_number = data["jwt_user"]["phone_number"]

        if phone_number == user_phone_number and country_code == user_country_code:
            raise UserCannotMarkItselfAsSpamException

        contact_storage: ContactStorageInterface = ContactStorageImpl()
        user_storage: UserStorageInterface = UserStorageImpl()
        spam_details_storage: SpamDetailsStorageInterface = SpamDetailsStorageImpl()

        contact_dto: ContactDTO = ContactDTO(
            country_code=country_code, phone_number=phone_number
        )

        contact = None
        if contact_storage.does_contact_exist(contact_dto=contact_dto) is False:
            contact = contact_storage.create_contact(contact_dto=contact_dto)
        else:
            contact = contact_storage.get_contact(contact_dto=contact_dto)

        spam_details_dto: SpamDetailsDTO = SpamDetailsDTO(
            marked_by=user_id, contact_id=contact.id
        )

        mark_spam_result = spam_details_storage.mark_contact_as_spam(
            spam_details_dto=spam_details_dto
        )

        if mark_spam_result is False:
            raise UserHasAlreadyMarkedThisContactAsSpamException

    def wrapper(self, data):
        presenter: MarkSpamPresenterInterface = MarkSpamPresenterImpl()
        try:
            self._interact(data=data)
            return presenter.user_marked_as_spam_successfully_presenter_response()
        except UserHasAlreadyMarkedThisContactAsSpamException as e:
            return presenter.user_already_marked_as_spam_presenter_response()

        except UserCannotMarkItselfAsSpamException as e:
            return presenter.user_cannot_mark_itself_as_spam_presenter_response()
