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

def generate_signs(n=10):
    # Example: pick from uppercase letters + digits
    symbols = string.ascii_letters + string.digits + "?![]@#$%^&*()_+"
    return ''.join(random.choices(symbols, k=n))

class Player(BasePlayer):
    shown_signs = models.StringField()
    answer = models.StringField(blank=True)
    total_correct = models.IntegerField(initial=0)
    skip = models.BooleanField(initial=0, blank=True)
    correct = models.StringField()

# PAGES
class Introduction(Page):
    def is_displayed(player):
        return player.round_number == 1

    def vars_for_template(player):
        return dict(
            message="Welcome to the real-effort typing task. Type the signs in reverse!"
            )

    
    @staticmethod
    def before_next_page(player, timeout_happened):
        # Pull out participant for convenience
        participant = player.participant

        # Initialize total_correct in participant.vars if it doesn't exist yet
        if "total_correct" not in participant.vars:
            participant.vars["total_correct"] = 0
            participant.vars["required_correct"] = 10
            participant.vars["finished_task"] = 0
            participant.vars["skip"] = 0

class TypingTask(Page):
    def is_displayed(player):
        return player.participant.vars["total_correct"] < player.participant.vars["required_correct"] and player.participant.vars['skip'] == 0

    form_model = "player"
    form_fields = ["answer", "skip"]

    @staticmethod
    def vars_for_template(player):
        return dict(shown_signs=player.shown_signs)

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Pull out participant for convenience
        participant = player.participant
        participant.vars["skip"] = player.skip

        # Initialize total_correct in participant.vars if it doesn't exist yet
        if "total_correct" not in participant.vars:
            participant.vars["total_correct"] = 0

        # Check correctness
        if player.answer == player.shown_signs[::-1]:
            player.payoff = cu(1)
            participant.vars["total_correct"] += 1
            player.correct = "Correct!"
        else:
            player.payoff = cu(0)
            player.correct = "Incorrect!"

class Results(Page):
    def is_displayed(player):
        return player.participant.vars['skip'] == 0

    def vars_for_template(player):
        required_correct = player.participant.vars["required_correct"]
        total_correct = player.participant.vars["total_correct"]

        return {'total_correct': total_correct,'required_correct': required_correct}
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.vars["finished_task"] = 1

page_sequence = [Introduction, TypingTask, Results]

def creating_session(subsession):
    for p in subsession.get_players():
        p.shown_signs = generate_signs(C.SIGN_COUNT)