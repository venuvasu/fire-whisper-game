"""
Integration tests for the game controller
"""
import unittest
from unittest.mock import MagicMock, patch

from src_new.domain.game.game_engine import GameEngine
from src_new.domain.story.story_engine import StoryEngine
from src_new.application.controllers.game_controller import GameController


class TestGameController(unittest.TestCase):
    """Test cases for the GameController class"""

    def setUp(self):
        """Set up test fixtures"""
        self.game_engine = GameEngine()
        self.story_engine = MagicMock(spec=StoryEngine)
        self.story_engine.generate_narrative.return_value = "Test narrative"
        self.story_engine.process_player_action.return_value = {"test": "context"}
        self.game_controller = GameController(self.game_engine, self.story_engine)

    def test_start_new_game(self):
        """Test starting a new game"""
        # Set up test data
        character_data = {
            "name": "Test Character",
            "race": "Human",
            "profession": "Warrior",
        }
        saga_name = "Test Saga"
        
        # Call the method
        result = self.game_controller.start_new_game(character_data, saga_name)
        
        # Check that the story engine was called to generate the opening narrative
        self.story_engine.generate_narrative.assert_called_once()
        
        # Check that the result contains the expected keys
        self.assertIn("narrative", result)
        self.assertIn("actions", result)
        self.assertIn("game_state", result)
        
        # Check that the narrative is the one returned by the story engine
        self.assertEqual(result["narrative"], "Test narrative")
        
        # Check that the actions are the ones returned by the game engine
        self.assertEqual(result["actions"], self.game_engine.get_available_actions())
        
        # Check that the game state is the one returned by the game engine
        self.assertEqual(result["game_state"], self.game_engine.get_game_state_summary())

    def test_process_turn(self):
        """Test processing a turn"""
        # Set up test data
        player_input = "examine area"
        
        # Call the method
        result = self.game_controller.process_turn(player_input)
        
        # Check that the game engine was called to process the action
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that the story engine was called to process the player action
        self.story_engine.process_player_action.assert_called_once()
        
        # Check that the story engine was called to generate the narrative
        self.story_engine.generate_narrative.assert_called_once()
        
        # Check that the result contains the expected keys
        self.assertIn("narrative", result)
        self.assertIn("actions", result)
        self.assertIn("game_state", result)
        self.assertIn("action_result", result)
        
        # Check that the narrative is the one returned by the story engine
        self.assertEqual(result["narrative"], "Test narrative")
        
        # Check that the actions are the ones returned by the game engine
        self.assertEqual(result["actions"], self.game_engine.get_available_actions())
        
        # Check that the game state is the one returned by the game engine
        self.assertEqual(result["game_state"], self.game_engine.get_game_state_summary())
        
        # Check that the action result contains the expected keys
        self.assertIn("type", result["action_result"])
        self.assertIn("success", result["action_result"])
        self.assertIn("discoveries", result["action_result"])

    def test_process_turn_with_dice_roll(self):
        """Test processing a turn that requires a dice roll"""
        # Set up the game engine to require a dice roll
        self.game_engine.current_location = self.game_engine.locations[
            self.game_engine._create_world()["crystal_cave_entrance"].id
        ]
        
        # Set up test data
        player_input = "prepare combat"
        
        # Call the method
        result = self.game_controller.process_turn(player_input)
        
        # Check that the game engine was called to process the action
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that the story engine was called to process the player action
        self.story_engine.process_player_action.assert_called_once()
        
        # Check that the story engine was called to generate the narrative
        self.story_engine.generate_narrative.assert_called_once()
        
        # Check that the result contains the expected keys
        self.assertIn("narrative", result)
        self.assertIn("actions", result)
        self.assertIn("game_state", result)
        self.assertIn("action_result", result)
        self.assertIn("dice_info", result)
        
        # Check that the dice info contains the expected keys
        self.assertIn("roll", result["dice_info"])
        self.assertIn("modifier", result["dice_info"])
        self.assertIn("total", result["dice_info"])
        self.assertIn("threshold", result["dice_info"])
        self.assertIn("success", result["dice_info"])

    def test_get_character_sheet(self):
        """Test getting the character sheet"""
        # Call the method
        result = self.game_controller.get_character_sheet()
        
        # Check that the result is a string
        self.assertIsInstance(result, str)
        
        # Check that the result contains the expected information
        self.assertIn("Character Status", result)
        self.assertIn("HP:", result)
        self.assertIn("Level:", result)
        self.assertIn("XP:", result)
        self.assertIn("Current Location:", result)
        self.assertIn("Turn:", result)
        self.assertIn("Progress Flags:", result)
        self.assertIn("Game State:", result)

    def test_get_available_actions_formatted(self):
        """Test getting formatted available actions"""
        # Call the method
        result = self.game_controller.get_available_actions_formatted()
        
        # Check that the result is a string
        self.assertIsInstance(result, str)
        
        # Check that the result contains the expected information
        self.assertIn("Examine the area carefully", result)
        self.assertIn("Ask Emberlyn for guidance", result)
        self.assertIn("Wait and observe", result)

    def test_save_and_load_game_state(self):
        """Test saving and loading game state"""
        # Make some changes to the game state
        self.game_controller.process_turn("examine area")
        self.game_controller.process_turn("move to Ashbrook Village")
        
        # Save the game state
        save_data = self.game_controller.save_game_state()
        
        # Create a new game controller
        new_game_engine = GameEngine()
        new_story_engine = MagicMock(spec=StoryEngine)
        new_game_controller = GameController(new_game_engine, new_story_engine)
        
        # Load the saved game state
        new_game_controller.load_game_state(save_data)
        
        # Check that the state was loaded correctly
        self.assertEqual(new_game_engine.turn_count, 2)
        self.assertEqual(
            new_game_engine.current_location.value, "ashbrook_village"
        )


if __name__ == "__main__":
    unittest.main()