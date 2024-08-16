from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import newTrip, Destination, Transport, Leg
from .forms import EventFormTrans

@login_required(login_url='login')
def create_event_trans(request):
    """
    View to handle the creation of a new leg for an existing trip.

    This view handles both GET and POST requests:
    - For GET requests, it initializes a blank form and retrieves existing legs for the trip.
    - For POST requests, it processes the data submitted by the user to create a new leg 
      with a specified destination and transport method.

    The user must be logged in to access this view. If the user is not logged in, 
    they will be redirected to the login page specified by 'login_url'.
    """

    # Retrieve the current trip using the primary key stored in the session
    trip = newTrip.objects.get(pk=request.session['strTripName_id'])

    # Retrieve all legs associated with the current trip
    legs = Leg.objects.filter(trip=trip)

    if request.method == 'POST':

        # Retrieve the selected destination and list of transport methods from the form
        location = request.POST.get('destination')
        transport_list = request.POST.getlist('transport')

        # Remove any empty values from the transport list
        transport_list = [t for t in transport_list if t]

        # Select the first non-empty transport method from the list, if any
        transport = transport_list[0] if transport_list else None
        print("transport::", transport)
        
        # Retrieve the selected transport method from the database
        selected_transport = Transport.objects.get(pk=transport)
        # (Optional) Uncomment the line below to associate the transport with an event
        # event.transport.add(selected_transport)

        try:
            # Try to retrieve the selected destination from the database
            selected_location = Destination.objects.get(name=location)
            # (Optional) Uncomment the line below to associate the destination with an event
            # event.destination.add(selected_location)
        except Exception as e:
            # If the destination doesn't exist, create a new one
            print("no destination in database")
            selected_location = Destination.objects.create(name=location)
            # (Optional) Uncomment the line below to associate the new destination with an event
            # event.destination.add(new_location)
        
        # Create a new leg for the trip with the selected destination and transport
        new_leg = Leg.objects.create(trip=trip, destination=selected_location, transport=selected_transport)
        print("new_leg:: ", new_leg)
        
        # Redirect the user back to the 'createtriptrans' view after the leg is created
        return redirect('createtriptrans')
    
    else:
        # If the request method is GET, initialize a blank form
        form = EventFormTrans()