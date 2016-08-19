from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), label = 'Upload Oligo File(s):')
    #Uses 'multiple' attribute to create a MultiValueDict

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