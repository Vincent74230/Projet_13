from django.shortcuts import render


def index(request):
    """Returns app main page"""
    return render(request, "application/index.html")

def search_results(request):
	"""Returns user search results"""
	return render (request, "application/search_results.html")