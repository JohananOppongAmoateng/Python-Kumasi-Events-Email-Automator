from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth.models import User

class SignUpUserForm(BaseUserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Enter valid email address.',required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')