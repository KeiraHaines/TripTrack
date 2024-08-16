from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('createtripdate/', views.create_event, name='createtripdate'),
    path('createtriptrans/', views.create_event_trans, name="createtriptrans"),
    path('home/', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logoutUser, name='logout'),
]
