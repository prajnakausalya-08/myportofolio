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
                    "placeholder": "SMA Negeri 82 Jakarta",
                    "maxlength": 255,
                }
            ),
            "start_year": NumberInput(
                attrs={
                    "placeholder": "2022",
                }
            ),
            "end_year": NumberInput(
                attrs={
                    "placeholder": "2025",
                }
            ),
            "curriculum": TextInput(
                attrs={
                    "placeholder": "Merdeka Curriculum",
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