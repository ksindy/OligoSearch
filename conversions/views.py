from django.shortcuts import render
#from django import forms
from .forms import sequence_input

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

def test(request):
    if (request.POST.get('Upper Case')):
        print('yes')
    if (request.POST.get('Reverse Complement')):
        print('pass if')
        form1 = sequence_input(request.POST)
        if form1.is_valid():
            sequence = (form1.cleaned_data['sequence_input']).upper().replace(" ","")
            rc_result = reverse_complement(sequence)
        return render(request, 'conversions/conversions_input.html', {'rc_output': rc_result, 'form1': form1})
    else:
        form1 = sequence_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1})



