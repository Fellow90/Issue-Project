from django.urls import path, include
from rest_framework.routers import DefaultRouter
from issue.views import TicketViewSet, CommentViewSet, CustomUserViewSet
app_name = 'issue'
userrouter = DefaultRouter()
userrouter.register(r'users',CustomUserViewSet, basename='users')

ticketrouter = DefaultRouter()
ticketrouter.register(r'tickets',TicketViewSet, basename='tickets')

commentrouter = DefaultRouter()
commentrouter.register(r'comments',CommentViewSet, basename='comments')


urlpatterns = [
    path('', include(userrouter.urls)),
    path('users/<int:user_pk>/', include(ticketrouter.urls)),
    path('users/<int:user_pk>/tickets/<int:ticket_pk>/',include(commentrouter.urls)),
    # path('users/<int:user_pk>/tickets/<int:ticket_pk>/comments/', CommentViewSet.as_view({'get': 'list'}), name='comment-list'),
    # path('users/<int:user_pk>/tickets/<int:ticket_pk>/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve'}), name='comment-detail'),
]
