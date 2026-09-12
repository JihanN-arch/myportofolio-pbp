from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import date

from main.models import Experience, Project, Expertise
# Create your tests here.
class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
            started_at=date(2025, 1, 1),
            
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Jan. 1, 2025")
        self.assertNotContains(response, "Sedang berlangsung")

# ![AI-ATTRIBUTION]: Kode unit test di-generate oleh AI (Claude) dengan penyesuaian assertions dan mock data secara mandiri
class ShowMainViewTest(TestCase):
    def test_show_main_url_accessible(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertEqual(response.status_code, 200)

    def test_show_main_uses_correct_template(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertTemplateUsed(response, 'index.html')

    def test_show_main_displays_profile_data(self):
        response = self.client.get(reverse('main:show_main'))
        self.assertContains(response, "Jihan Nabiilah Permata Sukma")
        self.assertContains(response, "2506549026")


class ShowExperienceViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Software Engineer Intern",
            description="Membangun fitur backend",
            category="internship",
            started_at=date(2025, 1, 1),
        )

    def test_show_experience_url_accessible(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)

    def test_show_experience_uses_correct_template(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertTemplateUsed(response, 'experience.html')

    def test_show_experience_displays_model_data(self):
        response = self.client.get(reverse('main:show_experience'))
        self.assertContains(response, self.experience.title)

    def test_show_experience_empty_state(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse('main:show_experience'))
        self.assertEqual(response.status_code, 200)


class ShowCaseViewTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Skinzym",
            image="/static/img/skinzym.png",
            github_url="https://github.com/JihanN-arch/PKM_2026_FE",
            demo_url="https://pkm-2026-fe.vercel.app/",
            category="web",
            year=2025,
        )
        self.expertise = Expertise.objects.create(
            name="Python",
            icon="devicon-python-plain",
            category="language",
        )

    def test_show_case_url_accessible(self):
        response = self.client.get(reverse('main:show_showcase'))
        self.assertEqual(response.status_code, 200)

    def test_show_case_uses_correct_template(self):
        response = self.client.get(reverse('main:show_showcase'))
        self.assertTemplateUsed(response, 'showcase.html')

    def test_show_case_displays_project_data(self):
        response = self.client.get(reverse('main:show_showcase'))
        self.assertContains(response, self.project.title)

    def test_show_case_displays_expertise_data(self):
        response = self.client.get(reverse('main:show_showcase'))
        self.assertContains(response, self.expertise.name)

    def test_show_case_empty_state(self):
        Project.objects.all().delete()
        Expertise.objects.all().delete()
        response = self.client.get(reverse('main:show_showcase'))
        self.assertContains(response, "Belum ada project yang ditambahkan")
        self.assertContains(response, "Belum ada expertise yang ditambahkan")


class ProjectModelTest(TestCase):
    def test_create_project(self):
        project = Project.objects.create(
            title="Test Project",
            category="mobile",
            year=2026,
        )
        self.assertEqual(str(project), "Test Project")
        self.assertEqual(Project.objects.count(), 1)

    def test_project_optional_fields_can_be_blank(self):
        project = Project.objects.create(title="No Links Project")
        self.assertIsNone(project.image)
        self.assertIsNone(project.github_url)
        self.assertIsNone(project.demo_url)
        self.assertIsNone(project.year)


class ExpertiseModelTest(TestCase):
    def test_create_expertise(self):
        expertise = Expertise.objects.create(
            name="Test Skill",
            icon="devicon-test-plain",
            category="tool",
        )
        self.assertEqual(str(expertise), "Test Skill")
        self.assertEqual(Expertise.objects.count(), 1)

    def test_expertise_default_category(self):
        expertise = Expertise.objects.create(
            name="Default Category Skill",
            icon="devicon-default-plain",
        )
        self.assertEqual(expertise.category, "language")