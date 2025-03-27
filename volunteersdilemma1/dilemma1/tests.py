# tests.py
from django.test import TestCase
from otree.models import Session
from .models import Subsession, Player

class GroupAssignmentTest(TestCase):
    def test_assign_individual_group(self):
        # Create a dummy session with empty vars.
        dummy_session = Session()
        dummy_session.vars = {}
        
        # Create a subsession with this dummy session.
        subsession = Subsession(session=dummy_session)
        
        # Simulate 80 players with alternating pet choices.
        simulated_players = []
        for i in range(1, 81):
            # Create a dummy player. In oTree, players are automatically given id_in_subsession,
            # but here we simulate it.
            player = Player(id_in_subsession=i)
            # Alternate pet choice: odd = cat, even = dog.
            player.pet_choice = 'cat' if i % 2 == 1 else 'dog'
            
            # Call our assignment function.
            subsession.assign_individual_group(player)
            simulated_players.append(player)
            
            # Print out assignment for observation (you can also use assertions).
            print(f"Player {i} ({player.pet_choice}) assigned to group: {player.group_assignment}")

        # Optionally, add assertions to check that players beyond the 75 threshold are in 'control'.
        for player in simulated_players:
            if player.pet_choice == 'cat' and player.id_in_subsession > 75:
                self.assertIn("control", player.group_assignment)
            if player.pet_choice == 'dog' and player.id_in_subsession > 75:
                self.assertIn("control", player.group_assignment)
