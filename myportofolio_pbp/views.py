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

    return render(request, "index.html", {
        "projects": projects
    })