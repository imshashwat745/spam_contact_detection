from abc import ABC, abstractmethod
from app.dtos import UserDTO, ContactDTO, SpamDetailsDTO
from rest_framework.response import Response


class MarkSpamPresenterInterface(ABC):
    @abstractmethod
    def user_marked_as_spam_successfully_presenter_response(self) -> Response:
        pass

    @abstractmethod
    def user_already_marked_as_spam_presenter_response(self):
        pass

    @abstractmethod
    def user_cannot_mark_itself_as_spam_presenter_response(self):
        pass
