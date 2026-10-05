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
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


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

    def clean_school(self):
        school = strip_tags(self.cleaned_data["school"]).strip()

        if not school:
            raise ValidationError(
                "Nama sekolah tidak boleh hanya berisi tag HTML."
            )

        return school

    def clean_curriculum(self):
        return strip_tags(self.cleaned_data["curriculum"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

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
        
        
    def clean_title(self):
        title = strip_tags(
            self.cleaned_data["title"]
        ).strip()

        if not title:
            raise ValidationError(
                "Judul experience tidak boleh hanya berisi tag HTML."
            )

        return title

    def clean_description(self):
        return strip_tags(
            self.cleaned_data["description"]
        ).strip()
