# models.py
from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True)
    members = models.ManyToManyField('CustomUser', related_name='groups')

    def __str__(self):
        return self.name
# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Your existing fields and methods

    groups = models.ManyToManyField('Group', related_name='users')

    def __str__(self):
        return self.username
# Creating groups and adding users to them programmatically
# Note: You should have a valid user object and group objects for this to work.

group1 = Group.objects.create(name='L1 Support')
group2 = Group.objects.create(name='L2 Support')
group3 = Group.objects.create(name='L3 Support')

user1 = CustomUser.objects.get(username='user1')  # Replace 'user1' with the actual username
user2 = CustomUser.objects.get(username='user2')  # Replace 'user2' with the actual username

group1.members.add(user1)
group1.members.add(user2)

group2.members.add(user2)

# Repeat this process for other users and groups as needed
