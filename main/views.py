from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages
from main.models import Experience, Project, Expertise
from main.forms import ProjectForm, ExperienceForm
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
import datetime
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        

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
    title_query = request.GET.get("title",  "").strip() 
    experiences = Experience.objects.all()
    
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize(
        "json", experiences,
        fields=["title", "description", "category", "started_at", "ended_at"]
    )
    return HttpResponse(experiences_json, content_type="application/json")

# show
def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [exp.object for exp in experiences]
    title_query = request.GET.get("title", "").strip()
    
    for exp in experience_list:
        exp.edit_form = ExperienceForm(instance=exp)
        
    context = {
        "experience_list": experience_list,
        "title_query": title_query,
        "form": ExperienceForm(),
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


# JSON PROJECT FOR SEARCH FITUR
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize(
        "json", projects, use_natural_foreign_keys=True,
        fields=["title", "image", "github_url", "demo_url", "year", "category"])
    return HttpResponse(projects_json, content_type="application/json")

# untuk list dan search
def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    for p in projects:
        p.edit_form = ProjectForm(instance=p)
        
    context = {
        "name": "Jihan",
        "projects": projects,
        "title_query": title_query,
        "form": ProjectForm(), 
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