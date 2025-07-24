#!/usr/bin/env python3
"""
Direct High-Level Arc Test - Tests direct selection of high-level arcs
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from scripts.local_runner import load_story_arcs, select_story_arc

def test_direct_high_level_selection():
    """Test direct selection of high-level arcs"""
    arcs = load_story_arcs()
    
    # Find high-level arcs
    high_level_arcs = [arc for arc in arcs if 'High-Level' in arc.get('type', '')]
    
    if not high_level_arcs:
        print("❌ No high-level arcs found!")
        return False
    
    print(f"\n🏆 HIGH-LEVEL ARCS ({len(high_level_arcs)} arcs):")
    for arc in high_level_arcs:
        print(f"  • {arc['name']} - Type: {arc['type']}, Level: {arc.get('character_level')}, Difficulty: {arc['difficulty']}")
    
    # Try direct selection with explicit context keywords
    print("\n🧪 Testing direct high-level arc selection:")
    
    # Try with different context keywords
    contexts = [
        "cosmic horror void breach",
        "dragon council politics",
        "divine conflict godslayer",
        "high-level challenge"
    ]
    
    for context in contexts:
        print(f"\n  Testing context: '{context}'")
        
        # Try with high-level character
        arc = select_story_arc(6, "sacred_grove", context)
        
        print(f"  • Selected: {arc['name']} - Type: {arc['type']}")
        
        # Check if this is a high-level arc
        is_high_level = 'High-Level' in arc['type']
        print(f"  • Is high-level arc: {is_high_level}")
        
        if is_high_level:
            print("  ✅ Successfully selected high-level arc!")
            return True
    
    print("❌ Failed to select any high-level arcs!")
    return False

if __name__ == "__main__":
    test_direct_high_level_selection()