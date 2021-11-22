from django.test import TestCase, Client
from .models import Ticket
from django.contrib.auth import get_user_model
import jwt
import datetime

User = get_user_model()


class TicketTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email='Vadim@gmail.com',
                                        date_of_birth='2001-09-10',
                                        password='12345',
                                        is_admin=True)
        self.ticket = Ticket.objects.create(title='Test', description='TestDesc', from_user=self.user.email)
        self.payload = {
            'id': self.user.id,
            'email': self.user.email,
            'isStaff?': self.user.is_admin,
            'expire': str(datetime.datetime.utcnow() + datetime.timedelta(minutes=10)),
            'create': str(datetime.datetime.utcnow())
        }
        self.token = jwt.encode(self.payload, 'secret', algorithm='HS256')
        self.cookies = jwt.decode(self.token, 'secret', algorithms=['HS256'])

    def test_instance_ticket(self):
        self.assertIsInstance(self.ticket, Ticket)

    def test_fill_ticket_fields(self):
        self.assertEqual(self.ticket.title, 'Test')
        self.assertEqual(self.ticket.description, 'TestDesc')
        self.assertEqual(self.ticket.from_user, 'Vadim@gmail.com')
        self.assertEqual(self.ticket.support_answer, 'None')
        self.assertEqual(self.ticket.user_answer, 'None')
        self.assertEqual(self.ticket.status, 'Unresolved')

    def test_fill_user_fields(self):
        self.assertEqual(self.user.email, 'Vadim@gmail.com')
        self.assertEqual(self.user.date_of_birth, '2001-09-10')
        self.assertEqual(self.user.password, '12345')

    def test_unauthorized_response(self):
        client = Client()
        response = client.get('/api/ticket/')
        self.assertEqual(response.status_code, 403)
