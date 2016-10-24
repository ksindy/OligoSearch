from django import forms
from django.forms import ModelForm
from .models import conversions

class sequence_input(ModelForm):
    class Meta:
        model = conversions
        fields = ('sequence_input',)


class pattern_input(forms.Form):
    pattern = forms.CharField(label='', required=False)
# class pattern_input(ModelForm):
#     class Meta:
#         model = conversions
#         fields = ('pattern_input',)
