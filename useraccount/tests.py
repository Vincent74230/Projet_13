"""Tests of useraccount application"""
import os
from django.test import LiveServerTestCase, TestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from .models import User, Rating
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

class ScoreRegistrationTest(TestCase):
    '''Tests of score registration'''
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

    def test_score_registration(self):
        users = User.objects.all()
        self.assertEqual(len(users), 3)

        response = self.client.get(
            "/useraccount/score",
            {
                "receiver": "AliceTest1",
            },
        )
        #User not connected, redirect to homepage
        self.assertEqual(response.status_code, 302)

        self.client.login(username='VincentTest1', password='Testpassword1')

        #Wrong user to be noted
        response = self.client.get(
            "/useraccount/score",
            {
                "receiver": "Alice",
            },
        )

        self.assertEqual(response.status_code, 302)


        response = self.client.get(
            "/useraccount/score",
            {
                "receiver": "AliceTest1",
            },
        )
        #User not connected, redirect to homepage
        self.assertEqual(response.status_code, 200)

        #Nothing in the mailbox before rating another user
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(
            "/useraccount/score?receiver=AliceTest1",
            {
                "rating_value": 5,
            },
        )

        self.assertEqual(response.status_code, 200)

        alice = User.objects.get(username='AliceTest1')

        alice_vincent_rating = Rating.objects.get(receiver_id=alice.id)

        self.assertEqual(alice_vincent_rating.score_pending, True)
        self.assertEqual(alice_vincent_rating.score_sent, 5)

        response = self.client.post(
            "/useraccount/score?receiver=AliceTest1",
            {
                "rating_value": 4,
            },
        )

        #Impossible to note another user twice
        self.assertEqual(response.status_code, 200)
        self.assertEqual(alice_vincent_rating.score_sent, 5)

        #Check if mail has been send
        self.assertEqual(len(mail.outbox), 1)

        self.client.logout()

        #Alice now noting Vincent
        self.client.login(username='AliceTest1', password='Testpassword3')

        response = self.client.post(
            "/useraccount/score?receiver=VincentTest1",
            {
                "rating_value": 4,
            },
        )

        #Check if bool switched to False, and registered score
        alice_vincent_rating = Rating.objects.get(receiver_id=alice.id)
        self.assertEqual(alice_vincent_rating.score_pending, False)
        self.assertEqual(alice_vincent_rating.score_received, 4)

        #A user cannot note himself

        response = self.client.post(
            "/useraccount/score?receiver=AliceTest1",
            {
                "rating_value": 5,
            },
        )

        all_ratings = Rating.objects.all()
        self.assertEqual(len(all_ratings),1)
        self.assertEqual(response.status_code, 302)
