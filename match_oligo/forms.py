from django import forms

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
    oligo_column = forms.ChoiceField(choices=OLIGO_COLUMN, required=True)
    name_column = forms.ChoiceField(choices=NAME_COLUMN, required=True)

from .models import ref_model_input

class RefForm(forms.ModelForm):
    class Meta:
        model = ref_model_input
        fields = ('reference',)
        labels = {'reference': ('Enter Reference Sequence:')}

class ChrLocForm(forms.Form):
    chr = forms.CharField(label= "Chromosome Number")
    loc_start = forms.IntegerField(label= "Start Base Location")
    loc_stop = forms.IntegerField(label="Stop Base Location")

