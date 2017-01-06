from django import forms
from django.forms import ModelForm, Textarea

mismatch_choices = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

class mismatch_input(forms.Form):
    mismatches = forms.ChoiceField(choices=mismatch_choices, required=True, label='How many mismatches are allowed?')

class user_sequence_input(forms.Form):
    sequence = forms.CharField(required = False, label='', widget=forms.Textarea(attrs={'placeholder': 'Eg. tatgcataaaa'}))

class UploadFileForm(forms.Form):
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}), label = 'Upload Oligo File(s):')
    #Uses 'multiple' attribute to create a MultiValueDict

OLIGO_COLUMN = (
    (2, 'Default'),
    (0, 'A'),
    (1, 'B'),
    (2, 'C'),
    (3, 'D'),
    (4, 'E'),
    (5, 'F'),
)

NAME_COLUMN = (
    (0, 'Default'),
    (0, 'A'),
    (1, 'B'),
    (2, 'C'),
    (3, 'D'),
    (4, 'E'),
    (5, 'F'),
)
class ColumnDropForm(forms.Form):
    oligo_column = forms.ChoiceField(choices=OLIGO_COLUMN, required=True, label='oligo')
    name_column = forms.ChoiceField(choices=NAME_COLUMN, required=True, label='name')

from .models import ref_model_input

class RefForm(ModelForm):
    class Meta:
        model = ref_model_input
        fields = ('reference',)
        widgets = {
            'reference':Textarea(attrs={'placeholder': 'Eg. tatattcaccacatgtaaaactttatttatgcataaaaccaccacacacacacaacctacacaaggaatgtgc agtcctgagtctatttagctacatgtgagtatatactccataaggcatataaaaccagtgcacagaaaatgcatccagatattaatatatctacattttaaaactgcatggaaaatacattattatatatacacaaagtgcatacctacccaatgtatggaaaatatattctgtgagttgtgtttatatacatactgtgtgtgtactaaatacattgaaattgcatt'})
        }
        labels = {'reference': ('Enter Reference Sequence')}


class ChrLocForm(forms.Form):
    reference = forms.CharField(required= False, label="reference", widget=forms.Textarea(attrs={'placeholder': 'Eg. tatattcaccacatgtaaaactttatttatgcataaaaccaccacacacacacaacctacacaaggaatgtgc agtcctgagtctatttagctacatgtgagtatatactccataaggcatataaaaccagtgcacagaaaatgcatccagatattaatatatctacattttaaaactgcatggaaaatacattattatatatacacaaagtgcatacctacccaatgtatggaaaatatattctgtgagttgtgtttatatacatactgtgtgtgtactaaatacattgaaattgcatt'}))
    chr = forms.CharField(required= False, label="Chromosome", widget=forms.TextInput(attrs={'placeholder': 'Eg. 12'}))
    loc_start = forms.IntegerField(required= False, label= "Start", widget=forms.TextInput(attrs={'placeholder': 'Eg. 54356092'}))
    loc_stop = forms.IntegerField(required= False, label="Stop", widget=forms.TextInput(attrs={'placeholder': 'Eg. 54368740'}))

def clean(self):
    cleaned_data = super(ChrLocForm, self).clean()
    chr = cleaned_data.get("chr")
    loc_start = cleaned_data.get("loc_start")
    loc_stop = cleaned_data.get("loc_stop")
    reference = cleaned_data.get("reference")
    if reference:
        raise forms.ValidationError(
            "Only fill out one reference "
        )
    return cleaned_data, chr, loc_stop, loc_start
