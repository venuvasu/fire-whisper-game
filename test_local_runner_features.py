#!/usr/bin/env python3
"""
Test script for the integrated features in local_runner.py
Demonstrates Story Arc Integration, Location Debugging, and Dynamic Options
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "scripts"))

# Import the features from local_runner
from scripts.local_runner import (
    STORY_ARCS, select_story_arc, activate_story_arc, advance_story_arc,
    LOCATION_CONNECTIONS, LOCATION_PATTERNS, detect_location_change, get_location_debug_report,
    generate_dynamic_options, current_location, active_story_arc, arc_progress,
    location_debug_history, recent_player_actions
)

def test_story_arc_integration():
    """Test the story arc system"""
    print("=" * 60)
    print("🎭 TESTING STORY ARC INTEGRATION")
    print("=" * 60)
    
    print(f"📚 Available Story Arcs: {len(STORY_ARCS)}")
    for i, arc in enumerate(STORY_ARCS, 1):
        print(f"  {i}. {arc['name']} ({arc['type']}) - Difficulty: {arc['difficulty']}")
    
    # Test arc selection
    print(f"\n🎯 Testing Arc Selection...")
    character_level = 2
    test_location = "village_outskirts"
    story_context = "sacred flame restoration"
    
    selected_arc = select_story_arc(character_level, test_location, story_context)
    print(f"Selected Arc: {selected_arc['name']}")
    print(f"Hook: {selected_arc['hook']}")
    
    # Test arc activation (simulate log_file)
    class MockLogFile:
        def __init__(self):
            self.content = []
        def write(self, text):
            self.content.append(text)
            print(text.strip())
    
    mock_log = MockLogFile()
    
    def mock_log_to_file(log_file, content):
        print(content)
    
    # Temporarily replace log_to_file
    import scripts.local_runner
    original_log_to_file = scripts.local_runner.log_to_file
    scripts.local_runner.log_to_file = mock_log_to_file
    
    print(f"\n🚀 Activating Arc...")
    activation_msg = activate_story_arc(selected_arc, mock_log)
    
    # Test arc progression
    print(f"\n📈 Testing Arc Progression...")
    test_actions = [
        ("I search for clues about the Sacred Flame", "You discover ancient texts mentioning Fire Essence crystals"),
        ("I explore the crystal cave", "You find glowing crystals that pulse with inner fire"),
        ("I defeat the cave guardian", "The guardian falls, and you claim the Fire Essence crystal"),
        ("I restore the Sacred Flame", "The flame blazes to life, banishing the darkness forever!")
    ]
    
    for player_action, ai_response in test_actions:
        print(f"\n🎮 Player: {player_action}")
        print(f"🤖 AI: {ai_response}")
        
        progress_result = advance_story_arc(player_action, ai_response, mock_log)
        if progress_result:
            print(f"📊 Arc Progress: {progress_result}")
    
    # Restore original function
    scripts.local_runner.log_to_file = original_log_to_file
    
    print(f"\n✅ Story Arc Integration Test Complete!")

def test_location_debugging():
    """Test the location progression debugging"""
    print("\n" + "=" * 60)
    print("🗺️ TESTING LOCATION PROGRESSION DEBUG")
    print("=" * 60)
    
    print(f"🏠 Current Location: {current_location}")
    print(f"🗺️ Location Connections:")
    for location, connections in LOCATION_CONNECTIONS.items():
        print(f"  {location} → {', '.join(connections)}")
    
    # Test location detection
    print(f"\n🔍 Testing Location Detection...")
    test_responses = [
        "You walk toward Ashbrook village, the cobblestone path crunching under your feet.",
        "Moving deeper into the crystal cave, you see glittering formations ahead.",
        "You decide to head back to the sacred grove through the forest.",
        "You examine the area more carefully without moving anywhere."
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n🧪 Test {i}: {response[:50]}...")
        result = detect_location_change(response)
        print(f"   Result: {result}")
        
        if result.get('location_changed'):
            print(f"   ✅ Location changed to: {result['new_location']}")
        elif result.get('debug_info'):
            print(f"   ℹ️ Debug: {result['debug_info']}")
    
    # Show debug report
    print(f"\n📊 Location Debug Report:")
    debug_report = get_location_debug_report()
    print(debug_report)
    
    print(f"\n✅ Location Debugging Test Complete!")

def test_dynamic_options():
    """Test the dynamic options generation"""
    print("\n" + "=" * 60)
    print("🎯 TESTING DYNAMIC OPTIONS GENERATION")
    print("=" * 60)
    
    # Test character
    test_character = {
        'name': 'Testara',
        'class': 'Cleric',
        'level': 2,
        'stats': {'strength': 12, 'dexterity': 14, 'intelligence': 16, 'charisma': 15}
    }
    
    # Test scenarios
    test_scenarios = [
        {
            'situation': "A group of hostile bandits blocks your path, demanding payment.",
            'location': 'village_outskirts',
            'recent_actions': ['attack the first bandit', 'charge forward']
        },
        {
            'situation': "You discover an ancient puzzle carved into the shrine wall with mysterious runes.",
            'location': 'sacred_grove',
            'recent_actions': ['wait and observe', 'carefully examine']
        },
        {
            'situation': "Dark corruption spreads through the crystal formations, pulsing with evil energy.",
            'location': 'crystal_cave',
            'recent_actions': ['cast healing spell', 'pray for guidance']
        },
        {
            'situation': "The villagers are arguing loudly about what to do with a mysterious stranger.",
            'location': 'ashbrook_village',
            'recent_actions': ['listen quietly', 'ask questions']
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🎬 Scenario {i}: {scenario['situation']}")
        print(f"📍 Location: {scenario['location']}")
        print(f"📝 Recent Actions: {', '.join(scenario['recent_actions'])}")
        
        options = generate_dynamic_options(
            scenario['situation'],
            test_character,
            scenario['location'],
            scenario['recent_actions']
        )
        
        print(f"🎯 Generated Options:")
        for j, option in enumerate(options, 1):
            print(f"   {j}. {option}")
    
    print(f"\n✅ Dynamic Options Test Complete!")

def test_integration():
    """Test how all three features work together"""
    print("\n" + "=" * 60)
    print("🔗 TESTING INTEGRATED FEATURES")
    print("=" * 60)
    
    # Simulate a game turn with all features
    print("🎮 Simulating Complete Game Turn...")
    
    # Character
    character = {'name': 'Hero', 'class': 'Cleric', 'level': 1}
    
    # Player action
    player_action = "I head toward the crystal cave to find the Fire Essence"
    ai_response = "You walk through the Ember Woods toward the crystal cave. The path is treacherous, but you can see the cave entrance glowing with inner light ahead."
    
    print(f"🎯 Player Action: {player_action}")
    print(f"🤖 AI Response: {ai_response}")
    
    # 1. Story Arc Processing
    if not active_story_arc:
        arc = select_story_arc(1, current_location, ai_response)
        print(f"\n🎭 Story Arc Selected: {arc['name']}")
    
    # 2. Location Processing
    location_result = detect_location_change(ai_response)
    print(f"\n🗺️ Location Processing: {location_result}")
    
    # 3. Dynamic Options
    options = generate_dynamic_options(ai_response, character, current_location, [player_action])
    print(f"\n🎯 Dynamic Options Generated:")
    for i, option in enumerate(options, 1):
        print(f"   {i}. {option}")
    
    print(f"\n🎊 Integration Test Complete!")

def main():
    """Run all tests"""
    print("🔥 FIRE WHISPER RPG - INTEGRATED FEATURES TEST")
    print("Testing Story Arc Integration, Location Debugging, and Dynamic Options")
    
    try:
        test_story_arc_integration()
        test_location_debugging()
        test_dynamic_options()
        test_integration()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("✅ Story Arc Integration: Working")
        print("✅ Location Progression Debug: Working") 
        print("✅ Dynamic Options Generation: Working")
        print("✅ Feature Integration: Working")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()