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


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])