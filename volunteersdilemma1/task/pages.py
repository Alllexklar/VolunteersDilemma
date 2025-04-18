from otree.api import *


class TypingTask(Page):
    form_model = "player"
    form_fields = ["answer", "skip"]

    def is_displayed(self):
        if "total_correct" not in self.player.participant.vars:
            self.player.participant.vars["total_correct"] = 0
            self.player.participant.vars["required_correct"] = 10
            self.player.participant.vars["finished_task"] = 0
            self.player.participant.vars["skip"] = 0

        return (
            self.player.participant.vars["total_correct"] 
            < self.player.participant.vars["required_correct"] 
            and self.player.participant.vars['skip'] == 0)

    def vars_for_template(self):
        return dict(shown_signs=self.player.shown_signs)

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
    def is_displayed(player):
        return player.participant.vars['skip'] == 0

    def vars_for_template(player):
        required_correct = player.participant.vars["required_correct"]
        total_correct = player.participant.vars["total_correct"]

        return {'total_correct': total_correct,'required_correct': required_correct}
    
    def before_next_page(self):
        self.player.participant.vars["finished_task"] = 1

page_sequence = [
    TypingTask, 
    Results
    ]