from app.presenters.interfaces.mark_spam_presenter_interface import (
    MarkSpamPresenterInterface,
)
from app.dtos import UserDTO, ContactDTO, SpamDetailsDTO
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_409_CONFLICT


class MarkSpamPresenterImpl(MarkSpamPresenterInterface):

    def user_marked_as_spam_successfully_presenter_response(self) -> Response:
        response = {"message": "Contact marked as spam successfully"}

        return Response(response, status=HTTP_200_OK)

    def user_already_marked_as_spam_presenter_response(self):
        response = {"message": "User is already marked as spam"}

        return Response(response, status=HTTP_409_CONFLICT)

    def user_cannot_mark_itself_as_spam_presenter_response(self):
        response = {"message": "User cannot mark itself as spam"}

        return Response(response, status=HTTP_409_CONFLICT)
