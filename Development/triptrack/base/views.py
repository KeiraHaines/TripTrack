# Title: TripTrack
# Author: Keira Haines
# Date Created: 12 September 2024
# Last Modified: 

# Purpose: This application is designed for new travellers aged 25-75 who face challenges in gathering and organizing holiday-related information. 
# It simplifies the process by tracking and organizing transportation options and providing interactive checklists. 
# It also includes essential details such as permitted baggage weights, flight item restrictions, and entry requirements for different countries. 
# Features encompass up-to-date travel information, external links, departure necessities, and a dedicated section for plotting all stops and modes of transportation.

# Import necessary Django modules and custom components
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Trip, Destination, Transport, TripLeg, ChecklistItem
from django.contrib import messages  # Import messages framework
from .forms import *
import requests
from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
import requests

def loginUser(request):
    """
    Handle user login process.
    
    This function manages both GET and POST requests for user login.
    For GET requests, it displays the login form.
    For POST requests, it attempts to authenticate the user.
    
    Logic:
    1. If POST, validate the form data.
    2. If valid, attempt to authenticate the user.
    3. If authentication successful, log the user in and redirect to 'createButton'.
    4. If authentication fails, display an error message.
    5. If GET, display the login form.

    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # cleaned_data is a dictionary that stores the validated and processed username and password 
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('createButton')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid input. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'base/pgLogin.html', {'form': form})


def logoutUser(request):
    """
    Log out the current user.
    
    This function handles the logout process for the current user.
    
    Logic:
    1. Call Django's logout function to end the user's session.
    2. Redirect the user to the login page.

    """
    logout(request)
    return redirect('login')


def createUser(request):
    """
    Handle user registration process.
    
    This function manages both GET and POST requests for user registration.
    For GET requests, it displays the registration form.
    For POST requests, it attempts to create a new user.
    
    Logic:
    1. If POST, validate the form data.
    2. If valid, create a new user and log them in.
    3. Redirect to 'createButton' after successful registration.
    4. If GET, display the registration form.

    """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # cleaned_data is a dictionary that stores the validated and processed user, which includes the email, username, password1, and password2
            user = form.cleaned_data.get('user')
            user = form.save()
            login(request, user)
            return redirect('createButton')
    else:
        form = CreateUserForm()
    return render(request, 'base/pgCreateUser.html', {'form': form})


@login_required(login_url='login')
def createButton(request):
    """
    Render the create button page.
    
    This function is a simple view that renders the create button page.
    It's protected by the login_required decorator to ensure only authenticated users can access it.
   
    """
    return render(request, 'base/pgCreateButton.html')

@login_required(login_url='login')
def createTripTwo(request):
    """
    Handle the second step of trip creation.
    
    This function manages the process of adding legs (destinations and transportation) to a trip.
    It handles both GET and POST requests.
    
    Logic:
    1. Retrieve the current trip from the session.
    2. If POST, process the form data:
       - Get the location and transportation info.
       - Create or retrieve the Destination object.
       - Create a new TripLeg object.
    3. If GET, display the form for adding a new leg.
    
    """
    # Ensure the session contains the trip ID
    tripId = request.session.get('strTripName_id')
    
    if not tripId:
        messages.error(request, "No trip ID found in the session.")
        return redirect('createButton')  # Redirect to an appropriate error page

    try:
        dictTranLst = Trip.objects.get(pk=tripId)

    except Trip.DoesNotExist:
        messages.error(request, "The trip you are trying to add legs to does not exist.")
        return redirect('createButton')

    legs = TripLeg.objects.filter(dictTripLst=dictTranLst)

    if request.method == 'POST':
        strLoc = request.POST.get('strLoc')
        lstTran = request.POST.getlist('strTran')

        # Validate location input
        if not strLoc:
            messages.error(request, "Please enter a valid location.")
            return redirect('createTripTwo')

        # Validate transportation input
        lstTran = [t for t in lstTran if t]  # Filter out empty strings

        if not lstTran:
            messages.error(request, "Please select a transportation option.")
            return redirect('createTripTwo')

        strTran = lstTran[0]

        try:
            selTransport = Transport.objects.get(pk=strTran)
        except Transport.DoesNotExist:
            messages.error(request, "Selected transportation option does not exist.")
            return redirect('createTripTwo')

        try:
            # Retrieve or create destination
            selLocation = Destination.objects.get(strLoc=strLoc)
        except Destination.DoesNotExist:
            selLocation = Destination.objects.create(strLoc=strLoc)

        # Create the new TripLeg
        newLeg = TripLeg.objects.create(dictTripLst=dictTranLst, strLoc=selLocation, strTran=selTransport)

        # Success message and redirect
        messages.success(request, "Trip leg added successfully.")
        return redirect('createTripTwo')

    else:
        form = EventFormTrans()

    return render(request, 'base/pgCreateTripTwo.html', {'form': form, 'legs': legs})

@login_required(login_url='login')
def createTripOne(request):
    """
    Handle the first step of trip creation.
    
    This function manages the initial creation of a Trip object.
    It handles both GET and POST requests.
    
    Logic:
    1. If POST, validate the form data.
    2. If valid, create a new Trip object and associate it with the current user.
    3. Store the trip ID in the session and redirect to the second step.
    4. If GET, display the trip creation form.
    
    """
    if request.method == 'POST':
        form = newTripForm(request.POST)
        if form.is_valid():
            # cleaned_data is a dictionary that stores the validated and processed trip, which includes the trip name, start date, and end date
            strTrip = form.cleaned_data.get('strTrip')
            strTrip = form.save(commit=False)
            strTrip.user = request.user
            strTrip.save()
            request.session['strTripName_id'] = strTrip.pk
            return redirect('createTripTwo')
    else:
        form = newTripForm()
    return render(request, 'base/pgCreateTripOne.html', {'form': form})


@login_required(login_url='login')
def createdTripOne(request):
    """
    Display the most recent trip for the user.
    
    This function retrieves and displays the user's most recent trip,
    along with its associated legs and checklist items.
    
    Logic:
    1. Set the active page in the session.
    2. Retrieve the most recent trip for the current user.
    3. If a trip exists, fetch its legs and checklist items.
    4. Render the appropriate template with the trip data.
    
    """
    request.session["active_page"] = 1
    dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate').first()
    request.session['strTripName_id'] = dictTripLst.pk
    if dictTripLst:
        legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
        checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by("pk")
        print(checklist)
        return render(request, 'base/pgPreviousTripOne.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    else:
        return render(request, 'base/pgCreateButton.html')
    

@login_required(login_url='login')
def createdTripTwo(request):
    """
    Display the next most recent trip for the user.
    
    This function retrieves and displays the user's most recent trip,
    along with its associated legs and checklist items.
    
    Logic:
    1. Set the active page in the session.
    2. Retrieve the most recent trip for the current user.
    3. If a trip exists, fetch its legs and checklist items.
    4. Render the appropriate template with the trip data.
    
    """
    request.session["active_page"] = 2
    try:
        dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate')[1]
        request.session['strTripName_id'] = dictTripLst.pk
        passURL = 'base/pgPreviousTripTwo.html'
    except Exception as e:
        dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate')[0]
        request.session['strTripName_id'] = dictTripLst.pk
        passURL = 'base/pgPreviousTripOne.html'
        request.session["active_page"] = 1

    if dictTripLst:
        legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
        checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by("pk")
        return render(request, passURL, {'trip': dictTripLst, 'legs': legs, 'checklist':checklist})
    else:
        return render(request, 'base/pgCreateButton.html')  # Create a template for no trips


@login_required(login_url='login')
def createdTripThree(request):
    """
    Display the next most recent trip for the user.
    
    This function retrieves and displays the user's most recent trip,
    along with its associated legs and checklist items.
    
    Logic:
    1. Set the active page in the session.
    2. Retrieve the most recent trip for the current user.
    3. If a trip exists, fetch its legs and checklist items.
    4. Render the appropriate template with the trip data.
    
    """
    request.session["active_page"] = 3
    dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate')[2]
    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = dictTripLst.pk

    if dictTripLst:
        legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
        checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by("pk")
        return render(request, 'base/pgPreviousTripThree.html', {'trip': dictTripLst, 'legs': legs, 'checklist':checklist})
    else:
        # If no trips exist, handle the case appropriately
        return render(request, 'base/pgCreateButton.html')  # Create a template for no trips


@login_required(login_url='login')
def createdTripFour(request):
    """
    Display the next most recent trip for the user.
    
    This function retrieves and displays the user's most recent trip,
    along with its associated legs and checklist items.
    
    Logic:
    1. Set the active page in the session.
    2. Retrieve the most recent trip for the current user.
    3. If a trip exists, fetch its legs and checklist items.
    4. Render the appropriate template with the trip data.
    
    """
    request.session["active_page"] = 4
    dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate')[3]
    request.session['strTripName_id'] = dictTripLst.pk

    if dictTripLst:
        legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
        checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by("pk")
        return render(request, 'base/pgPreviousTripFour.html', {'trip': dictTripLst, 'legs': legs, 'checklist':checklist})
    else:
        # If no trips exist, handle the case appropriately
        return render(request, 'base/pgCreateButton.html')  # Create a template for no trips \

# Redirects the user to the document information page
@login_required(login_url='login')
def docInfo(request):
     return render(request, 'base/docPage.html')

# Redirects the user to the product information page
@login_required(login_url='login')
def prodInfo(request):
     return render(request, 'base/prodPage.html')


@login_required(login_url='login')
def luggageWeight(request):
    """
    Handle luggage weight calculation and API integration.
    
    This function processes luggage weight input, interacts with an external API,
    and displays the results along with trip information.
    
    Logic:
    1. Process POST data for luggage weight.
    2. Retrieve the appropriate trip based on the active page.
    3. Make an API call to get luggage weight suggestions.
    4. Render the appropriate page with API results and trip data.
    
    """
    if request.method == 'POST':
        entry = request.POST
        intLuggageWeight = entry.get('intLuggageWeight', 0)

        # Validate the luggage weight input
        try:
            intLuggageWeight = int(intLuggageWeight) if intLuggageWeight else 0
        except ValueError:
            messages.error(request, "Please enter a valid numeric value for luggage weight.")
            return redirect('some_trip_page')

        # Determine which trip to retrieve based on the active page
        active_page = request.session.get("active_page", 1)
        trip_query = Trip.objects.filter(user=request.user).order_by('-intStartDate')
        
        if not trip_query.exists():
            messages.error(request, "No trips found.")
            return redirect('some_trip_page')

        if active_page == 1:
            dictTripLst = trip_query.first()
        else:
            try:
                dictTripLst = trip_query[active_page - 1]
            except IndexError:
                messages.error(request, "Invalid page selection.")
                return redirect('some_trip_page')

        # Store the trip ID in the session
        request.session['strTripName_id'] = dictTripLst.pk

        # Get the legs and checklist for the trip
        legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
        checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by('pk')

        # Make the API request for luggage weight suggestion
        url = f'https://api.assetsentinel.com.au/api/baggagecheck/australia/{intLuggageWeight}/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            suggestLuggageWeight = response.json()
        except requests.exceptions.RequestException as e:
            suggestLuggageWeight = 'Error'
            messages.error(request, "Failed to retrieve luggage weight suggestions from the API.")

        # Simplify the rendering logic using a page map
        page_map = {
            1: 'base/pgPreviousTripOne.html',
            2: 'base/pgPreviousTripTwo.html',
            3: 'base/pgPreviousTripThree.html',
            4: 'base/pgPreviousTripFour.html',
        }

        template = page_map.get(active_page, 'base/pgPreviousTripOne.html')
        return render(request, template, {
            'entry': entry,
            'data': suggestLuggageWeight,
            'trip': dictTripLst,
            'legs': legs,
            'checklist': checklist,
        })


@login_required(login_url='login')
def checklistCheck(request, strItem_id):
    print(request)
    """
    Toggle the completion status of a checklist item.
    
    This function handles the toggling of a checklist item's completion status
    and then re-renders the appropriate trip page.
    
    Logic:
    1. Retrieve the ChecklistItem by its ID.
    2. Toggle its 'completed' status.
    3. Save the updated item.
    4. Determine which trip to display based on the active page in the session.
    5. Retrieve the trip and its associated legs and checklist items.
    6. Render the appropriate page with updated data.
    
    """
    strItem = ChecklistItem.objects.get(id=strItem_id)
    strItem.completed = not strItem.completed
    print("mode", strItem.completed)
    strItem.save()
    
    if request.session["active_page"] == 1:
        dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate').first()
    if request.session["active_page"] > 1:
        dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate')[(request.session["active_page"] - 1)]

    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = dictTripLst.pk

    if dictTripLst:
        legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
        checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by("pk")
    
    if request.session["active_page"] == 1:
        return render(request, 'base/pgPreviousTripOne.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 2:
        return render(request, 'base/pgPreviousTripTwo.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 3:
        return render(request, 'base/pgPreviousTripThree.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 4:
        return render(request, 'base/pgPreviousTripFour.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    

@login_required(login_url='login')
def checklistDelete(request, strItem_id):
    """
    Delete a checklist item.
    
    This function handles the deletion of a checklist item and then re-renders
    the appropriate trip page.
    
    Logic:
    1. Retrieve the ChecklistItem by its ID.
    2. Delete the item.
    3. Determine which trip to display based on the active page in the session.
    4. Retrieve the trip and its associated legs and checklist items.
    5. Render the appropriate page with updated data.

    """
    strItem = ChecklistItem.objects.get(id=strItem_id)
    strItem.delete()
    if request.session["active_page"] == 1:
        dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate').first()
    if request.session["active_page"] > 1:
        dictTripLst = Trip.objects.filter(user=request.user).order_by('-intStartDate')[(request.session["active_page"] - 1)]
    
    # Store the trip's primary key in the session for later reference
    request.session['strTripName_id'] = dictTripLst.pk

    if dictTripLst:
        legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
        checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by("pk")

    if request.session["active_page"] == 1:
        return render(request, 'base/pgPreviousTripOne.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 2:
        return render(request, 'base/pgPreviousTripTwo.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 3:
        return render(request, 'base/pgPreviousTripThree.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
    if request.session["active_page"] == 4:
        return render(request, 'base/pgPreviousTripFour.html', {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})  


@login_required(login_url='login')
def checklistNew(request):
    """
    Create a new checklist item for the current trip with enhanced validation and refactored logic.
    """
    rePg={
        1:'page1',
        2:'page2',
        3:'page3',
        4:'page4'
    }

    # Get the active page or default to 1 if not set
    pgActive = request.session.get("active_page", 1)

    # Validate that the trip ID is in the session
    tripId = request.session.get('strTripName_id')
    if not tripId:
        return redirect(rePg[pgActive])  # Handle this as needed

    try:
        # Retrieve the current trip
        dictTripLst = Trip.objects.get(pk=tripId)
    except Trip.DoesNotExist:
        return redirect('createButton')

    # Validate that the checklist item is provided
    strItem = request.POST.get('strItem')
    if not strItem:
        return redirect(rePg[pgActive])  # Redirect to the appropriate trip page
    lenItem = len(strItem)
    if lenItem > 50:
        return redirect(rePg[pgActive])

    # Create the new checklist item
    ChecklistItem.objects.create(dictTripLst=dictTripLst, title=strItem)

    # Retrieve the updated trip legs and checklist items
    legs = TripLeg.objects.filter(dictTripLst=dictTripLst).order_by('pk')
    checklist = ChecklistItem.objects.filter(dictTripLst=dictTripLst).order_by('pk')

    # Determine which page to render based on the active page in the session
    pgMap = {
        1: 'base/pgPreviousTripOne.html',
        2: 'base/pgPreviousTripTwo.html',
        3: 'base/pgPreviousTripThree.html',
        4: 'base/pgPreviousTripFour.html',
    }

    # Render the appropriate page
    template = pgMap.get(pgActive, 'base/pgPreviousTripOne.html')
    return render(request, template, {'trip': dictTripLst, 'legs': legs, 'checklist': checklist})
