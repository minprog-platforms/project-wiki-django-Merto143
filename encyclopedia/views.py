from django.shortcuts import render
from django import forms
from django.http import HttpResponse
import markdown2
import random

from . import util

class SearchForm(forms.Form):
    search_tag = forms.CharField(label ="", max_length = 50,
                                 widget=forms.TextInput(attrs={'placeholder': "Search Encyclopedia"}))


class New_pageForm(forms.Form):
    input = forms.CharField(label = "", widget=forms.Textarea(attrs={'rows': 1}))


class New_page_titleForm(forms.Form):
    title = forms.CharField(label = "Title",
                            widget=forms.TextInput(attrs={'placeholder': "Your title"}))


def index(request):
    form = SearchForm()

    if request.method == "POST":
        return search_form(request)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),'form': form })

def page(request, title):
    form = SearchForm()

    if not util.get_entry(title) == None:
        return render(request, "encyclopedia/pages.html",
            {'content': markdown2.markdown(util.get_entry(title)), 'form': form})
    else:
        return render(request, "encyclopedia/not_found.html", {'form': form})

def search_form(request):
        form = SearchForm(request.POST)

        if form.is_valid():

            search_tag = form.cleaned_data["search_tag"]
            if util.get_entry(search_tag) != None:
                return render(request, "encyclopedia/pages.html",
                    {'content': markdown2.markdown(util.get_entry(search_tag)), 'form': form})
            else:
                return render(request, "encyclopedia/not_found.html", {'form': form})

def random_page(request):
    form = SearchForm()

    list = util.list_entries()
    item = random.choice(list)
    return render(request, "encyclopedia/pages.html",
        {'content': markdown2.markdown(util.get_entry(item)), "form": form})

def new_page(request):
    form = SearchForm()
    input_form = New_pageForm()
    title_form = New_page_titleForm()

    if request.method == "POST":
        input = New_pageForm(request.POST)
        title = New_page_titleForm(request.POST)

        if input.is_valid() and title.is_valid():
            input = input.cleaned_data["input"]
            title = title.cleaned_data["title"]

            if util.get_entry(title) != None:
                return render(request, "encyclopedia/already_exists.html", {'form': form})

            util.save_entry(title, input)

            return render(request, "encyclopedia/pages.html",
                {'content': markdown2.markdown(util.get_entry(title)), 'form': form})


    return render(request, "encyclopedia/new_page.html", {"form": form, "input_form": input_form, "title_form": title_form})
