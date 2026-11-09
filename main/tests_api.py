from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Education


class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="test-password")
        self.user = User.objects.create_user(username="student", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.education = Education.objects.create(
            school="Universitas Indonesia", start_year=2025, end_year=2029,
            curriculum="Computer Science", description="Student",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.pk])
        self.star_url = reverse("api:education-star", args=[self.education.pk])
        self.payload = {"school": "SMA", "start_year": 2022, "end_year": 2025,
                        "curriculum": "Merdeka", "description": "Student"}

    def test_public_list_detail_search_and_missing(self):
        response = self.client.get(self.list_url, {"school": "INDONESIA"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], self.education.pk)
        self.assertNotIn("fields", response.data[0])
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(self.client.get(self.list_url, {"school": "missing"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        self.assertEqual(self.client.get(reverse("api:education-detail", args=[999999])).status_code, 404)

    def test_guest_and_user_cannot_manage(self):
        for user in (None, self.user):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"school": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.education.refresh_from_db()
        self.assertEqual(self.education.school, "Universitas Indonesia")

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.patch(self.detail_url, {"school": "Updated"}, format="json").status_code, 200)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)

    def test_owner_crud_and_validation(self):
        self.client.force_authenticate(user=self.owner)
        for school in ("   ", '<img src="x">'):
            response = self.client.post(self.list_url, {**self.payload, "school": school}, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn("school", response.data)
        response = self.client.post(self.list_url, {**self.payload, "school": "SMA <b>Indonesia</b>",
                                                   "star_count": 99, "starred_by": [self.user.pk]}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["school"], "SMA Indonesia")
        self.assertEqual(response.data["star_count"], 0)
        self.assertEqual(self.client.patch(self.detail_url, {"school": "Changed"}, format="json").status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.description, "Student")
        self.assertEqual(self.client.put(self.detail_url, {"school": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=self.education.pk).exists())
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], "student")
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_session_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.get(self.list_url, HTTP_ACCEPT="text/html").status_code, 200)
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.list_url, self.payload, format="json",
                                     HTTP_X_CSRFTOKEN=token).status_code, 201)

    def test_id_and_all_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "id": 999999, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.user.pk],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], 999999)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        self.assertFalse(Education.objects.get(pk=response.data["id"]).starred_by.exists())

    def test_staff_without_editor_cannot_manage(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        for response in (self.client.post(self.list_url, self.payload, format="json"),
                         self.client.patch(self.detail_url, {"school": "Changed"}, format="json"),
                         self.client.delete(self.detail_url)):
            self.assertEqual(response.status_code, 403)

    def test_read_does_not_reveal_sensitive_user_data(self):
        self.education.starred_by.add(self.user)
        data = self.client.get(self.detail_url).data
        self.assertEqual(data["starred_by_names"], "student")
        self.assertNotIn("password", data)
        self.assertNotIn("email", data)
        self.assertNotIn("starred_by", data)

    def test_post_validates_required_fields_and_integer_years(self):
        self.client.force_authenticate(user=self.owner)
        for payload, field in (({**self.payload, "start_year": "abc"}, "start_year"),
                               ({**self.payload, "end_year": ""}, "end_year"),
                               ({**self.payload, "school": ""}, "school")):
            response = self.client.post(self.list_url, payload, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn(field, response.data)
        self.assertEqual(Education.objects.count(), 1)

    def test_patch_strips_tags_and_keeps_other_fields(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"school": "<b>Updated</b>",
                                                     "description": "<i>Text</i>"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.school, "Updated")
        self.assertEqual(self.education.description, "Text")
        self.assertEqual(self.education.start_year, 2025)

    def test_wrong_methods_and_missing_star(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        missing = reverse("api:education-star", args=[999999])
        self.assertEqual(self.client.post(missing).status_code, 404)

    def test_session_patch_and_delete_require_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        self.assertEqual(client.patch(self.detail_url, {"school": "Changed"}, format="json").status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        page = client.get(reverse("main:show_education"))
        self.assertEqual(page.status_code, 200)
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.patch(self.detail_url, {"school": "Changed"}, format="json",
                                      HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.delete(self.detail_url, HTTP_X_CSRFTOKEN=token).status_code, 204)

    def test_session_star_requires_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="student", password="test-password")
        self.assertEqual(client.post(self.star_url).status_code, 403)
        client.get(reverse("main:show_education"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)

    def test_education_page_and_edit_keep_server_side_access_control(self):
        self.assertEqual(self.client.get(reverse("main:show_education")).status_code, 200)
        edit_url = reverse("main:edit_education", args=[self.education.pk])
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(edit_url).status_code, 403)
        self.client.force_login(self.editor)
        page = self.client.get(edit_url)
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, self.detail_url)
        self.assertContains(page, 'method: "PATCH"')
