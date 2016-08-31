from django.shortcuts import render

from django.shortcuts import render, redirect
from django import forms

from .forms import NameForm


def name_input(request):

    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():

            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            name = form.save(commit=False)
            name.save()
            return redirect('/contact/thanks/')
    else:
        form = NameForm()

    return render(request, 'contact/home.html', {'form': form})

def thanks(request):
    return render (request, 'contact/name.html')