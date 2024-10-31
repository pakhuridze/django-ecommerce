# accounts/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import CustomUser  # Your custom user model
from .forms import CustomUserCreationForm  # Assuming you have a form for user registration
from django.contrib import messages
class RegisterView(CreateView):
    model = CustomUser
    template_name = 'accounts/register.html'  # Path to your registration template
    form_class = CustomUserCreationForm  # Custom form for user registration
    success_url = reverse_lazy('accounts:login')  # Redirect to login after successful registration

    def form_valid(self, form):
        messages.success(self.request, 'Registration successful. You can now log in.')
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Path to your login template

    def form_valid(self, form):
        messages.success(self.request, 'Login successful.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('eshop:index')

    def post(self, request, *args, **kwargs):
        messages.success(request, 'You have been logged out.')
        return super().post(request, *args, **kwargs)