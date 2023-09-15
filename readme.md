from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from .models import CustomUser, Ticket, Comment

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser 
        fields = ('username', 'email','role','password1', 'password2')  

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','gender','age','date_of_birth','address','username','email','role']


class LoginForm(AuthenticationForm):
    pass

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        # fields = '__all__'
        fields = ['status_code','priority','company_name','ticket_ref','assigned_to','resolved_by','code','image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     blank=True,
    #     related_name='custom_users' 
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     blank=True,
    #     related_name='custom_users' 
    # )

(env) aayulogic@aayulogic-OptiPlex-3040:~/Nabaraj/issueSerializer$ python manage.py makemigrations
SystemCheckError: System check identified some issues:

ERRORS:
auth.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'auth.User.groups' clashes with reverse accessor for 'issue.CustomUser.groups'.
        HINT: Add or change a related_name argument to the definition for 'auth.User.groups' or 'issue.CustomUser.groups'.
auth.User.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'auth.User.user_permissions' clashes with reverse accessor for 'issue.CustomUser.user_permissions'.
        HINT: Add or change a related_name argument to the definition for 'auth.User.user_permissions' or 'issue.CustomUser.user_permissions'.
issue.CustomUser.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'issue.CustomUser.groups' clashes with reverse accessor for 'auth.User.groups'.
        HINT: Add or change a related_name argument to the definition for 'issue.CustomUser.groups' or 'auth.User.groups'.
issue.CustomUser.user_permissions: (fields.E304) Reverse accessor 'Permission.user_set' for 'issue.CustomUser.user_permissions' clashes with reverse accessor for 'auth.User.user_permissions'.
        HINT: Add or change a related_name argument to the definition for 'issue.CustomUser.user_permissions' or 'auth.User.user_permissions'.