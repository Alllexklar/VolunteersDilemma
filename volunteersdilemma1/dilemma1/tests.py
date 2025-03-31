import random
import time
from otree.api import Bot, Submission
from .pages import AnimalChoice, Questionnaire1, MywaitingPage, Volunteering

class PlayerBot(Bot):
    def play_round(self):
        # Optional delay to simulate sequential arrival (in seconds)
        #time.sleep(0.1) # random.uniform(0.1, 0.5))
        
        # Randomly choose 'cat' or 'dog'
        yield AnimalChoice, dict(pet_choice=random.choices(['cat', 'dog'], weights=[0.3, 0.7])[0])

        yield Submission(MywaitingPage, {}, check_html=False)

        yield Volunteering, dict(volunteered=random.randint(0, 1))

        yield Questionnaire1, dict(satisfaction=random.randint(1, 5))


"""class PlayerBot(Bot):
    _counter = 0  # class-level variable

    def play_round(self):
        time.sleep(0.1)
        type(self)._counter += 1
        if type(self)._counter <= 75:
            pet_choice = 'cat'
        else:
            pet_choice = 'dog'
        yield Choice, dict(pet_choice=pet_choice)"""