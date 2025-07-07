#!/usr/bin/env python3
"""
Simple Prompt Tests - Basic functionality tests for common player actions
These test core game mechanics work correctly with simple, straightforward prompts
"""

import pytest
import json
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.game_state_manager import GameStateManager
from engine.ai_integration import AIIntegrationLayer
from utils.character_sheet import CharacterSheet
from utils.dice_system import DiceRoll


class TestSimplePrompts:
    """Test basic game functionality with simple player prompts"""
    
    def setup_method(self):
        """Setup fresh game state for each test"""
        # Load environment for API key
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        api_key = os.getenv('CLAUDE_API_KEY')
        
        # Initialize with complete character data
        character_data = {
            'name': 'Test Hero',
            'class': 'Cleric',
            'level': 1,
            'xp': 0,
            'stats': {
                'strength': 12,
                'dexterity': 14,
                'intelligence': 13,
                'charisma': 16
            },
            'resources': {
                'hp': 25,
                'max_hp': 25,
                'energy': 12,
                'max_energy': 12
            },
            'skills': {
                'Healing': 3,
                'Persuasion': 2,
                'Combat': 1
            },
            'achievements': [],
            'emberlyn_bond': 1
        }
        
        self.ai_integration = AIIntegrationLayer(api_key)
        self.game_result = self.ai_integration.start_new_game(character_data)
        
    def test_basic_attack_prompt(self):
        """Test simple attack command works"""
        prompt = "I attack"
        
        try:
            response = self.ai_integration.process_player_action(prompt)
            
            # Basic functionality checks
            assert response is not None, "Response should not be None"
            assert 'narrative' in response, "Response should contain narrative"
            assert len(response['narrative']) > 0, "Narrative should not be empty"
            assert isinstance(response['narrative'], str), "Narrative should be a string"
            
            # Content checks
            attack_indicators = ['attack', 'strike', 'hit', 'damage', 'weapon', 'combat', 'fight']
            assert any(indicator in response['narrative'].lower() for indicator in attack_indicators), \
                "Response should acknowledge the attack action"
                
            print(f"✅ Attack Response: {response['narrative'][:100]}...")
            
        except Exception as e:
            pytest.fail(f"Basic attack failed: {e}")
    
    def test_basic_movement_prompt(self):
        """Test simple movement command works"""
        prompt = "I go north"
        
        try:
            response = self.ai_integration.process_player_action(prompt)
            
            assert response is not None
            assert 'narrative' in response
            assert len(response['narrative']) > 0
            
            movement_indicators = ['north', 'move', 'go', 'travel', 'walk', 'direction']
            assert any(indicator in response['narrative'].lower() for indicator in movement_indicators), \
                "Response should acknowledge movement"
                
            print(f"✅ Movement Response: {response['narrative'][:100]}...")
            
        except Exception as e:
            pytest.fail(f"Basic movement failed: {e}")
    
    def test_basic_look_prompt(self):
        """Test simple look/examine command works"""
        prompt = "I look around"
        
        try:
            response = self.ai_integration.process_player_action(prompt)
            
            assert response is not None
            assert 'narrative' in response
            assert len(response['narrative']) > 0
            
            look_indicators = ['see', 'look', 'observe', 'notice', 'around', 'examine']
            assert any(indicator in response['narrative'].lower() for indicator in look_indicators), \
                "Response should provide environmental description"
                
            print(f"✅ Look Response: {response['narrative'][:100]}...")
            
        except Exception as e:
            pytest.fail(f"Basic look failed: {e}")
    
    def test_basic_talk_prompt(self):
        """Test simple talk/speak command works"""
        prompt = "I talk to the NPC"
        
        try:
            response = self.ai_integration.process_player_action(prompt)
            
            assert response is not None
            assert 'narrative' in response
            assert len(response['narrative']) > 0
            
            talk_indicators = ['talk', 'speak', 'say', 'conversation', 'dialogue', 'emberlyn']
            assert any(indicator in response['narrative'].lower() for indicator in talk_indicators), \
                "Response should handle dialogue"
                
            print(f"✅ Talk Response: {response['narrative'][:100]}...")
            
        except Exception as e:
            pytest.fail(f"Basic talk failed: {e}")
    
    def test_basic_inventory_prompt(self):
        """Test simple inventory command works"""
        prompt = "I check my inventory"
        
        try:
            response = self.ai_integration.process_player_action(prompt)
            
            assert response is not None
            assert 'narrative' in response
            assert len(response['narrative']) > 0
            
            inventory_indicators = ['inventory', 'items', 'carrying', 'have', 'possess', 'equipment']
            assert any(indicator in response['narrative'].lower() for indicator in inventory_indicators), \
                "Response should show inventory information"
                
            print(f"✅ Inventory Response: {response['narrative'][:100]}...")
            
        except Exception as e:
            pytest.fail(f"Basic inventory failed: {e}")
    
    def test_basic_help_prompt(self):
        """Test simple help command works"""
        prompt = "help"
        
        try:
            response = self.ai_integration.process_player_action(prompt)
            
            assert response is not None
            assert 'narrative' in response
            assert len(response['narrative']) > 0
            
            help_indicators = ['help', 'command', 'action', 'can', 'do', 'options']
            assert any(indicator in response['narrative'].lower() for indicator in help_indicators), \
                "Response should provide helpful information"
                
            print(f"✅ Help Response: {response['narrative'][:100]}...")
            
        except Exception as e:
            pytest.fail(f"Basic help failed: {e}")
    
    def test_character_sheet_access(self):
        """Test that character sheet information is accessible"""
        try:
            char_sheet = self.ai_integration.get_character_sheet()
            
            assert char_sheet is not None, "Character sheet should be accessible"
            assert len(char_sheet) > 0, "Character sheet should not be empty"
            
            # Check for basic character attributes
            expected_attributes = ['name', 'level', 'hp', 'str', 'dex', 'int', 'cha']
            assert any(attr.lower() in char_sheet.lower() for attr in expected_attributes), \
                f"Character sheet should contain basic attributes"
                    
            print(f"✅ Character Sheet: {char_sheet[:200]}...")
            
        except Exception as e:
            pytest.fail(f"Character sheet access failed: {e}")
    
    def test_dice_system_basic(self):
        """Test that dice system works for basic rolls"""
        try:
            # Create a test character for dice rolling
            from utils.character_sheet import CharacterSheet
            character = CharacterSheet()
            
            # Test basic dice roll creation
            dice_roll = DiceRoll(character, "Combat Test", "normal")
            result = dice_roll.roll("strength", "Combat")
            
            assert isinstance(result, dict), "Dice roll should return dictionary"
            assert 'roll' in result, "Result should contain roll value"
            assert 'success' in result, "Result should contain success status"
            assert 1 <= result['roll'] <= 20, "d20 should return value between 1 and 20"
            
            print(f"✅ Dice Roll: {result['roll']} (Success: {result['success']})")
            
        except Exception as e:
            pytest.fail(f"Basic dice system failed: {e}")
    
    def test_game_state_persistence(self):
        """Test that game state can be accessed and updated"""
        try:
            # Get initial character state
            initial_response = self.ai_integration.process_player_action("I examine my surroundings")
            assert 'character' in initial_response, "Should have character data"
            assert 'game_state' in initial_response, "Should have game state"
            
            # Make another action
            second_response = self.ai_integration.process_player_action("I take a step forward")
            assert 'character' in second_response, "Should maintain character data"
            assert 'game_state' in second_response, "Should maintain game state"
            
            print(f"✅ Game State: Persistent across actions")
            
        except Exception as e:
            pytest.fail(f"Game state persistence failed: {e}")
    
    def test_response_quality_basic(self):
        """Test that responses meet basic quality standards"""
        test_prompts = [
            "I attack the goblin",
            "I search for treasure", 
            "I talk to Emberlyn",
            "I cast a spell"
        ]
        
        for prompt in test_prompts:
            try:
                response = self.ai_integration.process_player_action(prompt)
                narrative = response['narrative']
                
                # Basic quality checks
                assert len(narrative) >= 50, f"Response too short for prompt '{prompt}': {len(narrative)} chars"
                assert len(narrative) <= 1000, f"Response too long for prompt '{prompt}': {len(narrative)} chars"
                
                # Should not be generic error messages
                error_indicators = ['error', 'failed', 'cannot process', 'invalid']
                assert not any(error in narrative.lower() for error in error_indicators), \
                    f"Response should not contain error messages for valid prompt: {prompt}"
                
                print(f"✅ Quality check passed for: '{prompt}'")
                
            except Exception as e:
                pytest.fail(f"Response quality failed for '{prompt}': {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])