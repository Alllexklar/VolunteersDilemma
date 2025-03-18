from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'dilemma1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    satisfaction = models.IntegerField(
        label="How satisfied are you with the experiment?",
        choices=[
            [1, 'Strongly Disagree'],
            [2, 'Disagree'],
            [3, 'Neutral'],
            [4, 'Agree'],
            [5, 'Strongly Agree']
        ],
        widget=widgets.RadioSelectHorizontal
    )


# PAGES
class test(Page):
    form_model = 'player'
    form_fields = ['satisfaction']


page_sequence = [test]
