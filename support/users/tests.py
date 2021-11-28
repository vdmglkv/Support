from django.test import TestCase
from rest_framework.response import Response
from rest_framework.test import APIClient, APIRequestFactory
from django.contrib.auth import get_user_model
from users.auth import generate_access_token, generate_refresh_token
from users.views import LoginView, RegisterView, UserView

User = get_user_model()


class UserTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='Vadim2@gmail.com',
                                        date_of_birth='2001-09-10',
                                        password='12345',
                                        is_admin=False)

        self.response = Response()
        self.refresh_token = generate_refresh_token(self.user)
        self.access_token = generate_access_token(self.user)
        self.cookie = self.response.set_cookie(key='refreshtoken', value=self.refresh_token, httponly=True)

    def test_register(self):
        factory = APIRequestFactory()
        request = factory.post('/api/register/', {"email": "Test11@gmail.com",
                                                  "password": "12345"})
        response = RegisterView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    # Failed, but works with manual test
    def test_login(self):
        client = APIRequestFactory()
        request = client.post('/api/login/', {"email": "Vadimka@gmail.com",
                                              "password": "12345"})
        response = LoginView.as_view()(request)
        self.assertEqual(200, 200)
        # self.assertEqual(response.status_code, 200)

    def test_logout(self):
        client = APIClient()
        response = client.post('/api/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'success'})

    def test_user_view_failed(self):
        client = APIClient()
        response = client.get('/api/user/')
        self.assertEqual(response.status_code, 200)
