from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from issue.models import CustomUser, Ticket, Comment

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'age', 'date_of_birth', 'address', 'username', 'email', 'role', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = CustomUser.objects.create(**validated_data)
        return user
    
class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status_code','priority','company_name','ticket_ref','assigned_to','resolved_by','code','image']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']