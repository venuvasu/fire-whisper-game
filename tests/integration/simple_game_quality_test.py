#!/usr/bin/env python3
"""
Simple Game Quality Test - Standalone version that works
"""
import sys
import os
import json
import time
import re
from typing import Dict, List

# Add backend to path
sys.path.append('backend')

# Import our hybrid game system
from engine.game_state_manager import GameStateManager, ActionType

class SimpleGameQualityChecker:
    def __init__(self):
        self.issues_found = []
        
    def run_quality_check(self, num_turns=10):
        """Run a simple quality check on the game system"""
        
        print("🧪 FIRE WHISPER QUALITY CHECK")
        print("=" * 50)
        print(f"Testing {num_turns} turns for quality and consistency...")
        
        # Create test character
        character_data = {
            'name': 'QualityTest',
            'class': 'Warrior',
            'level': 1,
            'xp': 0,
            'stats': {'strength': 16, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
            'skills': {'Combat': 2, 'Athletics': 1},
            'resources': {'hp': 35, 'max_hp': 35, 'energy': 10, 'max_energy': 10},
            'emberlyn_bond': 1,
            'achievements': []
        }
        
        # Initialize game manager
        game_manager = GameStateManager(character_data)
        
        # Test mechanical consistency
        print("\n⚙️ Testing Mechanical Consistency...")
        self.test_mechanical_consistency(game_manager, num_turns)
        
        # Test XP tracking
        print("✨ Testing XP Tracking...")
        self.test_xp_tracking(game_manager)
        
        # Test character progression
        print("📈 Testing Character Progression...")
        self.test_character_progression(game_manager)
        
        # Test dice system
        print("🎲 Testing Dice System...")
        self.test_dice_system(game_manager)
        
        # Generate report
        self.generate_report()
        
    def test_mechanical_consistency(self, game_manager, num_turns):
        """Test that mechanics remain consistent over multiple turns"""
        
        initial_character = game_manager.character.copy()
        
        for turn in range(num_turns):
            # Simulate different types of actions
            actions = [
                ('strength', 'Combat', 'normal'),
                ('dexterity', 'Stealth', 'normal'),
                ('intelligence', 'Knowledge', 'normal'),
                ('charisma', 'Persuasion', 'normal')
            ]
            
            stat, skill, difficulty = actions[turn % len(actions)]
            
            # Execute dice roll
            dice_roll = game_manager.execute_dice_roll(stat, skill, difficulty, f"Turn {turn+1}")
            
            # Validate dice roll
            if dice_roll.base_roll < 1 or dice_roll.base_roll > 20:
                self.issues_found.append(f"Turn {turn+1}: Invalid dice roll {dice_roll.base_roll}")
            
            # Check modifiers make sense
            expected_stat_mod = max(0, (game_manager.character['stats'][stat] - 10) // 2)
            actual_stat_mod = dice_roll.modifiers.get(stat.title(), 0)
            
            if expected_stat_mod != actual_stat_mod:
                self.issues_found.append(f"Turn {turn+1}: Stat modifier mismatch for {stat}")
            
            # Award XP and check consistency
            if dice_roll.success:
                xp_result = game_manager.award_xp(20, f"Turn {turn+1} success", "test")
            else:
                xp_result = game_manager.award_xp(5, f"Turn {turn+1} attempt", "test")
            
            # Clear pending rolls
            game_manager.clear_pending_rolls()
        
        print(f"   ✅ Completed {num_turns} turns of mechanical testing")
        
    def test_xp_tracking(self, game_manager):
        """Test XP tracking accuracy"""
        
        initial_xp = game_manager.character['xp']
        
        # Award various amounts of XP
        xp_awards = [10, 25, 15, 30, 5]
        total_expected = sum(xp_awards)
        
        for i, xp_amount in enumerate(xp_awards):
            result = game_manager.award_xp(xp_amount, f"Test award {i+1}", "test")
            
            # Check XP calculation
            if result['xp_awarded'] != xp_amount:
                self.issues_found.append(f"XP Award {i+1}: Expected {xp_amount}, got {result['xp_awarded']}")
        
        # Check total XP
        final_xp = game_manager.character['xp']
        expected_final = initial_xp + total_expected
        
        if final_xp != expected_final:
            self.issues_found.append(f"XP Total: Expected {expected_final}, got {final_xp}")
        else:
            print(f"   ✅ XP tracking accurate: {initial_xp} → {final_xp}")
            
    def test_character_progression(self, game_manager):
        """Test character progression systems"""
        
        initial_level = game_manager.character['level']
        
        # Award enough XP to trigger level up
        game_manager.award_xp(200, "Level up test", "test")
        
        if game_manager.character['level'] <= initial_level:
            self.issues_found.append("Level up failed despite sufficient XP")
        else:
            print(f"   ✅ Level progression working: {initial_level} → {game_manager.character['level']}")
            
    def test_dice_system(self, game_manager):
        """Test dice system reliability"""
        
        # Test multiple dice rolls
        rolls = []
        for i in range(20):
            roll = game_manager.execute_dice_roll('strength', 'Combat', 'normal', f"Dice test {i+1}")
            rolls.append(roll.base_roll)
            game_manager.clear_pending_rolls()
        
        # Check for reasonable distribution
        if min(rolls) < 1 or max(rolls) > 20:
            self.issues_found.append(f"Dice rolls outside valid range: {min(rolls)}-{max(rolls)}")
        
        # Check for variety (not all the same)
        if len(set(rolls)) < 5:
            self.issues_found.append("Dice rolls lack variety - possible randomization issue")
        else:
            print(f"   ✅ Dice system working: Range {min(rolls)}-{max(rolls)}, {len(set(rolls))} unique values")
            
    def generate_report(self):
        """Generate quality report"""
        
        print("\n📊 QUALITY CHECK REPORT")
        print("=" * 50)
        
        if not self.issues_found:
            print("🌟 EXCELLENT - No issues found!")
            print("✅ All mechanical systems working correctly")
            print("✅ XP tracking accurate")
            print("✅ Character progression functional")
            print("✅ Dice system reliable")
            print("\n🎯 Status: READY FOR PRODUCTION")
            
        else:
            print(f"⚠️ ISSUES FOUND: {len(self.issues_found)} problems detected")
            print("\n🔍 Detailed Issues:")
            for i, issue in enumerate(self.issues_found, 1):
                print(f"   {i}. {issue}")
            
            print(f"\n🎯 Status: NEEDS ATTENTION")
            print("Fix these issues before deploying changes")
        
        print("\n" + "=" * 50)

def main():
    print("🔥 FIRE WHISPER - SIMPLE QUALITY CHECK")
    print("This tests core game mechanics without AI integration")
    print()
    
    try:
        turns = int(input("Number of turns to test (default 10): ") or "10")
    except ValueError:
        turns = 10
    
    checker = SimpleGameQualityChecker()
    checker.run_quality_check(turns)
    
    print("\n💡 Next Steps:")
    print("- If this passes, your core mechanics are solid")
    print("- Run hybrid_game_test.py to test with AI integration")
    print("- Use this before making any rule changes")

if __name__ == "__main__":
    main()