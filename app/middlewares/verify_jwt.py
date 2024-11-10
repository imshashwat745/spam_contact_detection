from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import os
import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")


def verify_jwt(request) -> bool:
    auth_header = request.headers.get("Authorization", None)

    if auth_header:
        token = auth_header.split(" ")[1]
        try:
            decoded_data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            return decoded_data
        except Exception as e:
            return False

    return False
