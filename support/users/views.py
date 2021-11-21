from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from rest_framework.request import Request
from .models import User
import jwt
import datetime
# Create your views here.


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

        payload = {
            'id': user.id,
            'email': user.email,
            'isStaff?': user.is_admin,
            'expire': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=10)),
            'create': str(datetime.datetime.utcnow())
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': "Successfully login"
        }

        return response


class UserView(APIView):

    def get(self, request: Request) -> Response:
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):

    def post(self, request: Request) -> Response:
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response
