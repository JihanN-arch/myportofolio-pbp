from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.http import HttpResponse
from django.contrib import messages
from main.models import Experience, Project, Expertise
from main.forms import ProjectForm, ExperienceForm
from django.conf import settings
from django.urls import reverse

# Create your views here.

#* PROFFILE
def show_main(request):
    context = {
        "name" : "Jihan Nabiilah Permata Sukma",
        "npm" : "2506549026",
        "study_program" : "SI Ilmu Komputer",
        "bio_segments": [
            {"text": "RESISTANT. ", "highlight": False},
            {"text": "CREATIVITY.", "highlight": True},
            {"text": " NOLIFE.", "highlight": False},
        ],
    }
    return render(request, "pages/index.html", context)

#* EXPERIENCE
# experience for search
def get_experiences_json(request):
    title_query = request.GET.get("title",  "").strip() 
    experiences = Experience.objects.all()
    
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
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
        "create_experience_url": reverse("main:create_experience")
    }
    return render(request, "pages/experience.html", context)
    
# create
def create_experience(request):
    form = ExperienceForm(request.POST or None)
    
    if request.method == "POST" :
        secret_code = request.POST.get("secret_code", "")
    
        if secret_code != settings.PORTFOLIO_SECRET_CODE:
            messages.error(request, "Kode rahasia salah! Kamu tidak diizinkan menambah proyek.")
        elif form.is_valid(): 
            form.save()
            messages.success(request, "Experience baru berhasil ditambahakan!")
        return redirect("main:show_experience")
        
    context = {
        "name" : "Jihan",
        "form" : form,
    }
    
    return render(request, "pages/experienceForm.html", context)

#update
def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    
    if request.method == "POST":
        secret_code = request.POST.get("secret_code", "")
        form = ExperienceForm(request.POST, instance=experience)
        
        if secret_code != settings.PORTFOLIO_SECRET_CODE:
            messages.error(request, "Kode rahasia salah! Kamu tidak diizinkan mengubah experience.")
        elif form.is_valid():
            form.save()
            messages.success(request, "Experience berhasil diperbarui!")
        else:
            messages.error(request, "Data yang dimasukkan tidak valid")
        
        return redirect("main:show_experience")
    
    return redirect("main:show_experience")

# delete
def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk = experience_id)
    
    if request.method == "POST":
        secret_code = request.POST.get("secret_code", "")
        
        if secret_code != settings.PORTFOLIO_SECRET_CODE:
            messages.error(request, "Kode rahasia salah! Kamu tidak diizinkan menghapus experience.")
        else:
            experience.delete()
            messages.success(request, "Experience berhasil dihapus!")
            
        return redirect("main:show_experience")
     
    return redirect("main:show_experience")
            
            
#* EXPERTISE
def show_showcase(request):    
    context = {
        "expertise" : Expertise.objects.all()
    }
    
    return render(request, "pages/showcase.html",context)

##* PROJECT 
#* ADD PROJECT 
def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST":
        secret_code = request.POST.get("secret_code", "")

        if secret_code != settings.PORTFOLIO_SECRET_CODE:
            messages.error(request, "Kode rahasia salah! Kamu tidak diizinkan menambah proyek.")
        elif form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

# JSON PROJECT FOR SEARCH FITUR
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
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

    context = {
        "name": "Jihan",
        "projects": projects,
        "title_query": title_query,
        "form": ProjectForm(), 
        "create_project_url": reverse("main:create_project")
    }
    return render(request, "pages/project.html", context)

# Delete project
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        secret_code = request.POST.get("secret_code", "")

        if secret_code != settings.PORTFOLIO_SECRET_CODE:
            messages.error(request, "Kode rahasia salah! Kamu tidak diizinkan menghapus proyek.")
        else:
            project.delete()
            messages.success(request, "Project berhasil dihapus!")

        return redirect("main:show_projects")

    return redirect("main:show_projects")