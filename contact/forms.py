from django import forms
from .models import Name


class NameForm(forms.ModelForm):
    class Meta:
        model = Name
        fields = ('name_text', 'email', 'comments_text',)
        labels = {
            'name_text': ('Name (optional)'),
            'email': ('Email (optional)'),
            'comments_text': ('Comments'),
        }