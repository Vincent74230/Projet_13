from django.shortcuts import render


def index(request):
    """Returns app main page"""
    return render(request, "application/index.html")

def search(request):
	