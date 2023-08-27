from django.db import models


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
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['date']