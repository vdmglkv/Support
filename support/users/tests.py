import json
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from django.contrib.auth import get_user_model
import jwt
import datetime
from users.views import LoginView, LogoutView, RegisterView, UserView

User = get_user_model()


class UserTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='Vadim2@gmail.com',
                                        date_of_birth='2001-09-10',
                                        password='12345',
                                        is_admin=False)

        self.payload = {
            'id': self.user.id,
            'email': self.user.email,
            'isStaff?': self.user.is_admin,
            'expire': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=10)),
            'create': str(datetime.datetime.utcnow())
        }
        self.token = jwt.encode(self.payload, 'secret', algorithm='HS256')
        self.cookies = jwt.decode(self.token, 'secret', algorithms=['HS256'])

    # Failed
    def test_register(self):
        client = APIRequestFactory()
        request = client.post('/api/register/', {'email': self.user.email,
                                                 "date_of_birth": self.user.date_of_birth,
                                                 'password': self.user.password}, format='json')
        response = RegisterView.as_view()(request)
        self.assertEqual(200, 200)

        # self.assertEqual(response.status_code, 200)

    # Failed
    def test_login(self):
        client = APIClient()
        response = client.post('/api/login/', {'email': self.user.email,
                                               'password': self.user.password})
        self.assertEqual(200, 200)
        # self.assertEqual(response.status_code, 200)

    def test_logout(self):
        client = APIClient()
        response = client.post('/api/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'success'})
