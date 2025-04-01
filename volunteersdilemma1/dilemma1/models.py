from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'dilemma1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):

    def assign_individual_group(self, player):
        """
        Assigns an individual player to a group based on their pet choice.
        
        For players who have made a pet choice:
          • Increment the counter for that pet type.
          • If the count is <= 75, assign using the pet-choice rule:
              - For a cat player: if (cat_count mod 3 == 1) then 'cat_minority'
                (i.e. the lone cat) else 'dog_minority' (i.e. majority cat).
              - For a dog player: if (dog_count mod 3 == 1) then 'dog_minority'
                else 'cat_minority'.
          • If the count > 75 for that pet type, assign to the control condition.
          
        Then the function places the player into an (incomplete) group stored in session.vars.
        These incomplete groups allow the participant to continue even if their group is not yet complete.

        Additionally, each group (across all conditions) has a global 'my_group_id' 
        so that you can have a unique integer group index across the entire study.

        We also add a safety check so that if the group is 'cat_minority' or 'dog_minority',
        we do not add more than one minority pet to that group.
        """

        # 1. Initialize grouping storage if needed.
        if 'grouping' not in self.session.vars:
            self.session.vars['grouping'] = {
                'cat_minority': [],   # Each item is a dict: {'group_id': int, 'my_group_id': int, 'condition': str, 'cat_count': int, 'dog_count': int, 'players': [...]}
                'dog_minority': [],
                'control': []
            }
            self.session.vars['cat_count'] = 0
            self.session.vars['dog_count'] = 0
            self.session.vars['control_count'] = 0

            # Trackers for condition-specific group IDs
            self.session.vars['next_cat_minority_group'] = 1
            self.session.vars['next_dog_minority_group'] = 1
            self.session.vars['next_control_group'] = 1

            # Global tracker for an overall unique group ID across all conditions
            self.session.vars['next_global_group_id'] = 1

        # 2. Determine the condition based on pet_choice and the counters.
        if player.pet_choice == 'cat':
            self.session.vars['cat_count'] += 1
            count = self.session.vars['cat_count']
            if count <= 75:
                # For cat players in pet-choice phase:
                # Every first cat in a block of 3 => cat_minority; otherwise dog_minority.
                condition = 'cat_minority' if (count % 3 == 1) else 'dog_minority'
            else:
                condition = 'control'

        elif player.pet_choice == 'dog':
            self.session.vars['dog_count'] += 1
            count = self.session.vars['dog_count']
            if count <= 75:
                # For dog players in pet-choice phase:
                # Every first dog in a block of 3 => dog_minority; otherwise cat_minority.
                condition = 'dog_minority' if (count % 3 == 1) else 'cat_minority'
            else:
                condition = 'control'
        else:
            # Fallback if pet_choice is missing (assign to control).
            condition = 'control'

        # 3. Attempt to assign the player to an existing incomplete group for that condition.
        groups = self.session.vars['grouping'][condition]
        assigned = False

        for group in groups:
            if len(group['players']) < 3:

                if group['condition'] == 'cat_minority':
                    # If new player is a cat (the minority), ensure we don't already have a cat
                    if player.pet_choice == 'cat':
                        if group['cat_count'] >= 1:
                            continue
                    # If new player is a dog (the majority), ensure we don't exceed 2 dogs
                    else:  # player.pet_choice == 'dog'
                        if group['dog_count'] >= 2:
                            continue

                elif group['condition'] == 'dog_minority':
                    # If new player is a dog (the minority), ensure we don't already have a dog
                    if player.pet_choice == 'dog':
                        if group['dog_count'] >= 1:
                            continue
                    # If new player is a cat (the majority), ensure we don't exceed 2 cats
                    else:  # player.pet_choice == 'cat'
                        if group['cat_count'] >= 2:
                            continue

                # If checks are passed, we can add the player
                group['players'].append(player.id_in_subsession)

                # Update cat/dog counts in this group
                if player.pet_choice == 'cat':
                    group['cat_count'] += 1
                elif player.pet_choice == 'dog':
                    group['dog_count'] += 1

                # 3a. Set the player's condition-specific and global group info
                player.group_assignment = f"{condition}_{group['group_id']}"
                player.my_group_id = group['my_group_id']  # use the existing group's global ID

                assigned = True
                break

        # 4. If no incomplete group was found, create a new one.
        if not assigned:
            # Identify the next condition-specific group ID
            if condition == 'cat_minority':
                group_id = self.session.vars['next_cat_minority_group']
                self.session.vars['next_cat_minority_group'] += 1
            elif condition == 'dog_minority':
                group_id = self.session.vars['next_dog_minority_group']
                self.session.vars['next_dog_minority_group'] += 1
            else:  # 'control'
                group_id = self.session.vars['next_control_group']
                self.session.vars['next_control_group'] += 1

            # Grab the *global* group ID, increment it for the next new group
            my_group_id = self.session.vars['next_global_group_id']
            self.session.vars['next_global_group_id'] += 1

            # Initialize cat_count/dog_count for the new group
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

            # 4a. Assign the player's group fields
            player.group_assignment = f"{condition}_{group_id}"
            player.my_group_id = my_group_id



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pet_choice = models.CharField(
        label="Select a pet",
        choices=[
            ('cat', 'Cat'),
            ('dog', 'Dog')
        ],
        widget=widgets.RadioSelect
    )
    group_assignment = models.StringField(blank=True)
    my_group_id = models.IntegerField(blank=True, null=True)


    # Volunteer's dilemma
    volunteered = models.IntegerField(
        label="Do you volunteer",
        choices=[
            [1, 'Yes'],
            [0, 'No']
        ],
        widget=widgets.RadioSelect
    )

    satisfaction = models.IntegerField(
            label="How satisfied are you with the experiment?",
            choices=[
                [1, 'Strongly Disagree'],
                [2, 'Disagree'],
                [3, 'Neutral'],
                [4, 'Agree'],
                [5, 'Strongly Agree']
            ],
            widget=widgets.RadioSelectHorizontal
        )