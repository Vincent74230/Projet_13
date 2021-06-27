"""Contains class for score view"""
from .models import Rating, User

class ScoreRegistration:
    """Class that register score issued by users to note each other,
    sends mail to warn users, and then verifies if two users rated each other"""

    def __init__(self, receiver_username, sender_score_issued, sender_username):
        self.user1 = sender_username
        self.sender_score_issued = sender_score_issued
        self.user2 = receiver_username
        self.score_status = ''

    def score_status_verification(self):
        user1 = User.objects.get(username=self.user1)
        user2 = User.objects.get(username=self.user2)
        score_sent = int(self.sender_score_issued)

        #first case : The user wants to note somone he has already noted
        case1 = Rating.objects.filter(sender_id=user1.pk, receiver_id=user2.pk)

        #second case : User wants to note someone who has already noted him
        case2 = Rating.objects.filter(sender_id=user2.pk, receiver_id=user1.pk)

        if case1 and not case2:
            if case1[0].score_received == 0:
                self.score_status = 'Vous avez déjà noté cette personne, elle doit maintenant vous noter en retour'
            else:
                self.score_status = 'Vous avez noté cette personne, elle a répondu, notation complète'

        if case2 and not case1:
            if case2[0].score_received == 0:
                self.score_status = 'Cette personne vous a déjà noté, nous enregistrons votre note envers elle'
            else:
                self.score_status = 'Cette personne vous a noté, vous avez déjà répondu, notation complète'

        if not case1 and not case2:
            self.score_status = "Vous êtes le premier à noter cette personne, nous enregistrons votre note"
