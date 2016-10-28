from django.shortcuts import render
#from django import forms
from .forms import user_sequence_input, pattern_input
import re

def reverse_complement(text):
    text = text[::-1]
    reverse_complement_text = text.translate(str.maketrans('ACGTacgt','TGCAtgca'))
    return reverse_complement_text

def mismatch (string1, string2):
    mismatches = 0
    for (nucleotide1, nucleotide2) in zip(string1, string2):
        if nucleotide1 != nucleotide2:
            mismatches += 1
    return(mismatches)

def approximate_patterns(text, pattern, max_mismatches):
    pattern_matches = ''
    pattern_start = 0
    pattern_end = 0
    if pattern == '':
        return ('')
    else:
        for i, base in enumerate(text):
            pattern_matches += '<i></i>'
            query_pattern = text[i:i+len(pattern)]
            if mismatch(pattern, query_pattern) <= max_mismatches:
                pattern_matches += '<sup><b>'
                pattern_start = i
                pattern_end = i + len(pattern)
            if i == pattern_end and pattern_start != 0:
                pattern_matches +='</sup></b>'
                pattern_start = 0
                pattern_end = 0
            pattern_matches += base

        return(pattern_matches)

def test(request):
    if request.method == "POST":
        form1 = user_sequence_input(request.POST)
        form2 = pattern_input(request.POST)
        if form1.is_valid():
            sequence_list = []
            sequence_wrap = ''
            if (request.POST.get('Reverse Complement')):
                sequence = (form1.cleaned_data['sequence'])
                result = reverse_complement(sequence)
                result = str(result)
                sequence_list.append(result)
                print(type(sequence_list[0]))
            if (request.POST.get('Upper Case')):
                if sequence_list:
                    result = sequence_list[0].upper()
                    sequence_list[0] = result
                else:
                    result = (form1.cleaned_data['sequence']).upper()
                    sequence_list.append(result)
            if (request.POST.get('Lower Case')):
                if sequence_list:
                    result = sequence_list[0].lower()
                    sequence_list[0] = result
                else:
                    result = (form1.cleaned_data['sequence']).lower()
                    sequence_list.append(result)
            if (request.POST.get('Remove Spaces')):
                if sequence_list:
                    result = sequence_list[0].replace(" ","")
                    sequence_list[0] = result
                else:
                    result = (form1.cleaned_data['sequence']).replace(" ","")
                    sequence_list.append(result)

            if sequence_list:
                for i, nucleotide in enumerate(sequence_list[0]):
                    sequence_wrap += nucleotide
                    sequence_wrap += '<i></i>'

        if form2.is_valid():
            print('enterform2')
            text = (form1.cleaned_data['sequence'])
            pattern = (form2.cleaned_data['pattern'])
            bold = approximate_patterns(text, pattern, 0)
            #bold = "<b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A"
            #<b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>C<b></b>A<b></b>A<b></b>T<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>C<b></b>C<b></b>T<b></b>G<b></b>A<b></b>T<b></b>C<b></b>G<b></b>C<b></b>T<b></b>A<b></b>C<b></b>A<b></b>G<b></b>T<b></b>T<b></b>G<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>G<b></b>G<b></b>T<b></b>T<b></b>C<b></b>C<b></b>T<b></b>A<b></b>C<b></b>C<b></b>T<b></b>T<b></b>T
            print(bold)

        return render(request, 'conversions/conversions_input.html', {'output': sequence_wrap, 'form1': form1, 'form2': form2, 'output2': bold})
    else:
        form1 = user_sequence_input()
        form2 = pattern_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1, 'form2':form2})



