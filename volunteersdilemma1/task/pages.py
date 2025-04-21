from otree.api import *
from .models import C

import random
import string


def generate_signs():
    print("🖋️  Generating a new shown_signs")
    # Example: pick from uppercase letters + digits
    symbols = (
            string.ascii_letters.replace('l', '').replace('I', '') +
            string.digits +
            "?![]@#$%&*()_+"
        )
    return ''.join(random.choices(symbols, k=C.SIGN_COUNT))

class TypingTask(Page):
    form_model = "player"
    form_fields = ["answer", "skip"]

    def is_displayed(self):
        if "total_correct" not in self.player.participant.vars:
            self.player.participant.vars["total_correct"] = 0
            self.player.participant.vars["required_correct"] = C.REQUIRED_CORRECT
            self.player.participant.vars["finished_task"] = 0
            self.player.participant.vars["skip"] = 0

        return (
            self.player.participant.vars["total_correct"] 
            < self.player.participant.vars["required_correct"] 
            and self.player.participant.vars['skip'] == 0
            and self.player.participant.vars.get('volunteered') == 1
            )

    def vars_for_template(self):
        var = generate_signs()
        self.player.shown_signs = var

        return dict(shown_signs=var)

    def before_next_page(self):
        # Pull out participant for convenience
        participant = self.player.participant
        participant.vars["skip"] = self.player.skip
        self.player.correct_answer = self.player.shown_signs[::-1]

        # Initialize total_correct in participant.vars if it doesn't exist yet
        if "total_correct" not in participant.vars:
            participant.vars["total_correct"] = 0

        # Check correctness
        if self.player.answer == self.player.correct_answer:
            self.player.payoff = cu(1)
            participant.vars["total_correct"] += 1
            self.player.correct = "Correct!"
        else:
            self.player.payoff = cu(0)
            self.player.correct = "Incorrect!"

class Results(Page):
    def is_displayed(self):
        return (
            self.player.participant.vars['skip'] == 0
            and self.player.participant.vars.get('volunteered') == 1
            )

    def vars_for_template(player):
        required_correct = player.participant.vars["required_correct"]
        total_correct = player.participant.vars["total_correct"]

        return {
                'total_correct': total_correct,
                'required_correct': required_correct,
                'correct': player.player.correct,
            }
    
    def before_next_page(self):
        self.player.participant.vars["finished_task"] = 1

    def app_after_this_page(self, upcoming_apps):
        # your condition for stopping early
        if self.player.participant.vars["total_correct"] == self.player.participant.vars["required_correct"] :
            # mark that we’re skipping so later pages know
            self.player.finished = 1
            # upcoming_apps is a list of the remaining app names in order.
            # returning the first item means “go to the very next app”.
            return upcoming_apps[0]          # ← jump to next app

page_sequence = [
    TypingTask, 
    Results
    ]