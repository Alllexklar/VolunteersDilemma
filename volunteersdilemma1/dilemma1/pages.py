from otree.api import *
import time
import string
import random
from .models import *


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class DemographicQuestions(Page):
    form_model = 'player'
    form_fields = ['age','gender_identity', 'gender_other_input']

    def is_displayed(self):
        return self.round_number == 1

class AnimalChoice(Page):
    form_model = 'player'
    form_fields = ['pet_balance']

    def is_displayed(self):
        return self.round_number == 1
    
    def before_next_page(self):
        if self.player.pet_balance < 200:
            self.player.pet_choice = 'cat'
        elif self.player.pet_balance > 200:
            self.player.pet_choice = 'dog'
        else:
            print("Error: pet_balance is 200. This should not happen.")

class FunFact(Page):
    form_model = 'player'
    form_fields = []

    def is_displayed(self):
        return self.round_number == 1

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

    def is_displayed(self):
        return self.round_number == 1

    
    def before_next_page(self):
        start_time = time.time()

        self.subsession.assign_individual_group(self.player)

        elapsed = time.time() - start_time
        if elapsed < 3:
            pass #time.sleep(2 - elapsed)
            
class GroupPage(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
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
    def is_displayed(self):
        return self.round_number == 1

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

    def is_displayed(self):
        return self.round_number == 1

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

    
    def is_displayed(self):
        return self.round_number == 1

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
        print(self.player.volunteered)
        participant = self.player.participant
        if "total_correct" not in participant.vars:
            participant.vars["total_correct"] = 0
            participant.vars["required_correct"] = 5
            participant.vars["finished_task"] = 0
            participant.vars["skip"] = 0

class TypingTask(Page):
    form_model = "player"
    form_fields = ["answer", "skip"]


    def is_displayed(self):
        print(self.player.participant.vars["total_correct"] < self.player.participant.vars["required_correct"])
        print(self.player.participant.vars['skip'] == 0)
        print(self.player.volunteered == 1)

        return (
            self.player.participant.vars["total_correct"]
            < self.player.participant.vars["required_correct"]
            and self.player.participant.vars['skip'] == 0
            #and self.player.volunteered == 1 # if not volunteered, skip the task
        ) 

    

    def vars_for_template(self):
        new_signs = self.generate_signs(10)
        self.player.shown_signs = new_signs
        return dict(shown_signs=new_signs)

    def before_next_page(self):
        # Pull out participant for convenience
        participant = self.player.participant
        participant.vars["skip"] = self.player.skip
        self.player.correct_answer = self.player.shown_signs[::-1]

        # Initialize total_correct in participant.vars if it doesn't exist yet
        if "total_correct" not in participant.vars:
            participant.vars["total_correct"] = 0

        # Check correctness
        if self.player.answer == self.player.shown_signs[::-1]:
            participant.vars["total_correct"] += 1
            self.player.correct = "Correct!"
        else:
            self.player.payoff = cu(0)
            self.player.correct = "Incorrect!"

    def generate_signs(self, n=10):
        # Example: pick from uppercase letters + digits
        symbols = (
            string.ascii_letters.replace('l', '').replace('I', '') +
            string.digits +
            "?![]@#$%&*()_+"
        )
        return ''.join(random.choices(symbols, k=n))
    
    def handle_payoff(self):
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

class Questionnaire1(Page):
    form_model = 'player'
    form_fields = ['mpc1', 'mpc2', 'mpc3', 'mpc4', 'mpc5', 'mpc6', 'mpc7']
    
    def vars_for_template(self):
        oppdict = {
            'cat': 'dog',
            'dog': 'cat'
        }

        questions = {
            "mpc1": f"As a {self.player.pet_choice} lover, I felt I was on my own within my 3-person group.",
            "mpc2": "I felt I had something in common with the 2 other members of my group.",
            "mpc3": "I feel positively about people with my animal preference.",
            "mpc4": f"I feel negatively about people with {oppdict[self.player.pet_choice]} preference.",
            "mpc5": "I believe the preference for cats/dogs reveals something meaningful about people.",
            "mpc6": f"As a {self.player.pet_choice} lover, I felt I had a high status within my 3-person group.",
            "mpc7": f"As a {self.player.pet_choice} lover, I felt I had a low status within my 3-person group."
        }
        return {"questions": questions}

class Questionnaire2(Page):
    form_model = 'player'
    form_fields = [
        'stq1', 'stq2', 'stq3', 'stq4', 'stq5', 'stq6', 'stq7', 'stq8', 'stq9', 'stq10',
        'stq11', 'stq12', 'stq13', 'stq14', 'stq15', 'stq16', 'stq17', 'stq18', 'stq19', 'stq20',
        'stq21', 'stq22', 'stq23', 'stq24'
    ]
    
    def vars_for_template(self):
        questions = {
            "stq1": "I often put other people's needs before my own.",
            "stq2": "I find it difficult to be separated from people I love.",
            "stq3": "I am very sensitive to the effects I have on the feelings of other people.",
            "stq4": "I am very sensitive to criticism by others.",
            "stq5": "I worry a lot about hurting or offending other people.",
            "stq6": "It is hard for me to break off a relationship even if it is making me unhappy.",
            "stq7": "I am easily persuaded by others.",
            "stq8": "I try to please other people too much.",
            "stq9": "I find it difficult if I have to be alone all day.",
            "stq10": "I often feel responsible for solving other people's problems.",
            "stq11": "It is very hard for me to get over the feeling of loss when a relationship has ended.",
            "stq12": "It is very important to me to be liked or admired by others.",
            "stq13": "I feel I have to be nice to other people.",
            "stq14": "I like to be certain that there is somebody close I can contact in case something unpleasant happens to me.",
            "stq15": "I am too apologetic to other people.",
            "stq16": "I am very concerned with how people react to me.",
            "stq17": "I get very uncomfortable when I'm not sure whether or not someone likes me.",
            "stq18": "It is hard for me to say 'no' to other people's requests.",
            "stq19": "I become upset when something happens to me and there's nobody around to talk to.",
            "stq20": "I am most comfortable when I know my behavior is what others expect of me.",
            "stq21": "I often let people take advantage of me.",
            "stq22": "I become very upset when a friend breaks a date or forgets to call me as planned.",
            "stq23": "I judge myself based on how I think others feel about me.",
            "stq24": "It is hard for me to let people know when I am angry with them."
        }
        return {"questions": questions}

class Questionnaire3(Page):
    form_model = 'player'
    form_fields = ['bfp1', 'bfp2', 'bfp3', 'bfp4', 'bfp5', 'bfp6', 'bfp7', 'bfp8', 'bfp9', 'bfp10', 'bfp11']
    
    def vars_for_template(self):
        questions = {
            "bfp1": "...is reserved.",
            "bfp2": "...is generally trusting.",
            "bfp3": "...tends to be lazy.",
            "bfp4": "...is relaxed, handles stress well.",
            "bfp5": "...has few artistic interests.",
            "bfp6": "...is outgoing, sociable.",
            "bfp7": "...tends to find fault with others.",
            "bfp8": "...does a thorough job.",
            "bfp9": "...gets nervous easily.",
            "bfp10": "...has an active imagination.",
            "bfp11": "...is sometimes rude to others."
        }
        return {"questions": questions}


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
    TypingTask, 
    #Questionnaire1, 
    #Questionnaire2, 
    #Questionnaire3,
]

