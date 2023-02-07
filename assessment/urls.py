from django.urls import path
from . import views


urlpatterns = [
    path("", views.start_assessment, name="start"),
    path("name/", views.set_name, name="name"),
    path("dob/", views.set_dob, name="dob"),
    path("gender/", views.set_gender, name="gender"),
    path("issues/<id>/<pronoun>", views.view_issues, name="issues"),
    path("search/<gender>", views.search_symptoms, name="search"),
    path("new-user/", views.set_new_user_name, name="new-user"),
    path("new-user-gender/", views.set_new_user_gender, name="new-user-gender"),
    path("new-user-dob/", views.set_new_user_dob, name="new-user-dob"),
    path("diagnosis/<id>/<pronoun>", views.view_diagnosis, name="diagnosis"),
    path("get-symptoms", views.get_symptom_ids, name="get-symptoms")
]
