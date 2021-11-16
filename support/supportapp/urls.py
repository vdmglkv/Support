from rest_framework import routers
from .views import TicketView
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = [
    path('api/ticket/', TicketView.as_view()),
    path('', include(router.urls))
    ]
