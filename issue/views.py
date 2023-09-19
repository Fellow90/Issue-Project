from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from issue.models import CustomUser, Group, Ticket, Comment
from issue.serializers import TicketSerializer, CommentSerializer, CustomUserSerializer


class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    @property
    def user(self):
        return self.request.user

    @property
    def is_authenticated(self):
        if self.request.user.id == self.kwargs.get("user_pk"):
            return True

    def get_queryset(self):
        # for admin view with respective id of the user
        user_pk_for_admin = self.kwargs.get("user_pk")
        if self.user.is_superuser:
            return self.queryset.filter(issuer=user_pk_for_admin)

        # for authenticated user view
        user_pk = self.kwargs.get("user_pk")
        user = CustomUser.objects.get(id=user_pk)
        if self.is_authenticated:
            return self.queryset.filter(issuer=user)
        else:
            return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, url_path="solvebyl1")
    def resolve_ticket_by_l1(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        data["resolved_by"] = "L1"
        data['status_code'] = '200'
        serializer = TicketSerializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True,url_path='forwardtol2')
    def forward_to_l2(self,request,*args,**kwargs):
        instance = self.get_object()
        data = request.data
        if instance.status_code == '102' and instance.resolved_by == '':
            data['assigned_to'] = 'L2'
        serializer = TicketSerializer(instance=instance, data=data, partial = True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    
    @action(detail=True, url_path="solvebyl2")
    def resolve_ticket_by_l2(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        data["resolved_by"] = "L2"
        data['status_code'] = '200'
        serializer = TicketSerializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True,url_path='forwardtol3')
    def forward_to_l3(self,request,*args,**kwargs):
        instance = self.get_object()
        data = request.data
        if instance.status_code == '102' and instance.resolved_by == '':
            data['assigned_to'] = 'L3'
        serializer = TicketSerializer(instance=instance, data=data, partial = True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status= status.HTTP_201_CREATED)

    @action(detail=True, url_path="solvebyl3")
    def resolve_ticket_by_l3(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        data["resolved_by"] = "L3"
        data['status_code'] = '200'
        serializer = TicketSerializer(instance=instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
   

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @property
    def user(self):
        return self.request.user

    @property
    def is_authenticated(self):
        if self.request.user.id == self.kwargs.get("user_pk"):
            return True

    def get_queryset(self):
        user_pk = self.kwargs.get("user_pk")
        ticket_pk = self.kwargs.get("ticket_pk")

        # making the comments available to only authenticated user or the admin
        if self.user.is_superuser or self.user.is_authenticated:
            return Comment.objects.filter(ticket__pk=ticket_pk, issuer__pk=user_pk)

        else:
            return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
