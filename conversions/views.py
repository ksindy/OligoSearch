from django.shortcuts import render
#from django import forms
from .forms import sequence_input

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

def test(request):
    form1 = sequence_input(request.POST)
    if request.method == "POST":
        if form1.is_valid():
            sequence_list = []
            if (request.POST.get('Reverse Complement')):
                sequence = (form1.cleaned_data['sequence_input'])
                result = reverse_complement(sequence)
                sequence_list.append(result)
            if (request.POST.get('Upper Case')):
                result = (form1.cleaned_data['sequence_input']).upper()
                sequence_list.append(result)
            if (request.POST.get('Lower Case')):
                result = (form1.cleaned_data['sequence_input']).lower()
                sequence_list.append(result)
            if (request.POST.get('Remove Spaces')):
                result = (form1.cleaned_data['sequence_input']).replace(" ","")
                sequence_list.append(result)

        return render(request, 'conversions/conversions_input.html', {'output': sequence_list, 'form1': form1})
    else:
        form1 = sequence_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1})



