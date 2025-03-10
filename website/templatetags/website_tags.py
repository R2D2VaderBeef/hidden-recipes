from django import template
from website.models import UserProfile
from django.conf import settings

register = template.Library()

@register.filter
def find_picture(user):
    try:
        return UserProfile.objects.get(user=user).picture.url
    # In the case of super users without profiles, or old user objects who didn't have their profile picture set
    except:
        return settings.MEDIA_URL + "defaults/default_profile.png"