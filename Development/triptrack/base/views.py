from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import newTrip, Destination, Transport, Leg, ChecklistItem
from django.contrib import messages  # Import messages framework
from .forms import *
import requests
from django.http import JsonResponse
from django.views import View

def loginUser(request):
    """
    View to handle user login.

    This view processes both GET and POST requests:
    - For GET requests, it displays an empty login form.
    - For POST requests, it authenticates the user using the provided credentials.
    
    If the login is successful, the user is redirected to the 'createButton' page.
    """

    if request.method == 'POST':
        # Initialize the authentication form with the POST data
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # Get the username and password from the cleaned form data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in and redirect to the home page
                login(request, user)
                return redirect('createButton')  # Change 'createButton' to your desired redirect view
            else:
                # If authentication fails, add an error message
                messages.error(request, "Invalid username or password.")
        else:
            # If form is invalid, add an error message (e.g., if fields are missing)
            messages.error(request, "Invalid input. Please try again.")
    
    else:
        # If the request is GET, display an empty login form
        form = AuthenticationForm()

    # Render the login form on the login/register page with messages
    return render(request, 'base/pgLogin.html', {'form': form})


def logoutUser(request):
    """
    View to handle user logout.

    Logs out the current user and redirects them to the login page.
    """
    logout(request)
    return redirect('login')


def createUser(request):
    """
    View to handle user registration.

    This view processes both GET and POST requests:
    - For GET requests, it displays an empty registration form.
    - For POST requests, it registers the user with the provided details and logs them in.
    
    After successful registration, the user is redirected to the 'home' page.
    """

    if request.method == 'POST':
        # Initialize the registration form with POST data
        form = CreateUserForm(request.POST)

        if form.is_valid():
            # Save the new user and log them in
            user = form.save()
            login(request, user)
            return redirect('createButton')
    else:
        # If the request is GET, display an empty registration form
        form = CreateUserForm()

    # Render the registration form on the registration page
    return render(request, 'base/pgCreateUser.html', {'form': form})


@login_required(login_url='login')
def createButton(request):
    """
    View to render the home page.

    This view is protected by login and requires the user to be authenticated.
    If the user is not logged in, they will be redirected to the login page.
    """
    return render(request, 'base/pgCreateButton.html')


@login_required(login_url='login')
def createTripTwo(request):
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
        return redirect('createTripTwo')
    else:
        form = EventFormTrans()
    return render(request, 'base/pgCreateTripTwo.html', {'form': form, 'legs': legs})


@login_required(login_url='login')
def createTripOne(request):
    """
    View to handle the creation of a new trip (event).

    This view processes both GET and POST requests:
    - For GET requests, it displays an empty form to create a new trip.
    - For POST requests, it processes the form data to create a new trip.
    
    The user must be logged in to access this view.
    """

    if request.method == 'POST':
        # Initialize the trip creation form with POST data
        form = newTripForm(request.POST)

        if form.is_valid():
            # Save the new trip without committing it to the database
            trip = form.save(commit=False)

            # Associate the trip with the currently logged-in user
            trip.user = request.user

            # Save the trip to the database
            trip.save()

            # Store the trip's primary key in the session for later reference
            request.session['strTripName_id'] = trip.pk

            # Redirect the user to the 'createtriptrans' view for adding trip details
            return redirect('createTripTwo')
    else:
        # If the request is GET, display an empty trip form
        form = newTripForm()

    # Render the trip form on the 'newTripDate.html' template
    return render(request, 'base/pgCreateTripOne.html', {'form': form})





