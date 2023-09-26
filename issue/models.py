from django.db import models
from django.contrib.auth.models import AbstractUser
from issue.enums import GENDER_CHOICES, STATUS_CHOICES, PRIORITY_CHOICES, GROUP_CHOICES, ROLE_CHOICES, RESOLVED_BY_CHOICES, GROUP_NAME_CHOICES
from issue.managers import CustomUserManager

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30,null = True, blank = True)
    last_name = models.CharField(max_length=30, null = True, blank = True)
    gender = models.CharField(max_length=1, choices = GENDER_CHOICES, default='M')
    age = models.IntegerField(null = True, blank = True)
    address = models.CharField(max_length = 50, null = True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    username = models.CharField(max_length=30, unique = True)
    role = models.CharField(max_length=11,choices=ROLE_CHOICES, default='Normal User')
    group = models.ManyToManyField('Group',related_name='groups')
    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Group(models.Model):
    name = models.CharField(max_length=10,choices=GROUP_NAME_CHOICES, unique = True)
    members = models.ManyToManyField('CustomUser', related_name='members')

    def __str__(self):
        return self.name
    

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
    image = models.ImageField(upload_to='tickets', blank=True, null=True)

    def __str__(self):
        return self.ticket_ref
    

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    issuer = models.ForeignKey(CustomUser, on_delete = models.SET_NULL,null = True, blank=True, related_name='icomments')
    title = models.CharField(max_length=30)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
