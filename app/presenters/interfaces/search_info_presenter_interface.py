from abc import ABC, abstractmethod
from app.dtos import SearchInfoDTO
from rest_framework.response import Response
from typing import List


class SearchInfoPresenterInterface(ABC):

    @abstractmethod
    def search_result_presenter_response(
        self, search_results: List[SearchInfoDTO]
    ) -> Response:
        pass
