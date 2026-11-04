import uuid
import datetime

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Project

# Test API untuk Project (Tutorial 07), disesuaikan dengan field model Project:
# title, image, github_url, demo_url, year, category.

#! AI Attribution:
#! Penulisan test experience dan penambahan unit test pada file ini dibantu oleh Claude AI.
class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(title="Portfolio", year=2025, category="web")
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "image": "", "github_url": "https://github.com/x/y",
            "demo_url": "https://example.com/", "year": 2024, "category": "mobile",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"github_url": "javascript:alert(1)"}, "github_url"),
            ({"image": "javascript:alert(1)"}, "image"),
            ({"year": 1990}, "year"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.year, 2025)
        # Di model ini cuma title yang wajib, jadi PUT tanpa title yang harus gagal.
        response = self.client.put(self.detail_url, {"year": 2024}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_google_drive_link_is_converted(self):
        self.client.force_authenticate(user=self.owner)
        payload = {**self.payload, "image": "https://drive.google.com/file/d/1AbC-xyz_9/view?usp=sharing"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["image"], "https://lh3.googleusercontent.com/d/1AbC-xyz_9")

    def test_editor_can_update_but_not_create_or_delete(self):
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)

    def test_staff_without_editor_group_cannot_update(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_query_count_does_not_grow_with_data(self):
        """Daftar Project tetap 2 query berkat prefetch_related("starred_by"), berapa pun jumlahnya."""
        for i in range(20):
            project = Project.objects.create(title=f"Project {i}", year=2025)
            project.starred_by.add(self.owner, self.visitor)
        self.client.force_authenticate(user=self.visitor)
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 21)

# TEST EXPERIENCE
class ExperienceAPITest(APITestCase):
    """Test API Experience untuk keempat peran: pengunjung, pengguna biasa, Editor, dan pemilik."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        # Database pengujian selalu kosong, jadi grup Editor dibuat di sini
        self.editor.groups.add(Group.objects.create(name="Editor"))

        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa",
            category="part-time",
            started_at=datetime.date(2026, 8, 1),
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Magang Backend",
            "description": "Membangun API",
            "category": "internship",
            "started_at": "2026-01-01",
            "ended_at": "2026-03-01",
        }

    # --- Membaca (semua peran) ---
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertEqual(response.data[0]["category_display"], "Part-Time")
        self.assertTrue(response.data[0]["is_ongoing"])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "asisten"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "tidak-ada"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    # --- Pengunjung dan pengguna biasa ---
    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Diubah"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        # Cek isi database, bukan hanya status HTTP
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP")

    # --- Editor ---
    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Asdos PBP 2026"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asdos PBP 2026")
        self.assertEqual(self.experience.description, "Membantu mahasiswa")  # field lain tidak berubah

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Magang Backend")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    # --- Pemilik ---
    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    # --- Validasi ---
    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": "<b></b>"}, "title"),
            ({"category": "bukan-kategori"}, "category"),
            ({"started_at": "2026-05-01", "ended_at": "2026-01-01"}, "ended_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_html_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload,
            "title": "<b>Magang</b>",
            "description": "<script>alert(1)</script>Membangun API",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Magang")
        self.assertNotIn("<script>", created.description)

    def test_patch_end_date_checked_against_saved_start_date(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"ended_at": "2026-01-01"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", response.data)
        self.experience.refresh_from_db()
        self.assertIsNone(self.experience.ended_at)

    # --- Star ---
    def test_star_requires_login(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_star_toggles_for_request_user(self):
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(self.experience.starred_by.filter(pk=self.visitor.pk).exists())

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_star_cannot_be_given_on_behalf_of_another_user(self):
        self.client.force_authenticate(user=self.visitor)
        self.client.post(self.star_url, {"user": self.owner.pk, "starred_by": [self.owner.pk]}, format="json")
        self.assertTrue(self.experience.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertFalse(self.experience.starred_by.filter(pk=self.owner.pk).exists())

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True, "is_ongoing": True,
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertFalse(response.data["is_ongoing"])  # ended_at diisi, jadi tidak ongoing

    def test_no_sensitive_user_data_in_response(self):
        self.experience.starred_by.add(self.owner)
        response = self.client.get(self.detail_url)
        self.assertNotIn("owner@example.com", str(response.data))
        self.assertNotIn("password", str(response.data))

    # --- Method dan CSRF ---
    def test_wrong_method(self):
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        response = client.patch(self.detail_url, {"title": "Tanpa CSRF"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP")

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="editor", password="test-password")
        client.get(self.list_url, HTTP_ACCEPT="text/html")  # Browsable API memasang cookie csrftoken
        token = client.cookies["csrftoken"].value
        response = client.patch(
            self.detail_url, {"title": "Dengan CSRF"}, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
            # --- Efisiensi query ---
    def test_list_query_count_does_not_grow_with_data(self):
        """
        prefetch_related("starred_by") membuat jumlah query daftar tetap 2
        (1 untuk experience, 1 untuk semua relasi star), berapa pun jumlah datanya.
        Tanpa prefetch, setiap kartu akan menambah query sendiri (masalah N+1).
        """
        for i in range(20):
            experience = Experience.objects.create(title=f"Exp {i}", started_at=datetime.date(2026, 1, 1))
            experience.starred_by.add(self.visitor, self.editor)
        self.client.force_authenticate(user=self.visitor)
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
        self.assertEqual(len(response.data), 21)