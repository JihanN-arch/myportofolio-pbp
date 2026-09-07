from django.shortcuts import render


def landing_page(request):
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

    return render(request, "index.html", {
    #! [AI-ATTRIBUTION]: Penggunaan Jinja2 merupakan saran/ide dari AI (Claude)
        "projects": projects,
        "expertise": expertise
    })