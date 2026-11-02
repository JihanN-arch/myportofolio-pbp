import datetime
from urllib.parse import urlparse

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Experience, Project
from main.utils import to_direct_img_url


# TUTORIAL 7
class ProjectSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            "id", "title", "image", "github_url", "demo_url", "year",
            "category", "category_display",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
        
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
    
    def get_star_count(self, obj):
        return obj.starred_by.count()
    
    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())