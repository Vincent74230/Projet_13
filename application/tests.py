from django.test import TestCase
from django.urls import reverse
from useraccount.models import User, Services, Category
from useraccount.services import SERVICES_DICT


class IndexPageTest(TestCase):
    """Tests of main page display"""
    def test_index_page_display(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

class FilterResultsTest(TestCase):
    """Tests of search_results view"""
    def setUp(self):
        fake_user = User.objects.create_user(
        username="VincentTest1",
        password="Testpassword1",
        first_name="Vincent",
        last_name="VinceNow",
        email="vince1@gmail.com",
        gender=True,
        postcode='73000',
        )
        fake_user.save()
    
        fake_user = User.objects.create_user(
        username="VincentTest2",
        password="Testpassword2",
        first_name="Jules",
        last_name="Nono",
        email="vince2@gmail.com",
        gender=True,
        postcode='74230',
        )
        fake_user.save()

        fake_user = User.objects.create_user(
        username="AliceTest1",
        password="Testpassword3",
        first_name="Alice",
        last_name="Wonderland",
        email="alice@gmail.com",
        gender=False,
        postcode='44000',
        )
        fake_user.save()

        fake_user = User.objects.create_user(
        username="Cicolini",
        password="Testpassword3",
        first_name="Giorgio",
        last_name="Giorgissimo",
        email="cico@gmail.com",
        gender=True,
        postcode='20090',
        )
        fake_user.save()

        fake_user = User.objects.create_user(
        username="runner974",
        password="Testpassword3",
        first_name="Tim",
        last_name="Hoaro",
        email="timy@gmail.com",
        gender=True,
        postcode='97400',
        )
        fake_user.save()

        # Populate categories
        services_dict = SERVICES_DICT
        for category in services_dict:
            cat = Category(name=category)
            cat.save()

        # Populate services
        for key, value in services_dict.items():
            for element in value:
                service_query = Services(
                    name=element, category=Category.objects.get(name=key)
                )
                service_query.save()

        # Associating fake users with proposed & required services
        informatique_query = Services.objects.get(name='Informatique')
        petites_reparations_query = Services.objects.get(name='Petites réparations')
        jardinage_query = Services.objects.get(name='Jardinage')
        comptabilité_query = Services.objects.get(name='Comptabilité')
        langues_query = Services.objects.get(name='Langues étrangères')
        electricité_query = Services.objects.get(name='Electricité')
        maconnerie_query = Services.objects.get(name='Maçonnerie')
        coaching_query = Services.objects.get(name='Coaching')
        peinture_query = Services.objects.get(name='Peinture')
        ameublement_query = Services.objects.get(name='Ameublement')

        users = User.objects.all()

        users[0].proposed_services.add(informatique_query)
        users[0].required_services.add(petites_reparations_query)
        users[1].proposed_services.add(jardinage_query)
        users[1].required_services.add(comptabilité_query)
        users[2].proposed_services.add(langues_query)
        users[2].proposed_services.add(electricité_query)
        users[3].proposed_services.add(maconnerie_query)
        users[3].proposed_services.add(coaching_query)
        users[4].proposed_services.add(peinture_query)
        users[4].proposed_services.add(ameublement_query)


    def test_region_and_departement_parameters_response(self):
        response = self.client.get("/search_results")
        self.assertEqual(response.status_code, 200)

        # checking total users returned by view
        self.assertEqual(response.context[0]['total_nb_users'], 5)

        # checking users returned by view with default params
        self.assertEqual(response.context[0]['nb_users'], 5)

        response = self.client.get("/search_results", {'region':'Auvergne-Rhônes-Alpes','departement':'Tous les départements'})

        #in 'Auvergne-Rhônes-Alpes', there must be only 2 users (1 and 2)
        self.assertEqual(len(response.context[0]['users_info']), 2)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'VincentTest1')
        self.assertEqual(response.context[0]['users_info'][1]['username'], 'VincentTest2')

        response = self.client.get("/search_results", {'region':'Bretagne','departement':'Tous les départements'})

        #In this case, no users should be teturned
        self.assertEqual(response.context[0]['nb_users'], 0)

        response = self.client.get("/search_results", {'region':'Pays de la Loire','departement':'Tous les départements'})

        #Only user3 should be in this case
        self.assertEqual(len(response.context[0]['users_info']), 1)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'AliceTest1')

        #There must be only one user in this departements : Haute-savoie
        response = self.client.get("/search_results", {'region':'Toute la France/Régions','departement':'Haute-Savoie'})
        self.assertEqual(response.context[0]['nb_users'], 1)

        #There must be only one user in this region : Corse
        response = self.client.get("/search_results", {'region':'Corse','departement':'Tous les départements'})
        self.assertEqual(response.context[0]['nb_users'], 1)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'Cicolini')

        #There must be only one user in this departement : haute corse
        response = self.client.get("/search_results", {'region':'Toute la France/Régions','departement':'Haute-Corse'})
        self.assertEqual(response.context[0]['nb_users'], 1)

        #Still checking the numbers of total users with these parameters
        self.assertEqual(response.context[0]['total_nb_users'], 5)

        #There must be only one user in this region : Réunion
        response = self.client.get("/search_results", {'region':'Réunion','departement':'Tous les départements'})
        self.assertEqual(response.context[0]['nb_users'], 1)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'runner974')

        #There must be only one user in this departement : Réunion
        response = self.client.get("/search_results", {'region':'Toute la France/Régions','departement':'La Réunion'})
        self.assertEqual(response.context[0]['nb_users'], 1)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'runner974')

        #'region' and 'departement' selected
        response = self.client.get("/search_results", {'region':'Corse','departement':'Haute-Corse'})
        self.assertEqual(response.context[0]['nb_users'], 1)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'Cicolini')

    def test_only_category_response(self):
        #Testing only with one category parameter
        response = self.client.get("/search_results", {'region':'Toute la France/Régions','departement':'Tous les départements', 'category':'Cours'})

        #There must be 3 users with those params
        self.assertEqual(response.context[0]['nb_users'], 3)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'VincentTest1')
        self.assertEqual(response.context[0]['users_info'][1]['username'], 'AliceTest1')
        self.assertEqual(response.context[0]['users_info'][2]['username'], 'Cicolini')


    def test_region_and_category(self):
        #Test with 'Auvergne Rhônes Alpes as region and Travail'
        response = self.client.get("/search_results", {'region':'Auvergne-Rhônes-Alpes','departement':'Tous les départements', 'category':'Cours'})

        self.assertEqual(response.context[0]['nb_users'], 1)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'VincentTest1')

    def test_departement_and_category(self):
        #Test with 'haute corse', 'Bricolage' selected should return 1 user
        response = self.client.get("/search_results", {'region':'Toute la France/Régions','departement':'Haute-Corse', 'category':'Bricolage'})

        self.assertEqual(response.context[0]['nb_users'], 1)
        self.assertEqual(response.context[0]['users_info'][0]['username'], 'Cicolini')

        # Test with 'haute corse' and 'Travail' selected should return no users
        response = self.client.get("/search_results", {'region':'Toute la France/Régions','departement':'Haute-Corse', 'category':'Travail'})
        self.assertEqual(response.context[0]['nb_users'], 0)