from django.contrib import admin

# Register your models here.
from website.models import UserProfile

from website.models import Tag, Recipe
from website.models import UserProfile

admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(UserProfile)
