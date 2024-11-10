from app.presenters.interfaces.login_user_presenter_interface import (
    LoginUserPresenterInterface,
)
from app.dtos import UserDTO, ContactDTO
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class LoginUserPresenterImpl(LoginUserPresenterInterface):

    def user_logged_in_successfully_presenter_response(
        self, access_token: str
    ) -> Response:
        response = {
            "message": "User logged in successfully",
            "access_token": access_token,
        }
        return Response(response, status=HTTP_200_OK)

    def invalid_password_presenter_response(self) -> Response:
        response = {"message": "Invalid Password", "error": "Authentication Failed"}
        return Response(response, status=HTTP_400_BAD_REQUEST)

    def invalid_user_presenter_response(self) -> Response:
        response = {"message": "User does not exist", "error": "Authentication Failed"}
        return Response(response, status=HTTP_400_BAD_REQUEST)
