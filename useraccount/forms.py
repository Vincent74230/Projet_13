from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm, 
    PasswordChangeForm)
from .models import User, Services
from django.forms import ModelForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','gender', 'email','postcode', 'password1', 'password2']

class ModifyUserProfile(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'postcode']

class ChangePassword(PasswordChangeForm):
    model = User
