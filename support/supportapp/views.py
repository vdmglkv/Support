import jwt
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from supportapp.serializers import TicketSerializer
from supportapp.models import Ticket
from django.db.utils import DataError
from django.db.models import ObjectDoesNotExist


class TicketView(APIView):

    def get(self, request: Request) -> Response:

        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        if payload['isStaff?']:
            ticket = Ticket.objects.all()
            serializer = TicketSerializer(ticket, many=True)
            return Response(serializer.data)

        tickets = Ticket.objects.filter(from_user=payload['email'])
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:

        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        request.data['from_user'] = payload['email']
        forbidden = ['status', 'support_answer']
        if not payload['isStaff?']:
            for req in forbidden:
                try:
                    del request.data[req]
                except KeyError:
                    pass

        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request: Request) -> Response:

        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        if payload['isStaff?']:
            try:
                ticket = Ticket.objects.get(id=request.data['id'])
                ticket.status = request.data.get('status', ticket.status)
                ticket.support_answer = request.data.get('support_answer', ticket.support_answer)
                ticket.save()
            except KeyError:
                return Response({
                    'message': 'Ticket id excepted'
                })
            except DataError:
                return Response({
                    'message': 'Input error'
                })
            except ObjectDoesNotExist:
                return Response({
                    'message': 'No any ticket to update!'
                })

        else:
            try:
                ticket = Ticket.objects.get(id=request.data['id'], from_user=payload['email'])
                ticket.user_answer = request.data.get('user_answer', ticket.user_answer)
                ticket.save()
            except KeyError:
                return Response({
                    'message': 'Ticket id excepted'
                })

            except DataError:
                return Response({
                    'message': 'Input error'
                })

            except ObjectDoesNotExist:
                return Response({
                    'message': 'No any ticket to update!'
                })

        return Response({
            'message': 'success'
        })
