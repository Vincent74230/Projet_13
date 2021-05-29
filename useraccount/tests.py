"""Tests of useraccount application"""
import os
from django.test import LiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome


class ClasseDuTest(LiveServerTestCase):
    fixtures = [] # à remplir au besoin

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = Chrome()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_nom_du_test(self):
        """
            La docstring expliquant le but du test et la User Story
        """
        self.browser.get(os.path.join(self.live_server_url, 'http://127.0.0.1:8000'))
        self.assertEqual("Partagez, échangez", self.browser.title)






'''
from pathlib import Path
from django.test import TestCase, LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from .models import User


class TestRegistrationAndEmailValidation(LiveServerTestCase):
    """Live test of new user registration and email validation """

    def setUp(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        PATH = str(BASE_DIR / "webdrivers" / "chromedriver")

        #Options for chrome testing:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=1920x1080')

        self.driver = webdriver.Chrome((PATH), options=chrome_options)
        self.driver.get("http://127.0.0.1:8000")

    def test_useraccount_title_page(self):
        """Testing useraccount_page_display"""
        self.assertEqual("Partagez, échangez", self.driver.title)

    def tearDown(self):
        self.driver.close()



class SignUpTest(TestCase):
    """Sign up page tests"""

    def test_sign_up_page(self):
        response = self.client.get("/useraccount/")
        self.assertEqual(response.status_code, 200)


    def test_sign_in_post(self):
        """Tests if usercreationform is ok"""
        response = self.client.post(reverse('useraccount:index'),
            {
                "username": "Vincent74",
                "email": "vince@gmail.com",
                "password1": "DellInspirion1!",
                "password2": "DellInspirion1!",
                "postcode":"74230",
            },
        )

        self.assertRedirects(response, '/useraccount/login', status_code=302, target_status_code=200)

        users = User.objects.all()
        self.assertEqual (len(users), 1)
        self.assertEqual(users[0].username, 'Vincent74')
'''