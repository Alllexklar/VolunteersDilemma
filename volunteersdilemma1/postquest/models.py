from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'postquest'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Manipulation check questions, 1-7 likert scale "strongly disagree" to "strongly agree"
    mpc1 = models.IntegerField()
    mpc2 = models.IntegerField()
    mpc3 = models.IntegerField()
    mpc4 = models.IntegerField()
    mpc5 = models.IntegerField()
    mpc6 = models.IntegerField()
    mpc7 = models.IntegerField()

    # Sociotrophy questionnaire, 1-6 likert scale "strongly disagree" to "strongly agree"
    stq1 = models.IntegerField()
    stq2 = models.IntegerField()
    stq3 = models.IntegerField()
    stq4 = models.IntegerField()
    stq5 = models.IntegerField()
    stq6 = models.IntegerField()
    stq7 = models.IntegerField()
    stq8 = models.IntegerField()
    stq9 = models.IntegerField()
    stq10 = models.IntegerField()
    stq11 = models.IntegerField()
    stq12 = models.IntegerField()
    stq13 = models.IntegerField()
    stq14 = models.IntegerField()
    stq15 = models.IntegerField()
    stq16 = models.IntegerField()
    stq17 = models.IntegerField()
    stq18 = models.IntegerField()
    stq19 = models.IntegerField()
    stq20 = models.IntegerField()
    stq21 = models.IntegerField()
    stq22 = models.IntegerField()
    stq23 = models.IntegerField()
    stq24 = models.IntegerField()

    # Big Five Personality questionnaire, 1-5 likert scale "strongly disagree" to "strongly agree"
    bfp1 = models.IntegerField()
    bfp2 = models.IntegerField()
    bfp3 = models.IntegerField()
    bfp4 = models.IntegerField()
    bfp5 = models.IntegerField()
    bfp6 = models.IntegerField()
    bfp7 = models.IntegerField()
    bfp8 = models.IntegerField()
    bfp9 = models.IntegerField()
    bfp10 = models.IntegerField()
    bfp11 = models.IntegerField()
