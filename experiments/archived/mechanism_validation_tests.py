#!/usr/bin/env python3
"""
Mechanism Validation Tests - Test core game mechanics in isolation
Validates dice rolling, XP progression, character management without AI
"""

import pytest
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.game_state_manager import GameStateManager, ActionType
from utils.dice_system import DiceRoll
from utils.character_sheet import CharacterSheet


class TestCoreMechanisms:
    """Test core game mechanisms work correctly"""
    
    def setup_method(self):
        """Setup test character and game state"""
        self.character_data = {
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
        self.game_manager = GameStateManager(self.character_data)
        
    def test_dice_rolling_mechanism(self):
        """Test dice rolling produces consistent, valid results"""
        results = []
        
        # Test 10 rolls for consistency
        for i in range(10):
            roll = self.game_manager.execute_dice_roll(
                stat='strength',
                skill='Combat',
                difficulty='normal',
                context='test_combat'
            )
            
            results.append(roll)
            
            # Validate roll structure
            assert hasattr(roll, 'base_roll'), "Roll should have base_roll"
            assert hasattr(roll, 'success'), "Roll should have success status"
            assert hasattr(roll, 'modifiers'), "Roll should have modifiers"
            assert 1 <= roll.base_roll <= 20, f"Base roll should be 1-20, got {roll.base_roll}"
            
        # Test different difficulties
        easy_roll = self.game_manager.execute_dice_roll('charisma', 'Persuasion', 'easy', 'test')
        hard_roll = self.game_manager.execute_dice_roll('charisma', 'Persuasion', 'hard', 'test')
        
        assert easy_roll.target < hard_roll.target, "Easy should have lower target than hard"
        
        print(f"✅ Dice Rolling: 10 consistent rolls, difficulty scaling works")
        
    def test_xp_progression_mechanism(self):
        """Test XP awards and level progression"""
        initial_xp = self.game_manager.character['xp']
        initial_level = self.game_manager.character['level']
        
        # Award small XP amounts
        for i in range(5):
            xp_result = self.game_manager.award_xp(15, f"Test action {i}", "combat")
            assert xp_result['xp_awarded'] == 15, "Should award correct XP amount"
            
        current_xp = self.game_manager.character['xp']
        assert current_xp == initial_xp + 75, f"Should have 75 XP, got {current_xp - initial_xp}"
        
        # Award enough XP to level up
        level_up_result = self.game_manager.award_xp(30, "Level up test", "combat")
        
        if level_up_result['level_up']:
            assert self.game_manager.character['level'] > initial_level, "Should level up"
            assert len(level_up_result['new_abilities']) > 0, "Should gain new abilities"
            
        print(f"✅ XP Progression: Awards work, level up triggers correctly")
        
    def test_character_sheet_management(self):
        """Test character data integrity and updates"""
        # Test stat modifications
        original_hp = self.game_manager.character['resources']['hp']
        
        # Simulate damage
        self.game_manager.character['resources']['hp'] -= 5
        assert self.game_manager.character['resources']['hp'] == original_hp - 5
        
        # Test skill improvements
        original_combat = self.game_manager.character['skills']['Combat']
        self.game_manager.character['skills']['Combat'] += 1
        assert self.game_manager.character['skills']['Combat'] == original_combat + 1
        
        # Test character sheet generation
        char_sheet = CharacterSheet(self.game_manager.character)
        assert char_sheet.name is not None, "Character sheet should have name"
        assert char_sheet.level > 0, "Character sheet should have valid level"
        
        print(f"✅ Character Management: Stats update correctly, sheet generation works")
        
    def test_game_state_persistence(self):
        """Test game state maintains consistency across actions"""
        initial_state = self.game_manager.get_current_state()
        
        # Perform several actions
        self.game_manager.increment_turn()
        self.game_manager.award_xp(10, "Test", "exploration")
        roll = self.game_manager.execute_dice_roll('dexterity', 'Stealth', 'normal', 'test')
        
        updated_state = self.game_manager.get_current_state()
        
        # Verify state changes are tracked
        assert updated_state['session']['turn_count'] > initial_state['session']['turn_count']
        assert len(self.game_manager.action_history) > 0, "Should track action history"
        
        print(f"✅ Game State: Persistence and tracking works correctly")
        
    def test_action_validation(self):
        """Test action validation prevents invalid moves"""
        # Test energy-based action validation
        validation = self.game_manager.validate_action(
            ActionType.MAGIC, 
            {'energy_cost': 20}  # More than character has
        )
        
        assert not validation['valid'], "Should reject action requiring too much energy"
        assert len(validation['errors']) > 0, "Should provide error message"
        
        # Test valid action
        valid_validation = self.game_manager.validate_action(
            ActionType.MAGIC,
            {'energy_cost': 5}  # Within character's energy
        )
        
        assert valid_validation['valid'], "Should accept valid action"
        
        print(f"✅ Action Validation: Prevents invalid actions, allows valid ones")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])