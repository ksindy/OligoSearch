from django.shortcuts import render

def test(request):
    return render (request, 'contact/name.html')

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

