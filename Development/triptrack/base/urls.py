from django.urls import path
from . import views

urlpatterns = [
    # User authentication
    path('', views.loginUser, name='login'),  # Login page (root URL)
    path('logout/', views.logoutUser, name='logout'),  # Logout functionality
    path('createuser/', views.createUser, name='createUser'),  # User registration page

    # Trip creation process
    path('createtripone/', views.createTripOne, name='createTripOne'),  # First step of trip creation
    path('createtriptwo/', views.createTripTwo, name="createTripTwo"),  # Second step of trip creation
    path('createbutton/', views.createButton, name='createButton'),  # Possibly a helper view for trip creation

    # Trip viewing pages
    path('page1/', views.createdTripOne, name='page1'),  # View first part of created trip
    path('page2/', views.createdTripTwo, name='page2'),  # View second part of created trip
    path('page3/', views.createdTripThree, name='page3'),  # View third part of created trip
    path('page4/', views.createdTripFour, name='page4'),  # View fourth part of created trip

    # Checklist functionality
    path('toggle/<int:strItem_id>/', views.checklistCheck, name='toggle1'),  # Toggle checklist item status
    path('delete/<int:strItem_id>/', views.checklistDelete, name='delete1'),  # Delete checklist item
    path('todo/new/', views.checklistNew, name="todo1"),  # Add new checklist item

    # Information pages
    path('docInfo/', views.docInfo, name="docPage"),  # Document information page
    path('prodInfo/', views.prodInfo, name="prodPage"),  # Product information page

    # Luggage weight check
    path('baggage-check/', views.luggageWeight, name='baggage-check1'),  # Check luggage weight
]