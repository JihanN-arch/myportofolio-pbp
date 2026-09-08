from django.urls import path

from main.views import show_main, show_experience, show_case

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("showcase/", show_case, name='show_showcase'),
    path("experience/", show_experience, name="show_experience"),
]