from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', default="defaults/default_profile.png")
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=512)
    ingredients = models.TextField()
    instructions = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="recipes") 
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    date = models.DateTimeField()

    def __str__(self):
        return self.title
    

class Like(models.Model):
    date = models.DateTimeField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="likes")

class Comment(models.Model):
    date = models.DateTimeField()
    text = models.CharField(max_length=255)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")
