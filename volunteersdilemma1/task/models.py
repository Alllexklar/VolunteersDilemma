from otree.api import *
import random
import string

class C(BaseConstants):
    NAME_IN_URL = 'typing_backwards'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 100
    SIGN_COUNT = 10

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

def generate_signs():
    # Example: pick from uppercase letters + digits
    symbols = (
            string.ascii_letters.replace('l', '').replace('I', '') +
            string.digits +
            "?![]@#$%&*()_+"
        )
    return ''.join(random.choices(symbols, k=C.SIGN_COUNT))

class Player(BasePlayer):
    shown_signs     = models.StringField(default=generate_signs)
    answer          = models.StringField(blank=True)
    correct_answer  = models.StringField(blank=True)
    total_correct   = models.IntegerField(initial=0)
    skip            = models.BooleanField(initial=0, blank=True)
    correct         = models.StringField()