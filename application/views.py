from django.shortcuts import render
from useraccount.models import User, Category, Services
from .departements_list import departements
from .search_extend import filter_results, counting_users


def index(request):
    """Returns app main page"""
    categories = Category.objects.all()
    cat_names = ["Toutes les catégories"]
    for cat in categories:
        cat_names.append(cat.name)

    departement_choice_position = 0

    context = {
        "cat_names": cat_names,
        "departements_dict": departements,
        "departement_choice_position": departement_choice_position,
    }
    return render(request, "application/index.html", context)


def search_results(request):
    """Returns user search results"""

    # fetching user choices in search bar
    region = request.GET.get("region")
    departement = request.GET.get("departement")
    cate = request.GET.get("category")
    service_choice = request.GET.get("service")

    # gathering categories available in DB, making a list of it
    categories = Category.objects.all()
    cat_names = ["Toutes les catégories"]
    for cat in categories:
        cat_names.append(cat.name)

    # the search bar needs the position of a departement in the scroll menu,
    # to reposition it as it was before the submit click
    departement_choice_position = 0
    if region:
        departement_choice_position = departements[region].index(departement)

    # funtion that returns users accordingly to selected fields
    users = filter_results(region, departement, cate, service_choice)
    """
    # Returns a dict with services sorted by categories, for display
    services_dict = {}
    category_dict = {}
    for category in categories:
        services_per_category = Services.objects.filter(category__name=category.name)
        single_service_dict = {}
        users_service = 0
        for service in services_per_category:
            single_service_dict[service.name] = User.objects.filter(
                proposed_services__name=service.name
            ).count()
            users_service += User.objects.filter(
                proposed_services__name=service.name
            ).count()
        category_dict[category.name] = users_service
        services_dict[category.name] = single_service_dict
    """
    users_count = counting_users(region, departement)
    services_dict = users_count[1]
    category_dict = users_count[0]

    # We don't send the whole users info here,
    # we only send useful datas
    users_info = []
    for user in users:
        single_user_info = {}
        single_user_info["username"] = user.username
        single_user_info["postcode"] = user.postcode
        single_user_info["gender"] = user.gender
        single_user_info["required_services"] = user.required_services.all()
        single_user_info["proposed_services"] = user.proposed_services.all()
        users_info.append(single_user_info)

    context = {
        "total_nb_users": len(User.objects.all()),
        "nb_users": len(users),
        "cat_names": cat_names,
        "departements_dict": departements,
        "region": region,
        "departement": departement,
        "cate": cate,
        "departement_choice_position": departement_choice_position,
        "cat_dict": category_dict,
        "services_dict": services_dict,
        "users_info": users_info,
    }

    return render(request, "application/search_results.html", context)


"""
{'Cours': {'Cuisine': 10, 'Musique': 9, 'Informatique': 10, 'Langues étrangères': 8, 'Soutien scolaire': 10, 'Coaching': 11}, 'Bricolage': {'Electricité': 5, 'Maçonnerie': 11, 'Menuiserie': 12, 'Plomberie': 8, 'Tapisserie': 8, 'Peinture': 6}, 'Travail': {'Comptabilité': 10, 'Assistance': 10, 'Traduction': 8, 'Secrétariat': 8, "Recherche d'emploi": 12}, 'Vehicules': {'Entretien': 15, 'Location': 19, 'Vente': 14, 'Petites réparations': 15, 'Grosses réparations': 15}, 'Maison': {'Ameublement': 14, 'Colocation': 13, 'Décoration': 20, 'Jardinage': 9, 'Gardiennage': 10}}
{'Cours': 58, 'Bricolage': 50, 'Travail': 48, 'Vehicules': 78, 'Maison': 66}
"""
