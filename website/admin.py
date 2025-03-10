from django.contrib import admin
from website.models import UserProfile, Tag, Recipe, Like, Comment

admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Like)
admin.site.register(Comment)
