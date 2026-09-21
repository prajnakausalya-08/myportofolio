from django.urls import path
from main.views import show_main, show_experience, show_education, create_education, edit_education, get_education_json, delete_education, create_experience, edit_experience, delete_experience, get_experience_json

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("education/add/", create_education, name="create_education"),
    path("education/<int:education_id>/edit/", edit_education, name="edit_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/<int:education_id>/delete/", delete_education, name="delete_education"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
]