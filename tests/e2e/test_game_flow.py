"""
End-to-End Game Flow Tests

This module contains end-to-end tests for the complete game flow.
"""
import unittest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from application.services.game_service import GameService


class TestGameFlow(unittest.TestCase):
    """Test complete game flow scenarios"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.game_service = GameService()
        self.character_data = {
            "name": "TestHero",
            "race": "Human",
            "profession": "Warrior",
            "attributes": {
                "strength": 14,
                "dexterity": 12,
                "constitution": 14,
                "intelligence": 10,
                "wisdom": 12,
                "charisma": 10
            }
        }
        self.saga_name = "Test Saga"
    
    def test_complete_game_session(self):
        """Test a complete game session from start to finish"""
        # Start a new game
        response = self.game_service.start_new_game(self.character_data, self.saga_name)
        
        # Verify game was created
        self.assertIn("game_id", response)
        self.assertIn("initial_narrative", response)
        self.assertIn("actions", response)
        
        game_id = response["game_id"]
        
        # Process several turns
        actions = [
            "examine area",
            "ask emberlyn",
            "wait and observe",
            "move forward"
        ]
        
        for action in actions:
            turn_response = self.game_service.process_turn(game_id, action)
            
            # Verify turn response
            self.assertIn("narrative", turn_response)
            self.assertIn("actions", turn_response)
            self.assertIn("game_state", turn_response)
            self.assertIn("action_result", turn_response)
        
        # Get final game state
        final_state = self.game_service.get_game_state(game_id)
        
        # Verify final state
        self.assertEqual(final_state["game_id"], game_id)
        self.assertEqual(final_state["character"]["name"], self.character_data["name"])
        self.assertEqual(final_state["saga"], self.saga_name)
        self.assertTrue(len(final_state["messages"]) > 0)
    
    def test_save_and_load_game(self):
        """Test saving and loading a game"""
        # Start a new game
        response = self.game_service.start_new_game(self.character_data, self.saga_name)
        game_id = response["game_id"]
        
        # Process a few turns
        self.game_service.process_turn(game_id, "examine area")
        self.game_service.process_turn(game_id, "ask emberlyn")
        
        # Save the game
        save_data = self.game_service.save_game(game_id)
        
        # Verify save data
        self.assertIn("game_id", save_data)
        self.assertIn("character", save_data)
        self.assertIn("saga", save_data)
        self.assertIn("messages", save_data)
        self.assertIn("game_state", save_data)
        
        # Load the game
        loaded_game_id = self.game_service.load_game(save_data)
        
        # Verify loaded game
        loaded_state = self.game_service.get_game_state(loaded_game_id)
        self.assertEqual(loaded_state["character"]["name"], self.character_data["name"])
        self.assertEqual(loaded_state["saga"], self.saga_name)
        self.assertTrue(len(loaded_state["messages"]) > 0)
    
    def test_multiple_games(self):
        """Test managing multiple games simultaneously"""
        # Start multiple games
        game_ids = []
        for i in range(3):
            character = self.character_data.copy()
            character["name"] = f"TestHero{i}"
            
            response = self.game_service.start_new_game(character, f"Test Saga {i}")
            game_ids.append(response["game_id"])
        
        # Process turns in each game
        for game_id in game_ids:
            self.game_service.process_turn(game_id, "examine area")
        
        # List all games
        games = self.game_service.list_games()
        
        # Verify all games are listed
        self.assertEqual(len(games), 3)
        
        # Verify each game has correct data
        for i, game in enumerate(games):
            self.assertEqual(game["character"], f"TestHero{i}")
            self.assertEqual(game["saga"], f"Test Saga {i}")
            self.assertTrue(game["active"])
    
    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test processing turn for non-existent game
        with self.assertRaises(ValueError):
            self.game_service.process_turn("non-existent-id", "test action")
        
        # Test getting state for non-existent game
        with self.assertRaises(ValueError):
            self.game_service.get_game_state("non-existent-id")
        
        # Test saving non-existent game
        with self.assertRaises(ValueError):
            self.game_service.save_game("non-existent-id")


if __name__ == "__main__":
    unittest.main()