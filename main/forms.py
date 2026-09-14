from django.forms import ModelForm, TextInput, NumberInput, Textarea
from main.models import Education


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