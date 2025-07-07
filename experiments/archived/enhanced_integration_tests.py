#!/usr/bin/env python3
"""
Enhanced Integration Tests - Test the new narrative integration system
"""

import pytest
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.enhanced_ai_integration import EnhancedAIIntegrationLayer


class TestEnhancedIntegration:
    """Test enhanced narrative integration"""
    
    def setup_method(self):
        """Setup enhanced AI integration"""
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        api_key = os.getenv('CLAUDE_API_KEY')
        
        character_data = {
            'name': 'Enhanced Hero',
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
        
        self.ai_integration = EnhancedAIIntegrationLayer(api_key)
        self.game_result = self.ai_integration.start_new_game(character_data)
        
    def test_narrative_integration_combat(self):
        """Test that combat actions show integrated mechanics"""
        prompt = "I attack the goblin with my sword"
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        print(f"\n=== ENHANCED COMBAT RESPONSE ===")
        print(narrative)
        print(f"=====================================")
        
        # Check for narrative integration (not explicit mechanics)
        integration_indicators = [
            'strength', 'combat', 'skilled', 'approach', 'drawing', 'natural'
        ]
        
        has_integration = any(indicator in narrative.lower() for indicator in integration_indicators)
        assert has_integration, "Should integrate mechanics into narrative naturally"
        
        # Should NOT have explicit mechanics
        explicit_mechanics = ['🎲', 'roll:', '+25 xp', 'dice', 'modifier']
        has_explicit = any(mechanic in narrative.lower() for mechanic in explicit_mechanics)
        assert not has_explicit, "Should not show explicit mechanics in narrative"
        
        # Check for XP integration
        xp_integration_phrases = [
            'experience', 'skills', 'understanding', 'growing', 'stronger', 
            'capable', 'lessons', 'confidence', 'expertise', 'wisdom'
        ]
        
        has_xp_integration = any(phrase in narrative.lower() for phrase in xp_integration_phrases)
        assert has_xp_integration, "Should integrate XP rewards naturally"
        
        print("✅ Combat narrative integration working")
        
    def test_character_status_integration(self):
        """Test character status appears when relevant"""
        # Damage character first
        self.ai_integration.game_manager.character['resources']['hp'] = 8  # Low HP
        
        prompt = "I check my condition"
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        print(f"\n=== CHARACTER STATUS INTEGRATION ===")
        print(narrative)
        print(f"=====================================")
        
        # Should mention being wounded
        wound_indicators = ['wounded', 'injured', 'hurt', 'damage', 'healing']
        has_wound_mention = any(indicator in narrative.lower() for indicator in wound_indicators)
        assert has_wound_mention, "Should mention low HP naturally"
        
        print("✅ Character status integration working")
        
    def test_behavior_tracking(self):
        """Test behavior tracking and warnings"""
        # Test inappropriate behavior
        bad_prompts = [
            "I attack the innocent villager",
            "I try to seduce the NPC", 
            "I want to hack the game"
        ]
        
        for i, prompt in enumerate(bad_prompts):
            response = self.ai_integration.process_player_action(prompt)
            behavior_info = response.get('behavior_info', {})
            
            print(f"\n=== BEHAVIOR TEST {i+1}: {prompt} ===")
            print(f"Warning Level: {behavior_info.get('warning_level', 0)}")
            print(f"Stakes Level: {behavior_info.get('stakes_level', 'medium')}")
            print(f"Issues: {behavior_info.get('behavior_issues', [])}")
            
            if i < 2:  # First two should be warnings
                assert behavior_info.get('warning_level', 0) > 0, f"Should warn for inappropriate behavior: {prompt}"
            else:  # Third should escalate stakes
                assert behavior_info.get('stakes_level') == 'high', "Should escalate to high stakes after 3 warnings"
        
        print("✅ Behavior tracking working")
        
    def test_good_behavior_reset(self):
        """Test that good behavior resets warnings"""
        # First, trigger a warning
        self.ai_integration.process_player_action("I attack innocent people")
        
        # Then do good actions
        good_prompts = [
            "I help the villager with their problem",
            "I heal the wounded traveler", 
            "I donate to the local temple"
        ]
        
        for prompt in good_prompts:
            response = self.ai_integration.process_player_action(prompt)
            
        # Check final behavior state
        final_response = self.ai_integration.process_player_action("I continue my quest")
        behavior_info = final_response.get('behavior_info', {})
        
        print(f"\n=== BEHAVIOR RESET TEST ===")
        print(f"Final Warning Level: {behavior_info.get('warning_level', 0)}")
        print(f"Final Stakes Level: {behavior_info.get('stakes_level', 'medium')}")
        
        assert behavior_info.get('warning_level', 0) == 0, "Warnings should reset after good behavior"
        assert behavior_info.get('stakes_level') == 'medium', "Stakes should return to medium"
        
        print("✅ Good behavior reset working")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])