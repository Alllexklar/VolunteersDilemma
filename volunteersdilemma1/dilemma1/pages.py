from otree.api import *
import time
import string
import random


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return dict(
            message="Welcome to the real-effort typing task. Type the signs in reverse!"
            )

    def before_next_page(self):
        # Pull out participant for convenience
        participant = self.participant

        # Initialize total_correct in participant.vars if it doesn't exist yet
        if "total_correct" not in participant.vars:
            participant.vars["total_correct"] = 0
            participant.vars["required_correct"] = 5
            participant.vars["finished_task"] = 0
            participant.vars["skip"] = 0

class AnimalChoice(Page):
    form_model = 'player'
    form_fields = ['pet_choice']

    def is_displayed(self):
        return self.round_number == 1

class FunFact(Page):
    form_model = 'player'
    form_fields = []

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        if self.player.pet_choice == 'cat':
            top_text = "You're a cat person!"
            img_src = 'dilemma1/images/cat.png'
            fun_fact = "Cats have a special collarbone that allows them to always land on their feet."
        else:
            top_text = "You're a dog person!"
            img_src = 'dilemma1/images/dog.png'
            fun_fact = "Dogs have a sense of time and can predict future events."

        return {
            "top_text": top_text,
            "img_src": img_src,
            "fun_fact": fun_fact,
        }

class MywaitingPage(Page):
    form_model = 'player'
    form_fields = []

    def is_displayed(self):
        return self.round_number == 1

    
    def before_next_page(self):
        start_time = time.time()

        self.subsession.assign_individual_group(self.player)

        elapsed = time.time() - start_time
        if elapsed < 3:
            pass #time.sleep(2 - elapsed)
            

class Volunteering(Page):
    form_model = 'player'
    form_fields = ['volunteered']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

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




class TypingTask(Page):
    def is_displayed(self):
        return (
            self.player.participant.vars["total_correct"]
            < self.player.participant.vars["required_correct"]
            and self.player.participant.vars['skip'] == 0
            and self.player.volunteered == 1 # if not volunteered, skip the task
        ) 

    form_model = "player"
    form_fields = ["answer", "skip"]

    def vars_for_template(self):
        new_signs = self.generate_signs(2)
        self.player.shown_signs = new_signs
        return dict(shown_signs=new_signs)

    def before_next_page(self):
        # Pull out participant for convenience
        participant = self.player.participant
        participant.vars["skip"] = self.player.skip

        # Initialize total_correct in participant.vars if it doesn't exist yet
        if "total_correct" not in participant.vars:
            participant.vars["total_correct"] = 0

        # Check correctness
        if self.player.answer == self.player.shown_signs[::-1]:
            self.player.payoff = cu(1)
            participant.vars["total_correct"] += 1
            self.player.correct = "Correct!"
        else:
            self.player.payoff = cu(0)
            self.player.correct = "Incorrect!"

    def generate_signs(self, n=10):
        # Example: pick from uppercase letters + digits
        symbols = string.ascii_letters + string.digits + "?![]@#$%&*()_+"
        return ''.join(random.choices(symbols, k=n))

class Questionnaire1(Page):
    form_model = 'player'
    form_fields = ['satisfaction']


page_sequence = [Introduction, AnimalChoice, FunFact, MywaitingPage, Volunteering, TypingTask, Questionnaire1]

