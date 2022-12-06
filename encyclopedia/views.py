from django.shortcuts import render
from django import forms
from django.http import HttpResponse
import markdown2

from . import util

class SearchForm(forms.Form):
    search_tag = forms.CharField(label ="", max_length = 50,
                                 widget=forms.TextInput(attrs={'placeholder': "Search Encyclopedia"}))

def index(request):
    form = SearchForm()

    if request.method == "POST":
        return search_form(request)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),'form': form })

def page(request, title):

    if not util.get_entry(title) == None:
        form = SearchForm()
        if request.method == "POST":
            return search_form(request)
        return render(request, "encyclopedia/pages.html",
            {'content': markdown2.markdown(util.get_entry(title)), 'form': form})
    else:
        return render(request, "encyclopedia/not_found.html")

def search_form(request):
        form = SearchForm(request.POST)
        if form.is_valid():
            search_tag = form.cleaned_data["search_tag"]
            return render(request, "encyclopedia/pages.html",
                {'content': markdown2.markdown(util.get_entry(search_tag)), 'form': form})
