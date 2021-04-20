from django.shortcuts import render
from useraccount.models import User, Ad, Category, Services


def index(request):
    """Returns app main page"""
    return render(request, "application/index.html")

def search_results(request):
	"""Returns user search results"""
	category_choice = ''
	if request.method == 'POST':
		category_choice = request.POST.get('which_category')
	categories = Category.objects.all()
	services_dict = {}
	category_dict = {}
	for category in categories:
		services_per_category = Services.objects.filter(category__name=category.name)
		single_service_dict = {}
		users_service = 0
		for service in services_per_category:
			single_service_dict[service.name] = User.objects.filter(proposed_services__name=service.name).count()
			users_service += User.objects.filter(proposed_services__name=service.name).count()
		category_dict[category.name] = users_service
		services_dict[category.name] = single_service_dict

	context = {
	'nb_users':len(User.objects.all()),
	'nb_annonces':len(Ad.objects.all()),
	'categories':Category.objects.all(),
	'category_dict':category_dict,
	'service_dict':services_dict,
	'category_choice':category_choice,
	}
	return render (request, "application/search_results.html", context)
