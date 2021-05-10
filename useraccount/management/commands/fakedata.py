from django.core.management.base import BaseCommand
from faker import Factory
from ... import models
import random


class Command(BaseCommand):
    help = "Command that populates dev DB with fake datas"

    def handle(self, *args, **kwargs):

        models.Services.objects.all().delete()

        models.Category.objects.all().delete()

        models.Ad.objects.all().delete()

        models.Rating.objects.all().delete()

        models.User.objects.all().delete()

        fake = Factory.create('fr_FR')
        # users you want to create
        nb_users = 100

        # Services dictionnary sorted by categories
        services_dict = {
            "Cours": [
                "Cuisine",
                "Musique",
                "Informatique",
                "Langues étrangères",
                "Soutien scolaire",
                "Coaching",
            ],
            "Bricolage": [
                "Electricité",
                "Maçonnerie",
                "Menuiserie",
                "Plomberie",
                "Tapisserie",
                "Peinture",
            ],
            "Travail": [
                "Comptabilité",
                "Assistance",
                "Traduction",
                "Secrétariat",
                "Recherche d'emploi",
            ],
            "Vehicules": [
                "Entretien",
                "Location",
                "Vente",
                "Petites réparations",
                "Grosses réparations",
            ],
            "Maison": [
                "Ameublement",
                "Colocation",
                "Décoration",
                "Jardinage",
                "Gardiennage",
            ],
        }
        # just making a 1 to 100 list..
        users_rank = [0]
        for i in range(nb_users - 1):
            u = users_rank[i] + 1
            users_rank.append(u)

        # Populate User
        for _ in range(nb_users):
            genders = random.choice([True, False])
            fake_user = models.User(
                password=fake.password(),
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.ascii_email(),
                postcode=fake.postcode(),
                gender=genders,
            )
            fake_user.save()

        all_users = models.User.objects.all()

        # Populate Ad
        for _ in range(30):
            fake_ad = models.Ad(
                advert=fake.paragraph(nb_sentences=1, variable_nb_sentences=True),
                pending=random.choice([True, False]),
                date=fake.date_time(),
                user=all_users[random.randint(0, nb_users - 1)],
            )
            fake_ad.save()

        # populate Rating
        for _ in range(25):
            users = users_rank
            score_sent_temp = random.randint(0, 5)
            score_received_temp = random.randint(0, 5)
            score_pending_temp = False
            if score_sent_temp == 0 or score_received_temp == 0:
                score_pending_temp = True
            sender_temp = random.choice(users)
            users.remove(sender_temp)
            receiver_temp = random.choice(users)

            fake_rating = models.Rating(
                score_sent=score_sent_temp,
                score_received=score_received_temp,
                score_pending=score_pending_temp,
                comment_pending=random.choice([True, False]),
                comment=fake.paragraph(nb_sentences=1, variable_nb_sentences=True),
                sender=all_users[sender_temp],
                receiver=all_users[receiver_temp],
            )
            fake_rating.save()

        # Populate categories
        for category in services_dict:
            cat = models.Category(name=category)
            cat.save()

        # Populate Services
        for key, value in services_dict.items():
            for element in value:
                service_query = models.Services(
                    name=element, category=models.Category.objects.get(name=key)
                )
                service_query.save()

        # Populates proposed and required services
        # Takes randomly 2 services in 2 != categories as proposed services
        # and 2 services in 2 different categories as required services

        for user in users_rank:
            categories = random.sample(list(services_dict), 4)
            list_of_services = []
            for category in categories:
                list_of_services.append(random.sample(services_dict[category], 2))
            for i, two_services in enumerate(list_of_services):
                if i < 2:
                    for service_name in two_services:
                        service_query = models.Services.objects.get(name=service_name)
                        all_users[user].proposed_services.add(service_query)
                else:
                    for service_name in two_services:
                        service_query = models.Services.objects.get(name=service_name)
                        all_users[user].required_services.add(service_query)
