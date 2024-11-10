import json
from typing import List
import bcrypt
from app.dtos import UserDTO, ContactDTO, SearchInfoDTO
from app.exceptions import UserDoesNotExist, InvalidPasswordException
from app.storages.interfaces.user_storage_interface import UserStorageInterface
from app.storages.implementations.user_storage_impl import UserStorageImpl
from app.storages.interfaces.user_contact_storage_interface import (
    UserContactStorageInterface,
)
from app.storages.implementations.user_contact_storage_impl import (
    UserContactStorageImpl,
)
from app.presenters.interfaces.search_info_presenter_interface import (
    SearchInfoPresenterInterface,
)
from app.presenters.implementations.search_info_presenter_impl import (
    SearchInfoPresenterImpl,
)

from app.storages.interfaces.spam_details_storage_interface import (
    SpamDetailsStorageInterface,
)
from app.storages.implementations.spam_details_storage_impl import (
    SpamDetailsStorageImpl,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

import jwt

import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


class SearchInfoByContactInteractor:

    def _interact(self, request):
        country_code = request.query_params.get("country_code")
        phone_number = request.query_params.get("phone_number")

        jwt_contact_id = request.data["jwt_user"]["contact_id"]

        contact_dto: ContactDTO = ContactDTO(
            country_code=country_code, phone_number=phone_number
        )

        search_info_dtos: List[SearchInfoDTO] = []

        user_storage: UserStorageInterface = UserStorageImpl()
        user_contact_storage: UserContactStorageInterface = UserContactStorageImpl()
        spam_details_storage: SpamDetailsStorageInterface = SpamDetailsStorageImpl()

        user_storage_response = user_storage.get_user_having_contact(
            contact_dto=contact_dto
        )

        if user_storage_response is None:
            search_info_dtos.extend(
                user_contact_storage.get_user_contacts_having_contact(
                    contact_dto=contact_dto
                )
            )

        else:
            search_info_dtos.append(user_storage_response)

        search_info_dtos = list(set(search_info_dtos))

        for dto in search_info_dtos:
            dto.spam_count = spam_details_storage.get_count_of_spam(
                contact_id=dto.contact_id
            )

            if (
                dto.user_id is None
                or user_contact_storage.does_contact_list_of_contact_has_current_user(
                    jwt_contact_id=jwt_contact_id, user_id=dto.user_id
                )
                is False
            ):
                dto.email = None

        return search_info_dtos

    def wrapper(self, request) -> Response:
        presenter: SearchInfoPresenterInterface = SearchInfoPresenterImpl()
        try:
            search_info_dtos = self._interact(request=request)
            return presenter.search_result_presenter_response(
                search_results=search_info_dtos
            )
        except Exception as e:
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
