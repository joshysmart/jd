from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.expressions import fields


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={"placeholder": "Type in your email address"}))
    password1 = forms.CharField(label='Enter password',
                                widget=forms.PasswordInput(attrs={"placeholder": "Set a password"}))
    password2 = forms.CharField(label='Confirm password',
                                widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        help_texts = {
            "username": None
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
