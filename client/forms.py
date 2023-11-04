from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomClient


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomClient
        fields = ("username", "race", "class_name", "profile_avatar")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomClient
        exclude = ("username", "password", "race", "first_name", "is_superuser", "date_joined", "user_permissions",
                   "last_name", "is_staff", "is_active", "last_login", "groups", "money")
