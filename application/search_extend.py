'''Extention of search_results view'''
from useraccount.models import User
from .departements_list import departements, departements_number

def filter_results(region, departement, category, service):
    """Fetches users who matches with the fields of search bar"""
    if region == "Toute la France/Régions":
        region = None
    if departement == "Tous les départements":
        departement = None
    if category == 'Toutes les catégories':
        category = None

    all_users_info = []

    #First case : no field switched
    if not region and not departement and not category and not service:
        users = User.objects.all()
        
        for user in users:
            single_user_info = {}
            single_user_info['username'] = user.username
            single_user_info['postcode'] = user.postcode
            single_user_info['gender'] = user.gender
            single_user_info['required_services'] = user.required_services.all()
            single_user_info['proposed_services'] = user.proposed_services.all()
            all_users_info.append(single_user_info)

    #Second case : Only 'region' field switched
    if region and not departement and not category and not service:
        departements_in_region = departements[region]
        departements_number_in_region = []
        for departement_name in departements_in_region:
            for name, number in departements_number.items():
                if name == departement_name:
                    departements_number_in_region.append(number)

    for dep_number in departements_number_in_region:
        if len(dep_number) == 3:
            print ('outre-mer')
        else:
            print('métropole')

        

    return all_users_info
