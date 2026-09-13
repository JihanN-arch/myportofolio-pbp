from datetime import date
from main.models import Project, Expertise, Experience

# Project
Project.objects.create(
    title="My Old Portfolio",
    image="/static/img/oldPortf.png",
    github_url="https://github.com/JihanN-arch/PortofolioJN",
    demo_url="https://webpofilejn.netlify.app/",
    category="web",
    year=2025,
)

Project.objects.create(
    title="Arung's Website",
    image="/static/img/arung.png",
    demo_url="https://arung.csui.dev/",
    category="web",
    year=2025,
)

Project.objects.create(
    title="Skinzym",
    image="/static/img/skinzym.png",
    github_url="https://github.com/JihanN-arch/PKM_2026_FE",
    demo_url="https://pkm-2026-fe.vercel.app/",
    category="web",
    year=2025,
)

# Expertise
skills = [
    ("Java", "devicon-java-plain", "language"),
    ("Python", "devicon-python-plain", "language"),
    ("JavaScript", "devicon-javascript-plain", "language"),
    ("HTML5", "devicon-html5-plain", "language"),
    ("CSS3", "devicon-css3-plain", "language"),
    ("Tailwind CSS", "devicon-tailwindcss-plain", "framework"),
    ("Bootstrap", "devicon-bootstrap-plain", "framework"),
    ("React", "devicon-react-original", "framework"),
    ("Flutter", "devicon-flutter-plain", "framework"),
    ("PostgreSQL", "devicon-postgresql-plain", "database"),
]

for name, icon, category in skills:
    Expertise.objects.create(name=name, icon=icon, category=category)

# Experience
Experience.objects.create(
    title="Kontingen Gemastik XIX",
    description="Menjadi salah satu kontingen UI untuk lomba Gemastik XIX dalam bidang software engineer",
    category="research",
    started_at=date(2026, 4, 26),
    ended_at=date(2026, 8, 1),
)

print("Seeding selesai!")