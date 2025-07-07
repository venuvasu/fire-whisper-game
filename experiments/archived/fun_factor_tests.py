#!/usr/bin/env python3
"""
Fun Factor Tests - Verify Fire Whisper delivers core RPG motivations
Tests both functionality AND entertainment value based on player psychology
"""

import pytest
import json
import re
from typing import Dict, List, Any
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.game_state_manager import GameStateManager
from engine.ai_integration import AIIntegrationLayer
from utils.character_sheet import CharacterSheet
from utils.dice_system import DiceRoll


class FunFactorTester:
    """Tests that verify the game delivers on core RPG motivations"""
    
    def __init__(self):
        # Load environment for API key
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        api_key = os.getenv('CLAUDE_API_KEY')
        
        # Initialize with complete character data
        character_data = {
            'name': 'Fun Hero',
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
        
    def test_agency_and_identity(self, prompt: str) -> Dict[str, Any]:
        """Test if player feels agency and can build unique identity"""
        results = {
            'character_ownership': False,
            'meaningful_choices': False,
            'progression_visible': False,
            'unique_identity': False,
            'score': 0
        }
        
        # Test character ownership
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check if character stats are mentioned/visible
        if any(stat in narrative.lower() for stat in ['strength', 'dexterity', 'intelligence', 'wisdom', 'charisma', 'constitution']):
            results['character_ownership'] = True
            results['score'] += 25
            
        # Check for meaningful choice presentation
        choice_indicators = ['choose', 'decide', 'option', 'approach', 'method', 'way']
        if any(indicator in narrative.lower() for indicator in choice_indicators):
            results['meaningful_choices'] = True
            results['score'] += 25
            
        # Check for progression visibility
        progression_indicators = ['xp', 'experience', 'level', 'skill', 'ability', 'unlock']
        if any(indicator in narrative.lower() for indicator in progression_indicators):
            results['progression_visible'] = True
            results['score'] += 25
            
        # Check for unique identity building
        identity_indicators = ['your', 'you are', 'your character', 'your approach', 'your style']
        if any(indicator in narrative.lower() for indicator in identity_indicators):
            results['unique_identity'] = True
            results['score'] += 25
            
        return results
    
    def test_dopamine_loops(self, prompt: str) -> Dict[str, Any]:
        """Test if game provides satisfying dopamine hits"""
        results = {
            'immediate_rewards': False,
            'uncertainty_excitement': False,
            'completion_satisfaction': False,
            'collection_urges': False,
            'score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check for immediate reward feedback
        reward_indicators = ['success', 'gain', 'earn', 'find', 'discover', 'achieve']
        if any(indicator in narrative.lower() for indicator in reward_indicators):
            results['immediate_rewards'] = True
            results['score'] += 25
            
        # Check for uncertainty/mystery elements
        mystery_indicators = ['mysterious', 'unknown', 'hidden', 'secret', 'wonder', 'curious']
        if any(indicator in narrative.lower() for indicator in mystery_indicators):
            results['uncertainty_excitement'] = True
            results['score'] += 25
            
        # Check for completion elements
        completion_indicators = ['complete', 'finish', 'accomplish', 'solve', 'defeat']
        if any(indicator in narrative.lower() for indicator in completion_indicators):
            results['completion_satisfaction'] = True
            results['score'] += 25
            
        # Check for collectible/loot elements
        collection_indicators = ['item', 'treasure', 'loot', 'collect', 'gather', 'equipment']
        if any(indicator in narrative.lower() for indicator in collection_indicators):
            results['collection_urges'] = True
            results['score'] += 25
            
        return results
    
    def test_social_connection(self, prompt: str) -> Dict[str, Any]:
        """Test if game creates shareable, memorable moments"""
        results = {
            'memorable_moments': False,
            'emberlyn_personality': False,
            'unique_outcomes': False,
            'shareable_content': False,
            'score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check for memorable moment creation
        memorable_indicators = ['dramatic', 'epic', 'incredible', 'amazing', 'unforgettable']
        if any(indicator in narrative.lower() for indicator in memorable_indicators):
            results['memorable_moments'] = True
            results['score'] += 25
            
        # Check for Emberlyn personality showing through
        if 'emberlyn' in narrative.lower():
            results['emberlyn_personality'] = True
            results['score'] += 25
            
        # Check for unique outcomes
        unique_indicators = ['unusual', 'rare', 'special', 'unique', 'extraordinary']
        if any(indicator in narrative.lower() for indicator in unique_indicators):
            results['unique_outcomes'] = True
            results['score'] += 25
            
        # Check for shareable content potential
        if len(narrative) > 200 and any(indicator in narrative.lower() for indicator in ['story', 'tale', 'adventure']):
            results['shareable_content'] = True
            results['score'] += 25
            
        return results
    
    def test_intellectual_engagement(self, prompt: str) -> Dict[str, Any]:
        """Test if game provides meaningful strategic depth"""
        results = {
            'tactical_choices': False,
            'resource_management': False,
            'strategic_thinking': False,
            'problem_solving': False,
            'score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check for tactical choice presentation
        tactical_indicators = ['strategy', 'tactic', 'approach', 'method', 'plan']
        if any(indicator in narrative.lower() for indicator in tactical_indicators):
            results['tactical_choices'] = True
            results['score'] += 25
            
        # Check for resource management elements
        resource_indicators = ['energy', 'mana', 'health', 'stamina', 'resources', 'cost']
        if any(indicator in narrative.lower() for indicator in resource_indicators):
            results['resource_management'] = True
            results['score'] += 25
            
        # Check for strategic thinking requirements
        strategy_indicators = ['consider', 'think', 'plan', 'prepare', 'consequence']
        if any(indicator in narrative.lower() for indicator in strategy_indicators):
            results['strategic_thinking'] = True
            results['score'] += 25
            
        # Check for problem-solving elements
        problem_indicators = ['puzzle', 'riddle', 'challenge', 'obstacle', 'problem']
        if any(indicator in narrative.lower() for indicator in problem_indicators):
            results['problem_solving'] = True
            results['score'] += 25
            
        return results
    
    def test_emotional_investment(self, prompt: str) -> Dict[str, Any]:
        """Test if game creates emotional attachment and investment"""
        results = {
            'character_attachment': False,
            'narrative_tension': False,
            'achievement_pride': False,
            'discovery_wonder': False,
            'score': 0
        }
        
        response = self.ai_integration.process_player_action(prompt)
        narrative = response['narrative']
        
        # Check for character attachment building
        attachment_indicators = ['bond', 'relationship', 'trust', 'friendship', 'companion']
        if any(indicator in narrative.lower() for indicator in attachment_indicators):
            results['character_attachment'] = True
            results['score'] += 25
            
        # Check for narrative tension
        tension_indicators = ['danger', 'risk', 'threat', 'urgent', 'critical', 'stakes']
        if any(indicator in narrative.lower() for indicator in tension_indicators):
            results['narrative_tension'] = True
            results['score'] += 25
            
        # Check for achievement pride potential
        achievement_indicators = ['overcome', 'triumph', 'victory', 'succeed', 'master']
        if any(indicator in narrative.lower() for indicator in achievement_indicators):
            results['achievement_pride'] = True
            results['score'] += 25
            
        # Check for discovery wonder
        wonder_indicators = ['discover', 'reveal', 'uncover', 'explore', 'find', 'wonder']
        if any(indicator in narrative.lower() for indicator in wonder_indicators):
            results['discovery_wonder'] = True
            results['score'] += 25
            
        return results


class TestSimplePromptsWithFunFactor:
    """Test suite combining functionality and fun factor validation"""
    
    def setup_method(self):
        self.tester = FunFactorTester()
        
    def test_basic_combat_fun_factor(self):
        """Test basic combat prompt for both function and fun"""
        prompt = "I attack the goblin with my sword"
        
        # Test all fun factors
        agency_results = self.tester.test_agency_and_identity(prompt)
        dopamine_results = self.tester.test_dopamine_loops(prompt)
        social_results = self.tester.test_social_connection(prompt)
        intellectual_results = self.tester.test_intellectual_engagement(prompt)
        emotional_results = self.tester.test_emotional_investment(prompt)
        
        # Calculate overall fun score
        total_score = (
            agency_results['score'] + 
            dopamine_results['score'] + 
            social_results['score'] + 
            intellectual_results['score'] + 
            emotional_results['score']
        ) / 5
        
        print(f"\n=== COMBAT TEST RESULTS ===")
        print(f"Agency & Identity: {agency_results['score']}/100")
        print(f"Dopamine Loops: {dopamine_results['score']}/100")
        print(f"Social Connection: {social_results['score']}/100")
        print(f"Intellectual Engagement: {intellectual_results['score']}/100")
        print(f"Emotional Investment: {emotional_results['score']}/100")
        print(f"OVERALL FUN SCORE: {total_score}/100")
        
        # Assert minimum fun threshold
        assert total_score >= 60, f"Combat fun score too low: {total_score}/100"
        
    def test_exploration_fun_factor(self):
        """Test exploration prompt for both function and fun"""
        prompt = "I want to explore the mysterious forest to the north"
        
        agency_results = self.tester.test_agency_and_identity(prompt)
        dopamine_results = self.tester.test_dopamine_loops(prompt)
        social_results = self.tester.test_social_connection(prompt)
        intellectual_results = self.tester.test_intellectual_engagement(prompt)
        emotional_results = self.tester.test_emotional_investment(prompt)
        
        total_score = (
            agency_results['score'] + 
            dopamine_results['score'] + 
            social_results['score'] + 
            intellectual_results['score'] + 
            emotional_results['score']
        ) / 5
        
        print(f"\n=== EXPLORATION TEST RESULTS ===")
        print(f"Agency & Identity: {agency_results['score']}/100")
        print(f"Dopamine Loops: {dopamine_results['score']}/100")
        print(f"Social Connection: {social_results['score']}/100")
        print(f"Intellectual Engagement: {intellectual_results['score']}/100")
        print(f"Emotional Investment: {emotional_results['score']}/100")
        print(f"OVERALL FUN SCORE: {total_score}/100")
        
        assert total_score >= 60, f"Exploration fun score too low: {total_score}/100"
        
    def test_social_interaction_fun_factor(self):
        """Test social interaction prompt for both function and fun"""
        prompt = "I want to convince the merchant to give me a better price using my charisma"
        
        agency_results = self.tester.test_agency_and_identity(prompt)
        dopamine_results = self.tester.test_dopamine_loops(prompt)
        social_results = self.tester.test_social_connection(prompt)
        intellectual_results = self.tester.test_intellectual_engagement(prompt)
        emotional_results = self.tester.test_emotional_investment(prompt)
        
        total_score = (
            agency_results['score'] + 
            dopamine_results['score'] + 
            social_results['score'] + 
            intellectual_results['score'] + 
            emotional_results['score']
        ) / 5
        
        print(f"\n=== SOCIAL INTERACTION TEST RESULTS ===")
        print(f"Agency & Identity: {agency_results['score']}/100")
        print(f"Dopamine Loops: {dopamine_results['score']}/100")
        print(f"Social Connection: {social_results['score']}/100")
        print(f"Intellectual Engagement: {intellectual_results['score']}/100")
        print(f"Emotional Investment: {emotional_results['score']}/100")
        print(f"OVERALL FUN SCORE: {total_score}/100")
        
        assert total_score >= 60, f"Social interaction fun score too low: {total_score}/100"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "-s"])