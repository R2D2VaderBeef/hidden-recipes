from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    



class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="recipes") 
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes') 
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)

    
    def __str__(self):
        return self.title
