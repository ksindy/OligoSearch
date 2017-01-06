from django import forms

class user_sequence_input(forms.Form):
    sequence = forms.CharField(label='', widget=forms.Textarea)

class pattern_input(forms.Form):
    pattern = forms.CharField(label='', required=False)

mismatch_choices = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class mismatch_input(forms.Form):
    mismatches = forms.ChoiceField(choices=mismatch_choices, required=True, label='Number of mismatches allowed:')
