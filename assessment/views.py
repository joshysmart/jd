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


def get_token():
    endpoint = "https://authservice.priaid.ch/login"

    response = requests.post(endpoint, headers={
        "Authorization": config("AUTHORIZATION")})

    token = response.json()["Token"]
    return token


def get_symptom_ids(user_symptom):
    symptom_ids = []
    with open("symptoms.json") as f:
        lines = f.read()
        symptoms_json = json.loads(lines)
        for symptom_obj in symptoms_json:
            symptom = symptom_obj["Name"].lower()
            if user_symptom in symptom:
                symptom_ids.append(symptom_obj["ID"])
    return symptom_ids


def get_user_age(gender, user):
    profile = user.profiles.last()
    dob = user.dob if gender == "you" else profile.dob
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
    with open("diagnosis.json", "w") as f2:
        f2.write(str(diagnosis))
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


def search_symptoms(request, gender):
    endpoint = "https://healthservice.priaid.ch/diagnosis?symptoms={symptoms}&gender={gender}&year_of_birth={age}&token={token}&format=json&language=en-gb"
    user_gender = request.user.gender if gender == "you" else gender
    token = get_token()

    pronoun = "him" if gender == "male" else "her"
    you = "you" if gender == "you" else pronoun

    if request.method == 'POST':
        form = SearchSymptom(request.POST)
        if form.is_valid():
            user_symptom = form.cleaned_data['symptom'].lower()
            symptom_ids = get_symptom_ids(user_symptom)
            user_age = get_user_age(gender, request.user)
            response = requests.get(endpoint.format(
                symptoms=symptom_ids, gender=user_gender, age=user_age, token=token))
            diagnosis = store_response(response)
            # send_to = "/assessment/search/" + gender
            # return redirect(to=send_to)
            return render(request=request, template_name="search.html", context={"pronoun": you, "search_form": form, "diagnosis": diagnosis})

    else:
        form = SearchSymptom()
    return render(request=request, template_name="search.html", context={"pronoun": you, "search_form": form})


def view_symptoms(request):
    return render(request, "symptoms.html")


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
            profile_form = CreateProfileDob(request.POST)

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
            profile_form = CreateProfileGender(request.POST)
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
