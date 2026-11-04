import datetime
from urllib.parse import urlparse

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project
from main.utils import to_direct_img_url


# STAR SERIALIZER
class StarFieldsMixin(serializers.Serializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    
    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        """True jika akun yang sedang login sudah memberi star. Butuh context["request"]."""
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()
    
    def get_starred_by_names(self, obj):
        """Username pemberi star (tanpa email atau data akun lain)."""
        return ", ".join(user.username for user in obj.starred_by.all())

# TUTORIAL 7
# PROJECT
class ProjectSerializer(StarFieldsMixin, serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    
    class Meta:
        model = Project
        fields = [
            "id", "title", "image", "github_url", "demo_url", "year",
            "category", "category_display",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
        
        extra_kwargs = {
            "title": {"error_messages": {"blank": "Nama proyek tidak boleh kosong."}},
            "year": {"error_messages": {"invalid": "Tahun harus berupa angka."}},
        }
        
    def validate_title(self, value):
        value = strip_tags(value).strip()
        
        if not value:
            raise serializers.ValidationError("Nama proyek tidak boleh kosong atau hanya berisi tag HTML")
        return value
    
    def validate_image(self, value):
        value = (value or "").strip()
        
        if not value:
            return None
        
        scheme = urlparse(value).scheme
        if scheme and scheme not in ("http", "https"):
            raise serializers.ValidationError("Gambar harus berupa path file atau URL http(s)://.") 
        return to_direct_img_url(value)
    
    def validate_year(self, value):
        current_year = datetime.date.today().year
        if value is not None and not (2000 <= value <= current_year):
            raise serializers.ValidationError(f"Tahun harus antara 2000 dan {current_year}.")
        return value

    

# EXPERIENCE
class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    # id, title, description, category, starred_at, endded_at, starred_by
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True) 
    class Meta:
        model = Experience
        
        fields = [
            "id", "title", "description", "category", "category_display",
            "started_at", "ended_at", "is_ongoing", "star_count", "is_starred",  "starred_by_names",
        ]
        
        read_only_fields = [
            "id"
        ]
        
        extra_kwargs = {
            "title": {"error_messages": {"blank": "Nama experience tidak boleh kosong."}},
            "started_at": {"error_messages": {"invalid": "Format tanggal mulai tidak valid."}},
        }
        
        
    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama experience tidak boleh kosong.")
        return value

    def validate_description(self, value):
        return strip_tags(value or "").strip()
    
    def validate(self, attrs):
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        
        if started and ended and ended < started:
            raise serializers.ValidationError(
                {"ended_at" : "Tanggal akhir tidak boleh sebelum tanggal mulai"}
            )   
            
        return attrs 
