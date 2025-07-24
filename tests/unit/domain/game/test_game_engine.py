"""
Unit tests for the game engine component
"""
import unittest
from unittest.mock import MagicMock, patch

from src_new.domain.game.game_engine import GameEngine, ActionType, LocationId, ActionResult


class TestGameEngine(unittest.TestCase):
    """Test cases for the GameEngine class"""

    def setUp(self):
        """Set up test fixtures"""
        self.game_engine = GameEngine()

    def test_initialization(self):
        """Test game engine initialization"""
        # Check initial state
        self.assertEqual(self.game_engine.current_location, LocationId.VILLAGE_OUTSKIRTS)
        self.assertEqual(self.game_engine.turn_count, 0)
        self.assertTrue(self.game_engine.game_flags["met_emberlyn"])
        self.assertFalse(self.game_engine.game_flags["knows_about_crystal"])
        self.assertFalse(self.game_engine.game_flags["cave_explored"])
        self.assertFalse(self.game_engine.game_flags["beetle_defeated"])
        self.assertFalse(self.game_engine.game_flags["crystal_obtained"])

    def test_get_current_location(self):
        """Test getting the current location"""
        location = self.game_engine.get_current_location()
        self.assertEqual(location.id, LocationId.VILLAGE_OUTSKIRTS)
        self.assertEqual(location.name, "Village Outskirts")
        self.assertEqual(
            location.description,
            "A peaceful path leading toward Ashbrook village, surrounded by autumn trees",
        )

    def test_get_available_actions(self):
        """Test getting available actions"""
        actions = self.game_engine.get_available_actions()
        
        # Check that we have the expected number of actions
        self.assertGreaterEqual(len(actions), 3)
        
        # Check that we have the expected action types
        action_ids = [action["id"] for action in actions]
        self.assertIn("examine_area", action_ids)
        self.assertIn("ask_emberlyn", action_ids)
        self.assertIn("wait_observe", action_ids)
        
        # Check that we have the expected action texts
        action_texts = [action["text"] for action in actions]
        self.assertIn("Examine the area carefully", action_texts)
        self.assertIn("Ask Emberlyn for guidance", action_texts)
        self.assertIn("Wait and observe", action_texts)

    def test_process_action_examine_area(self):
        """Test processing an examine area action"""
        result = self.game_engine.process_action("examine area")
        
        # Check result properties
        self.assertTrue(result.success)
        self.assertEqual(result.action_type, ActionType.EXAMINE)
        self.assertEqual(result.description, "Carefully examined Village Outskirts")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that the location was marked as visited
        self.assertTrue(self.game_engine.get_current_location().visited)
        
        # Check that discoveries were made
        self.assertGreaterEqual(len(result.discoveries), 1)
        
        # Check that narrative focus was set
        self.assertIn("environmental_details", result.narrative_focus)
        self.assertIn("emberlyn_observations", result.narrative_focus)
        
        # Check that next options were provided
        self.assertGreaterEqual(len(result.next_options), 1)

    def test_process_action_ask_emberlyn(self):
        """Test processing an ask emberlyn action"""
        result = self.game_engine.process_action("ask emberlyn")
        
        # Check result properties
        self.assertTrue(result.success)
        self.assertEqual(result.action_type, ActionType.SOCIAL)
        self.assertEqual(result.description, "Asked Emberlyn for her wisdom and guidance")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that discoveries were made
        self.assertGreaterEqual(len(result.discoveries), 1)
        
        # Check that narrative focus was set
        self.assertIn("emberlyn_wisdom", result.narrative_focus)
        self.assertIn("fairy_insights", result.narrative_focus)
        
        # Check that next options were provided
        self.assertGreaterEqual(len(result.next_options), 1)
        
        # Check that the story context was updated
        self.assertEqual(
            self.game_engine.story_context["current_situation"],
            "Consulting with Emberlyn at Village Outskirts",
        )
        self.assertEqual(self.game_engine.story_context["mood"], "seeking_guidance")

    def test_process_action_wait_observe(self):
        """Test processing a wait and observe action"""
        result = self.game_engine.process_action("wait and observe")
        
        # Check result properties
        self.assertTrue(result.success)
        self.assertEqual(result.action_type, ActionType.WAIT)
        self.assertEqual(result.description, "Waited and observed at Village Outskirts")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that discoveries were made
        self.assertGreaterEqual(len(result.discoveries), 1)
        
        # Check that narrative focus was set
        self.assertIn("patient_observation", result.narrative_focus)
        self.assertIn("subtle_details", result.narrative_focus)
        
        # Check that next options were provided
        self.assertGreaterEqual(len(result.next_options), 1)
        
        # Check that the story context was updated
        self.assertEqual(self.game_engine.story_context["mood"], "peaceful_contemplation")

    def test_process_action_prepare_combat(self):
        """Test processing a prepare combat action"""
        # Set up a location with enemies
        self.game_engine.current_location = LocationId.CRYSTAL_CAVE_ENTRANCE
        
        result = self.game_engine.process_action("prepare combat")
        
        # Check result properties
        self.assertTrue(result.success)
        self.assertEqual(result.action_type, ActionType.COMBAT)
        self.assertEqual(result.description, "Prepared for combat against fire_beetle")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that discoveries were made
        self.assertIn("tactical_advantage", result.discoveries)
        self.assertIn("enemy_weaknesses", result.discoveries)
        
        # Check that narrative focus was set
        self.assertIn("combat_preparation", result.narrative_focus)
        self.assertIn("tactical_assessment", result.narrative_focus)
        self.assertIn("emberlyn_support", result.narrative_focus)
        
        # Check that next options were provided
        self.assertIn("attack", result.next_options)
        self.assertIn("defensive_strategy", result.next_options)
        self.assertIn("attempt_negotiation", result.next_options)
        
        # Check that dice roll is required
        self.assertTrue(result.requires_dice_roll)
        
        # Check that the story context was updated
        self.assertEqual(
            self.game_engine.story_context["current_situation"],
            "Preparing for combat with fire_beetle",
        )
        self.assertEqual(self.game_engine.story_context["immediate_threat"], "fire_beetle")
        self.assertEqual(self.game_engine.story_context["mood"], "combat_ready")

    def test_process_action_prepare_combat_no_enemies(self):
        """Test processing a prepare combat action with no enemies"""
        result = self.game_engine.process_action("prepare combat")
        
        # Check result properties
        self.assertFalse(result.success)
        self.assertEqual(result.action_type, ActionType.COMBAT)
        self.assertEqual(result.description, "No immediate threats detected")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that narrative focus was set
        self.assertIn("false_alarm", result.narrative_focus)
        self.assertIn("overly_cautious", result.narrative_focus)
        
        # Check that next options were provided
        self.assertIn("relax_stance", result.next_options)
        self.assertIn("examine_area", result.next_options)
        self.assertIn("ask_emberlyn", result.next_options)

    def test_process_action_movement(self):
        """Test processing a movement action"""
        result = self.game_engine.process_action("move to Ashbrook Village")
        
        # Check result properties
        self.assertTrue(result.success)
        self.assertEqual(result.action_type, ActionType.MOVE)
        self.assertEqual(result.description, "Moved to Ashbrook Village")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that the location was changed
        self.assertEqual(self.game_engine.current_location, LocationId.ASHBROOK_VILLAGE)
        
        # Check that discoveries were made
        self.assertIn("new_location", result.discoveries)
        self.assertIn("travel_experience", result.discoveries)
        
        # Check that narrative focus was set
        self.assertIn("journey_description", result.narrative_focus)
        self.assertIn("new_environment", result.narrative_focus)
        self.assertIn("emberlyn_commentary", result.narrative_focus)
        
        # Check that next options were provided
        self.assertIn("examine_new_area", result.next_options)
        self.assertIn("ask_emberlyn", result.next_options)
        self.assertIn("continue_exploring", result.next_options)
        
        # Check that the story context was updated
        self.assertEqual(
            self.game_engine.story_context["current_situation"],
            "Moved from Village Outskirts to Ashbrook Village",
        )
        self.assertEqual(self.game_engine.story_context["mood"], "exploration")
        
        # Check that location-specific flags were reset
        self.assertFalse(self.game_engine.game_flags["aware_of_enemies"])
        self.assertFalse(self.game_engine.game_flags["items_spotted"])

    def test_process_action_invalid_movement(self):
        """Test processing an invalid movement action"""
        result = self.game_engine.process_action("move to Crystal Cave Interior")
        
        # Check result properties
        self.assertFalse(result.success)
        self.assertEqual(result.action_type, ActionType.MOVE)
        self.assertEqual(
            result.description, "Cannot reach Crystal Cave Interior from here"
        )
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that the location was not changed
        self.assertEqual(self.game_engine.current_location, LocationId.VILLAGE_OUTSKIRTS)
        
        # Check that narrative focus was set
        self.assertIn("blocked_path", result.narrative_focus)
        self.assertIn("alternative_routes", result.narrative_focus)
        
        # Check that next options were provided
        self.assertIn("find_another_way", result.next_options)
        self.assertIn("examine_area", result.next_options)
        self.assertIn("ask_emberlyn", result.next_options)

    def test_process_action_examine_feature(self):
        """Test processing an examine feature action"""
        result = self.game_engine.process_action("examine autumn trees")
        
        # Check result properties
        self.assertTrue(result.success)
        self.assertEqual(result.action_type, ActionType.EXAMINE)
        self.assertEqual(result.description, "Examined autumn trees")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that discoveries were made
        self.assertIn("autumn_trees", result.discoveries)
        
        # Check that narrative focus was set
        self.assertIn("detailed_examination", result.narrative_focus)
        self.assertIn("emberlyn_knowledge", result.narrative_focus)
        
        # Check that next options were provided
        self.assertIn("investigate_further", result.next_options)
        self.assertIn("ask_emberlyn", result.next_options)
        self.assertIn("take_action", result.next_options)

    def test_process_action_examine_nonexistent_feature(self):
        """Test processing an examine action for a nonexistent feature"""
        result = self.game_engine.process_action("examine crystal")
        
        # Check result properties
        self.assertFalse(result.success)
        self.assertEqual(result.action_type, ActionType.EXAMINE)
        self.assertEqual(result.description, "No crystal found here")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that narrative focus was set
        self.assertIn("search_failure", result.narrative_focus)
        self.assertIn("emberlyn_suggestion", result.narrative_focus)

    def test_process_action_general(self):
        """Test processing a general action"""
        result = self.game_engine.process_action("dance")
        
        # Check result properties
        self.assertTrue(result.success)
        self.assertEqual(result.action_type, ActionType.EXAMINE)
        self.assertEqual(result.description, "Attempted: dance")
        
        # Check that the turn count was incremented
        self.assertEqual(self.game_engine.turn_count, 1)
        
        # Check that discoveries were made
        self.assertIn("creative_approach", result.discoveries)
        
        # Check that narrative focus was set
        self.assertIn("player_creativity", result.narrative_focus)
        self.assertIn("emberlyn_response", result.narrative_focus)
        
        # Check that next options were provided
        self.assertIn("try_different_approach", result.next_options)
        self.assertIn("ask_emberlyn", result.next_options)
        self.assertIn("examine_area", result.next_options)

    def test_get_ai_context(self):
        """Test getting AI context"""
        context = self.game_engine.get_ai_context()
        
        # Check that the context contains the expected keys
        self.assertIn("location", context)
        self.assertIn("situation", context)
        self.assertIn("game_state", context)
        self.assertIn("immediate_context", context)
        
        # Check location context
        self.assertEqual(context["location"]["name"], "Village Outskirts")
        self.assertEqual(
            context["location"]["description"],
            "A peaceful path leading toward Ashbrook village, surrounded by autumn trees",
        )
        self.assertFalse(context["location"]["visited"])
        
        # Check situation context
        self.assertEqual(
            context["situation"]["current_situation"], "Beginning adventure with Emberlyn"
        )
        self.assertIsNone(context["situation"]["immediate_threat"])
        self.assertEqual(context["situation"]["active_npcs"], ["emberlyn"])
        self.assertEqual(context["situation"]["mood"], "curious_exploration")
        
        # Check game state context
        self.assertEqual(context["game_state"]["turn"], 0)
        self.assertIn("flags", context["game_state"])
        self.assertIn("character", context["game_state"])
        
        # Check immediate context
        self.assertEqual(context["immediate_context"]["enemies_present"], [])
        self.assertEqual(context["immediate_context"]["npcs_present"], [])
        self.assertEqual(context["immediate_context"]["items_available"], [])
        self.assertEqual(
            context["immediate_context"]["special_features"],
            ["autumn_trees", "cobblestone_path"],
        )

    def test_get_game_state_summary(self):
        """Test getting game state summary"""
        summary = self.game_engine.get_game_state_summary()
        
        # Check that the summary contains the expected information
        self.assertIn("Turn 0", summary)
        self.assertIn("Location: Village Outskirts", summary)
        self.assertIn("Situation: Beginning adventure with Emberlyn", summary)

    def test_save_and_load_game_state(self):
        """Test saving and loading game state"""
        # Make some changes to the game state
        self.game_engine.process_action("examine area")
        self.game_engine.process_action("move to Ashbrook Village")
        self.game_engine.game_flags["knows_about_crystal"] = True
        
        # Save the game state
        save_data = self.game_engine.save_game_state()
        
        # Create a new game engine
        new_engine = GameEngine()
        
        # Load the saved game state
        new_engine.load_game_state(save_data)
        
        # Check that the state was loaded correctly
        self.assertEqual(new_engine.current_location, LocationId.ASHBROOK_VILLAGE)
        self.assertEqual(new_engine.turn_count, 2)
        self.assertTrue(new_engine.game_flags["knows_about_crystal"])
        self.assertEqual(
            new_engine.story_context["current_situation"],
            "Moved from Village Outskirts to Ashbrook Village",
        )


if __name__ == "__main__":
    unittest.main()