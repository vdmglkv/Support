from rest_framework import routers
from supportapp.views import TicketViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('api/ticket', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls))
    ]
