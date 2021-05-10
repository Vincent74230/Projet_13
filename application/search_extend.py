"""Extention of search_results view"""
from useraccount.models import User, Category, Services
from .departements_list import departements, departements_number


def filter_results(region, departement, category, service):
    """Fetches users who matches with the fields of search bar"""
    if region == "Toute la France/Régions":
        region = None
    if departement == "Tous les départements":
        departement = None
    if category == "Toutes les catégories":
        category = None

    # 1st : no field selected
    if not region and not departement and not category and not service:
        users = User.objects.all()

    # 2nd : Only 'region' field selected
    if region and not departement and not category and not service:

        # just fetching all departement numbers in this region
        departements_in_region = departements[region]
        departements_number_in_region = []
        for departement_name in departements_in_region:
            for name, number in departements_number.items():
                if name == departement_name:
                    departements_number_in_region.append(number)

        if len(departements_number_in_region[0]) == 3:
            users = User.objects.filter(
                postcode__startswith=departements_number_in_region[0]
            )
        else:
            if departements_number_in_region[0] == "20":
                departements_number_in_region.pop()
            users = User.objects.filter(
                postcode__startswith=departements_number_in_region[0]
            )
            for dep_number in departements_number_in_region[1:]:
                users = users | User.objects.filter(postcode__startswith=dep_number)

    # 3rd : Only 'departement' selected
    if not region and departement and not category and not service:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            users = User.objects.filter(postcode__startswith=dep_number)
        else:
            users = User.objects.filter(postcode__startswith=dep_number)

    # 4th: 'region' and 'departement' selected
    if region and departement and not category and not service:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            users = User.objects.filter(postcode__startswith=dep_number)
        else:
            users = User.objects.filter(postcode__startswith=dep_number)

    # 5th : only 'category' selected
    if not region and not departement and category and not service:
        users = User.objects.filter(proposed_services__category__name=category)

    # 6th: 'region' and 'category' selected
    if region and not departement and category and not service:

        # just fetching all departement numbers in this region
        departements_in_region = departements[region]
        departements_number_in_region = []
        for departement_name in departements_in_region:
            for name, number in departements_number.items():
                if name == departement_name:
                    departements_number_in_region.append(number)

        if len(departements_number_in_region[0]) == 3:
            users = User.objects.filter(
                postcode__startswith=departements_number_in_region[0],
                proposed_services__category__name=category,
            )
        else:
            if departements_number_in_region[0] == "20":
                departements_number_in_region.pop()
            users = User.objects.filter(
                postcode__startswith=departements_number_in_region[0],
                proposed_services__category__name=category,
            )
            for dep_number in departements_number_in_region[1:]:
                users = users | User.objects.filter(
                    postcode__startswith=dep_number,
                    proposed_services__category__name=category,
                )

    return users
