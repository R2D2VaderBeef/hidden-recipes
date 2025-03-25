from django.contrib import admin

# Register your models here.
from website.models import UserProfile, Tag, Recipe, Comment

admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Comment)