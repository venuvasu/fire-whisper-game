#!/usr/bin/env python3
"""
Test script for the integrated story systems
Demonstrates story arc integration, location debugging, and dynamic options
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.core.integrated_story_controller import IntegratedStoryController
from src.core.game_state_manager import GameStateManager
from src.core.story_state_manager import StoryStateManager

def test_story_arc_integration():
    """Test story arc system"""
    print("=== TESTING STORY ARC INTEGRATION ===")
    
    controller = IntegratedStoryController()
    
    # Check available story arcs
    arc_stats = controller.story_arc_manager.get_arc_statistics()
    print(f"Total story arcs available: {arc_stats['total_arcs']}")
    print(f"Currently available: {arc_stats['available_arcs']}")
    
    # Try to activate a story arc
    character_level = 1
    story_context = {
        'character_level': character_level,
        'turn_count': 1,
        'story_flags': {'met_emberlyn': True},
        'themes': ['restoration', 'mystery']
    }
    
    selected_arc = controller.story_arc_manager.select_arc_for_context(
        character_level, story_context, 'village_outskirts'
    )
    
    if selected_arc:
        print(f"\\nSelected arc: {selected_arc.name}")
        print(f"Type: {selected_arc.arc_type.value}")
        print(f"Hook: {selected_arc.hook}")
        
        # Activate the arc
        activation_result = controller.story_arc_manager.activate_arc(selected_arc)
        print(f"\\nArc activated: {activation_result['arc_activated']}")
        print(f"Integration context generated: {len(activation_result['integration_context'])} characters")
    else:
        print("No suitable arc found for current context")
    
    print("\\n" + "="*50 + "\\n")

def test_location_debugging():
    """Test location progression debugging"""
    print("=== TESTING LOCATION DEBUGGING ===")
    
    controller = IntegratedStoryController()
    
    # Test location transition detection
    test_ai_responses = [
        "You walk toward Ashbrook village, the path winding through autumn trees.",
        "Moving deeper into the crystal cave, you see glittering formations ahead.",
        "The sacred grove beckons as you approach through the forest.",
        "You decide to stay and examine the area more carefully."  # No movement
    ]
    
    current_location = "village_outskirts"
    
    for i, ai_response in enumerate(test_ai_responses):
        print(f"Test {i+1}: {ai_response[:50]}...")
        
        debug_result = controller.location_debugger.debug_location_transition(
            ai_response, current_location, None, i+1
        )
        
        print(f"  Transition detected: {debug_result['transition_detected']}")
        if debug_result['transition_detected']:
            print(f"  New location: {debug_result['new_location']}")
            print(f"  Transition valid: {debug_result['transition_valid']}")
            if debug_result['fixes_applied']:
                print(f"  Fixes applied: {debug_result['fixes_applied']}")
        
        print()
    
    # Test connectivity map
    connectivity = controller.location_debugger.get_location_connectivity_map()
    print(f"Location connectivity map:")
    for location, data in connectivity['connections'].items():
        connected = ', '.join(data['connected_to'])
        print(f"  {location}: -> {connected}")
        if data['requires_dice']:
            print(f"    (Requires dice roll, difficulty: {data['difficulty']})")
    
    print("\\n" + "="*50 + "\\n")

def test_dynamic_options():
    """Test dynamic option generation"""
    print("=== TESTING DYNAMIC OPTIONS ===")
    
    controller = IntegratedStoryController()
    
    # Set up character with some skills
    controller.game_state_manager.character.update({
        'class': 'Cleric',
        'level': 2,
        'stats': {'strength': 12, 'dexterity': 14, 'intelligence': 16, 'charisma': 15},
        'skills': {'Combat': 2, 'Persuasion': 3, 'Investigation': 1}
    })
    
    # Test different situations
    test_situations = [
        "A group of hostile bandits blocks your path, demanding payment.",
        "You discover an ancient puzzle carved into the shrine wall.",
        "The villagers are arguing about what to do with the mysterious stranger.",
        "A magical barrier prevents you from entering the sacred grove."
    ]
    
    for i, situation in enumerate(test_situations):
        print(f"Situation {i+1}: {situation}")
        
        # Generate dynamic options
        options_text = controller.generate_dynamic_options(situation)
        print("Generated options:")
        print(options_text)
        print()
    
    print("\\n" + "="*50 + "\\n")

def test_integrated_turn_processing():
    """Test complete turn processing with all systems"""
    print("=== TESTING INTEGRATED TURN PROCESSING ===")
    
    controller = IntegratedStoryController()
    
    # Simulate a few turns
    test_turns = [
        {
            'player_action': "I decide to head toward Ashbrook village to seek help.",
            'ai_response': "You walk along the cobblestone path toward Ashbrook village. The autumn leaves crunch under your feet as you approach the village outskirts. Smoke rises from chimneys in the distance.",
            'dice_rolls': None
        },
        {
            'player_action': "I try to sneak through the forest to avoid the main path.",
            'ai_response': "You attempt to move stealthily through the Ember Woods, but the undergrowth is thick and the magical atmosphere makes navigation difficult.",
            'dice_rolls': [
                {
                    'roll_type': 'stealth_movement',
                    'stat_used': 'dexterity',
                    'skill_used': 'Stealth',
                    'base_roll': 15,
                    'modifiers': {'Dexterity': 2},
                    'target': 12,
                    'success': True
                }
            ]
        },
        {
            'player_action': "I examine the crystal formations in the cave.",
            'ai_response': "The crystals pulse with inner fire, and you sense they contain powerful magical energy. This could be the Fire Essence you need for the Sacred Flame!",
            'dice_rolls': None
        }
    ]
    
    for i, turn_data in enumerate(test_turns):
        print(f"\\n--- TURN {i+1} ---")
        print(f"Player Action: {turn_data['player_action']}")
        print(f"AI Response: {turn_data['ai_response'][:100]}...")
        
        # Process the turn
        turn_result = controller.process_turn(
            turn_data['player_action'],
            turn_data['ai_response'],
            turn_data['dice_rolls']
        )
        
        print(f"Turn processed: {turn_result['turn_processed']}")
        
        # Show location processing results
        location_data = turn_result['integration_data']['location_processing']
        if location_data['location_changed']:
            print(f"Location changed: {location_data['old_location']} -> {location_data['new_location']}")
        
        # Show story arc processing
        arc_data = turn_result['integration_data']['story_arc_processing']
        if arc_data['arc_progression']:
            print(f"Story arc progressed: {arc_data['progress_result']}")
        
        # Show current context
        print("\\nCurrent AI Context:")
        context = controller.generate_enhanced_context_for_ai()
        print(context[:300] + "..." if len(context) > 300 else context)
    
    print("\\n" + "="*50 + "\\n")

def test_integration_status():
    """Test integration status reporting"""
    print("=== TESTING INTEGRATION STATUS ===")
    
    controller = IntegratedStoryController()
    
    # Run a few operations to generate some state
    controller.process_turn(
        "I explore the area",
        "You discover interesting clues about the ancient magic",
        None
    )
    
    # Get status
    status = controller.get_integration_status()
    
    print("Integration Status:")
    print(f"  Active: {status['integration_active']}")
    print(f"  Debug Mode: {status['debug_mode']}")
    
    print("\\nSystems Status:")
    for system, data in status['systems_status'].items():
        print(f"  {system}:")
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"    {key}: {value}")
            else:
                print(f"    {key}: {value}")
    
    print("\\nCurrent State:")
    for key, value in status['current_state'].items():
        print(f"  {key}: {value}")
    
    print("\\n" + "="*50 + "\\n")

def main():
    """Run all tests"""
    print("INTEGRATED STORY SYSTEMS TEST")
    print("="*50)
    
    try:
        test_story_arc_integration()
        test_location_debugging()
        test_dynamic_options()
        test_integrated_turn_processing()
        test_integration_status()
        
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        print(f"ERROR during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()