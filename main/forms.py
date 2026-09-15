from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "image",
            "github_url",
            "demo_url",
            "year",
            "category",
        ]

        labels = {
            "title": "Nama Proyek",
            "image": " URL gambar proyek",
            "github_url": "URL menuju github proyek",
            "demo_url": "URL menuju demo proyek",
            "year": "Tahun proyek dibuat",
            "category" : "Kategori proyek"
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Judul Proyek",
                    "maxlength": 255,
                }
            ),
            "image": URLInput(
                attrs={
                    "placeholder": "!! NTAR KITA UBAH !!",
                }
            ),
            
            "github_url": URLInput(
                attrs={
                    "placeholder": "Tautan Proyek Github",      
                }
            ),
            "demo_url": URLInput(
                attrs={
                    "placeholder": "Tautan Demo Proyek",
                }
            ),
            "year": TextInput(
                attrs={
                    "placeholder": "Tahun Proyek Dibuat",
                    "maxlength" : 5
                }
            ),
            "category" : TextInput(
                attrs={
                    "placeholder" : "Kategori Proyek"
                }
            )   
        }