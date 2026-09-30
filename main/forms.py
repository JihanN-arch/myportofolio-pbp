from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput
from django.utils.html import strip_tags
from urllib.parse import urlparse
from main.models import Project, Experience
import datetime

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
            
            "image": TextInput(
                attrs={
                    "placeholder": "Tautan atau path gambar proyek",
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


    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    # image di model berupa CharField (bukan URLField), jadi kita validasi URL or path
    # dilakukan di sini agar skema berbahaya seperti javascript: ditolak
    def clean_image(self): # nanti bbakal kubuah jadi URL cuma untuk sekarang seperti ini dulu
        image = (self.cleaned_data.get("image") or "").strip()
        if not image:
            return None
        # Path tanpa skema (images/foo.png, /static/foo.png) diizinkan.
        # Yang ditolak hanya skema selain http/https, misalnya javascript:
        scheme = urlparse(image).scheme
        if scheme and scheme not in ("http", "https"):
            raise ValidationError("Gambar harus berupa path file atau URL http(s)://.")
        return image

    # Untuk membersihkan jika user memasukan range yang diluar akal
    def clean_year(self):
        year = self.cleaned_data.get("year")
        current_year = datetime.date.today().year
        if year is not None and not (2000 <= year <= current_year):
            raise ValidationError(f"Tahun harus antara 2000 dan {current_year}.")
        return year
        
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
        
        def clean_title(self):
            title = strip_tags(self.cleaned_data["title"]).strip()
            if not title:
                raise ValidationError("Nama experience tidak boleh hanya berisi tag HTML.")
            return title
    
        def clean_description(self):
            return strip_tags(self.cleaned_data.get("description") or "").strip()
        
        def clean(self):
            cleaned_data = super().clean()
            started_at = cleaned_data.get("started_at")
            ended_at = cleaned_data.get("ended_at")
            if started_at and ended_at and ended_at < started_at:
                self.add_error("ended_at", "Tanggal akhir tidak boleh sebelum tanggal awal.")
            return cleaned_data