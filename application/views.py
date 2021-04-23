from django.shortcuts import render
from useraccount.models import User, Ad, Category, Services


def index(request):
    """Returns app main page"""
    return render(request, "application/index.html")

def search_results(request):
	"""Returns user search results"""
	category_choice = ''
	service_choice = ''
	if request.method == 'POST':
		category_choice = request.POST.get('which_category')
		service_choice = request.POST.get('which_service')
	print (category_choice)
	print (service_choice)

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
	'''
	users = []
	all_users = User.objects.all()
	single_user = {}
	proposed_services = []
	required_services = []
	for user in all_users:
		single_user["username"] = user.username
		single_user["postcode"] = user.postcode
		user_proposed_services = Services.objects.filter(proposed_services__pk=user.pk)
		for proposed_service in user_proposed_services:
			proposed_services.append(proposed_service.name)
		single_user["proposed"] = proposed_services
		user_required_services = Services.objects.filter(required_services__pk=user.pk)
		for required_service in user_required_services:
			required_services.append(required_service.name)
		single_user["required"] = proposed_services

	'''

	context = {
	'nb_users':len(User.objects.all()),
	'nb_annonces':len(Ad.objects.all()),
	'categories':Category.objects.all(),
	'category_dict':category_dict,
	'service_dict':services_dict,
	'category_choice':category_choice,
	}
	return render (request, "application/search_results.html", context)
