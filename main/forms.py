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
            "supporting_subjects",
        ]
        labels = {
            "school": "Nama Sekolah",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
            "curriculum": "Kurikulum",
            "supporting_subjects": "Mata Pelajaran Pendukung",
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
            "supporting_subjects": Textarea(
                attrs={
                    "placeholder": "Advanced Mathematics, Physics, Chemistry, and Biology",
                    "rows": 3,
                }
            ),
        }