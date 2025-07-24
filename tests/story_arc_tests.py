#!/usr/bin/env python3
"""
Story Arc Tests - Tests for the expanded story arc system
Tests the loading, selection, and progression of story arcs
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.local_runner import load_story_arcs, select_story_arc, activate_story_arc, advance_story_arc

class MockLogFile:
    """Mock log file for testing"""
    def __init__(self):
        self.logs = []
    
    def write(self, content):
        self.logs.append(content)
    
    def read(self):
        return "\n".join(self.logs)

def test_story_arc_loading():
    """Test that story arcs are loaded correctly"""
    arcs = load_story_arcs()
    
    # Check that we have arcs
    assert len(arcs) > 0, "No story arcs were loaded"
    
    # Check that we have the original arcs
    original_arc_names = [
        "The Crimson Prophecy",
        "The Last Dragon's Quest",
        "The Memory Thief"
    ]
    
    # Check that we have the new arcs
    new_arc_names = [
        "The Whispering Shadows",
        "Blood Moon Rising",
        "The Ember's Heart",
        "The Fate Weaver's Thread"
    ]
    
    # Check that at least some of the original arcs are present
    original_arcs_found = [name for name in original_arc_names if any(arc['name'] == name for arc in arcs)]
    assert len(original_arcs_found) > 0, f"None of the expected original arcs were found: {original_arc_names}"
    
    # Check that at least some of the new arcs are present
    new_arcs_found = [name for name in new_arc_names if any(arc['name'] == name for arc in arcs)]
    assert len(new_arcs_found) > 0, f"None of the expected new arcs were found: {new_arc_names}"
    
    print(f"✅ Successfully loaded {len(arcs)} story arcs")
    print(f"   Original arcs found: {original_arcs_found}")
    print(f"   New arcs found: {new_arcs_found}")
    
    # Check that new arcs have the additional properties
    new_arc = next((arc for arc in arcs if arc['name'] in new_arc_names), None)
    if new_arc:
        assert 'difficulty' in new_arc, f"New arc {new_arc['name']} missing 'difficulty' property"
        assert 'turns' in new_arc, f"New arc {new_arc['name']} missing 'turns' property"
        assert 'location_start' in new_arc, f"New arc {new_arc['name']} missing 'location_start' property"
        assert 'character_level' in new_arc, f"New arc {new_arc['name']} missing 'character_level' property"
        
        print(f"✅ New arc {new_arc['name']} has all required properties")
        print(f"   Difficulty: {new_arc['difficulty']}")
        print(f"   Turns: {new_arc['turns']}")
        print(f"   Location Start: {new_arc['location_start']}")
        print(f"   Character Level: {new_arc['character_level']}")

def test_story_arc_selection():
    """Test that story arcs are selected correctly based on context"""
    arcs = load_story_arcs()
    
    # Test location-based selection
    crystal_cave_arc = select_story_arc(3, 'crystal_cave', 'exploring the cave')
    assert crystal_cave_arc is not None, "Failed to select an arc for crystal_cave"
    print(f"✅ Selected arc for crystal_cave: {crystal_cave_arc['name']}")
    
    # Test context-based selection
    shadow_arc = select_story_arc(3, 'village_tavern', 'mysterious shadows whisper secrets')
    assert shadow_arc is not None, "Failed to select an arc for shadow context"
    print(f"✅ Selected arc for shadow context: {shadow_arc['name']}")
    
    # Test character level-based selection
    high_level_arc = select_story_arc(5, 'sacred_grove', 'powerful magic')
    assert high_level_arc is not None, "Failed to select an arc for high level character"
    assert high_level_arc['difficulty'] <= 6, f"Selected arc difficulty {high_level_arc['difficulty']} too high for level 5"
    print(f"✅ Selected arc for level 5 character: {high_level_arc['name']} (Difficulty: {high_level_arc['difficulty']})")
    
    # Test low level character
    low_level_arc = select_story_arc(1, 'village_outskirts', 'beginning adventure')
    assert low_level_arc is not None, "Failed to select an arc for low level character"
    assert low_level_arc['difficulty'] <= 2, f"Selected arc difficulty {low_level_arc['difficulty']} too high for level 1"
    print(f"✅ Selected arc for level 1 character: {low_level_arc['name']} (Difficulty: {low_level_arc['difficulty']})")

def test_story_arc_activation_and_progression():
    """Test that story arcs can be activated and progressed"""
    arcs = load_story_arcs()
    mock_log = MockLogFile()
    
    # Select a test arc
    test_arc = next((arc for arc in arcs if arc['name'] == "The Ember's Heart"), arcs[0])
    
    # Activate the arc
    activation_msg = activate_story_arc(test_arc, mock_log)
    assert "STORY ARC ACTIVATED" in activation_msg, "Arc activation message not generated"
    assert test_arc['name'] in activation_msg, "Arc name not in activation message"
    print(f"✅ Successfully activated arc: {test_arc['name']}")
    
    # Test progression
    progress_result = advance_story_arc("I search for clues to restore the flame", 
                                       "You discover ancient runes that might help restore the eternal flame", 
                                       mock_log)
    assert progress_result is not None, "Arc progression failed"
    print(f"✅ Successfully progressed arc: {test_arc['name']}")
    
    # Test multiple progressions to reach climax
    for i in range(test_arc['turns'] - 3):  # -3 because we already did one progression and need to leave room for climax
        advance_story_arc(f"I continue the quest step {i}", 
                         f"You make progress in your quest to restore the flame", 
                         mock_log)
    
    # This should trigger the climax phase
    climax_result = advance_story_arc("I prepare for the final ritual", 
                                     "You gather the necessary components for the ritual to restore the flame", 
                                     mock_log)
    assert climax_result is not None, "Failed to reach climax phase"
    
    # Check if we're in climax phase or if we've already completed (depends on the turns count)
    is_climax_or_complete = (
        climax_result.get('phase') == 'climax' or 
        'Climax' in str(climax_result.get('message', '')) or
        climax_result.get('completed') == True
    )
    assert is_climax_or_complete, f"Expected climax phase or completion but got {climax_result}"
    
    if climax_result.get('completed'):
        print(f"✅ Arc completed directly: {test_arc['name']}")
        completion_result = climax_result
    else:
        print(f"✅ Successfully reached climax phase of arc: {test_arc['name']}")
        
        # Final progression should complete the arc
        completion_result = advance_story_arc("I perform the ritual and make the sacrifice", 
                                            "You successfully rekindle the eternal flame at the heart of Ember Woods", 
                                            mock_log)
    assert completion_result is not None, "Failed to complete arc"
    assert completion_result.get('completed') is True, "Arc not marked as completed"
    print(f"✅ Successfully completed arc: {test_arc['name']}")

def run_all_tests():
    """Run all story arc tests"""
    print("\n🧪 RUNNING STORY ARC TESTS\n" + "=" * 50)
    
    print("\n📚 Testing Story Arc Loading...")
    test_story_arc_loading()
    
    print("\n🎯 Testing Story Arc Selection...")
    test_story_arc_selection()
    
    print("\n🎭 Testing Story Arc Activation and Progression...")
    test_story_arc_activation_and_progression()
    
    print("\n✅ ALL STORY ARC TESTS PASSED")

if __name__ == "__main__":
    run_all_tests()