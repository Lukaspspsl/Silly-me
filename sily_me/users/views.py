from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from .forms import UserRegisterForm
from .models import Profile

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get(
                'password1')
            try:
                user = User.objects.create_user(username=email, email=email, password=password)
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("homepage")
            except IntegrityError:
                form.add_error('email', 'Email is already in use.')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid data.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")