@login_required(login_url='login')
def page1(request):
    """
    View to display the details of a trip.

    This view attempts to retrieve the trip using the session's `strTripName_id`.
    If `strTripName_id` is not found, it defaults to the most recent trip.
    """
    request.session["active_page"] = 1
    trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate').first()
    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = trip.pk


    if trip:
        legs = Leg.objects.filter(trip=trip).order_by('pk')
        checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")
        return render(request, 'base/page1.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    else:
        # If no trips exist, handle the case appropriately
        return render(request, 'base/no_trips.html')  # Create a template for no trips

@login_required(login_url='login')
def page2(request):
    """
    View to display the details of a trip.

    This view attempts to retrieve the trip using the session's `strTripName_id`.
    If `strTripName_id` is not found, it defaults to the most recent trip.
    """
    request.session["active_page"] = 2
    trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate')[1]
    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = trip.pk

    if trip:
        legs = Leg.objects.filter(trip=trip).order_by('pk')
        checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")
        return render(request, 'base/page2.html', {'trip': trip, 'legs': legs, 'checklist':checklist})
    else:
        # If no trips exist, handle the case appropriately
        return render(request, 'base/no_trips.html')  # Create a template for no trips
    
@login_required(login_url='login')
def page3(request):
    """
    View to display the details of a trip.

    This view attempts to retrieve the trip using the session's `strTripName_id`.
    If `strTripName_id` is not found, it defaults to the most recent trip.
    """
    request.session["active_page"] = 3
    trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate')[2]
    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = trip.pk

    if trip:
        legs = Leg.objects.filter(trip=trip).order_by('pk')
        checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")
        return render(request, 'base/page3.html', {'trip': trip, 'legs': legs, 'checklist':checklist})
    else:
        # If no trips exist, handle the case appropriately
        return render(request, 'base/no_trips.html')  # Create a template for no trips

@login_required(login_url='login')
def page4(request):
    """
    View to display the details of a trip.

    This view attempts to retrieve the trip using the session's `strTripName_id`.
    If `strTripName_id` is not found, it defaults to the most recent trip.
    """
    request.session["active_page"] = 4
    trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate')[3]
    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = trip.pk

    if trip:
        legs = Leg.objects.filter(trip=trip).order_by('pk')
        checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")
        return render(request, 'base/page4.html', {'trip': trip, 'legs': legs, 'checklist':checklist})
    else:
        # If no trips exist, handle the case appropriately
        return render(request, 'base/no_trips.html')  # Create a template for no trips \
    

def index(request):
    items = ChecklistItem.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            ChecklistItem.objects.create(title=title)
        return redirect('home')
    return render(request, 'base/checklist.html', {'items': items})


def docInfo(request):
     return render(request, 'base/docPage.html')

def prodInfo(request):
     return render(request, 'base/prodPage.html')


def baggage_check_view1(request):
    if request.method == 'POST':
        entry = request.POST
        if entry['number'] is None or entry['number'] == '':
            number = 0
        if request.session["active_page"] == 1:
            trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate').first()
        if request.session["active_page"] > 1:
            trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate')[(request.session["active_page"] - 1)]
        # Store the trip's primary key in the session for later reference
        request.session['strTripName_id'] = trip.pk

        if trip:
            legs = Leg.objects.filter(trip=trip).order_by('pk')
            checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")
        if entry:
            number = entry['number']
            url = f'https://api.assetsentinel.com.au/api/baggagecheck/australia/{number}/'
            response = requests.get(url)
            print(response.status_code, response.json(), request.session["active_page"])
            if response.status_code == 200:
                data = response.json()
                if request.session["active_page"] == 1:
                    return render(request, 'base/page1.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
                if request.session["active_page"] == 2:
                    return render(request, 'base/page2.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
                if request.session["active_page"] == 3:
                    return render(request, 'base/page3.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
                if request.session["active_page"] == 4:
                    return render(request, 'base/page4.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
            else:
                data = 'Error'
                if request.session["active_page"] == 1:
                    return render(request, 'base/page1.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
                if request.session["active_page"] == 2:
                    return render(request, 'base/page2.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
                if request.session["active_page"] == 3:
                    return render(request, 'base/page3.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
                if request.session["active_page"] == 4:
                    return render(request, 'base/page4.html', {'entry': entry, 'data': data, 'trip': trip, 'legs': legs, 'checklist': checklist})
                # return JsonResponse({'error': 'Failed to fetch data from external API'}, status=response.status_code)
    
    
    # return render(request, 'base/page1.html', {'entry': entry, 'data': data})

def toggle_completion1(request, item_id):
    item = ChecklistItem.objects.get(id=item_id)
    item.completed = not item.completed
    item.save()
    
    if request.session["active_page"] == 1:
        trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate').first()
    if request.session["active_page"] > 1:
        trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate')[(request.session["active_page"] - 1)]

    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = trip.pk

    if trip:
        legs = Leg.objects.filter(trip=trip).order_by('pk')
        checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")
    
    if request.session["active_page"] == 1:
        return render(request, 'base/page1.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 2:
        return render(request, 'base/page2.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 3:
        return render(request, 'base/page3.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 4:
        return render(request, 'base/page4.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    

def delete_item1(request, item_id):
    item = ChecklistItem.objects.get(id=item_id)
    item.delete()
    if request.session["active_page"] == 1:
        trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate').first()
    if request.session["active_page"] > 1:
        trip = newTrip.objects.filter(user=request.user).order_by('-intStartDate')[(request.session["active_page"] - 1)]
    
    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = trip.pk

    if trip:
        legs = Leg.objects.filter(trip=trip).order_by('pk')
        checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")

    if request.session["active_page"] == 1:
        return render(request, 'base/page1.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 2:
        return render(request, 'base/page2.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 3:
        return render(request, 'base/page3.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 4:
        return render(request, 'base/page4.html', {'trip': trip, 'legs': legs, 'checklist': checklist})

def new_todo1(request):
    trip = newTrip.objects.get(pk=request.session['strTripName_id'])
    ChecklistItem.objects.create(trip=trip,title=request.POST['title'])
    if trip:
        legs = Leg.objects.filter(trip=trip).order_by('pk')
        checklist = ChecklistItem.objects.filter(trip=trip).order_by("pk")

    if request.session["active_page"] == 1:
        return render(request, 'base/page1.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 2:
        return render(request, 'base/page2.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 3:
        return render(request, 'base/page3.html', {'trip': trip, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 4:
        return render(request, 'base/page4.html', {'trip': trip, 'legs': legs, 'checklist': checklist})