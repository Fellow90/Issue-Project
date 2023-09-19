from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from issue.enums import STATUS_CHOICES, GROUP_CHOICES

from issue.models import CustomUser, Ticket, Comment

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)

    

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'age', 'date_of_birth', 'address', 'username', 'email', 'role', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = CustomUser.objects.create(**validated_data)

        if validated_data.get('role')== 'Admin':
            user.is_superuser=True
            user.is_staff = True
            user.save()
        return user
    
    

    # def validate(self, attrs):
    #     attrs = super().validate(attrs)
    #     if attrs.get('first_name') == 'Nabaraj':
    #         raise serializers.ValidationError({'msg':"Sorry!! Not allowed!!"})
    #     return attrs

    
class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status_code','priority','company_name','ticket_ref','assigned_to','resolved_by','code','image']

    def create(self, validated_data):
        logged_in_pk = self.context['request'].user.pk
        user = CustomUser.objects.get(pk = logged_in_pk)
        validated_data['issuer'] = user
        validated_data['assigned_to'] = 'L1'
        validated_data['status_code'] = 'PENDING'
        return Ticket.objects.create(**validated_data)
    
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['title','comment']

    def create(self, validated_data):
        logged_in_pk = self.context['request'].user.pk
        issuer = CustomUser.objects.get(pk = logged_in_pk)
        assigned_ticket_id = self.context['request'].path.split('/')[4]
        ticket = Ticket.objects.get(pk = assigned_ticket_id)
        validated_data['ticket'] = ticket
        validated_data['issuer'] = issuer
        return Comment.objects.create(**validated_data)
        