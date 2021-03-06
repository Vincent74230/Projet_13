from django.shortcuts import render, redirect
from useraccount.models import User, Category, Services
from .departements_list import DEPARTEMENTS as departements
from .search_extend import filter_results, counting_users
from useraccount.models import User, Rating
from useraccount.services import SERVICES_DICT



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

    #conditional block to secure search bar inputs
    if region and region not in departements:
        return redirect("application:index")
            
    if departement and departement not in departements["Toute la France/Régions"]:
        return redirect("application:index")
            
    if cate and cate not in cat_names:
        return redirect("application:index")

    if not cate and service_choice:
        return redirect("application:index")
    
    if service_choice:
        # Making a list of all services
        services_list = []
        for services_list_per_cat in SERVICES_DICT.values():
            services_list += services_list_per_cat
        if service_choice not in services_list:
            return redirect("application:index")
    
    # the search bar needs the position of a departement in the scroll menu,
    # to reposition it as it was before the submit click
    departement_choice_position = 0
    if region:
        departement_choice_position = departements[region].index(departement)
    

    # funtion that returns users accordingly to selected fields
    users = filter_results(region, departement, cate, service_choice)

    users_count = counting_users(region, departement)
    services_dict = users_count[1]
    category_dict = users_count[0]

    # We don't send the whole users info here,
    # we only send useful data
    users_info = []
    for user in users:
        single_user_info = {}
        single_user_info["pk"] = user.pk
        single_user_info["username"] = user.username
        single_user_info["postcode"] = user.postcode
        single_user_info["gender"] = user.gender
        single_user_info["required_services"] = user.required_services.all()
        single_user_info["proposed_services"] = user.proposed_services.all()
        single_user_info["email"] = user.email
        users_info.append(single_user_info)

    #Star rating average per user
    ratings = Rating.objects.filter(score_pending=False)
    noted_users_list = []
    for rating in ratings:
        noted_users_list.append(rating.sender_id)
        noted_users_list.append(rating.receiver_id)

    noted_users_list = list(set(noted_users_list))

    all_users_average_rating_list = []
    for noted_user_id in noted_users_list:
        all_notes_per_user = []
        average_dict = {}
        for rating in ratings:
            if rating.receiver_id == noted_user_id:
                all_notes_per_user.append(rating.score_sent)
            if rating.sender_id == noted_user_id:
                all_notes_per_user.append(rating.score_received)
        average_note = sum(all_notes_per_user)/len(all_notes_per_user)
        average_dict[noted_user_id]=average_note
        all_users_average_rating_list.append(average_dict)


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
        "average_list":all_users_average_rating_list,
    }

    return render(request, "application/search_results.html", context)

def mentions_legales(request):
    """Shows terms of use page"""
    return render(request, "application/mentions_legales.html", {})

def about(request):
    """Shows info about me"""
    return render(request, "application/about.html", {})
