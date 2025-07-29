from django.db import models
from .helper import *

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug =  models.SlugField(unique=True)
    order = models.IntegerField()

    def __str__(self):
        return f"{self.title}"

class Article(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('blocked','Blocked'),
        ('deleted','Deteled'),
    )

    title = models.CharField(max_length=255)
    author = models.ForeignKey("users.CustomUser", related_name='articles', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='articles', on_delete=models.CASCADE)
    content = models.TextField()
    status =  models.CharField(max_length=10, choices=STATUS_CHOICE, default="draft")
    order = models.IntegerField()
    image = models.ImageField(upload_to=get_file_path)
    slug = models.SlugField(unique=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    user = models.ForeignKey("users.CustomUser", related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    
    def __str__(self):
            return f"{self.content}"