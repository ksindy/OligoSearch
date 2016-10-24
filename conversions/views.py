from django.shortcuts import render
#from django import forms
from .forms import user_sequence_input, pattern_input

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

def test(request):
    form1 = user_sequence_input(request.POST)
    form2 = pattern_input(request.POST)
    if request.method == "POST":
        if form1.is_valid():
            sequence_list = []
            if (request.POST.get('Reverse Complement')):
                sequence = (form1.cleaned_data['sequence'])
                result = reverse_complement(sequence)
                sequence_list.append(result)
            if (request.POST.get('Upper Case')):
                result = (form1.cleaned_data['sequence']).upper()
                sequence_list.append(result)
            if (request.POST.get('Lower Case')):
                result = (form1.cleaned_data['sequence']).lower()
                sequence_list.append(result)
            if (request.POST.get('Remove Spaces')):
                result = (form1.cleaned_data['sequence']).replace(" ","")
                sequence_list.append(result)
        if form2.is_valid():
            print('test')

        return render(request, 'conversions/conversions_input.html', {'output': sequence_list, 'form1': form1})
    else:
        form1 = user_sequence_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1, 'form2':form2})



