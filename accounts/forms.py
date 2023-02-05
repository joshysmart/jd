from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={"placeholder": "Type in your email address"}))
    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput(attrs={"placeholder": "Set a password"}))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))

    class Meta:
        model = get_user_model()
        fields = ["email", "password1", "password2"]
        help_texts = {
            "username": None
        }

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email',  widget=forms.TextInput(
        attrs={"placeholder": "Type in your email address"}))
    password = forms.CharField(label='Password',  widget=forms.PasswordInput(
        attrs={"placeholder": "Enter your password"}))
