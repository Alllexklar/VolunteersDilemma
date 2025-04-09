from otree.api import *
from .models import Player  # import models if needed by the view
import time
import requests
from otree.settings import RECAPTCHA_SECRET_KEY, RECAPTCHA_SITE_KEY
import random


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

    def vars_for_template(self):

        print(self.player.group_assignment)
        # Decide which image to display
        self_image_src = f'dilemma1/images/{self.player.pet_choice}.png'
        opposite_src = 'dilemma1/images/dog.png' if self.player.pet_choice == 'cat' else 'dilemma1/images/cat.png'
        
        if self.player.pet_choice in self.player.group_assignment:
            player_a_img_src = opposite_src
            player_b_img_src = opposite_src
            self.player.img_position = "none"
        else:
            # randomly assign images for player A and B
            if random.random() < 0.5:
                player_a_img_src = self_image_src
                player_b_img_src = opposite_src
                self.player.img_position = "left"
            else:
                player_a_img_src = opposite_src
                player_b_img_src = self_image_src
                self.player.img_position = "right"

        return {
            "self_image_src": self_image_src,
            "player_a_img_src": player_a_img_src,
            "player_b_img_src": player_b_img_src,
        }

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


def recaptcha_valid(response_token):
    res = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response_token
    })
    return res.json()["success"]

class Task(Page):
    def is_displayed(self):
        return self.player.volunteered == 1

    def vars_for_template(player: Player):
        return {
            "RECAPTCHA_SITE_KEY": RECAPTCHA_SITE_KEY
        }

    def live_method(player: Player, data):
        if recaptcha_valid(data["response_token"]):
            player.is_human = True

    """@staticmethod
    def error_message(player, values):
        if not player.is_human:
            return 'You did not solve the captcha.'"""


page_sequence = [AnimalChoice, MywaitingPage, Volunteering, Task, Questionnaire1]