from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='login'),
    path('createtripone/', views.createTripOne, name='createTripOne'),
    path('createtriptwo/', views.createTripTwo, name="createTripTwo"),
    path('createbutton/', views.createButton, name='createButton'),
    path('createuser/', views.createUser, name='createUser'),
    path('logout/', views.logoutUser, name='logout'),
    path('page1/', views.page1, name='page1'),
    path('page2/', views.page2, name='page2'),
    path('page3/', views.page3, name='page3'),
    path('page4/', views.page4, name='page4'),
    path('checklist/', views.index, name='home'),
    path('toggle/<int:item_id>/', views.toggle_completion1, name='toggle1'),
    path('delete/<int:item_id>/', views.delete_item1, name='delete1'),
    path('todo/new/', views.new_todo1, name="todo1"),
    path('docInfo/', views.docInfo, name="docPage"),
    path('prodInfo/', views.prodInfo, name="prodPage"),
    path('baggage-check/', views.baggage_check_view1, name='baggage-check1'),
    # path('baggage-check/', views.baggage_check_view4, name='baggage-check4'), 
]
