from django import forms
from .models import ref_model_input

class RefForm(ModelForm):
    class Meta:
        model = ref_model_input
        fields = ('reference',)
        widgets = {
            'reference':Textarea(attrs={'placeholder': 'Eg. tatattcaccacatgtaaaactttatttatgcataaaaccaccacacacacacaacctacacaaggaatgtgc agtcctgagtctatttagctacatgtgagtatatactccataaggcatataaaaccagtgcacagaaaatgcatccagatattaatatatctacattttaaaactgcatggaaaatacattattatatatacacaaagtgcatacctacccaatgtatggaaaatatattctgtgagttgtgtttatatacatactgtgtgtgtactaaatacattgaaattgcatt'})
        }
        labels = {'reference': ('Enter Reference Sequence')}