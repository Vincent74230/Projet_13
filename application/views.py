import json
from django.shortcuts import render
from useraccount.models import User, Ad, Category, Services
from .annex import departements


def index(request):
    """Returns app main page"""
    return render(request, "application/index.html")

def search_results(request):
	"""Returns user search results"""

	region = request.GET.get('region')
	departement = request.GET.get('departement')
	category = request.GET.get('category')
	
	user_fields = {'region':region, 'departement':departement, 'category':category}

	print (region, departement, category)
	categories = Category.objects.all()
	cat_names = ['Catégories']
	for category in categories:
		cat_names.append(category.name)

	users_info = {}
	users = User.objects.all()
	for user in users:
		single_user_info = {}
		single_user_info['user_id'] = user.id
		single_user_info['username'] = user.username
		single_user_info['postcode'] = user.postcode
		single_user_info['gender'] = user.gender
		users_info[user.id] = single_user_info


	context = {
	'nb_users':len(User.objects.all()),
	'nb_annonces':len(Ad.objects.all()),
	'users_info':users_info,
	'cat_names':cat_names,
	'departements_dict':departements,
	'user_fields':user_fields,
	}
	

	return render (request, "application/search_results.html", context)

	"""
	if request.method == 'POST':
		category_choice = request.POST.get('which_category')
		service_choice = request.POST.get('which_service')
	print (category_choice)
	print (service_choice)
	

	if request.method == 'GET':
		category_choice = cat_choice
		service_choice = serv_choice
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
	"""