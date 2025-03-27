from otree.api import *
from .models import Player  # import models if needed by the view


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['satisfaction']

class Choice(Page):
    form_model = 'player'
    form_fields = ['pet_choice']

    def before_next_page(self):
        self.subsession.assign_individual_group(self.player)

page_sequence = [Choice]