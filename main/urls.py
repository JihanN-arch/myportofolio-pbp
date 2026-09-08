from django.urls import path

from main.views import show_main, show_experience, show_showcase

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("showcase/", show_showcase, name='show_showcase'),
    path("experience/", show_experience, name="show_experience"),
]