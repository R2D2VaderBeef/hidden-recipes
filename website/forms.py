from django import forms
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from website.models import Comment

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
       

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
