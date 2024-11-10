from abc import ABC, abstractmethod
from app.dtos import UserDTO, ContactDTO
from rest_framework.response import Response


class RegisterUserPresenterInterface(ABC):

    @abstractmethod
    def user_created_successfully_presenter_response(
        self, user_dto: UserDTO, contact_dto: ContactDTO
    ) -> Response:
        pass

    @abstractmethod
    def user_already_exist_response(self) -> Response:
        pass
