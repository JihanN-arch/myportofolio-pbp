from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput

from main.models import Project, Experience

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
            "category": Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }
        
class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "started_at",
            "ended_at"
        ]
        
        labels = {
            "title": "Nama experience",
            "description": "Deskripsi experience",
            "category": "Kategori experience",
            "started_at": "Awal experience",
            "ended_at": "Akhir experience"
        }
        
        widgets = {
            "title" : TextInput(
                attrs={
                    "placeholder" : "Judul experience",
                    "maxlength" : 225,
                }
            ),
            "description" : Textarea(
                attrs={
                    "placeholder" : "Deskripsi experience",
                    "rows" : 5,
                    "maxlength" : 1000,
                }
            ),   
            "category": Select(
                attrs={
                    "class": "form-select"
                }
            ),
            "started_at" : DateInput(
                attrs={
                    "type" : "date"
                }
            ),
            "ended_at" : DateInput(
                attrs={
                    "type" : "date"
                }
            )
        }