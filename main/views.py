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

def show_case(request):
    projects = [
            {
                "title": "My Old Portfolio",
                "img": "/static/img/oldPortf.png",
                "link": "https://webpofilejn.netlify.app/"
            },
            {
                "title": "Arung's Website",
                "img": "/static/img/arung.png",
                "link": "https://arung.csui.dev/"
            },
            {
                "title": "Skinzym",
                "img": "/static/img/skinzym.png",
                "link": "https://pkm-2026-fe.vercel.app/"
            },
        ]
    
    expertise = [
        #! [AI-ATTRIBUTION]: Penggunaan library icon dari Devicon merupakan saran/ide dari AI (Claude)
        {"name": "Java", "icon": "devicon-java-plain"},
        {"name": "Python", "icon": "devicon-python-plain"},
        {"name": "JavaScript", "icon": "devicon-javascript-plain"},
        {"name": "HTML5", "icon": "devicon-html5-plain"},
        {"name": "CSS3", "icon": "devicon-css3-plain"},
        {"name": "Tailwind CSS", "icon": "devicon-tailwindcss-plain"},
        {"name": "Bootstrap", "icon": "devicon-bootstrap-plain"},
        {"name": "React", "icon": "devicon-react-original"},
        {"name": "Flutter", "icon": "devicon-flutter-plain"},
        {"name": "PostgreSQL", "icon": "devicon-postgresql-plain"},
    ]
    
    return render(request, "showcase.html",{
        "projects" : projects,
        "expertise" : expertise,
    })