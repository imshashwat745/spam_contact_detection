from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.interactors.login_user_interactor import LoginUserInteractor


from app.dtos import UserDTO, ContactDTO
from django.shortcuts import redirect
from app.middlewares.verify_jwt import verify_jwt
from rest_framework.status import HTTP_403_FORBIDDEN


@api_view(["POST"])
def login_user(request):

    if verify_jwt(request=request) is not False:
        return Response({"error": "User already logged in"}, status=HTTP_403_FORBIDDEN)
    data = request.data

    interactor = LoginUserInteractor()

    return interactor.wrapper(data=data)
