from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from dateutil import relativedelta
from datetime import datetime

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from issue.enums import STATUS_CHOICES, GROUP_CHOICES
from issue.models import CustomUser, Ticket, Comment, Group

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField( write_only=True)
    calculated_age = serializers.SerializerMethodField()
    ## this will provide all the tickets associated with the user.
    tickets = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    #this will provide the tickets associated with the user calling the __str__ method
    # tickets = serializers.StringRelatedField(many = True)

    class Meta:
        model = CustomUser
        #adding 'tickets' in the field below will add tickets pk in user instance. displays all associated tickets 
        fields = ['id','tickets','first_name', 'last_name', 'gender','calculated_age', 'date_of_birth', 'address', 'username', 'email', 'role','password']
        exclude_fields = ['tickets']
        # exclude = ['password']

    def create(self, validated_data):
        # validated_data['password'] = make_password(validated_data.get('password'))
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        if validated_data.get('role')== 'Admin':
            user.is_superuser=True
            user.is_staff = True
            user.save()
        return user
    
    def update(self, instance, validated_data):
        user =  super().update(instance, validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    def get_calculated_age(self,instance):
        current_date = datetime.now()
        age_in_years = relativedelta.relativedelta(current_date, instance.date_of_birth).years
        return age_in_years
    
    # def validate(self, attrs):
    #     attrs = super().validate(attrs)
    #     if attrs.get('first_name') == 'Nabaraj':
    #         raise serializers.ValidationError({'msg':"Sorry!! Not allowed!!"})
    #     return attrs


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
        hidden_fields = ['members']

    
class TicketSerializer(ModelSerializer):
    #source map the serializer field name with the  model field name
    issuer_first_name = serializers.CharField(source = 'issuer.first_name',read_only = True)
    # issuer = CustomUserSerializer(read_only = True)
    # issuer = serializers.PrimaryKeyRelatedField(queryset= CustomUser.objects.all()) 
    #relates the string representation 
    # issuer = serializers.StringRelatedField(many = False)
    # photo_url = serializers.SerializerMethodField()
    class Meta:
        model = Ticket
        fields = ['id','issuer_first_name','status_code','priority','company_name','ticket_ref','assigned_to','resolved_by','code','image']

    def create(self, validated_data):
        logged_in_pk = self.context['request'].user.pk
        user = CustomUser.objects.get(pk = logged_in_pk)
        validated_data['issuer'] = user
        validated_data['assigned_to'] = 'L1'
        validated_data['status_code'] = 'PENDING'
        return Ticket.objects.create(**validated_data) 
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')
        if request and request.method == 'GET':
            fields['issuer'] = CustomUserSerializer()
        return fields
    
    # def get_photo_url(self,ticket):
    #     request = self.context.get('request')
    #     photo_url = ticket.image.path
    #     return request.build_absolute_uri(photo_url)

    
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['title','comment']

    def create(self, validated_data):
        logged_in_pk = self.context['request'].user.pk
        issuer = CustomUser.objects.get(pk = logged_in_pk)
        assigned_ticket_id = self.context['request'].path.split('/')[2]
        ticket = Ticket.objects.get(pk = assigned_ticket_id)
        validated_data['ticket'] = ticket
        validated_data['issuer'] = issuer
        return Comment.objects.create(**validated_data)
