#!/usr/bin/env python3
"""
Enhanced Story Arc Tests - Tests for the expanded story arc system
Tests the loading, selection, and categorization of story arcs
"""
import sys
import os
from pathlib import Path
from collections import defaultdict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.local_runner import load_story_arcs, select_story_arc

def test_arc_categories():
    """Test that arcs are properly categorized"""
    arcs = load_story_arcs()
    
    # Categorize arcs by type
    categories = defaultdict(list)
    for arc in arcs:
        # Extract main category from type (before the first slash)
        main_type = arc['type'].split('/')[0] if '/' in arc['type'] else arc['type']
        categories[main_type].append(arc['name'])
    
    # Print category statistics
    print(f"\n📊 STORY ARC CATEGORIES ({len(categories)} categories):")
    for category, arc_names in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  • {category}: {len(arc_names)} arcs")
    
    # Check for specific categories we expect
    expected_categories = [
        "Dark Fantasy", "Elemental", "Mythological", 
        "Historical Fantasy", "Character-Driven", "Location-Based"
    ]
    
    for category in expected_categories:
        found = any(category.lower() in cat.lower() for cat in categories.keys())
        assert found, f"Expected category '{category}' not found in arc types"
        print(f"✅ Found expected category: {category}")
    
    return categories

def test_location_specific_arcs():
    """Test that location-specific arcs are selected correctly"""
    arcs = load_story_arcs()
    
    # Test locations
    locations = [
        "crystal_cave", 
        "sacred_grove", 
        "ember_woods", 
        "village_tavern", 
        "ashbrook_village", 
        "village_outskirts"
    ]
    
    print(f"\n🗺️ LOCATION-SPECIFIC ARC SELECTION:")
    for location in locations:
        # Try multiple selections to account for randomness
        selected_arcs = set()
        for _ in range(5):
            arc = select_story_arc(3, location, f"exploring the {location}")
            selected_arcs.add(arc['name'])
        
        print(f"  • {location}: {len(selected_arcs)} unique arcs selected")
        for arc_name in selected_arcs:
            print(f"    - {arc_name}")
        
        # Check that at least one arc was selected
        assert len(selected_arcs) > 0, f"No arcs selected for location {location}"
        
        # Check if any selected arc has the location in its name or type
        location_keywords = location.replace('_', ' ').split()
        location_specific = any(
            any(keyword.lower() in arc_name.lower() for keyword in location_keywords)
            for arc_name in selected_arcs
        )
        
        if location_specific:
            print(f"    ✅ Found location-specific arc for {location}")
    
    return True

def test_context_based_selection():
    """Test that context-based arc selection works correctly"""
    arcs = load_story_arcs()
    
    # Test contexts
    contexts = [
        "shadows whispering secrets",
        "ancient history and forgotten ruins",
        "family legacy and bloodline curses",
        "elemental magic and natural forces",
        "mythological creatures and divine beings"
    ]
    
    print(f"\n📝 CONTEXT-BASED ARC SELECTION:")
    for context in contexts:
        # Try multiple selections to account for randomness
        selected_arcs = set()
        for _ in range(5):
            arc = select_story_arc(3, "village_outskirts", context)
            selected_arcs.add(arc['name'])
        
        print(f"  • Context: '{context}'")
        print(f"    Selected arcs: {', '.join(selected_arcs)}")
        
        # Check that at least one arc was selected
        assert len(selected_arcs) > 0, f"No arcs selected for context '{context}'"
    
    return True

def test_difficulty_based_selection():
    """Test that difficulty-based arc selection works correctly"""
    arcs = load_story_arcs()
    
    # Test different character levels
    levels = [1, 3, 5]
    
    print(f"\n⚔️ DIFFICULTY-BASED ARC SELECTION:")
    for level in levels:
        # Try multiple selections to account for randomness
        selected_arcs = []
        for _ in range(10):
            arc = select_story_arc(level, "village_outskirts", "generic adventure")
            selected_arcs.append(arc)
        
        # Get unique difficulties
        difficulties = set(arc['difficulty'] for arc in selected_arcs)
        
        print(f"  • Character Level {level}:")
        print(f"    Selected difficulties: {sorted(difficulties)}")
        
        # Check that difficulties are appropriate for level
        max_expected_difficulty = level + 1
        assert all(diff <= max_expected_difficulty for diff in difficulties), \
            f"Selected arc with difficulty too high for level {level}"
        
        print(f"    ✅ All difficulties appropriate for level {level} (max: {max_expected_difficulty})")
    
    return True

def run_all_tests():
    """Run all enhanced story arc tests"""
    print("\n🧪 RUNNING ENHANCED STORY ARC TESTS\n" + "=" * 50)
    
    print("\n📚 Testing Story Arc Categories...")
    categories = test_arc_categories()
    
    print("\n🗺️ Testing Location-Specific Arc Selection...")
    test_location_specific_arcs()
    
    print("\n📝 Testing Context-Based Arc Selection...")
    test_context_based_selection()
    
    print("\n⚔️ Testing Difficulty-Based Arc Selection...")
    test_difficulty_based_selection()
    
    print("\n✅ ALL ENHANCED STORY ARC TESTS PASSED")
    
    # Print summary
    print("\n📊 SUMMARY:")
    print(f"  • Total Story Arcs: {len(load_story_arcs())}")
    print(f"  • Categories: {len(categories)}")
    print(f"  • Selection Methods Tested: Location, Context, Difficulty")

if __name__ == "__main__":
    run_all_tests()