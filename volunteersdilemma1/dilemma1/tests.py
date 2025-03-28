import random
import time
from otree.api import Bot
from .pages import Choice, Questionnaire1

class PlayerBot2(Bot):
    def play_round(self):
        # Optional delay to simulate sequential arrival (in seconds)
        time.sleep(0.1)#random.uniform(0.1, 0.5))
        
        # Randomly choose 'cat' or 'dog'
        yield Choice, dict(pet_choice=random.choice(['cat', 'dog']))

class PlayerBot(Bot):
    def play_round(self):
        # Optional delay to simulate sequential arrival (in seconds)
        time.sleep(0.1)#random.uniform(0.1, 0.5))
        
        # Randomly choose 'cat' or 'dog'
        yield Choice, dict(pet_choice=random.choices(['cat', 'dog'], weights=[0.3, 0.7])[0])


class PlayerBot3(Bot):
    _counter = 0  # class-level variable

    def play_round(self):
        time.sleep(0.1)
        type(self)._counter += 1
        if type(self)._counter <= 75:
            pet_choice = 'cat'
        else:
            pet_choice = 'dog'
        yield Choice, dict(pet_choice=pet_choice)