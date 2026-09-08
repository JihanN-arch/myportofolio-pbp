from django.shortcuts import render
from main.models import Experience
# Create your views here.

def show_main(request):
    context = {
        "name" : "Jihan Nabiilah Permata Sukma",
        "npm" : "2506549026",
        "study_program" : "SI Ilmu Komputer",
        "bio" : (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang berusaha "
            "survive dan bahagia dalam menjalani pendidikan"
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name" : "Jihan",
        "experience_list" : Experience.objects.all(),
    }
    return render(request, "experience.html", context)