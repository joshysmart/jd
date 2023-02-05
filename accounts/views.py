from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def signup_request(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/home")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = RegisterForm()
    return render(request=request, template_name="registration/signup.html", context={"signup_form": form})


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


def logout_request(request):
    logout(request)
    return redirect("home")
