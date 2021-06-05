"""Tests of useraccount application"""
import os
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from .models import User
from django.core import mail


class UseraccountLiveTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BASE_DIR = Path(__file__).resolve().parent.parent
        PATH = str(BASE_DIR / "webdrivers" / "chromedriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=1920x1080')
        cls.driver = webdriver.Chrome((PATH), options=chrome_options)
        cls.driver.get('%s%s' % (cls.live_server_url, '/useraccount/'))
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_useraccount_display(self):
        """see if page displays ok"""
        self.assertEqual("Partagez, échangez", self.driver.title)

    def test_useraccount_post(self):
        """Tests user registration and email checking"""
        username = self.driver.find_element_by_id("id_username")
        postcode = self.driver.find_element_by_id("id_postcode")
        email = self.driver.find_element_by_id("id_email")
        password1 = self.driver.find_element_by_id("id_password1")
        password2 = self.driver.find_element_by_id("id_password2")
        submit = self.driver.find_element_by_name("create_user")
        username.send_keys('testuserselenium1')
        postcode.send_keys('74230')
        email.send_keys('testuser1@gmail.fr')
        password1.send_keys('DellInspirion1!')
        password2.send_keys('DellInspirion1!')
        submit.send_keys(Keys.RETURN)

        user = User.objects.all()

        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].username, 'testuserselenium1')
        self.assertEqual(user[0].verified_status, False)
        self.assertEqual(user[0].email_confirmed, False)
        self.assertEqual(user[0].is_active, False)
        self.assertEqual(len(mail.outbox), 1)
        html_content = mail.outbox[0].alternatives[0][0]
        self.assertTrue("testuserselenium1" in html_content)
        print (mail.outbox[0].alternatives[0][0])
