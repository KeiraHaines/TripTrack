from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import newTrip, Destination, Transport, Leg
from .forms import newTripForm, CreateUserForm, EventFormTrans

def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
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
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'base/register.html', {'form': form})

@login_required(login_url='login')
def home(request):
    return render(request, 'base/home.html')

@login_required(login_url='login')
def create_event_trans(request):
    trip = newTrip.objects.get(pk=request.session['strTripName_id'])
    legs = Leg.objects.filter(trip=trip)
    if request.method == 'POST':
        print(request.POST)
        location = request.POST.get('destination')
        transport_list = request.POST.getlist('transport')
        transport_list = [t for t in transport_list if t]
        transport = transport_list[0] if transport_list else None
        selected_transport = Transport.objects.get(pk=transport)        
        try:
            selected_location = Destination.objects.get(name=location)
        except Exception as e:
            selected_location = Destination.objects.create(name=location)
        new_leg = Leg.objects.create(trip=trip, destination=selected_location, transport=selected_transport)
        return redirect('createtriptrans')
    else:
        form = EventFormTrans()
    return render(request, 'base/newTripTran.html', {'form': form, 'legs': legs})

@login_required(login_url='login')
def create_event(request):
    """
    View to handle the creation of a new event.

    This view handles both GET and POST requests:
    - For GET requests, it initializes a blank form to be filled by the user.
    - For POST requests, it processes the form data submitted by the user.

    The user must be logged in to access this view. If the user is not logged in, 
    they will be redirected to the login page specified by 'login_url'.
    """

    if request.method == 'POST':
        # Initialize the form with POST data
        form = newTripForm(request.POST)

        if form.is_valid():
            # If the form is valid, create an event object without saving it to the database yet
            trip = form.save(commit=False)

            # Associate the event with the currently logged-in user
            trip.user = request.user

            # Save the event to the database
            trip.save()

            # Store the event's primary key in the session for later use
            request.session['strTripName_id'] = trip.pk

            # Redirect the user to the 'createtriptrans' view after successful event creation
            return redirect('createtriptrans')
        else:
            # If the form is invalid, print the form errors to the console (for debugging purposes)
            print(form.errors)
    else:
        # If the request method is GET, initialize a blank form
        form = newTripForm()

    # Render the form on the 'newTripDate.html' template for the user to fill out
    return render(request, 'base/newTripDate.html', {'form': form})


