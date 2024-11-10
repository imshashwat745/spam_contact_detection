from app.presenters.interfaces.register_user_presenter_interface import (
    RegisterUserPresenterInterface,
)
from app.dtos import UserDTO, ContactDTO
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_409_CONFLICT


class RegisterUserPresenterImpl(RegisterUserPresenterInterface):

    def user_created_successfully_presenter_response(
        self, user_dto: UserDTO, contact_dto: ContactDTO
    ) -> Response:
        response = {
            "message": "User Created Successfully",
            "user_id": user_dto.user_id,
            "name": user_dto.name,
            "email": user_dto.email,
            "contact": {
                "country_code": contact_dto.country_code,
                "phone_number": contact_dto.phone_number,
            },
        }

        return Response(response, status=HTTP_201_CREATED)

    def user_already_exist_response(self) -> Response:
        response = {"message": "User already exists"}

        return Response(response, status=HTTP_409_CONFLICT)
