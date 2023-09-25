from django.urls import path, include
from rest_framework.routers import DefaultRouter
from issue.views import TicketViewSet, CommentViewSet, CustomUserViewSet, GroupViewSet
app_name = 'issue'
userrouter = DefaultRouter()
userrouter.register(r'users',CustomUserViewSet, basename='users')

ticketrouter = DefaultRouter()
ticketrouter.register(r'tickets',TicketViewSet, basename='tickets')

commentrouter = DefaultRouter()
commentrouter.register(r'comments',CommentViewSet, basename='comments')

grouprouter = DefaultRouter()
grouprouter.register(r'groups', GroupViewSet, basename='groups')


urlpatterns = [
    path('', include(userrouter.urls)),
    path('', include(ticketrouter.urls)),
    path('tickets/<int:ticket_pk>/',include(commentrouter.urls)),
    path('', include(grouprouter.urls)),
]
