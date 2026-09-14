from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect, render

from main.forms import EducationForm
from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "Prajna Kausalya Damdami",
        "npm": "2506657213",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science Student who deeply interested in "
            "technology, programming, design, and arts with high creativity. "
            "Lately focused on studying in CS Universitas Indonesia."
        ),
    }

    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Prajna Kausalya Damdami",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Prajna Kausalya Damdami",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Prajna Kausalya Damdami",
        "form": form,
    }

    return render(request, "education_form.html", context)

def get_education_json(request):
    educations = Education.objects.all()
    education_json = serializers.serialize("json", educations)
    return HttpResponse(
        education_json,
        content_type="application/json",
    )