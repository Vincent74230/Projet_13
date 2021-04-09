"""models of useraccount"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    """Added 2 fields to default user class:
    postcode and pending status"""

    postcode = models.CharField(max_length=5)
    verified_status = models.BooleanField(default=False)
    gender = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Rating(models.Model):
    """Store score people make each other and comments"""

    score_sent = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ],
    )
    score_received = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ],
    )

    # Boolean that passes to False when 2 users has rated each other
    score_pending = models.BooleanField(default=True)

    # Boolean that indicates admin to check comments before displaying it
    comment_pending = models.BooleanField(default=True)

    comment = models.CharField(max_length=200, blank=True)

    sender = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.PROTECT, default=None, related_name="receiver"
    )

    def __str__(self):
        return "Rating n°{} of user n°{}".format(self.pk, self.receiver.pk)


class Ad(models.Model):
    """Contains the ads a user can make 10 times a month"""

    advert = models.CharField(max_length=300)
    pending = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.pk)


class Category(models.Model):
    """Services category"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Services(models.Model):
    """All the services offred and required by the members"""

    name = models.CharField(max_length=100)
    proposed_services = models.ManyToManyField(User, related_name="proposed_services")
    required_services = models.ManyToManyField(User, related_name="required_services")
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.name)
