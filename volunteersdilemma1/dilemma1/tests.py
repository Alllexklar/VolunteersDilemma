import random
import time
from otree.api import Bot
from .pages import Choice, Questionnaire1

class PlayerBot(Bot):
    def play_round(self):
        # Optional delay to simulate sequential arrival (in seconds)
        time.sleep(random.uniform(0.1, 0.2))
        
        # Randomly choose 'cat' or 'dog'
        yield Choice, dict(pet_choice=random.choice(['cat', 'dog']))
        
        # Randomly choose satisfaction level from 1 to 7
        yield Questionnaire1, dict(satisfaction=random.randint(1, 5))
