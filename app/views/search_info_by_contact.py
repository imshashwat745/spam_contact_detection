from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.interactors.search_info_by_contact_interactor import (
    SearchInfoByContactInteractor,
)
from rest_framework.status import HTTP_403_FORBIDDEN

from app.dtos import UserDTO, ContactDTO
from django.shortcuts import redirect
from app.middlewares.verify_jwt import verify_jwt


@api_view(["GET"])
def search_info_by_contact(request):

    jwt_verification_response = verify_jwt(request=request)

    if jwt_verification_response is False:
        return Response(status=HTTP_403_FORBIDDEN)
    request.data["jwt_user"] = jwt_verification_response

    interactor = SearchInfoByContactInteractor()

    return interactor.wrapper(request=request)
