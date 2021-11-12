from rest_framework import routers
from .api import TicketViewSet

router = routers.DefaultRouter()
router.register('api/ticket', TicketViewSet, 'ticket')

urlpatterns = router.urls
