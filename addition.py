from django.db import models
from django.contrib.auth.models import AbstractUser
from issue.enums import GENDER_CHOICES, STATUS_CHOICES, PRIORITY_CHOICES, GROUP_CHOICES, ROLE_CHOICES, RESOLVED_BY_CHOICES
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30,null = True, blank = True)
    last_name = models.CharField(max_length=30, null = True, blank = True)
    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, default='M')
    age = models.IntegerField(null = True, blank = True)
    address = models.CharField(max_length = 50, null = True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    username = models.CharField(max_length=30, unique = True)
    role = models.CharField(max_length=11,choices=ROLE_CHOICES,default='Normal User')

    def __str__(self):
        return self.username
    
class Ticket(models.Model):
    issuer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')
    status_code = models.CharField(max_length=3,choices=STATUS_CHOICES, default=200)
    priority = models.CharField(max_length=6,choices = PRIORITY_CHOICES, default='Low')
    company_name = models.CharField(max_length=50)
    ticket_ref = models.CharField(max_length=10)
    assigned_to = models.CharField(max_length=2, choices= GROUP_CHOICES, default='L1')
    resolved_by = models.CharField(max_length=2,choices=RESOLVED_BY_CHOICES,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    code = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    
class Epic(models.Model):
    project_name = models.CharField(max_length=50)
    project_description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    tickets = models.ManyToManyField(Ticket, related_name='epics')

    def __str__(self):
        return self.project_name
    
class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    issuer = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,null = True, blank=True, related_name='icomments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    