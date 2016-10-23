from django.shortcuts import render
from .forms import sequence_input

def reverse_complement(text):
    text = text[::-1].upper().replace(' ','')
    reverse_complement_text = text.translate(str.maketrans('ACGT','TGCA'))
    return reverse_complement_text

def test(request):
    if request.method == "POST":
        form1 = sequence_input(request.POST, request.FILES)
        if(request.GET.get('rc-btn')):
            reverse_complement(form1)
        return render(request, 'conversions/rc_output.html')
    else:
        form1 = sequence_input()
    return render (request, 'conversions/conversions_input.html', {'form1': form1})



