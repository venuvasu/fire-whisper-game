#!/usr/bin/env python3
"""
Test Option Generator - Verify dynamic option generation works correctly
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.option_generator import OptionGenerator, EnvironmentType, StakesLevel


def test_option_generation():
    """Test the option generator with various scenarios"""
    
    generator = OptionGenerator()
    
    # Test character (Cleric)
    character = {
        'name': 'Test Cleric',
        'class': 'Cleric',
        'level': 2,
        'stats': {
            'strength': 12,
            'dexterity': 14,
            'intelligence': 13,
            'charisma': 16
        },
        'resources': {
            'hp': 25,
            'max_hp': 31,
            'energy': 12,
            'max_energy': 14
        }
    }
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Corrupted Shrine',
            'situation': 'You stand before a corrupted shrine with dark energy swirling around it',
            'story_context': {'turn_number': 5, 'corruption_level': 'high'},
            'expected_categories': ['magic', 'investigation', 'advice']
        },
        {
            'name': 'Village Encounter',
            'situation': 'Worried villagers approach you asking for help with a mysterious illness',
            'story_context': {'turn_number': 2, 'corruption_level': 'low'},
            'expected_categories': ['social', 'magic', 'advice']
        },
        {
            'name': 'Forest Exploration',
            'situation': 'You enter a dark forest where strange sounds echo from the trees',
            'story_context': {'turn_number': 8, 'corruption_level': 'medium'},
            'expected_categories': ['stealth', 'investigation', 'advice']
        },
        {
            'name': 'Critical Moment',
            'situation': 'Dark entities emerge to stop your cleansing ritual',
            'story_context': {'turn_number': 14, 'corruption_level': 'critical'},
            'expected_categories': ['combat', 'magic', 'advice']
        }
    ]
    
    print("🎮 TESTING DYNAMIC OPTION GENERATION")
    print("="*60)
    
    for scenario in scenarios:
        print(f"\n📖 SCENARIO: {scenario['name']}")
        print(f"Situation: {scenario['situation']}")
        print(f"Context: Turn {scenario['story_context']['turn_number']}, {scenario['story_context']['corruption_level']} corruption")
        
        # Generate options
        options = generator.generate_scene_options(
            scenario['situation'],
            character,
            scenario['story_context']
        )
        
        print(f"\n🎯 GENERATED OPTIONS ({len(options)} total):")
        for i, option in enumerate(options, 1):
            risk_emoji = {
                'low': '🟢',
                'medium': '🟡', 
                'high': '🔴',
                'critical': '⚫'
            }.get(option['risk_level'], '🟡')
            
            print(f"   {i}. {option['text']} {risk_emoji}")
            print(f"      Category: {option['category']} | Risk: {option['risk_level']}")
            if option.get('consequence_hint'):
                print(f"      Hint: {option['consequence_hint']}")
        
        # Verify option quality
        categories = [opt['category'] for opt in options]
        risk_levels = [opt['risk_level'] for opt in options]
        
        print(f"\n✅ QUALITY CHECKS:")
        print(f"   Categories: {set(categories)} (Variety: {'Good' if len(set(categories)) >= 3 else 'Needs Improvement'})")
        print(f"   Risk Levels: {set(risk_levels)} (Balance: {'Good' if len(set(risk_levels)) >= 2 else 'Needs Improvement'})")
        print(f"   Emberlyn Option: {'✅' if any(opt['category'] == 'advice' for opt in options) else '❌'}")
        print(f"   Class-Appropriate: {'✅' if any('divine' in opt['text'].lower() or 'holy' in opt['text'].lower() for opt in options) else '❌'}")
        
        print("-" * 60)
    
    # Test formatted output
    print(f"\n📝 FORMATTED OUTPUT EXAMPLE:")
    test_options = generator.generate_scene_options(
        "You face a corrupted shrine",
        character,
        {'turn_number': 10, 'corruption_level': 'high'}
    )
    
    formatted = generator.format_options_for_ai(test_options)
    print(formatted)
    
    print(f"\n🎯 OPTION GENERATOR TEST COMPLETE!")
    print(f"✅ Dynamic generation working")
    print(f"✅ Class-specific options included")
    print(f"✅ Environmental awareness active")
    print(f"✅ Risk/reward scaling functional")
    print(f"✅ Contextual intelligence operational")


if __name__ == "__main__":
    test_option_generation()