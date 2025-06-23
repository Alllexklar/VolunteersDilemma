from otree.api import *
import time
import string
import random
from .models import *


class Introduction(Page):
    pass

class DemographicQuestions(Page):
    form_model = 'player'
    form_fields = ['age','gender_identity']

class AnimalChoice(Page):
    form_model = 'player'
    form_fields = ['pet_balance']
    
    def before_next_page(self):
        if self.player.pet_balance < 200:
            self.player.pet_choice = 'cat'
            self.player.participant.vars['pet_choice'] = 'cat'
        elif self.player.pet_balance > 200:
            self.player.pet_choice = 'dog'
            self.player.participant.vars['pet_choice'] = 'dog'
        else:
            print("Error: pet_balance is 200. This should not happen.")

class FunFact(Page):
    form_model = 'player'
    form_fields = []

    def vars_for_template(self):
        if self.player.pet_choice == 'cat':
            top_text = "You're a cat person!"
            img_src = 'dilemma1/images/cat.png'
            fun_fact = "Fun fact: Cats can sleep between 12 - 18 hours per day."
        else:
            top_text = "You're a dog person!"
            img_src = 'dilemma1/images/dog.png'
            fun_fact = "Fun fact: A dog's nose print is unique, much like a person's fingerprint."

        return {
            "top_text": top_text,
            "img_src": img_src,
            "fun_fact": fun_fact,
        }

class MywaitingPage(Page):
    form_model = 'player'
    form_fields = []

    
    def before_next_page(self):
        start_time = time.time()

        self.subsession.assign_individual_group(self.player)

        elapsed = time.time() - start_time
        if elapsed < 3:
            pass #time.sleep(2 - elapsed)
            
class GroupPage(Page):

    def vars_for_template(self):
        self.player.participant.vars["group_assignment"] = self.player.group_assignment
        if "control" in self.player.group_assignment:
            return {
            "self_image_src": 'dilemma1/images/blank.png',
            "player_a_img_src": 'dilemma1/images/blank.png',
            "player_b_img_src": 'dilemma1/images/blank.png',
            "msg": "You have been placed in a group two other participants",
        }



        # Decide which image to display
        self_image_src = f'dilemma1/images/{self.player.pet_choice}.png'
        opposite_src = 'dilemma1/images/dog.png' if self.player.pet_choice == 'cat' else 'dilemma1/images/cat.png'

        oppdict = {
            'cat': 'dog',
            'dog': 'cat'
        }
        
        if self.player.pet_choice in self.player.group_assignment:
            player_a_img_src = opposite_src
            player_b_img_src = opposite_src
            self.player.img_position = "none"
            msg = f'You have been placed in a group with two {oppdict[self.player.pet_choice]} lovers.'
        else:
            msg = f'You have been placed in a group with one {self.player.pet_choice} lover and one {oppdict[self.player.pet_choice]} lover.'

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
            "msg": msg,
        }

class Instructions(Page):
    pass

class ComprehensionQuestions(Page):
    form_model = 'player'
    form_fields = ['cc1', 'cc2', 'cc3', 'cc4', 'cc5']

    CORRECT_ANSWERS = {
        'cc1': 'C',
        'cc2': 'A',
        'cc3': 'B',
        'cc4': 'C',
        'cc5': 'B'
    }

    def error_message(self, values):
        """
        If you return a dict like {'cc2': 'nope'} then
        that error will be shown under cc2 and the page
        won’t advance. Only when this returns {} does
        the user move on.
        """
        errors = {}
        for field, answer in values.items():
            correct = self.CORRECT_ANSWERS[field]
            if answer != correct:
                errors[field] = (
                    f"“{answer}” is not correct - please review the instructions and try again."
                )
        return errors

class DecisionPage(Page):
    form_model = 'player'
    form_fields = ['volunteered']

    def vars_for_template(self):
        


        oppdict = {
            'cat': 'dog',
            'dog': 'cat'
        }


        # Decide which image to display
        self_image_src = f'dilemma1/images/{self.player.pet_choice}.png'
        opposite_src = 'dilemma1/images/dog.png' if self.player.pet_choice == 'cat' else 'dilemma1/images/cat.png'
        
        if self.player.pet_choice in self.player.group_assignment:
            player_a_img_src = opposite_src
            player_b_img_src = opposite_src
            msg = f'You are in a group with two {oppdict[self.player.pet_choice]} lovers.'
        
        elif self.player.img_position == "left":
            player_a_img_src = self_image_src
            player_b_img_src = opposite_src
            msg = f'You are in a group with one {self.player.pet_choice} lover and one {oppdict[self.player.pet_choice]} lover.'
        elif self.player.img_position == "right":
            player_a_img_src = opposite_src
            player_b_img_src = self_image_src
            msg = f'You are in a group with one {self.player.pet_choice} lover and one {oppdict[self.player.pet_choice]} lover.'
        else:
            print("Error: img_position is not set. This should not happen.")

        return {
            "self_image_src": self_image_src,
            "player_a_img_src": player_a_img_src,
            "player_b_img_src": player_b_img_src,
            "msg": msg,
        }
    
    def before_next_page(self):
        self.player.participant.vars["volunteered"] = self.player.volunteered


page_sequence = [
    Introduction, 
    DemographicQuestions,
    AnimalChoice, 
    FunFact, 
    MywaitingPage, 
    GroupPage, 
    Instructions,
    ComprehensionQuestions,
    DecisionPage,
]

