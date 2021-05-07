from django.shortcuts import render
from useraccount.models import User, Ad, Category, Services
from .annex import departements


def index(request):
    """Returns app main page"""
    categories = Category.objects.all()
    cat_names = ['Toutes les catégories']
    for cat in categories:
    	cat_names.append(cat.name)

    departement_choice_position = 0

    context = {
    'cat_names':cat_names,
    'departements_dict':departements,
    'departement_choice_position':departement_choice_position,
    }
    return render(request, "application/index.html", context)

def search_results(request):
	"""Returns user search results"""

	#fetching user choices in search bar
	region = request.GET.get('region')
	departement = request.GET.get('departement')
	cate = request.GET.get('category')
	service_choice = request.GET.get('service')

	print(region, departement, cate, service_choice)

	#gathering categories available in DB, making a list of it
	categories = Category.objects.all()
	cat_names = ['Toutes les catégories']
	for cat in categories:
		cat_names.append(cat.name)

	#gathering users info
	users_info = {}
	users = User.objects.all()
	for user in users:
		single_user_info = {}
		single_user_info['user_id'] = user.id
		single_user_info['username'] = user.username
		single_user_info['postcode'] = user.postcode
		single_user_info['gender'] = user.gender
		users_info[user.id] = single_user_info
	
	#the search bar needs the position of a departement in the scroll menu,
	#to reposition it as it was before the submit click
	departement_choice_position = 0
	if region:
		departement_choice_position = departements[region].index(departement)

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
	'users_info':users_info,
	'cat_names':cat_names,
	'departements_dict':departements,
	'region':region,
	'departement':departement,
	'cate':cate,
	'departement_choice_position':departement_choice_position,
	'cat_dict':category_dict,
	'services_dict':services_dict,
	}
	

	return render (request, "application/search_results.html", context)
