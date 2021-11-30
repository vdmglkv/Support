import jwt
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from supportapp.serializers import TicketSerializer
from supportapp.models import Ticket
from django.db.utils import DataError
from django.db.models import ObjectDoesNotExist
from django.conf import settings


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.all()

    def list(self, request, *args, **kwargs):

        token = request.COOKIES.get('refreshtoken')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload['isStaff?']:
            ticket = Ticket.objects.all()
            serializer = TicketSerializer(ticket, many=True)
            return Response(serializer.data)

        tickets = Ticket.objects.filter(from_user=payload['email'])
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        token = request.COOKIES.get('refreshtoken')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        try:
            ticket = Ticket.objects.create(title=request.data['title'],
                                           description=request.data['description'],
                                           from_user=payload['email'])
        except KeyError:
            return Response({
                'message': 'Title and description excepted!'
            })

        ticket.save()

        serializer = TicketSerializer(ticket)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):

        token = request.COOKIES.get('refreshtoken')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload['isStaff?']:
            return super(TicketViewSet, self).retrieve(request, *args, **kwargs)

        ticket = get_object_or_404(self.get_queryset(), pk=pk, from_user=payload['email'])
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):

        token = request.COOKIES.get('refreshtoken')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload['isStaff?']:

            ticket = Ticket.objects.filter(id=pk).first()
            ticket.delete()

            response_message = {"message": "Item has been deleted"}
        else:
            response_message = {"message": "Not Allowed"}

        return Response(response_message)

    def update(self, request, pk=None, *args, **kwargs):

        token = request.COOKIES.get('refreshtoken')
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        if payload['isStaff?']:
            try:
                ticket = Ticket.objects.get(id=pk)
                ticket.status = request.data.get('status', ticket.status)
                ticket.support_answer = request.data.get('support_answer', ticket.support_answer)
                ticket.save()
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
                ticket = Ticket.objects.get(id=pk, from_user=payload['email'])
                ticket.title = request.data.get('title', ticket.title)
                ticket.description = request.data.get('description', ticket.description)
                ticket.user_answer = request.data.get('user_answer', ticket.user_answer)
                ticket.save()
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
