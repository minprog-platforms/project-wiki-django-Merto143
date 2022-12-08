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
    input = forms.CharField(label = "", widget=forms.Textarea())


class New_page_titleForm(forms.Form):
    title = forms.CharField(label = "Title",
                            widget=forms.TextInput(attrs={'placeholder': "Your title"}))

class Edit_pageForm(forms.Form):
    input = forms.CharField(label="", widget=forms.Textarea())

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
            {'content': markdown2.markdown(util.get_entry(title)), 'form': form, 'title': title})
    else:
        return render(request, "encyclopedia/not_found.html", {'form': form})

def search_form(request):
        form = SearchForm(request.POST)
        search_list = []

        if form.is_valid():
            search_tag = form.cleaned_data["search_tag"]
            if util.get_entry(search_tag) != None:
                return render(request, "encyclopedia/pages.html",
                    {'content': markdown2.markdown(util.get_entry(search_tag)), 'form': form, 'title': search_tag})
            else:
                for entry in util.list_entries():
                    if search_tag.lower() in entry.lower():
                        search_list.append(entry)
                if search_list == []:
                    return render(request, "encyclopedia/not_found.html", {'form': form})
                else:
                    return render(request, "encyclopedia/did_you_mean.html", {'form': form, 'search_list':search_list})

def random_page(request):
    form = SearchForm()

    list = util.list_entries()
    item = random.choice(list)
    return render(request, "encyclopedia/pages.html",
        {'content': markdown2.markdown(util.get_entry(item)), "form": form, "title": item})


def edit(request, title):
    form = SearchForm()
    content = util.get_entry(title)
    edit = Edit_pageForm(initial={'input': content})


    if request.method == "POST":
        edit = Edit_pageForm(request.POST)
        if edit.is_valid():
            edit = edit.cleaned_data["input"]

            util.save_entry(title, edit)

            return render(request, "encyclopedia/pages.html",
                {'content': markdown2.markdown(util.get_entry(title)), 'form': form, 'title':title})
    if util.get_entry(title) != None:
        return render(request, "encyclopedia/edit_page.html", {"form": form, "edit":edit, "title":title})
    else:
        return render(request, "encyclopedia/not_found.html", {'form': form})



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
                {'content': markdown2.markdown(util.get_entry(title)), 'form': form, 'title':title})


    return render(request, "encyclopedia/new_page.html", {"form": form, "input_form": input_form, "title_form": title_form})
