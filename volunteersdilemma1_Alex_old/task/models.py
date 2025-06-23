from otree.api import *

class C(BaseConstants):
    NAME_IN_URL = 'typing_backwards'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 50
    SIGN_COUNT = 10
    REQUIRED_CORRECT = 10

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    shown_signs     = models.StringField()
    answer          = models.StringField(blank=True)
    correct_answer  = models.StringField(blank=True)
    total_correct   = models.IntegerField(initial=0)
    skip            = models.BooleanField(initial=0, blank=True)
    correct         = models.StringField()
    finished        = models.BooleanField(initial=0, blank=True)