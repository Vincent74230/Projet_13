from django.test import TestCase, LiveServerTestCase, tag
from django.urls import reverse
from useraccount.models import User, Services, Category
from useraccount.services import SERVICES_DICT as services_dict
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pathlib import Path


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
            postcode="73000",
        )
        fake_user.save()

        fake_user = User.objects.create_user(
            username="VincentTest2",
            password="Testpassword2",
            first_name="Jules",
            last_name="Nono",
            email="vince2@gmail.com",
            gender=True,
            postcode="74230",
        )
        fake_user.save()

        fake_user = User.objects.create_user(
            username="AliceTest1",
            password="Testpassword3",
            first_name="Alice",
            last_name="Wonderland",
            email="alice@gmail.com",
            gender=False,
            postcode="44000",
        )
        fake_user.save()

        fake_user = User.objects.create_user(
            username="Cicolini",
            password="Testpassword3",
            first_name="Giorgio",
            last_name="Giorgissimo",
            email="cico@gmail.com",
            gender=True,
            postcode="20090",
        )
        fake_user.save()

        fake_user = User.objects.create_user(
            username="runner974",
            password="Testpassword3",
            first_name="Tim",
            last_name="Hoaro",
            email="timy@gmail.com",
            gender=True,
            postcode="97400",
        )
        fake_user.save()

        # Populate categories
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
        informatique_query = Services.objects.get(name="Informatique")
        petites_reparations_query = Services.objects.get(name="Petites réparations")
        jardinage_query = Services.objects.get(name="Jardinage")
        comptabilité_query = Services.objects.get(name="Comptabilité")
        langues_query = Services.objects.get(name="Langues étrangères")
        electricité_query = Services.objects.get(name="Electricité")
        maconnerie_query = Services.objects.get(name="Maçonnerie")
        coaching_query = Services.objects.get(name="Coaching")
        peinture_query = Services.objects.get(name="Peinture")
        ameublement_query = Services.objects.get(name="Ameublement")

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
        self.assertEqual(response.context[0]["total_nb_users"], 5)

        # checking users returned by view with default params
        self.assertEqual(response.context[0]["nb_users"], 5)

        response = self.client.get(
            "/search_results",
            {"region": "Auvergne-Rhônes-Alpes", "departement": "Tous les départements"},
        )

        # in 'Auvergne-Rhônes-Alpes', there must be only 2 users (1 and 2)
        self.assertEqual(len(response.context[0]["users_info"]), 2)
        self.assertEqual(
            response.context[0]["users_info"][0]["username"], "VincentTest1"
        )
        self.assertEqual(
            response.context[0]["users_info"][1]["username"], "VincentTest2"
        )

        response = self.client.get(
            "/search_results",
            {"region": "Bretagne", "departement": "Tous les départements"},
        )

        # In this case, no users should be teturned
        self.assertEqual(response.context[0]["nb_users"], 0)

        response = self.client.get(
            "/search_results",
            {"region": "Pays de la Loire", "departement": "Tous les départements"},
        )

        # Only user3 should be in this case
        self.assertEqual(len(response.context[0]["users_info"]), 1)
        self.assertEqual(response.context[0]["users_info"][0]["username"], "AliceTest1")

        # There must be only one user in this departements : Haute-savoie
        response = self.client.get(
            "/search_results",
            {"region": "Toute la France/Régions", "departement": "Haute-Savoie"},
        )
        self.assertEqual(response.context[0]["nb_users"], 1)

        # There must be only one user in this region : Corse
        response = self.client.get(
            "/search_results",
            {"region": "Corse", "departement": "Tous les départements"},
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(response.context[0]["users_info"][0]["username"], "Cicolini")

        # There must be only one user in this departement : haute corse
        response = self.client.get(
            "/search_results",
            {"region": "Toute la France/Régions", "departement": "Haute-Corse"},
        )
        self.assertEqual(response.context[0]["nb_users"], 1)

        # Still checking the numbers of total users with these parameters
        self.assertEqual(response.context[0]["total_nb_users"], 5)

        # There must be only one user in this region : Réunion
        response = self.client.get(
            "/search_results",
            {"region": "Réunion", "departement": "Tous les départements"},
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(response.context[0]["users_info"][0]["username"], "runner974")

        # There must be only one user in this departement : Réunion
        response = self.client.get(
            "/search_results",
            {"region": "Toute la France/Régions", "departement": "La Réunion"},
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(response.context[0]["users_info"][0]["username"], "runner974")

        #'region' and 'departement' selected
        response = self.client.get(
            "/search_results", {"region": "Corse", "departement": "Haute-Corse"}
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(response.context[0]["users_info"][0]["username"], "Cicolini")

    def test_only_category_response(self):
        # Testing only with one category parameter
        response = self.client.get(
            "/search_results",
            {
                "region": "Toute la France/Régions",
                "departement": "Tous les départements",
                "category": "Cours",
            },
        )

        # There must be 3 users with those params
        self.assertEqual(response.context[0]["nb_users"], 3)
        self.assertEqual(
            response.context[0]["users_info"][0]["username"], "VincentTest1"
        )
        self.assertEqual(response.context[0]["users_info"][1]["username"], "AliceTest1")
        self.assertEqual(response.context[0]["users_info"][2]["username"], "Cicolini")

    def test_region_and_category(self):
        # Test with 'Auvergne Rhônes Alpes as region and Travail'
        response = self.client.get(
            "/search_results",
            {
                "region": "Auvergne-Rhônes-Alpes",
                "departement": "Tous les départements",
                "category": "Cours",
            },
        )

        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(
            response.context[0]["users_info"][0]["username"], "VincentTest1"
        )

    def test_departement_and_category(self):
        # Test with 'haute corse', 'Bricolage' selected should return 1 user
        response = self.client.get(
            "/search_results",
            {
                "region": "Toute la France/Régions",
                "departement": "Haute-Corse",
                "category": "Bricolage",
            },
        )

        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(response.context[0]["users_info"][0]["username"], "Cicolini")

        # Test with 'haute corse' and 'Travail' selected should return no users
        response = self.client.get(
            "/search_results",
            {
                "region": "Toute la France/Régions",
                "departement": "Haute-Corse",
                "category": "Travail",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 0)

    def test_region_departement_and_category(self):
        # Should return 1 user
        response = self.client.get(
            "/search_results",
            {
                "region": "Auvergne-Rhônes-Alpes",
                "departement": "Haute-Savoie",
                "category": "Maison",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 1)

        # Should return no users
        response = self.client.get(
            "/search_results",
            {
                "region": "Auvergne-Rhônes-Alpes",
                "departement": "Haute-Savoie",
                "category": "Bricolage",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 0)

    def test_category_and_service(self):
        # Sould return 1 user
        response = self.client.get(
            "/search_results",
            {
                "region": "Toute la France/Régions",
                "departement": "Tous les départements",
                "category": "Cours",
                "service": "Informatique",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(
            response.context[0]["users_info"][0]["username"], "VincentTest1"
        )

        # Sould return 0 users
        response = self.client.get(
            "/search_results",
            {
                "region": "Toute la France/Régions",
                "departement": "Tous les départements",
                "category": "Travail",
                "service": "Traduction",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 0)

    def test_departement_category_and_service(self):
        # Sould return 1 user
        response = self.client.get(
            "/search_results",
            {
                "region": "Toute la France/Régions",
                "departement": "Savoie",
                "category": "Cours",
                "service": "Informatique",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(
            response.context[0]["users_info"][0]["username"], "VincentTest1"
        )

        # Sould return 0 users
        response = self.client.get(
            "/search_results",
            {
                "region": "Toute la France/Régions",
                "departement": "Savoie",
                "category": "Travail",
                "service": "Traduction",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 0)

    def test_region_departement_category_and_service(self):
        # Sould return 1 user
        response = self.client.get(
            "/search_results",
            {
                "region": "Auvergne-Rhônes-Alpes",
                "departement": "Savoie",
                "category": "Maison",
                "service": "Informatique",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(
            response.context[0]["users_info"][0]["username"], "VincentTest1"
        )

        # Sould return 0 users
        response = self.client.get(
            "/search_results",
            {
                "region": "Auvergne-Rhônes-Alpes",
                "departement": "Savoie",
                "category": "Travail",
                "service": "Traduction",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 0)

    def test_region_category_service(self):
        # Should return 1 user
        response = self.client.get(
            "/search_results",
            {
                "region": "Auvergne-Rhônes-Alpes",
                "departement": "Tous les départements",
                "category": "Cours",
                "service": "Informatique",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 1)
        self.assertEqual(
            response.context[0]["users_info"][0]["username"], "VincentTest1"
        )

        # Should return 0 users
        response = self.client.get(
            "/search_results",
            {
                "region": "Auvergne-Rhônes-Alpes",
                "departement": "Tous les départements",
                "category": "Bricolage",
                "service": "Peinture",
            },
        )
        self.assertEqual(response.context[0]["nb_users"], 0)

    def test_only_service_selected(self):
        # Should redirect to home page
        response = self.client.get("/search_results", {"service": "Assistance"})
        self.assertEqual(response.status_code, 302)

    def test_wrong_input(self):
        # A wrong input in search bar fields should redirect user to homepage
        response = self.client.get(
            "/search_results",
            {
                "region": "Auves-Alpes",
                "departement": "Tous lestements",
                "category": "Cour",
                "service": "Informatique",
            },
        )
        self.assertEqual(response.status_code, 302)

@tag('not_in_CI')
class Hosttest(LiveServerTestCase):
    """Browser tests index page and search bar"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BASE_DIR = Path(__file__).resolve().parent.parent
        PATH = str(BASE_DIR / "webdrivers" / "chromedriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=1920x1080')

        cls.driver = webdriver.Chrome((PATH), options=chrome_options)
        cls.driver.get(cls.live_server_url)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_home_page(self):
        '''Testing home page display'''
        self.assertEqual("Partagez, échangez", self.driver.title)

    def test_search_bar(self):
        """test if selected fields leads to search_page, and good response"""
        region_menu = self.driver.find_element_by_id("region-menu")
        rechercher_btn = self.driver.find_element_by_id("rechercher-btn")
        drp = Select(region_menu)
        drp.select_by_visible_text("Toute la France/Régions")
        rechercher_btn.send_keys(Keys.RETURN)
        category_tag = self.driver.find_elements_by_tag_name("h4")

        self.assertEqual(len(category_tag), 1)


class TermsPage(TestCase):
    """Tests of main page display"""

    def test_terms_page_display(self):
        response = self.client.get("/mentions_legales")
        self.assertEqual(response.status_code, 200)

class AboutPage(TestCase):
    """Tests of main page display"""

    def test_about_page_display(self):
        response = self.client.get("/A_propos")
        self.assertEqual(response.status_code, 200)
