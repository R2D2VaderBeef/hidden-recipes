from django import forms

from django.contrib.auth.models import User
from website.models import UserProfile
from website.models import Recipe, Tag

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'picture','bio')


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'tags']