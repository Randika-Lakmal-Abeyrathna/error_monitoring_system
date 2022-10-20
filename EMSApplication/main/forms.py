from django.contrib.auth.forms import UserCreationForm,SetPasswordForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model= User
        fields= ('username','email','password1','password2')


class SetPasswordForm(SetPasswordForm):

    class Meta:
        model = User
        fields =('new_password1','new_password2')