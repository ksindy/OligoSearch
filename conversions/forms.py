from django import forms
#from django.forms import ModelForm
#from .models import conversions

# class sequence_input(ModelForm):
#     class Meta:
#         model = conversions
#         fields = ('sequence_input',)

class user_sequence_input(forms.Form):
    sequence = forms.CharField(label='', widget=forms.Textarea)


class pattern_input(forms.Form):
    pattern = forms.CharField(label='', required=False)

