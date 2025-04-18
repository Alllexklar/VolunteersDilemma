import os
import string
import random
import redis
import json
import fakeredis
from otree.api import *
from dotenv import load_dotenv


load_dotenv()


doc = """
Your app description
"""

USE_FAKEREDIS = os.environ.get('USE_FAKEREDIS', 'false').lower() == 'true'

if USE_FAKEREDIS:
    import fakeredis
    print("Using FakeRedis for testing.")
    redis_client = fakeredis.FakeStrictRedis()
    
    # Monkey-patch the release function used in Lock.
    def fake_do_release(self, expected_token):
        self.redis.delete(self.name)
        return True
    redis.lock.Lock.do_release = fake_do_release

else:
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    print(f"Connecting to Redis at {redis_url}")
    try:
        redis_client = redis.from_url(
            redis_url,
            ssl_cert_reqs=None,
        )
    except redis.ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")
        redis_client = None



class C(BaseConstants):
    NAME_IN_URL = 'dilemma1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):

    def assign_individual_group(self, player):
        """
        Assigns an individual player to a group based on their pet choice.
        
        For players who have made a pet choice:
          • Increments the counter for that pet type.
          • If the count is <= 75, assign using the pet-choice rule:
              - For a cat player: if (cat_count mod 3 == 1) then 'cat_minority'
                (i.e. the lone cat) else 'dog_minority' (i.e. majority cat).
              - For a dog player: if (dog_count mod 3 == 1) then 'dog_minority'
                else 'cat_minority'.
          • If the count > 75 for that pet type, assign to the control condition.
          
        Then the function assigns the player into an (incomplete) group. Each
        group (across all conditions) has a global 'my_group_id' so that you can
        have a unique integer group index across the study.
        
        A safety check prevents adding more than one minority pet to a minority group.
        
        The grouping data (counters, lists of groups, and ID trackers) are stored
        in Redis and updated atomically within a Redis lock.
        """
        minority_condition_count = 75  # Number of players in minority condition before switching to control.

        # Compose unique Redis keys for grouping data and locking, based on session.pk.
        grouping_key = f"dilemma1:{self.session.code}:grouping_data"
        lock_key = f"dilemma1:{self.session.code}:grouping_lock"

        # Use Redis lock to ensure that this block is executed exclusively.
        with redis_client.lock(lock_key, timeout=360, blocking=True):
            # Get the current grouping data from Redis (stored as JSON).
            data_str = redis_client.get(grouping_key)
            if not data_str:
                # Initialize grouping data if it doesn't already exist.
                data = {
                    'grouping': {
                        'cat_minority': [],   # Each group is a dict: 
                        # {'group_id': int, 'my_group_id': int, 'condition': str,
                        #  'cat_count': int, 'dog_count': int, 'players': [...]}
                        'dog_minority': [],
                        'control': []
                    },
                    'cat_count': 0,
                    'dog_count': 0,
                    'control_count': 0,
                    # Trackers for condition-specific group IDs
                    'next_cat_minority_group': 1,
                    'next_dog_minority_group': 1,
                    'next_control_group': 1,
                    # Global tracker for overall unique group ID
                    'next_global_group_id': 1
                }
            else:
                data = json.loads(data_str)

            # Determine the condition based on pet_choice and update counters.
            if player.pet_choice == 'cat':
                data['cat_count'] += 1
                count = data['cat_count']
                if count <= minority_condition_count:
                    # For cat players in pet-choice phase:
                    # Every first cat in a block of 3 => cat_minority; otherwise dog_minority.
                    condition = 'cat_minority' if (count % 3 == 1) else 'dog_minority'
                else:
                    condition = 'control'
            elif player.pet_choice == 'dog':
                data['dog_count'] += 1
                count = data['dog_count']
                if count <= minority_condition_count:
                    # For dog players in pet-choice phase:
                    # Every first dog in a block of 3 => dog_minority; otherwise cat_minority.
                    condition = 'dog_minority' if (count % 3 == 1) else 'cat_minority'
                else:
                    condition = 'control'
            else:
                # Fallback if pet_choice is missing (assign to control).
                condition = 'control'

            # Attempt to assign the player to an existing incomplete group for that condition.
            groups = data['grouping'][condition]
            assigned = False

            for group in groups:
                if len(group['players']) < 3:
                    if group['condition'] == 'cat_minority':
                        # For a 'cat_minority' group:
                        if player.pet_choice == 'cat':
                            if group['cat_count'] >= 1:
                                continue
                        else:  # player.pet_choice == 'dog'
                            if group['dog_count'] >= 2:
                                continue
                    elif group['condition'] == 'dog_minority':
                        # For a 'dog_minority' group:
                        if player.pet_choice == 'dog':
                            if group['dog_count'] >= 1:
                                continue
                        else:  # player.pet_choice == 'cat'
                            if group['cat_count'] >= 2:
                                continue

                    # If the checks pass, add the player.
                    group['players'].append(player.id_in_subsession)
                    if player.pet_choice == 'cat':
                        group['cat_count'] += 1
                    elif player.pet_choice == 'dog':
                        group['dog_count'] += 1

                    # Assign player's group identifiers.
                    player.group_assignment = f"{condition}_{group['group_id']}"
                    player.my_group_id = group['my_group_id']
                    assigned = True
                    break

            # If no incomplete group was found, create a new one.
            if not assigned:
                if condition == 'cat_minority':
                    group_id = data['next_cat_minority_group']
                    data['next_cat_minority_group'] += 1
                elif condition == 'dog_minority':
                    group_id = data['next_dog_minority_group']
                    data['next_dog_minority_group'] += 1
                else:  # 'control'
                    group_id = data['next_control_group']
                    data['next_control_group'] += 1

                # Allocate a global group ID.
                my_group_id = data['next_global_group_id']
                data['next_global_group_id'] += 1

                # Initialize counts for the new group.
                cat_in_new_group = 1 if player.pet_choice == 'cat' else 0
                dog_in_new_group = 1 if player.pet_choice == 'dog' else 0

                new_group = {
                    'group_id': group_id,
                    'my_group_id': my_group_id,
                    'condition': condition,
                    'cat_count': cat_in_new_group,
                    'dog_count': dog_in_new_group,
                    'players': [player.id_in_subsession]
                }
                groups.append(new_group)

                # Set player's group info.
                new_group_assignment = f"{condition}_{group_id}"

                print(f"Assigning player to {new_group_assignment}, group id: {my_group_id}")

                player.group_assignment = new_group_assignment
                player.my_group_id = my_group_id

            # Save the updated grouping data back into Redis.
            redis_client.set(grouping_key, json.dumps(data))

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    age = models.IntegerField(
        label="How old are you?",
        min=18,
        max=120,
    )
    gender_identity = models.StringField(
        label="Which gender do you identify with?",
        choices=[
            ['male', 'Male'],
            ['female', 'Female'],
            ['nonbinary', 'Non-binary'],
            ['undisclosed', 'Prefer not to disclose'],
            ['other', 'Other:'],
        ],
        widget=widgets.RadioSelect
    )

    pet_balance = models.IntegerField()
    pet_choice = models.CharField()

    # Waiting page assignment variables
    group_assignment = models.StringField(blank=True)
    my_group_id = models.IntegerField(blank=True, null=True)
    
    # Comprehension Check
    cc1 = models.StringField(
        label="How many members are in one group?",
        choices=[
            ["A", "One"],
            ["B", "Two"],
            ["C", "Three"],
        ],
        widget=widgets.RadioSelect,
    )
    cc2 = models.StringField(
        label="Is executing the task optional?",
        choices=[
            ["A", "Yes"],
            ["B", "No"],
        ],
        widget=widgets.RadioSelect,
    )
    cc3 = models.StringField(
        label="What would be the task, should you choose to execute it?",
        choices=[
            ["A", "Choosing animal preference"],
            ["B", "Bachwards typing task"],
            ["C", "Filling out a questionnaire"],
        ],
        widget=widgets.RadioSelect,
    )
    cc4 = models.StringField(
        label="What happens if you choose to complete the task?",
        choices=[
            ["A", "Only I get the bonus"],
            ["B", "Only people with the same animal preference as me get the bonus"],
            ["C", "Everyone in the group gets the bonus"],
        ],
        widget=widgets.RadioSelect,
    )
    cc5 = models.StringField(
        label="What happens if you choose not to complete the task?",
        choices=[
            ["A", "I do not get any bonus"],
            ["B", "I get the bonus if at least one other person completes the task"],
        ],
        widget=widgets.RadioSelect,
    )

    # Grouping page
    img_position = models.StringField(blank=True) #if image of same group member in majority is "left" or "right", for minority "none"


    # Volunteer's dilemma
    volunteered = models.IntegerField(
        label="Do you volunteer",
        choices=[
            [1, 'Yes'],
            [0, 'No']
        ],
        widget=widgets.RadioSelect,
        blank=True,
    )


    