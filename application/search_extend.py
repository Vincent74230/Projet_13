"""Extention of search_results view"""
from useraccount.models import User, Category, Services
from .departements_list import DEPARTEMENTS as departements, DEPARTEMENTS_NUMBER as departements_number


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

    # 7th: 'departement' and 'category' selected
    if not region and departement and category and not service:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            users = User.objects.filter(
                postcode__startswith=dep_number,
                proposed_services__category__name=category,
            )
        else:
            users = User.objects.filter(
                postcode__startswith=dep_number,
                proposed_services__category__name=category,
            )

    # 8th: 'region', 'departement' and 'category' selected
    if region and departement and category and not service:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            users = User.objects.filter(
                postcode__startswith=dep_number,
                proposed_services__category__name=category,
            )
        else:
            users = User.objects.filter(
                postcode__startswith=dep_number,
                proposed_services__category__name=category,
            )

    # 9th: Only 'category' and 'service' selected
    if not region and not departement and category and service:
        users = User.objects.filter(proposed_services__name=service)

    # 10th: 'departement', 'category' and 'service' selected
    if not region and departement and category and service:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            users = User.objects.filter(
                postcode__startswith=dep_number, proposed_services__name=service
            )
        else:
            users = User.objects.filter(
                postcode__startswith=dep_number, proposed_services__name=service
            )

    # 11th: 'region', 'category' and 'service' selected
    if region and not departement and category and service:
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
                proposed_services__name=service,
            )
        else:
            if departements_number_in_region[0] == "20":
                departements_number_in_region.pop()
            users = User.objects.filter(
                postcode__startswith=departements_number_in_region[0],
                proposed_services__name=service,
            )
            for dep_number in departements_number_in_region[1:]:
                users = users | User.objects.filter(
                    postcode__startswith=dep_number,
                    proposed_services__name=service,
                )
    # 12th: 'region, 'departement', 'category' and 'service':
    if region and departement and category and service:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            users = User.objects.filter(
                postcode__startswith=dep_number, proposed_services__name=service
            )
        else:
            users = User.objects.filter(
                postcode__startswith=dep_number, proposed_services__name=service
            )

    return users


def counting_users(region, departement):
    """function that returns number of users in cat and services accordingly to selected fields"""
    if region == "Toute la France/Régions":
        region = None
    if departement == "Tous les départements":
        departement = None

    categories = Category.objects.all()
    services_dict = {}
    category_dict = {}

    if not region and not departement:
        for category in categories:
            category_dict[category.name] = User.objects.filter(
                proposed_services__category__name=category.name
            ).count()
            services_per_category = Services.objects.filter(
                category__name=category.name
            )
            services_count = {}
            for service in services_per_category:
                services_count[service.name] = User.objects.filter(
                    proposed_services__name=service.name
                ).count()
            services_dict[category.name] = services_count

    if not region and departement:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            for category in categories:
                category_dict[category.name] = User.objects.filter(
                    proposed_services__category__name=category.name,
                    postcode__startswith=dep_number,
                ).count()
                services_per_category = Services.objects.filter(
                    category__name=category.name
                )
                services_count = {}
                for service in services_per_category:
                    services_count[service.name] = User.objects.filter(
                        proposed_services__name=service.name,
                        postcode__startswith=dep_number,
                    ).count()
                services_dict[category.name] = services_count
        else:
            for category in categories:
                category_dict[category.name] = User.objects.filter(
                    postcode__startswith=dep_number,
                    proposed_services__category__name=category.name,
                ).count()
                services_per_category = Services.objects.filter(
                    category__name=category.name
                )
                services_count = {}
                for service in services_per_category:
                    services_count[service.name] = User.objects.filter(
                        proposed_services__name=service.name,
                        postcode__startswith=dep_number,
                    ).count()
                services_dict[category.name] = services_count

    if region and not departement:
        # fetching all departement numbers in this region
        departements_in_region = departements[region]
        departements_number_in_region = []
        for departement_name in departements_in_region:
            for name, number in departements_number.items():
                if name == departement_name:
                    departements_number_in_region.append(number)

        if len(departements_number_in_region[0]) == 3:
            for category in categories:
                category_dict[category.name] = User.objects.filter(
                    proposed_services__category__name=category.name,
                    postcode__startswith=departements_number_in_region[0],
                ).count()
                services_per_category = Services.objects.filter(
                    category__name=category.name
                )
                services_count = {}
                for service in services_per_category:
                    services_count[service.name] = User.objects.filter(
                        proposed_services__name=service.name,
                        postcode__startswith=departements_number_in_region[0],
                    ).count()
                services_dict[category.name] = services_count
        else:
            for category in categories:
                users_in_region = 0

                for departement_number in departements_number_in_region:
                    users_in_region += User.objects.filter(
                        proposed_services__category__name=category.name,
                        postcode__startswith=departement_number,
                    ).count()

                services_count = {}
                services_per_category = Services.objects.filter(
                    category__name=category.name
                )
                for service in services_per_category:
                    total_users_per_service = 0
                    for dep in departements_number_in_region:
                        total_users_per_service += User.objects.filter(
                            proposed_services__name=service.name,
                            postcode__startswith=dep,
                        ).count()
                    services_count[service.name] = total_users_per_service

                category_dict[category.name] = users_in_region
                services_dict[category.name] = services_count

    if region and departement:
        dep_number = departements_number[departement]
        if len(dep_number) == 3:
            for category in categories:
                category_dict[category.name] = User.objects.filter(
                    proposed_services__category__name=category.name,
                    postcode__startswith=dep_number,
                ).count()
                services_per_category = Services.objects.filter(
                    category__name=category.name
                )
                services_count = {}
                for service in services_per_category:
                    services_count[service.name] = User.objects.filter(
                        proposed_services__name=service.name,
                        postcode__startswith=dep_number,
                    ).count()
                services_dict[category.name] = services_count
        else:
            for category in categories:
                category_dict[category.name] = User.objects.filter(
                    postcode__startswith=dep_number,
                    proposed_services__category__name=category.name,
                ).count()
                services_per_category = Services.objects.filter(
                    category__name=category.name
                )
                services_count = {}
                for service in services_per_category:
                    services_count[service.name] = User.objects.filter(
                        proposed_services__name=service.name,
                        postcode__startswith=dep_number,
                    ).count()
                services_dict[category.name] = services_count

    users_count = [category_dict, services_dict]
    return users_count
