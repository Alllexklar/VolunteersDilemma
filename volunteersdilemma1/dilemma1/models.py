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
        """
        # Initialize grouping storage if needed.
        if 'grouping' not in self.session.vars:
            self.session.vars['grouping'] = {
                'cat_minority': [],   # Each item is a dict: {'group_id': int, 'players': [player ids]}
                'dog_minority': [],
                'control': []
            }
            self.session.vars['cat_count'] = 0
            self.session.vars['dog_count'] = 0
            self.session.vars['control_count'] = 0
            self.session.vars['next_cat_minority_group'] = 1
            self.session.vars['next_dog_minority_group'] = 1
            self.session.vars['next_control_group'] = 1

        # Determine condition based on pet_choice and count.
        if player.pet_choice == 'cat':
            self.session.vars['cat_count'] += 1
            count = self.session.vars['cat_count']
            if count <= 75:
                # For cat players in pet-choice phase:
                # Every first cat in a block of 3 becomes the minority in a cat_minority group.
                condition = 'cat_minority' if (count % 3 == 1) else 'dog_minority'
            else:
                condition = 'control'
        elif player.pet_choice == 'dog':
            self.session.vars['dog_count'] += 1
            count = self.session.vars['dog_count']
            if count <= 75:
                # For dog players in pet-choice phase:
                # Every first dog in a block of 3 becomes the minority in a dog_minority group.
                condition = 'dog_minority' if (count % 3 == 1) else 'cat_minority'
            else:
                condition = 'control'
        else:
            # Fallback in case pet_choice is not set.
            condition = 'control'

        # Assign the player to an incomplete group for the given condition.
        groups = self.session.vars['grouping'][condition]
        assigned = False

        # Look for an existing group with fewer than 3 players.
        for group in groups:
            if len(group['players']) < 3:
                group['players'].append(player.id_in_subsession)
                player.group_assignment = f"{condition}_{group['group_id']}"
                assigned = True
                break

        if not assigned:
            # No incomplete group exists; create a new one.
            if condition == 'cat_minority':
                group_id = self.session.vars['next_cat_minority_group']
                self.session.vars['next_cat_minority_group'] += 1
            elif condition == 'dog_minority':
                group_id = self.session.vars['next_dog_minority_group']
                self.session.vars['next_dog_minority_group'] += 1
            elif condition == 'control':
                group_id = self.session.vars['next_control_group']
                self.session.vars['next_control_group'] += 1
            new_group = {'group_id': group_id, 'players': [player.id_in_subsession]}
            groups.append(new_group)
            player.group_assignment = f"{condition}_{group_id}"



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



"""
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
    )"""