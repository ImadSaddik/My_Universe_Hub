from django.db import models
from django.contrib.auth.models import User


class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Gallery(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    explanation = models.TextField()
    image_url = models.CharField(max_length=150)
    image_is_liked = models.BooleanField(default=False)
    image_likes_count = models.IntegerField(default=0)
    keywords = models.ManyToManyField(Keyword)
    liked_by_users = models.ManyToManyField(User, related_name='liked_images')
    
    def __str__(self):
        return self.title
    
    def update_likes(self):
        self.image_likes_count = self.liked_by_users.count()
        self.save()
    
    class Meta:
        ordering = ['-date']