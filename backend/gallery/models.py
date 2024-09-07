from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    # To create simple user, use the following command:
    # python manage.py createuser
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        
        # hash the password
        user.set_password(password)
        user.save()
        
        return user
    
    # python manage.py createsuperuser
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def get_full_name(self):
        return self.name
    
    def __str__(self):
        return self.email


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
    liked_by_users = models.ManyToManyField(UserAccount, related_name='liked_images')
    comments = models.ManyToManyField(UserAccount, through='Comment', related_name='commented_images')
    
    def __str__(self):
        return self.title
    
    def update_likes(self):
        self.image_likes_count = self.liked_by_users.count()
        self.save()
    
    class Meta:
        ordering = ['-date']
        
        
class Comment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Comment by {self.user.email} on {self.gallery.title}'
