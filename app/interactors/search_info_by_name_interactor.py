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
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
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


class SearchInfoByNameInteractor:

    def _interact(self, request):
        search_query = request.query_params.get("search_query")
        jwt_contact_id = request.data["jwt_user"]["contact_id"]

        search_info_dtos: List[SearchInfoDTO] = []

        user_storage: UserStorageInterface = UserStorageImpl()
        user_contact_storage: UserContactStorageInterface = UserContactStorageImpl()
        spam_details_storage: SpamDetailsStorageInterface = SpamDetailsStorageImpl()

        search_info_dtos.extend(
            list(
                set(
                    user_storage.get_users_whose_name_starts_with(
                        search_query=search_query
                    )
                )
            )
        )

        search_info_dtos.extend(
            list(
                set(
                    user_contact_storage.get_user_contacts_whose_name_starts_with(
                        search_query=search_query
                    )
                )
            )
        )

        search_info_dtos.extend(
            list(
                set(
                    user_storage.get_users_whose_name_contains_but_not_starts_with(
                        search_query=search_query
                    )
                )
            )
        )

        search_info_dtos.extend(
            list(
                set(
                    user_contact_storage.get_user_contacts_whose_name_contains_but_not_starts_with(
                        search_query=search_query
                    )
                )
            )
        )

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
