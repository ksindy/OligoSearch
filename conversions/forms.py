from django import forms

class user_sequence_input(forms.Form):
    sequence = forms.CharField(label='', widget=forms.Textarea)

class pattern_input(forms.Form):
    pattern = forms.CharField(label='', required=False)


