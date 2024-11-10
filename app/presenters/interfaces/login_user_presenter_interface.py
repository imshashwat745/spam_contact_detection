from abc import ABC, abstractmethod
from app.dtos import UserDTO, ContactDTO
from rest_framework.response import Response


class LoginUserPresenterInterface(ABC):

    @abstractmethod
    def user_logged_in_successfully_presenter_response(
        self, access_token: str
    ) -> Response:
        pass

    @abstractmethod
    def invalid_password_presenter_response(self) -> Response:
        pass

    @abstractmethod
    def invalid_user_presenter_response(self) -> Response:
        pass
