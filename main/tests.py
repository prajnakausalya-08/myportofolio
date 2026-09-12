from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
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
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Volunteer")
        self.assertContains(response, "Ongoing")
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
        response = self.client.get(reverse("main:show_experience"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

class EducationTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            school="SMA Negeri 82 Jakarta",
            start_year=2022,
            end_year=2025,
            curriculum="Merdeka Curriculum",
            supporting_subjects="Advanced Mathematics, Physics, Chemistry, and Biology",
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, self.education.school)
        self.assertContains(response, str(self.education.start_year))
        self.assertContains(response, str(self.education.end_year))
        self.assertContains(response, self.education.curriculum)
        self.assertContains(response, self.education.supporting_subjects)

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "No education history has been added yet."
        )