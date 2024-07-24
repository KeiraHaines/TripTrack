from django.urls import path
from . import views
from.views import CalendarEventView

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('createtripdate/', CalendarEventView, name='createtripdate'),
    path('home/', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logoutUser, name='logout'),
]
