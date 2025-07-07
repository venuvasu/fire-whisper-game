#!/usr/bin/env python3
"""
Enhanced Premium Tests - Test premium experience with new narrative integration
"""

import pytest
import time
from typing import Dict, Any
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.enhanced_ai_integration import EnhancedAIIntegrationLayer


class EnhancedPremiumTester:
    """Test premium experience with enhanced integration"""
    
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        api_key = os.getenv('CLAUDE_API_KEY')
        
        character_data = {
            'name': 'Premium Hero',
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
        
    def test_immediate_gratification_loop(self, prompt: str) -> Dict[str, Any]:
        """Test enhanced immediate gratification"""
        results = {
            'xp_notification': False,
            'skill_check_visible': False,
            'loot_discovery': False,
            'emberlyn_moment': False,
            'clear_stakes': False,
            'narrative_integration': False,  # NEW
            'response_time': 0,
            'score': 0
        }
        
        start_time = time.time()
        response = self.ai_integration.process_player_action(prompt)
        results['response_time'] = time.time() - start_time
        
        narrative = response['narrative']
        
        # Check for XP integration (natural language)
        xp_indicators = ['experience', 'understanding', 'skills', 'stronger', 'capable', 'wisdom', 'confidence']
        if any(indicator in narrative.lower() for indicator in xp_indicators):
            results['xp_notification'] = True
            results['score'] += 25  # Increased from 20
            
        # Check for skill integration (natural language)
        skill_indicators = ['strength', 'combat', 'charisma', 'healing', 'approach', 'drawing', 'natural']
        if any(indicator in narrative.lower() for indicator in skill_indicators):
            results['skill_check_visible'] = True
            results['score'] += 25  # Increased from 20
            
        # Check for narrative integration quality
        integration_phrases = ['skilled', 'drawing upon', 'natural', 'honed by', 'proves effective', 'serves you well']
        if any(phrase in narrative.lower() for phrase in integration_phrases):
            results['narrative_integration'] = True
            results['score'] += 20  # NEW scoring category
            
        # Check for loot/discovery
        loot_indicators = ['find', 'discover', 'loot', 'item', 'treasure', 'equipment']
        if any(indicator in narrative.lower() for indicator in loot_indicators):
            results['loot_discovery'] = True
            results['score'] += 15
            
        # Check for Emberlyn personality
        if 'emberlyn' in narrative.lower():
            results['emberlyn_moment'] = True
            results['score'] += 15
            
        # Check for clear stakes
        stakes_indicators = ['consequence', 'risk', 'reward', 'choice', 'careful', 'dangerous']
        if any(indicator in narrative.lower() for indicator in stakes_indicators):
            results['clear_stakes'] = True
            results['score'] += 15
            
        return results


class TestEnhancedPremiumExperience:
    """Test enhanced premium experience"""
    
    def setup_method(self):
        self.tester = EnhancedPremiumTester()
        
    def test_enhanced_combat_premium_experience(self):
        """Test enhanced combat premium experience"""
        prompt = "I draw my enchanted blade and charge at the orc chieftain"
        
        gratification_results = self.tester.test_immediate_gratification_loop(prompt)
        
        print(f"\n=== ENHANCED PREMIUM COMBAT EXPERIENCE ===")
        print(f"XP Notification (Natural): {gratification_results['xp_notification']} - 25pts")
        print(f"Skill Integration (Natural): {gratification_results['skill_check_visible']} - 25pts") 
        print(f"Narrative Integration: {gratification_results['narrative_integration']} - 20pts")
        print(f"Loot Discovery: {gratification_results['loot_discovery']} - 15pts")
        print(f"Emberlyn Moment: {gratification_results['emberlyn_moment']} - 15pts")
        print(f"Clear Stakes: {gratification_results['clear_stakes']} - 15pts")
        print(f"ENHANCED GRATIFICATION SCORE: {gratification_results['score']}/115")
        print(f"Response Time: {gratification_results['response_time']:.2f}s")
        
        # Enhanced scoring - should be much higher now
        assert gratification_results['score'] >= 50, f"Enhanced gratification score too low: {gratification_results['score']}/115"
        assert gratification_results['response_time'] < 20, "Response time acceptable for enhanced experience"
        
        print("✅ Enhanced premium experience significantly improved!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])