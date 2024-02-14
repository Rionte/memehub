from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

projects_ = {"Roulette Game": "https://rionte.toxi.ca/roulette/", "Portfolio Site": "https://www.google.com/", "Blog Site": "https://remi.home.sabra.ca/"}

def memes(request):
    context = {
        "projects": projects_
    }
    return render(request, "home.html", context)

def contact(request):
    context = {
        "projects": projects_
    }
    return render(request, "content.html", context)