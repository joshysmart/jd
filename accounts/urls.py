from django.contrib import admin
from django.urls import path

from accounts.views import LoginView
from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', views.signup_request, name='signup'),
    path('logout/', views.logout_request, name='logout')

]
