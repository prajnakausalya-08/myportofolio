from django.forms import (
    ModelForm,
    TextInput,
    NumberInput,
    Textarea,
    Select,
    URLInput,
    DateTimeInput,
)

from main.models import Education, Experience


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "school",
            "start_year",
            "end_year",
            "curriculum",
            "description",
        ]
        labels = {
            "school": "Nama Sekolah",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
            "curriculum": "Kurikulum",
            "description": "Deskripsi",
        }
        widgets = {
            "school": TextInput(
                attrs={
                    "placeholder": "Nama institusi",
                    "maxlength": 255,
                }
            ),
            "start_year": NumberInput(
                attrs={
                    "placeholder": "Masukkan tahun mulai",
                }
            ),
            "end_year": NumberInput(
                attrs={
                    "placeholder": "Masukkan tahun selesai",
                }
            ),
            "curriculum": TextInput(
                attrs={
                    "placeholder": "Jenis kurikulum",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsikan pendidikanmu",
                    "rows": 3,
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Judul pengalaman",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Deskripsikan pengalamanmu",
                    "rows": 4,
                }
            ),
            "category": Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/image.jpg",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }