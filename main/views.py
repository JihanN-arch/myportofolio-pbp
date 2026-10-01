from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import JsonResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from main.models import Experience, Project, Expertise
from main.forms import ProjectForm, ExperienceForm
from django.utils.formats import date_format
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

# Create your views here.

#* PROFFILE
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name" : "Jihan Nabiilah Permata Sukma",
        "npm" : "2506549026",
        "study_program" : "SI Ilmu Komputer",
        "bio_segments": [
            {"text": "RESISTANT. ", "highlight": False},
            {"text": "CREATIVITY.", "highlight": True},
            {"text": " NOLIFE.", "highlight": False},
        ],
        "last_login": last_login,
    }
    return render(request, "pages/index.html", context)

#* EXPERIENCE
# experience for search
def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        starred_users = experience.starred_by.all()
        data.append({
            "pk": str(experience.pk),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category_display": experience.get_category_display(),
                "is_ongoing": experience.is_ongoing,
                "started_at_display": date_format(experience.started_at),
                "ended_at_display": date_format(experience.ended_at) if experience.ended_at else "",
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and request.user in starred_users,
                "star_url": experience.get_star_url(),
                "star_ajax_url": reverse("main:toggle_star_experience_ajax", args=[experience.pk]),
                "update_url": experience.get_update_url(),
                "delete_url": experience.get_delete_url(),
                "form_values": model_to_dict(experience, fields=ExperienceForm._meta.fields),
            }
        })

    return JsonResponse(data, safe=False)

# show
# list and search dimuat dgn AJAX
def show_experience(request):
    context = {
            "title_query": request.GET.get("title", "").strip(),
            "form": ExperienceForm(),
            "edit_form": ExperienceForm(auto_id="edit_%s"),
            "create_experience_url": reverse("main:create_experience"),
            "is_editor": is_editor(request.user),
        }
    return render(request, "pages/experience.html", context)

# create (superuser only)
@login_required(login_url="/login/")
def create_experience(request):
    if not can_create_or_delete(request.user):
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Experience baru berhasil ditambahkan!")
        else:
            messages.error(request, "Data yang dimasukkan tidak valid.")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

#create dgn AJAX
@require_POST
def create_experience_ajax(request):
    if not can_create_or_delete(request.user):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )
 
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )
 
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

#update
@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not can_update(request.user):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience berhasil diperbarui!")
        else:
            messages.error(request, "Data yang dimasukkan tidak valid.")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

# delete
@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not can_create_or_delete(request.user):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk = experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

#toggle star
@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
            messages.info(request, f"Star pada '{experience.title}' dibatalkan.")
        else:
            experience.starred_by.add(request.user)
            messages.success(request, f"Kamu memberi star pada '{experience.title}'!")
    return redirect("main:show_experience")

@require_POST
def toggle_star_experience_ajax(request, experience_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login terlebih dahulu untuk memberi star."},
            status=401,
        )
 
    experience = get_object_or_404(Experience, pk=experience_id)
 
    if experience.starred_by.filter(pk=request.user.pk).exists():
        experience.starred_by.remove(request.user)
        is_starred = False
        message = f"Star pada '{experience.title}' dibatalkan."
    else:
        experience.starred_by.add(request.user)
        is_starred = True
        message = f"Kamu memberi star pada '{experience.title}'!"
 
    return JsonResponse({
        "is_starred": is_starred,
        "star_count": experience.starred_by.count(),
        "message": message,
    })


#* EXPERTISE
def show_showcase(request):
    context = {
        "expertise" : Expertise.objects.all()
    }

    return render(request, "pages/showcase.html",context)

##* PROJECT
#* ADD PROJECT
@login_required(login_url="/login/")
def create_project(request):
    if not can_create_or_delete(request.user):
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
        else:
            messages.error(request, "Data yang dimasukkan tidak valid.")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


# ADD PROJECT via AJAX (dipanggil dari modal tambah proyek)
# ga pke @login_required karena redirect ke halaman login ga bisa
# dikenali sebagai kegagalan oleh fetch. AnonymousUser.is_superuser bernilai False,
# soo pemeriksaan di bawah ini sudah menolak pengunjung yang belum login.
@require_POST
def create_project_ajax(request):
    if not can_create_or_delete(request.user):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


# JSON PROJECT (dipakai AJAX di halaman project)
# JSON dirakit manual agar bisa menyisipkan data star milik user yang login
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        data.append({
            "pk": str(project.pk),
            "fields": {
                "title": project.title,
                "image": project.image,
                "github_url": project.github_url,
                "demo_url": project.demo_url,
                "year": project.year,
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and request.user in starred_users,
                "star_url": project.get_star_url(),
                "update_url": project.get_update_url(),
                "delete_url": project.get_delete_url(),
                # nilai field ProjectForm, dipakai untuk mengisi edit modal
                "star_url": project.get_star_url(),
                "star_ajax_url": reverse("main:toggle_star_project_ajax", args=[project.pk]),
                "form_values": model_to_dict(project, fields=ProjectForm._meta.fields),
            }
        })

    return JsonResponse(data, safe=False)

# halaman project (list & search dimuat lewat AJAX)
def show_projects(request):
    context = {
        "name": "Jihan",
        "title_query": request.GET.get("title", "").strip(),
        "form": ProjectForm(),
        # auto_id hanya mengubah id input agar tidak bentrok dengan modal tambah
        "edit_form": ProjectForm(auto_id="edit_%s"),
        "create_project_url": reverse("main:create_project"),
        "is_editor": is_editor(request.user),
    }

    return render(request, "pages/project.html", context)

# update
@login_required(login_url="/login/")
def update_project(request, project_id):
    if not can_update(request.user):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project berhasil diperbarui!")
        else:
            messages.error(request, "Data yang dimasukkan tidak valid")

        return redirect("main:show_projects")

    return redirect("main:show_projects")

# Delete project
@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not can_create_or_delete(request.user):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project  berhasil dihapus")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

# STAR
@login_required(login_url="/login/")
def toggle_star_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
            messages.info(request, f"Star pada '{project.title}' dibatalkan.")
        else:
            project.starred_by.add(request.user)
            messages.success(request, f"Kamu memberi star pada '{project.title}'!")
    return redirect("main:show_projects")

@require_POST
def toggle_star_project_ajax(request, project_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Silakan login terlebih dahulu untuk memberi star."},
            status=401,
        )

    project = get_object_or_404(Project, pk=project_id)

    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
        is_starred = False
        message = f"Star pada '{project.title}' dibatalkan."
    else:
        project.starred_by.add(request.user)
        is_starred = True
        message = f"Kamu memberi star pada '{project.title}'!"

    return JsonResponse({
        "is_starred": is_starred,
        "star_count": project.starred_by.count(),
        "message": message,
    })


#* AUTHENTUKASIH
# register
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "form": form,
    }

    return render(request, "pages/register.html", context)

# login
def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect(request.GET.get("next") or "main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "form": form,
    }

    return render(request, "pages/login.html", context)

# logout
def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


#* HELPER ROLE
def is_editor(user):
    if not user.is_authenticated:
        return False
    return user.groups.filter(name="Editor").exists()

def can_update(user):
    return user.is_authenticated and (user.is_superuser or is_editor(user))

def can_create_or_delete(user):
    return user.is_authenticated and user.is_superuser