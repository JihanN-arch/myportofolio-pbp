from django.urls import path

from main.views import (show_main, show_showcase, 
                        create_project, show_projects, delete_project, get_projects_json,
                         show_experience, create_experience)

app_name = "main"

urlpatterns = [
    # main
    path("", show_main, name="show_main"),
    
    # expertise
    path("showcase/", show_showcase, name='show_showcase'),
    
    # experience
    path("experience/", show_experience, name="show_experience"),
    path('experience/add', create_experience, name='create_Experience'),
    
    # project
    path('projects/', show_projects, name='show_projects'),
    path('projects/add/', create_project, name="create_project"),
    path('projects/json/', get_projects_json, name='get_project_json'),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
]