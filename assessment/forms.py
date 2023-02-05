from django import forms
from django.db import models
from django.contrib.auth.models import User

from accounts.models import Profile


class UpdateUserName(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Type in your name'}))

    class Meta:
        model = User
        fields = ['username']


class CreateProfileName(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               label="",
                               widget=forms.TextInput(attrs={'placeholder': 'Type in his/her name'}))

    class Meta:
        model = Profile
        fields = ["username"]


class UpdateUserDob(forms.ModelForm):
    dob = forms.DateField(label="", widget=forms.DateInput(
        attrs={'placeholder': '1 January, !996'}))
    profile_completed = forms.BooleanField(
        initial=True, widget=(forms.HiddenInput), label="")

    class Meta:
        model = User
        fields = ["dob", "profile_completed"]


class CreateProfileDob(forms.ModelForm):
    dob = forms.DateField(label="", widget=forms.DateInput(
        attrs={'placeholder': '1 January, !996'}))
    profile_completed = forms.BooleanField(
        initial=True, widget=(forms.HiddenInput), label="")

    class Meta:
        model = Profile
        fields = ["dob", "profile_completed"]


class UpdateUserGender(forms.ModelForm):
    GENDER = [
        ('female', 'Female'),
        ('male', 'Male'),
    ]

    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=GENDER,
        label=""
    )

    class Meta:
        model = User
        fields = ["gender"]


class CreateProfileGender(forms.ModelForm):
    GENDER = [
        ('female', 'Female'),
        ('male', 'Male'),
    ]

    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=GENDER,
        label=""
    )

    class Meta:
        model = Profile
        fields = ["gender"]


class SearchSymptom(forms.Form):
    symptom = forms.CharField(label='', max_length=255, widget=forms.TextInput(
        attrs={"placeholder": "e.g. headache"}))
