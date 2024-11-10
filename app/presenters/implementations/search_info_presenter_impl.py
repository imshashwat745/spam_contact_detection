from app.presenters.interfaces.search_info_presenter_interface import (
    SearchInfoPresenterInterface,
)
from app.dtos import SearchInfoDTO
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from typing import List


class SearchInfoPresenterImpl(SearchInfoPresenterInterface):

    def search_result_presenter_response(
        self, search_results: List[SearchInfoDTO]
    ) -> Response:
        response = [
            {
                "user_id": search_result.user_id,
                "name": search_result.name,
                "contact": {
                    "contact_id": search_result.contact_id,
                    "country_code": search_result.country_code,
                    "phone_number": search_result.phone_number,
                },
                "spam_count": search_result.spam_count,
                "email": search_result.email,
            }
            for search_result in search_results
        ]
        return Response(response, status=HTTP_200_OK)
