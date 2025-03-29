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
            time.sleep(2 - elapsed)

class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteered']



page_sequence = [AnimalChoice, MywaitingPage, Questionnaire1]