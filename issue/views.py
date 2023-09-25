from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from issue.models import CustomUser, Group, Ticket, Comment
from issue.serializers import TicketSerializer, CommentSerializer, CustomUserSerializer, GroupSerializer
from issue.mappers import GroupNameMappers
from issue.enums import GROUP_NAME_CHOICES
from issue.permissions  import AssigneePermission

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)
        group_selection = request.data.get('role')
        group_name = GroupNameMappers.get(group_selection)
        if group_name :
            group = get_object_or_404(Group, name = group_name)
            group.members.add(serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        group_selection = request.data.get('role')
        group_name = GroupNameMappers.get(group_selection)
        if group_name :
            group = get_object_or_404(Group, name = group_name)
            group.members.add(serializer.instance)
        return Response(serializer.data)
    

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        return serializer.save()

class TicketViewSet(ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [AssigneePermission]
    
    @property
    def user(self):
        return self.request.user
    
    def get_queryset(self):
        if self.user.is_superuser:
            return self.queryset
        if self.user.role == 'Admin':
            return self.queryset
        elif self.user.role == 'L1 User':
            return self.queryset.filter(assigned_to = 'L1')
        elif self.user.role == 'L2 User':
            return self.queryset.filter(assigned_to = 'L2')
        elif self.user.role == 'L3 User':
            return self.queryset.filter(assigned_to = 'L3')
        return self.queryset.filter(issuer = self.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=True, url_path="solvebyl1")
    def resolve_ticket_by_l1(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if instance.status_code == 'PENDING' and instance.resolved_by == '' and instance.assigned_to == 'L1':
            data["resolved_by"] = "L1"
            data['status_code'] = '200'
            serializer = TicketSerializer(instance=instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'The ticket cant be solved by L1'},status=status.HTTP_400_BAD_REQUEST)
            
    @action(detail=True,url_path='forwardtol2')
    def forward_to_l2(self,request,*args,**kwargs):
        instance = self.get_object()
        data = request.data
        if instance.status_code == 'PENDING' and instance.resolved_by == '' and instance.assigned_to == 'L1':
            data['status_code'] = '102'
            data['assigned_to'] = 'L2'
            serializer = TicketSerializer(instance=instance, data=data, partial = True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response({'msg':'The ticket cant be  forwarded to L2'},status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, url_path="solvebyl2")
    def resolve_ticket_by_l2(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        if instance.status_code == '102' and instance.resolved_by == '' and instance.assigned_to  == 'L2':
            data["resolved_by"] = "L2"
            data['status_code'] = '200'
            serializer = TicketSerializer(instance=instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'The ticket cant be solved by L2'},status=status.HTTP_400_BAD_REQUEST)  
    
    @action(detail=True,url_path='forwardtol3')
    def forward_to_l3(self,request,*args,**kwargs):
        instance = self.get_object()
        data = request.data
        if instance.status_code == '102' and not instance.resolved_by and instance.assigned_to == 'L2':
            data['assigned_to'] = 'L3'
            data['status_code'] = '102'
            serializer = TicketSerializer(instance=instance, data=data, partial = True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response({'msg':'The ticket cant be forwarded to L3'},status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path="solvebyl3")
    def resolve_ticket_by_l3(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        if instance.status_code  == '102' and instance.resolved_by == '' and instance.assigned_to == 'L3':
            data["resolved_by"] = "L3"
            data['status_code'] = '200'
            serializer = TicketSerializer(instance=instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg':'The ticket cant be solved by L3'},status=status.HTTP_400_BAD_REQUEST)
        

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
        return Comment.objects.filter(ticket__pk = self.kwargs.get('ticket_pk'))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

