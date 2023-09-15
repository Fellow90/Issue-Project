from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet


from issue.models import CustomUser, Epic, Ticket, Comment
from issue.serializers import TicketSerializer, CommentSerializer, CustomUserSerializer

class TicketViewSet(ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer