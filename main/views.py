from django.shortcuts import render
from main.models import Experience, Project, Expertise
# Create your views here.

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

def show_experience(request):
    context = {
        "experience_list" : Experience.objects.all(),
    }
    return render(request, "pages/experience.html", context)

def show_showcase(request):    
    context = {
        "projects" : Project.objects.all(),
        "expertise" : Expertise.objects.all()
    }
    
    return render(request, "pages/showcase.html",context)