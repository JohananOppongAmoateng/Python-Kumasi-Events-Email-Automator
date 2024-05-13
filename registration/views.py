from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpUserForm
from django.views.generic.edit import CreateView
# Create your views here.


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignUpUserForm
    success_url = '/accounts/login/'
