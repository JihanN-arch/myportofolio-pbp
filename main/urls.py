from django.urls import path

from main.views import (show_main, show_experience, show_showcase, 
                        create_project, show_projects, delete_project, get_projects_json)

app_name = "main"

urlpatterns = [
    # main
    path("", show_main, name="show_main"),
    
    # expertise
    path("showcase/", show_showcase, name='show_showcase'),
    
    # experience
    path("experience/", show_experience, name="show_experience"),
    
    # project
    path('projects/', show_projects, name='show_projects'),
    path('projects/add/', create_project, name="create_project"),
    path('projects/json/', get_projects_json, name='get_project_json'),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
]