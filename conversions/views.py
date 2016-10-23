from django.shortcuts import render
from .forms import sequence_input

def test(request):
    if request.method == "POST":
        form1 = sequence_input(request.POST, request.FILES)
    else:
        form1 = sequence_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1})

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

