"""Tests of useraccount application"""
import os
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from .models import User
from django.core import mail
from bs4 import BeautifulSoup


class UseraccountLiveTest(LiveServerTestCase):
    """tests sign in, email confirmation, login, logout"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        BASE_DIR = Path(__file__).resolve().parent.parent
        PATH = str(BASE_DIR / "webdrivers" / "chromedriver")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("window-size=1920x1080")
        cls.driver = webdriver.Chrome((PATH), options=chrome_options)
        cls.driver.get("%s%s" % (cls.live_server_url, "/useraccount/"))
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
        username.send_keys("testuserselenium1")
        postcode.send_keys("74230")
        email.send_keys("testuser1@gmail.fr")
        password1.send_keys("DellInspirion1!")
        password2.send_keys("DellInspirion1!")
        submit.send_keys(Keys.RETURN)

        user = User.objects.all()

        #let's see if user is in DB, email not confirmed and inactive
        self.assertEqual(len(user), 1)
        self.assertEqual(user[0].username, "testuserselenium1")
        self.assertEqual(user[0].verified_status, False)
        self.assertEqual(user[0].email_confirmed, False)
        self.assertEqual(user[0].is_active, False)
        self.assertEqual(len(mail.outbox), 1)

        #Retreiving url confirmation in the email html
        html_content = mail.outbox[0].alternatives[0][0]
        self.assertTrue("testuserselenium1" in html_content)
        message_html = mail.outbox[0].alternatives[0][0]
        message_html = str(message_html)
        soup = BeautifulSoup(message_html, "html.parser")
        link_list = []
        for link in soup.find_all("a", href=True):
            link_list.append(link["href"])

        clickable_link = link_list[0]
        clickable_link = str(clickable_link)

        #User is trying to connect without having confirmed email
        user = User.objects.all()
        username_on_login_page = self.driver.find_element_by_name('username')
        password_on_login_page = self.driver.find_element_by_name('password')
        username_on_login_page.send_keys("testuserselenium1")
        password_on_login_page.send_keys("DellInspirion1!")
        self.assertEqual(user[0].email_confirmed, False)
        self.assertEqual(user[0].is_active, False)

        #User is 'clicking' on the link of his mail box
        self.driver.get(clickable_link)
        user = User.objects.all()
        self.assertEqual(user[0].email_confirmed, True)
        self.assertEqual(user[0].is_active, True)

        #Before that : check if user is connected

        #User disconnects
        log_out = self.driver.find_element_by_id('deconnexion')
        log_out.send_keys(Keys.RETURN)

        #Connects with wrong password
        log_in = self.driver.find_element_by_id('connexion')
        log_in.send_keys(Keys.RETURN)
        username_on_login_page = self.driver.find_element_by_name('username')
        password_on_login_page = self.driver.find_element_by_name('password')
        username_on_login_page.send_keys("testuserselenium1")
        password_on_login_page.send_keys("Dellzopfjizf")        
        submit_btn = self.driver.find_element_by_id('login_btn')
        submit_btn.send_keys(Keys.RETURN)
        wrong_identifiers_message = self.driver.find_element_by_id('bad_identifiers').text
        self.assertEqual(wrong_identifiers_message, "Votre nom d'utilisateur ou mot de passe est incorrect")

        #Connects with right password
        username_on_login_page = self.driver.find_element_by_name('username')
        password_on_login_page = self.driver.find_element_by_name('password')
        username_on_login_page.send_keys("testuserselenium1")
        password_on_login_page.send_keys("DellInspirion1!")        
        submit_btn = self.driver.find_element_by_id('login_btn')
        submit_btn.send_keys(Keys.RETURN)
        home_page_title = self.driver.find_element_by_tag_name('h2').text
        self.assertEqual(home_page_title, 'SERVICES')
