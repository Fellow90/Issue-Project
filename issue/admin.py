from django.contrib import admin
from issue.models import CustomUser, Ticket, Comment
# Register your models here.
admin.site.register([CustomUser, Ticket, Comment])
