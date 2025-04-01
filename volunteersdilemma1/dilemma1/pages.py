from otree.api import *
from .models import Player  # import models if needed by the view
import time


class Questionnaire1(Page):
    form_model = 'player'
    form_fields = ['satisfaction']

class AnimalChoice(Page):
    form_model = 'player'
    form_fields = ['pet_choice']

class MywaitingPage(Page):
    form_model = 'player'
    form_fields = []

    
    def before_next_page(self):
        start_time = time.time()

        self.subsession.assign_individual_group(self.player)

        elapsed = time.time() - start_time
        if elapsed < 3:
            pass #time.sleep(2 - elapsed)
            

class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteered']

    def before_next_page(self):
        matching_players = [
            p for p in self.group.get_players()
            if p.field_maybe_none('group_assignment') == self.player.group_assignment
        ]

        # Check if any matching player already has bonus==1.
        if any(p.field_maybe_none('payoff') == 1 for p in matching_players):
            self.player.payoff = 1
            return

        # Determine bonus based on whether any matching player's volunteered field equals 1.
        bonus_payout = 1 if any(p.field_maybe_none('volunteered') == 1 for p in matching_players) else 0

        # Set bonus for all matching players.
        for p in matching_players:
            p.payoff = bonus_payout

class Task(Page):
    pass


page_sequence = [AnimalChoice, MywaitingPage, Volunteering, Task, Questionnaire1]