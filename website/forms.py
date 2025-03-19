from django import forms
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from website.models import UserProfile
from website.models import Recipe, Tag

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("email", "username", "password",)
        help_texts = {
            'username': _('Letters, digits and @/./+/-/_ only.'),
        }
        error_messages = {
            'username': {
                'unique': _("That username is already taken. Please choose another username."),
            },
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture','bio')


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Recipe
<<<<<<< HEAD
        fields = ['title', 'description', 'picture', 'ingredients', 'instructions', 'tags']
=======
        fields = ['title', 'description', 'picture', 'ingredients', 'instructions', 'tags']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
>>>>>>> 8fd4916 (allowed comment deletion)
