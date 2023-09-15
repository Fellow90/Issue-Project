from django.urls import path, include
from rest_framework.routers import DefaultRouter
from issue.views import TicketViewSet, CommentViewSet, CustomUserViewSet
app_name = 'issue'
router = DefaultRouter()
router.register(r'tickets',TicketViewSet, basename='tickets')
router.register(r'comments',CommentViewSet, basename='comments')
router.register(r'users',CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
]