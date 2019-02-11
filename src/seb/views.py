from django.views.generic import DetailView
from django.shortcuts import render


def about1(request):
    print("about")
    return render(request, "about1.html", {})