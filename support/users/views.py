from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from users.serializers import UserSerializer
from rest_framework.request import Request
from users.models import User
from django.conf import settings
from users.auth import generate_access_token, generate_refresh_token
import jwt


class RegisterView(APIView):

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):

    def post(self, request: Request) -> Response:
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            return Response({
                'message': "Invalid data"
            })

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = Response()
        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)

        response.data = {
            'access_token': access_token,
            'message': "Successfully login"
        }

        return response


class UserView(APIView):

    def get(self, request: Request) -> Response:
        token = request.COOKIES.get('refreshtoken')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):

    def post(self, request: Request) -> Response:
        response = Response()
        response.delete_cookie('refreshtoken')
        response.data = {
            'message': 'success'
        }

        return response
