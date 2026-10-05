from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Logistics Staff COMPFEST - 2026",
            description="Served as a member of the logistics division in the COMPFEST organizing committee.",
            category="volunteer",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"'
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Logistics Staff COMPFEST - 2026")
        self.assertEqual(self.experience.category, "volunteer")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"'
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(
            response,
            "Belum ada pengalaman yang ditambahkan."
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        self.assertFalse(self.experience.is_ongoing)

class EducationTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="testsuperuser",
            password="testpassword123",
        )

        self.education = Education.objects.create(
            school="SMA Negeri 82 Jakarta",
            start_year=2022,
            end_year=2025,
            curriculum="Merdeka Curriculum",
            description="Student at SMA Negeri 82 Jakarta.",
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears(self):
        response = self.client.get(
            reverse("main:get_education_json")
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(len(data), 1)

        education = data[0]["fields"]

        self.assertEqual(
            education["school"],
            self.education.school
        )
        self.assertEqual(
            education["start_year"],
            self.education.start_year
        )
        self.assertEqual(
            education["end_year"],
            self.education.end_year
        )
        self.assertEqual(
            education["curriculum"],
            self.education.curriculum
        )
        self.assertEqual(
            education["description"],
            self.education.description
        )

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "No education history has been added yet."
        )

    def test_education_json_endpoint(self):
        response = self.client.get(reverse("main:get_education_json"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        self.assertContains(response, self.education.school)
        self.assertContains(response, self.education.curriculum)
        self.assertContains(response, self.education.description)

    def test_delete_education(self):
        self.client.login(
            username="testsuperuser",
            password="testpassword123",
        )

        response = self.client.post(
            reverse(
                "main:delete_education",
                kwargs={"education_id": self.education.id},
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Education.objects.filter(id=self.education.id).exists()
        )

    def test_create_education(self):
        self.client.login(
            username="testsuperuser",
            password="testpassword123",
        )
        
        response = self.client.post(
            reverse("main:create_education"),
            {
                "school": "Universitas Indonesia",
                "start_year": 2025,
                "end_year": 2029,
                "curriculum": "Kurikulum Pendidikan Tinggi",
                "description": "Computer Science student.",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Education.objects.filter(
                school="Universitas Indonesia"
            ).exists()
        )

    def test_create_education_ajax_requires_superuser(self):
        response = self.client.post(
            reverse("main:create_education_ajax"),
            {
                "school": "Universitas Indonesia",
                "start_year": 2025,
                "end_year": 2029,
                "curriculum": "Kurikulum Pendidikan Tinggi",
                "description": "Computer Science student.",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.json())

    def test_create_education_ajax_validates_and_sanitizes_input(self):
        self.client.login(
            username="testsuperuser",
            password="testpassword123",
        )

        invalid_response = self.client.post(
            reverse("main:create_education_ajax"),
            {
                "school": '<img src="x" onerror="alert(1)">',
                "start_year": 2025,
                "end_year": 2029,
                "curriculum": "Kurikulum Pendidikan Tinggi",
                "description": "Computer Science student.",
            },
        )

        self.assertEqual(invalid_response.status_code, 400)
        self.assertIn("school", invalid_response.json()["errors"])

        valid_response = self.client.post(
            reverse("main:create_education_ajax"),
            {
                "school": "Universitas <b>Indonesia</b>",
                "start_year": 2025,
                "end_year": 2029,
                "curriculum": "Kurikulum <i>Pendidikan Tinggi</i>",
                "description": "Computer <script>alert(1)</script> Science student.",
            },
        )

        self.assertEqual(valid_response.status_code, 201)
        education = Education.objects.get(school="Universitas Indonesia")
        self.assertEqual(education.curriculum, "Kurikulum Pendidikan Tinggi")
        self.assertEqual(education.description, "Computer alert(1) Science student.")

    def test_education_json_includes_star_information(self):
        user = User.objects.create_user(
            username="student",
            password="testpassword123",
        )
        self.education.starred_by.add(user)
        self.client.login(username="student", password="testpassword123")

        response = self.client.get(reverse("main:get_education_json"))
        education = response.json()[0]["fields"]

        self.assertTrue(education["is_authenticated"])
        self.assertTrue(education["is_starred"])
        self.assertEqual(education["star_count"], 1)
        self.assertEqual(education["starred_by_names"], "student")
