from django import forms
from django.forms import ModelForm, Textarea

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), label = 'Upload Oligo File(s):')
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
    chr = forms.CharField(label= "Chromosome Number", widget=forms.TextInput(attrs={'placeholder': 'Eg. 12'}))
    loc_start = forms.IntegerField(label= "Start Base Location", widget=forms.TextInput(attrs={'placeholder': 'Eg. 54356092'}))
    loc_stop = forms.IntegerField(label="Stop Base Location", widget=forms.TextInput(attrs={'placeholder': 'Eg. 54368740'}))