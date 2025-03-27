from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'dilemma1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    def can_add_to_group(subsession, group, player):
        """
        Returns True if 'player' can be added to 'group' based on the
        minority/majority rules. Returns False otherwise.
        """
        # Gather current composition
        current_players = [
            p for p in subsession.get_players()
            if p.id_in_subsession in group['players']
        ]
        num_cats = sum(1 for p in current_players if p.pet_choice == 'cat')
        num_dogs = sum(1 for p in current_players if p.pet_choice == 'dog')

        # Check if the group is already full
        if len(group['players']) >= 3:
            return False

        # Now check based on condition
        condition = group['condition']
        if condition == 'cat_minority':
            # Final composition: 1 cat, 2 dogs
            if player.pet_choice == 'cat':
                # We can add this cat only if there are 0 cats so far
                return num_cats < 1
            else:
                # We can add this dog only if there are fewer than 2 dogs
                return num_dogs < 2

        elif condition == 'dog_minority':
            # Final composition: 1 dog, 2 cats
            if player.pet_choice == 'dog':
                return num_dogs < 1
            else:
                return num_cats < 2

        else:
            # 'control' groups can have any 3 players
            return len(group['players']) < 3

    def assign_individual_group(self, player):
        """
        Assigns an individual player to a group based on their pet choice.

        For players who have made a pet choice:
        • Increment the counter for that pet type.
        • If the count is <= 75, assign using the pet-choice rule:
            - For a cat player: if (cat_count mod 3 == 1) then 'cat_minority'
                (the lone cat) else 'dog_minority' (majority cat).
            - For a dog player: if (dog_count mod 3 == 1) then 'dog_minority'
                else 'cat_minority'.
        • If the count > 75 for that pet type, assign 'control'.

        Then the function places the player into an (incomplete) group stored in session.vars,
        ensuring that 'cat_minority' groups always end up with 1 cat and 2 dogs,
        and 'dog_minority' groups have 1 dog and 2 cats. 'control' groups simply hold any 3 players.
        """
        # If we haven't initialized the grouping storage, do so now.
        if 'grouping' not in self.session.vars:
            self.session.vars['grouping'] = {
                'cat_minority': [],  # each item: {'condition': 'cat_minority', 'group_id': int, 'global_id': int, 'players': [...]}
                'dog_minority': [],
                'control': []
            }
            self.session.vars['cat_count'] = 0
            self.session.vars['dog_count'] = 0
            self.session.vars['control_count'] = 0
            self.session.vars['next_cat_minority_group'] = 1
            self.session.vars['next_dog_minority_group'] = 1
            self.session.vars['next_control_group'] = 1
            self.session.vars['next_global_group'] = 1

        # Determine the condition for this player based on pet_choice and counters.
        if player.pet_choice == 'cat':
            self.session.vars['cat_count'] += 1
            count = self.session.vars['cat_count']
            if count <= 75:
                # every 1st cat in a block of 3 => cat_minority
                condition = 'cat_minority' if (count % 3 == 1) else 'dog_minority'
            else:
                condition = 'control'
        elif player.pet_choice == 'dog':
            self.session.vars['dog_count'] += 1
            count = self.session.vars['dog_count']
            if count <= 75:
                # every 1st dog in a block of 3 => dog_minority
                condition = 'dog_minority' if (count % 3 == 1) else 'cat_minority'
            else:
                condition = 'control'
        else:
            condition = 'control'

        # Attempt to place the player into an existing incomplete group
        # that still has room for this composition.
        groups = self.session.vars['grouping'][condition]
        assigned = False
        for group in groups:
            if can_add_to_group(self, group, player):
                group['players'].append(player.id_in_subsession)
                player.group_assignment = f"{condition}_{group['group_id']}"
                player.my_group_id = group['global_id']
                assigned = True
                break

        # If we didn't find a suitable existing group, create a new one.
        if not assigned:
            if condition == 'cat_minority':
                group_id = self.session.vars['next_cat_minority_group']
                self.session.vars['next_cat_minority_group'] += 1
            elif condition == 'dog_minority':
                group_id = self.session.vars['next_dog_minority_group']
                self.session.vars['next_dog_minority_group'] += 1
            else:
                # control
                group_id = self.session.vars['next_control_group']
                self.session.vars['next_control_group'] += 1

            global_id = self.session.vars['next_global_group']
            self.session.vars['next_global_group'] += 1

            # Create a new group dict with this player's ID
            new_group = {
                'condition': condition,
                'group_id': group_id,
                'global_id': global_id,
                'players': [player.id_in_subsession],
            }
            groups.append(new_group)

            # Assign the player's fields
            player.group_assignment = f"{condition}_{group_id}"
            player.my_group_id = global_id


    







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