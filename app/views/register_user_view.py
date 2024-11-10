from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.interactors.register_user_interactor import RegisterUserInteractor


from app.dtos import UserDTO, ContactDTO
from app.middlewares.verify_jwt import verify_jwt
from rest_framework.status import HTTP_403_FORBIDDEN


@api_view(["POST"])
def register_user(request):

    if verify_jwt(request=request) is not False:
        return Response({"error": "User already logged in"}, status=HTTP_403_FORBIDDEN)
    data = request.data

    interactor = RegisterUserInteractor()

    return interactor.wrapper(data=data)
