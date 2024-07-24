# myapp/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.conf import settings
from calendar import monthcalendar
from django.views import View
from .models import NewTrip
from .forms import CalendarEventForm, CreateUserForm


def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page.
    else:
        form = AuthenticationForm()
    return render(request, 'base/login_register.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to TripTrack, {user.username}! Your account has been created successfully.")
            return redirect('home')  # Redirect to dashboard or home page after successful registration
        else:
            print("Form is invalid. Errors:")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Field: {field}, Error: {error}")
    else:
        form = CreateUserForm()
    
    return render(request, 'base/register.html', {'form': form})

@login_required(login_url='login')
def home(request):
    return render(request, 'base/home.html')

@login_required(login_url='login')
def CalendarEventView(request):
    if request.method == 'POST':
        form = CalendarEventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createtripdate')
    else:
        form = CalendarEventForm()
    
    events = NewTrip.objects.all().order_by('date')
    return render(request, 'base/newTripDate.html', {'events': events, 'form': form})