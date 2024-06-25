from datetime import datetime

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from first_app.serializers.user_register_serializer import UserRegisterSerializer
from first_app.utils.set_jwt import set_jwt_cookies


class AuthView(APIView):
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            data={
                f"Hello, {request.user.username}",
            },
            status=status.HTTP_200_OK
        )


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            response = Response(
                data={
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_201_CREATED
            )

            set_jwt_cookies(response, user)

            return response
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        username = request.data['username']
        password = request.data['password']

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            access_expiry = datetime.fromtimestamp(access_token['exp'])
            refresh_expiry = datetime.fromtimestamp(refresh['exp'])

            response = Response(
                status=status.HTTP_200_OK
            )

            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=access_expiry,
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry,
            )

            return response
        else:
            return Response(
                data={
                    "message": "Invalid Credentials",
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutUserView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
