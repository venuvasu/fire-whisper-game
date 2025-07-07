#!/usr/bin/env python3
"""
Run Fun Tests - Quick test runner for the enhanced system
"""

import pytest
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.ai_integration import AIIntegrationLayer


def test_enhanced_system():
    """Quick test of enhanced system"""
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv('.env.local')
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✅ API key loaded: {api_key[:20]}...")
    
    # Test character creation
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
    
    try:
        ai_integration = AIIntegrationLayer(api_key)
        print("✅ AI Integration created")
        
        game_result = ai_integration.start_new_game(character_data)
        print("✅ Game started")
        print(f"Initial narrative: {game_result['narrative'][:100]}...")
        
        # Test action
        response = ai_integration.process_player_action("I attack the goblin")
        print("✅ Action processed")
        print(f"Enhanced response: {response['narrative'][:200]}...")
        
        # Check for enhancements
        narrative = response['narrative']
        
        enhancements_found = []
        if any(word in narrative.lower() for word in ['strength', 'combat', 'skilled', 'drawing']):
            enhancements_found.append("✅ Dice integration")
        if any(word in narrative.lower() for word in ['experience', 'understanding', 'stronger', 'wisdom']):
            enhancements_found.append("✅ XP integration")
        if 'emberlyn' in narrative.lower():
            enhancements_found.append("✅ Emberlyn personality")
        
        print(f"\nEnhancements detected: {len(enhancements_found)}/3")
        for enhancement in enhancements_found:
            print(f"  {enhancement}")
            
        print(f"\n🎯 ENHANCED SYSTEM STATUS: {'WORKING' if len(enhancements_found) >= 2 else 'NEEDS WORK'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_enhanced_system()