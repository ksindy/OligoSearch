#from django import forms
from django.forms import ModelForm, Textarea
from .models import conversions

class sequence_input(ModelForm):
    class Meta:
        model = conversions
        fields = ('sequence_input',)
        widgets = {
            'reference':Textarea(attrs={'placeholder': 'Eg. tatattcaccacatgtaaaactttatttatgcataaaaccaccacacacacacaacctacacaaggaatgtgc agtcctgagtctatttagctacatgtgagtatatactccataaggcatataaaaccagtgcacagaaaatgcatccagatattaatatatctacattttaaaactgcatggaaaatacattattatatatacacaaagtgcatacctacccaatgtatggaaaatatattctgtgagttgtgtttatatacatactgtgtgtgtactaaatacattgaaattgcatt'})
        }
        labels = {'reference': ('Enter Reference Sequence')}