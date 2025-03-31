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
            #time.sleep(2 - elapsed)
            pass

class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteered']

    def before_next_page(self):
        bonus = False

        matching_players = [p for p in self.group.get_players() if p.group_assigned == self.player.group_assigned]
        for p in matching_players:
            if p.volunteered == 1:
                bonus = True
                break
        
        if bonus:
            for p in matching_players:
                p.bonus = 1
        else:
            for p in matching_players:
                p.bonus = 0


page_sequence = [AnimalChoice , MywaitingPage, Volunteering, Questionnaire1]