from django.db import models
import uuid

# Create your models here.
class Experience(models.Model):
    EXPERIENCE_CHOICES =[
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField()
    ended_at = models.DateField(blank=True,null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('mobile', 'Mobile'),
        ('web', 'Web'),
        ('desain', 'Desain'),
    ]
    
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=225)
    image = models.CharField(max_length=225, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True) 
    demo_url = models.URLField(blank=True, null=True)
    # year dan category akan digunakan untuk filter dan sort
    year = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    
    def __str__(self):
        return self.title
    
class Expertise(models.Model):
    CATEGORY_CHOICES = [
        ('language', 'Language'),
        ('framework', 'Framework'),
        ('database', 'Database'),
        ('tool', 'Tool'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='language')
    
    def __str__(self):
        return self.name