import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import TicketSerializer
from .models import Ticket


class TicketView(APIView):
    def get(self, request: Request) -> Response:
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        if payload['isStaff?']:
            ticket = Ticket.objects.all()
            serializer = TicketSerializer(ticket, many=True)
            return Response(serializer.data)

        tickets = Ticket.objects.filter(from_user=payload['email'])
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        request.data['from_user'] = payload['email']
        if not payload['isStaff?'] and 'status' in request.data.keys():
            del request.data['status']
        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        if payload['isStaff?']:
            ticket = Ticket.objects.get(id=request.data['id'])
            ticket.status = request.data.get('status', ticket.status)
            ticket.answer = request.data.get('answer', ticket.answer)
            ticket.save()

        else:
            ticket = Ticket.objects.get(id=request.data['id'])
            ticket.answer = request.data.get('answer', ticket.answer)
            ticket.save()

        return Response({
            'message': 'success'
        })




