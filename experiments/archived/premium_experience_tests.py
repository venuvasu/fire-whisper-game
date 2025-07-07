#!/usr/bin/env python3
"""
Premium Experience Tests - Verify Fire Whisper delivers Netflix-quality RPG experience
Tests the specific elements that make players willing to pay
"""

import pytest
import json
import time
from typing import Dict, List, Any
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.game_state_manager import GameStateManager
from engine.ai_integration import AIIntegrationLayer
from utils.character_sheet import CharacterSheet


class PremiumExperienceTester:
    """Tests that verify the game delivers premium, pay-worthy experiences"""
    
    def __init__(self):
        # Load environment for API key
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        api_key = os.getenv('CLAUDE_API_KEY')
        
        # Initialize with complete character data
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
        
        self.ai_integration = AIIntegrationLayer(api_key)
        self.game_result = self.ai_integration.start_new_game(character_data)
        
    def test_immediate_gratification_loop(self, prompt: str) -> Dict[str, Any]:
        """Test if game provides rewards every 2-3 minutes of play"""
        results = {
            'xp_notification': False,
            'skill_check_visible': False,
            'loot_discovery': False,
            'emberlyn_moment': False,
            'clear_stakes': False,
            'response_time': 0,
            'score': 0
        }
        
        start_time = time.time()
        response = self.ai_integration.process_player_action(prompt)
        results['response_time'] = time.time() - start_time
        
        narrative = response['narrative']
        
        # Check for XP/progression notifications
        xp_indicators = ['xp', 'experience', 'points', 'level up', 'gained', '+']
        if any(indicator in narrative.lower() for indicator in xp_indicators):
            results['xp_notification'] = True
            results['score'] += 20
            
        # Check for visible skill checks/dice rolls
        dice_indicators = ['roll', 'd20', 'dice', 'check', 'bonus', 'modifier']
        if any(indicator in narrative.lower() for indicator in dice_indicators):
            results['skill_check_visible'] = True
            results['score'] += 20
            
        # Check for loot/item discovery
        loot_indicators = ['find', 'discover', 'loot', 'item', 'treasure', 'equipment']
        if any(indicator in narrative.lower() for indicator in loot_indicators):
            results['loot_discovery'] = True
            results['score'] += 20
            
        # Check for Emberlyn personality moments
        if 'emberlyn' in narrative.lower():
            results['emberlyn_moment'] = True
            results['score'] += 20
            
        # Check for clear stakes/consequences
        stakes_indicators = ['if you', 'consequence', 'risk', 'reward', 'choice']
        if any(indicator in narrative.lower() for indicator in stakes_indicators):
            results['clear_stakes'] = True
            results['score'] += 20
            
        return results
    
    def test_character_investment_system(self, prompt: str) -> Dict[str, Any]:
        """Test if players feel invested in their character"""
        results = {
            'stats_visible': False,
            'player_choice_stats': False,
            'progression_bars': False,
            'unlockable_abilities': False,
            'emberlyn_relationship': False,
            'score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check if character stats are shown
        stat_names = ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'constitution']
        if any(stat in narrative.lower() for stat in stat_names):
            results['stats_visible'] = True
            results['score'] += 20
            
        # Check if player can choose/influence stats
        choice_indicators = ['choose', 'select', 'pick', 'decide', 'build']
        if any(indicator in narrative.lower() for indicator in choice_indicators):
            results['player_choice_stats'] = True
            results['score'] += 20
            
        # Check for progression indicators
        progress_indicators = ['progress', 'advance', 'improve', 'grow', 'develop']
        if any(indicator in narrative.lower() for indicator in progress_indicators):
            results['progression_bars'] = True
            results['score'] += 20
            
        # Check for unlockable content
        unlock_indicators = ['unlock', 'learn', 'gain', 'acquire', 'master']
        if any(indicator in narrative.lower() for indicator in unlock_indicators):
            results['unlockable_abilities'] = True
            results['score'] += 20
            
        # Check for Emberlyn relationship development
        relationship_indicators = ['bond', 'trust', 'friendship', 'relationship', 'closer']
        if any(indicator in narrative.lower() for indicator in relationship_indicators):
            results['emberlyn_relationship'] = True
            results['score'] += 20
            
        return results
    
    def test_stakes_and_tension(self, prompt: str) -> Dict[str, Any]:
        """Test if game creates real consequences and tension"""
        results = {
            'health_resources_matter': False,
            'permanent_changes': False,
            'world_changes': False,
            'time_pressure': False,
            'moral_dilemmas': False,
            'score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check for resource management
        resource_indicators = ['health', 'mana', 'energy', 'stamina', 'resources', 'limited']
        if any(indicator in narrative.lower() for indicator in resource_indicators):
            results['health_resources_matter'] = True
            results['score'] += 20
            
        # Check for permanent consequences
        permanent_indicators = ['permanent', 'forever', 'cannot undo', 'irreversible', 'lasting']
        if any(indicator in narrative.lower() for indicator in permanent_indicators):
            results['permanent_changes'] = True
            results['score'] += 20
            
        # Check for world state changes
        world_indicators = ['world', 'village', 'kingdom', 'realm', 'changes', 'affected']
        if any(indicator in narrative.lower() for indicator in world_indicators):
            results['world_changes'] = True
            results['score'] += 20
            
        # Check for urgency/time pressure
        urgency_indicators = ['urgent', 'quickly', 'time', 'hurry', 'before', 'deadline']
        if any(indicator in narrative.lower() for indicator in urgency_indicators):
            results['time_pressure'] = True
            results['score'] += 20
            
        # Check for moral complexity
        moral_indicators = ['right', 'wrong', 'moral', 'ethical', 'dilemma', 'difficult choice']
        if any(indicator in narrative.lower() for indicator in moral_indicators):
            results['moral_dilemmas'] = True
            results['score'] += 20
            
        return results
    
    def test_gameplay_variety(self, prompt: str) -> Dict[str, Any]:
        """Test if game provides varied, never-boring gameplay"""
        results = {
            'combat_elements': False,
            'social_challenges': False,
            'exploration_discovery': False,
            'puzzles_mysteries': False,
            'variety_score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check for combat elements
        combat_indicators = ['fight', 'battle', 'attack', 'defend', 'weapon', 'combat']
        if any(indicator in narrative.lower() for indicator in combat_indicators):
            results['combat_elements'] = True
            results['variety_score'] += 25
            
        # Check for social challenges
        social_indicators = ['persuade', 'convince', 'negotiate', 'charm', 'intimidate', 'deceive']
        if any(indicator in narrative.lower() for indicator in social_indicators):
            results['social_challenges'] = True
            results['variety_score'] += 25
            
        # Check for exploration/discovery
        explore_indicators = ['explore', 'search', 'investigate', 'discover', 'find', 'hidden']
        if any(indicator in narrative.lower() for indicator in explore_indicators):
            results['exploration_discovery'] = True
            results['variety_score'] += 25
            
        # Check for puzzles/mysteries
        puzzle_indicators = ['puzzle', 'riddle', 'mystery', 'solve', 'figure out', 'clue']
        if any(indicator in narrative.lower() for indicator in puzzle_indicators):
            results['puzzles_mysteries'] = True
            results['variety_score'] += 25
            
        return results
    
    def test_netflix_moment_quality(self, prompt: str) -> Dict[str, Any]:
        """Test if response quality matches premium entertainment standards"""
        results = {
            'professional_writing': False,
            'engaging_narrative': False,
            'character_depth': False,
            'world_building': False,
            'emotional_resonance': False,
            'length_appropriate': False,
            'score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check writing quality (length, complexity, descriptiveness)
        if len(narrative) > 150 and len(narrative.split('.')) > 3:
            results['professional_writing'] = True
            results['score'] += 15
            
        # Check for engaging narrative elements
        narrative_indicators = ['story', 'tale', 'adventure', 'journey', 'epic', 'legend']
        if any(indicator in narrative.lower() for indicator in narrative_indicators):
            results['engaging_narrative'] = True
            results['score'] += 15
            
        # Check for character depth
        character_indicators = ['personality', 'motivation', 'background', 'history', 'feelings']
        if any(indicator in narrative.lower() for indicator in character_indicators):
            results['character_depth'] = True
            results['score'] += 15
            
        # Check for world-building details
        world_indicators = ['ancient', 'kingdom', 'realm', 'culture', 'tradition', 'lore']
        if any(indicator in narrative.lower() for indicator in world_indicators):
            results['world_building'] = True
            results['score'] += 15
            
        # Check for emotional engagement
        emotion_indicators = ['feel', 'emotion', 'heart', 'soul', 'passion', 'fear', 'hope']
        if any(indicator in narrative.lower() for indicator in emotion_indicators):
            results['emotional_resonance'] = True
            results['score'] += 20
            
        # Check appropriate length (not too short, not overwhelming)
        if 100 <= len(narrative) <= 500:
            results['length_appropriate'] = True
            results['score'] += 20
            
        return results


class TestPremiumExperience:
    """Test suite for premium experience validation"""
    
    def setup_method(self):
        self.tester = PremiumExperienceTester()
        
    def test_combat_premium_experience(self):
        """Test if combat delivers premium experience worthy of payment"""
        prompt = "I draw my enchanted blade and charge at the orc chieftain"
        
        gratification_results = self.tester.test_immediate_gratification_loop(prompt)
        investment_results = self.tester.test_character_investment_system(prompt)
        tension_results = self.tester.test_stakes_and_tension(prompt)
        variety_results = self.tester.test_gameplay_variety(prompt)
        quality_results = self.tester.test_netflix_moment_quality(prompt)
        
        total_score = (
            gratification_results['score'] + 
            investment_results['score'] + 
            tension_results['score'] + 
            variety_results['variety_score'] + 
            quality_results['score']
        ) / 5
        
        print(f"\n=== PREMIUM COMBAT EXPERIENCE ===")
        print(f"Immediate Gratification: {gratification_results['score']}/100")
        print(f"Character Investment: {investment_results['score']}/100")
        print(f"Stakes & Tension: {tension_results['score']}/100")
        print(f"Gameplay Variety: {variety_results['variety_score']}/100")
        print(f"Netflix Quality: {quality_results['score']}/100")
        print(f"PREMIUM SCORE: {total_score}/100")
        print(f"Response Time: {gratification_results['response_time']:.2f}s")
        
        # Premium experience should score 70+ to justify payment
        assert total_score >= 70, f"Premium experience score too low: {total_score}/100"
        assert gratification_results['response_time'] < 5, "Response too slow for premium experience"
        
    def test_exploration_premium_experience(self):
        """Test if exploration delivers premium experience"""
        prompt = "I want to investigate the ancient ruins that Emberlyn mentioned, looking for clues about the lost civilization"
        
        gratification_results = self.tester.test_immediate_gratification_loop(prompt)
        investment_results = self.tester.test_character_investment_system(prompt)
        tension_results = self.tester.test_stakes_and_tension(prompt)
        variety_results = self.tester.test_gameplay_variety(prompt)
        quality_results = self.tester.test_netflix_moment_quality(prompt)
        
        total_score = (
            gratification_results['score'] + 
            investment_results['score'] + 
            tension_results['score'] + 
            variety_results['variety_score'] + 
            quality_results['score']
        ) / 5
        
        print(f"\n=== PREMIUM EXPLORATION EXPERIENCE ===")
        print(f"Immediate Gratification: {gratification_results['score']}/100")
        print(f"Character Investment: {investment_results['score']}/100")
        print(f"Stakes & Tension: {tension_results['score']}/100")
        print(f"Gameplay Variety: {variety_results['variety_score']}/100")
        print(f"Netflix Quality: {quality_results['score']}/100")
        print(f"PREMIUM SCORE: {total_score}/100")
        
        assert total_score >= 70, f"Premium exploration score too low: {total_score}/100"
        
    def test_social_premium_experience(self):
        """Test if social interactions deliver premium experience"""
        prompt = "I want to build trust with the suspicious tavern keeper by sharing a personal story and buying drinks for the house"
        
        gratification_results = self.tester.test_immediate_gratification_loop(prompt)
        investment_results = self.tester.test_character_investment_system(prompt)
        tension_results = self.tester.test_stakes_and_tension(prompt)
        variety_results = self.tester.test_gameplay_variety(prompt)
        quality_results = self.tester.test_netflix_moment_quality(prompt)
        
        total_score = (
            gratification_results['score'] + 
            investment_results['score'] + 
            tension_results['score'] + 
            variety_results['variety_score'] + 
            quality_results['score']
        ) / 5
        
        print(f"\n=== PREMIUM SOCIAL EXPERIENCE ===")
        print(f"Immediate Gratification: {gratification_results['score']}/100")
        print(f"Character Investment: {investment_results['score']}/100")
        print(f"Stakes & Tension: {tension_results['score']}/100")
        print(f"Gameplay Variety: {variety_results['variety_score']}/100")
        print(f"Netflix Quality: {quality_results['score']}/100")
        print(f"PREMIUM SCORE: {total_score}/100")
        
        assert total_score >= 70, f"Premium social score too low: {total_score}/100"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])