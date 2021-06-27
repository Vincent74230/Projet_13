"""Contains class for score view"""
from .models import Rating, User

class ScoreRegistration:
    """Class that register score issued by users to note each other,
    sends mail to warn users, and then verifies if two users rated each other"""

    def __init__(self, receiver_username, sender_score_issued, sender_username):
        self.user1 = sender_username
        self.sender_score_issued = sender_score_issued
        self.user2 = receiver_username

    def score_registration_verification(self):
        print(self.user1)
        print(self.user2)
        print(self.sender_score_issued)
        user1 = User.objects.get(username=self.user1)
        user2 = User.objects.get(username=self.user2)
        score_sent = int(self.sender_score_issued)

        print (user1.pk, user2.pk)

        #first case : The user wants to note somone he has already noted
        case1 = Rating.objects.filter(sender_id=user1.pk, receiver_id=user2.pk)

        #second case : User wants to note someone who has already noted him
        case2 = Rating.objects.filter(sender_id=user2.pk, receiver_id=user1.pk)
        print(case1)
        print(case2)

        if case1 and not case2:
            print('you already have noted this guy')
            if case1[0].score_received == 0:
                print('This guy must now note you')
            else:
                print('notation complete')

        if case2 and not case1:
            print('this persone has already noted you')
            print('now registering your note to complete')
            print('passing pending score from true to false')

        if not case1 and not case2:
            print("you are the first to note this person")
            print ("registering your note")
