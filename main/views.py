from django.shortcuts import render
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