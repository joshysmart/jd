from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UpdateUserName, UpdateUserDob, UpdateUserGender, CreateProfileName, CreateProfileGender, CreateProfileDob, SearchSymptom
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

import json
import datetime
from decouple import config
import requests
from django.http import JsonResponse


def get_token():
    endpoint = "https://authservice.priaid.ch/login"

    response = requests.post(endpoint, headers={
        "Authorization": config("AUTHORIZATION")})

    token = response.json()["Token"]
    return token


def get_symptom_ids(user_symptom):
    endpoint = "https://healthservice.priaid.ch/symptoms?token={token}&format=json&language=en-gb"
    token = get_token()

    response = requests.get(endpoint.format(token=token))

    return JsonResponse(response.json(), safe=False)


def get_user_age(user):
    dob = user.dob
    this_year = datetime.date.today().year
    dob_year = dob.year
    age = this_year - dob_year
    return age


def store_response(response_obj):
    diagnosis = []
    response_json = response_obj.json()
    for response in response_json:
        diagnosis.append([
            response["Issue"]["Name"],
            response["Issue"]["ID"],
            response["Issue"]["ProfName"]
        ])
    return diagnosis


def store_diagnosis(response_obj):
    response_json = response_obj.json()
    diagnosis = [
        response_json["Name"],
        response_json["ProfName"],
        response_json["DescriptionShort"],
        response_json["Description"],
        ", ".join(response_json["PossibleSymptoms"].split(",")),
        response_json["TreatmentDescription"]
    ]
    return diagnosis


def start_assessment(request):
    return render(request, "start.html")


def search_symptoms(request, gender):
    pronoun = "him" if gender == "male" else "her"
    you = "you" if gender == "you" else pronoun

    return render(request=request, template_name="search.html", context={"pronoun": you, })


def view_issues(request, id, pronoun):
    endpoint = "https://healthservice.priaid.ch/diagnosis?symptoms={symptoms}&gender={gender}&year_of_birth={age}&token={token}&format=json&language=en-gb"
    current_user = request.user if pronoun == "you" else request.user.profiles.last()
    user_gender = current_user.gender
    user_age = get_user_age(current_user)
    token = get_token()
    symptom_id = [id]

    response = requests.get(endpoint.format(
        symptoms=symptom_id, gender=user_gender, age=user_age, token=token))
    diagnosis = store_response(response)

    return render(request, "issues.html", context={"pronoun": pronoun, "diagnosis": diagnosis})


def view_diagnosis(request, id, pronoun):
    endpoint = "https://healthservice.priaid.ch/issues/{id}/info?token={token}&format=json&language=en-gb"
    token = get_token()
    response = requests.get(endpoint.format(
        id=id, token=token))
    result = store_diagnosis(response)

    current_user = request.user if pronoun == "you" else request.user.profiles.last()
    username = current_user.username
    year = current_user.dob.year
    gender = current_user.gender

    return render(request=request, template_name="diagnosis.html", context={"result": result, "current_user": "{username}, {gender}, {year}".format(username=username, gender=gender, year=year)})


def set_dob(request):
    if request.method == 'POST':
        user_form = UpdateUserDob(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your dob is updated successfully')
            return redirect(to='/assessment/search/you')
    else:
        user_form = UpdateUserDob()

    return render(request=request, template_name="dob.html", context={"dob_form": user_form})


def set_new_user_dob(request):
    if request.method == 'POST':

        last_profile = request.user.profiles.last()
        is_last_profile_completed = False if last_profile is None else last_profile.profile_completed

        if not is_last_profile_completed:
            profile_form = CreateProfileDob(
                request.POST, instance=last_profile)
        else:
            return redirect(to="/assessment/new-user")

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile dob is updated successfully')
            send_to = "/assessment/search/" + profile.gender
            return redirect(to=send_to)
    else:
        profile_form = CreateProfileDob()

    return render(request=request, template_name="new_user_dob.html", context={"dob_form": profile_form})


def set_gender(request):
    if request.method == 'POST':
        user_form = UpdateUserGender(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your dob is updated successfully')
            return redirect(to='/assessment/dob')
    else:
        user_form = UpdateUserGender()

    return render(request=request, template_name="gender.html", context={"gender_form": user_form})


def set_new_user_gender(request):
    if request.method == 'POST':
        last_profile = request.user.profiles.last()
        is_last_profile_completed = False if last_profile is None else last_profile.profile_completed

        if not is_last_profile_completed:
            profile_form = CreateProfileGender(
                request.POST, instance=last_profile)
        else:
            return redirect(to="/assessment/new-user")
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your gender is updated successfully')
            return redirect(to='/assessment/new-user-dob')
    else:
        profile_form = CreateProfileGender()

    return render(request=request, template_name="new_user_gender.html", context={"gender_form": profile_form})


def set_name(request):
    if request.method == 'POST':
        user_form = UpdateUserName(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your name is updated successfully')
            return redirect(to='/assessment/gender')
    else:
        user_form = UpdateUserName()

    return render(request=request, template_name="name.html", context={"name_form": user_form})


def set_new_user_name(request):
    if request.method == "POST":
        last_profile = request.user.profiles.last()
        is_last_profile_completed = False if last_profile is None else last_profile.profile_completed

        if not is_last_profile_completed:
            profile_form = CreateProfileName(
                request.POST, instance=last_profile)
        else:
            profile_form = CreateProfileName(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "New profile name addedd successfully.")
            return redirect("/assessment/new-user-gender")
    profile_form = CreateProfileName()

    return render(request=request, template_name="new_user_name.html", context={"name_form": profile_form})
