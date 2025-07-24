#!/usr/bin/env python3
"""
Gameplay Improvement Tests - Tests for the new gameplay improvement systems

This script tests the integration of:
1. Action-Outcome Framework
2. Narrative Coherence System
3. Story Progression Accelerator
4. Enhanced Location System
"""
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.core.action_outcome_framework import ActionOutcomeFramework
from src.core.narrative_coherence_system import NarrativeCoherenceSystem
from src.core.story_progression_accelerator import StoryProgressionAccelerator
from src.core.enhanced_location_system import EnhancedLocationSystem

def test_action_outcome_framework():
    """Test the Action-Outcome Framework"""
    print("\n🎯 TESTING ACTION-OUTCOME FRAMEWORK")
    print("=" * 50)
    
    # Create framework
    action_framework = ActionOutcomeFramework()
    
    # Test scenarios
    scenarios = [
        {"action_type": "attack", "risk_level": "high", "roll": 18, "dc": 15},
        {"action_type": "attack", "risk_level": "high", "roll": 5, "dc": 15},
        {"action_type": "investigate", "risk_level": "moderate", "roll": 15, "dc": 15},
        {"action_type": "persuade", "risk_level": "low", "roll": 10, "dc": 15},
        {"action_type": "cast spell", "risk_level": "high", "roll": 3, "dc": 15}
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        outcome = action_framework.resolve_action(
            scenario["action_type"], 
            scenario["risk_level"], 
            scenario["roll"], 
            scenario["dc"]
        )
        
        print(f"\nScenario {i}:")
        print(f"Action: {scenario['action_type']} (Risk: {scenario['risk_level']})")
        print(f"Roll: {scenario['roll']} vs DC: {scenario['dc']} (Adjusted: {outcome['difficulty_class']})")
        print(f"Outcome: {outcome['outcome_type']}")
        print(f"Narrative Template: {outcome['narrative_template']}")
        print(f"State Changes: {outcome['state_changes']}")
    
    # Print statistics
    print("\nOutcome Statistics:")
    stats = action_framework.get_outcome_statistics()
    for outcome_type, percentage in stats.items():
        print(f"{outcome_type}: {percentage:.1f}%")
    
    # Test AI prompt generation
    character = {
        "name": "Bob",
        "race": "Human",
        "class": "Warrior"
    }
    
    location = {
        "name": "Village Outskirts",
        "brief_description": "A peaceful path leading to Ashbrook village"
    }
    
    story_state = {
        "current_phase": "introduction"
    }
    
    # Generate prompt for spectacular success
    spectacular_success = action_framework.resolve_action("attack", "high", 20, 15)
    prompt = action_framework.generate_ai_prompt(spectacular_success, character, location, story_state)
    
    print("\nAI Prompt for Spectacular Success:")
    print(prompt[:300] + "...\n")
    
    return True

def test_narrative_coherence_system():
    """Test the Narrative Coherence System"""
    print("\n📖 TESTING NARRATIVE COHERENCE SYSTEM")
    print("=" * 50)
    
    # Create system
    coherence_system = NarrativeCoherenceSystem()
    
    # Register some elements
    coherence_system.register_element(
        "emberlyn", "character",
        {"name": "Emberlyn", "description": "A fairy companion with flame-colored wings"},
        importance=5,
        keywords=["fairy", "companion", "wings", "flame-colored"]
    )
    
    coherence_system.register_element(
        "shadow_blight", "threat",
        {"name": "Shadow Blight", "description": "A corruption spreading through the shadows"},
        importance=4,
        keywords=["shadow", "corruption", "darkness", "blight"]
    )
    
    coherence_system.set_current_location(
        "village_outskirts",
        {"name": "Village Outskirts", "description": "The path leading to Ashbrook village"}
    )
    
    # Test continuity checking
    print("Testing continuity checking:")
    
    # Good response that maintains continuity
    good_response = """
    *Emberlyn flutters nervously as she points toward the writhing shadows*
    
    "The Shadow Blight is spreading faster than I feared. We need to warn the villagers 
    before it reaches Ashbrook," she whispers urgently.
    
    *The path ahead winds through the Village Outskirts, where fallen autumn leaves 
    crunch beneath your feet*
    """
    
    # Bad response that drops important elements
    bad_response = """
    *A gentle breeze rustles through the trees*
    
    "We should continue on our journey," she suggests. "The village isn't far now."
    
    *The afternoon sun casts long shadows across the path ahead*
    """
    
    # Check good response
    coherence_system.advance_turn()
    coherence_system.update_mentions(good_response)
    violations_good = coherence_system.check_continuity_violations(good_response)
    print("\nGood Response Violations:", violations_good)
    
    # Check bad response
    coherence_system.advance_turn()
    violations_bad = coherence_system.check_continuity_violations(bad_response)
    print("\nBad Response Violations:", violations_bad)
    
    # Generate enforcement prompt
    if violations_bad:
        enforcement_prompt, _ = coherence_system.enforce_continuity(bad_response)
        print("\nEnforcement Prompt:")
        print(enforcement_prompt[:300] + "...\n")
    
    # Extract narrative elements
    new_text = """
    Elder Marcus from Ashbrook village warned about the Crimson Cult that has been 
    performing rituals in the Dark Hollow. They've been using the Ancient Amulet 
    to channel dark energies.
    """
    
    suggestions = coherence_system.suggest_new_elements(new_text)
    print("\nSuggested New Elements:")
    for suggestion in suggestions:
        print(f"- {suggestion['element_type']}: {suggestion['element_id']} ({suggestion['data']['name']})")
    
    return True

def test_story_progression_accelerator():
    """Test the Story Progression Accelerator"""
    print("\n📚 TESTING STORY PROGRESSION ACCELERATOR")
    print("=" * 50)
    
    # Create a sample story arc
    story_arc = {
        "name": "The Crimson Prophecy",
        "type": "Epic Fantasy",
        "hook": "An ancient prophecy speaks of a crimson blade that will either save or doom the realm.",
        "elements": ["Rival seekers", "moral choices about power", "ancient weapon", "prophecy interpretation"],
        "climax": "Confrontation at the Sundering Peaks where the blade's true nature is revealed"
    }
    
    # Create accelerator with target climax at turn 20
    accelerator = StoryProgressionAccelerator(story_arc, target_climax_turn=20)
    
    # Simulate a story with varied progression
    print("Simulating story progression:")
    print(f"Target climax turn: {accelerator.target_climax_turn}")
    print(f"Starting phase: {accelerator.current_phase.name}")
    
    # Progress through turns with different amounts of progress
    progress_amounts = [
        0.05, 0.03, 0.02, 0.04, 0.03,  # Turns 1-5
        0.05, 0.07, 0.06, 0.04, 0.05,  # Turns 6-10
        0.03, 0.02, 0.04, 0.06, 0.08,  # Turns 11-15
        0.10, 0.12, 0.15, 0.20, 0.10   # Turns 16-20
    ]
    
    for i, amount in enumerate(progress_amounts, 1):
        # Advance turn
        turn_result = accelerator.advance_turn()
        
        # Add some progress (simulating player actions)
        progress_result = accelerator.add_progress(amount, "player_action")
        
        # Print status
        print(f"\nTurn {i}:")
        print(f"  Phase: {accelerator.current_phase.name}")
        print(f"  Progress: {accelerator.get_progress_percentage():.1f}%")
        print(f"  Expected: {turn_result['expected_progress'] * 100:.1f}%")
        
        if turn_result.get("force_progression"):
            print(f"  FORCED PROGRESSION: +{turn_result['forced_progression']['amount'] * 100:.1f}%")
        
        if progress_result["phase_changed"]:
            print(f"  PHASE CHANGE: {progress_result['old_phase']} → {progress_result['new_phase']}")
    
    # Print final phase summary
    print("\nFinal Phase Summary:")
    phase_summary = accelerator.get_phase_summary()
    
    for phase_name, data in phase_summary.items():
        status = "ACTIVE" if data["is_active"] else "COMPLETED" if data["exited_turn"] is not None else "UPCOMING"
        turn_info = f"Turns {data['entered_turn']}-{data['exited_turn']}" if data["entered_turn"] is not None else f"Est. Turn {data['estimated_turn']}"
        
        print(f"  {phase_name.upper()} ({status}): {turn_info}")
    
    # Test progress prompt
    prompt = accelerator.generate_progress_prompt()
    print("\nProgress Prompt:")
    print(prompt[:300] + "...\n")
    
    return True

def test_enhanced_location_system():
    """Test the Enhanced Location System"""
    print("\n🗺️ TESTING ENHANCED LOCATION SYSTEM")
    print("=" * 50)
    
    # Create location system
    location_system = EnhancedLocationSystem()
    
    # Add locations
    location_system.add_location(
        "village_outskirts",
        "Village Outskirts",
        "A peaceful path leading to Ashbrook village, surrounded by autumn trees",
        ["outskirts", "path", "road", "outside village"],
        ["Tall oak trees line the path", "A small stream crosses under a wooden bridge", "Wild flowers grow along the edges"]
    )
    
    location_system.add_location(
        "ashbrook_village",
        "Ashbrook Village",
        "A quaint village with thatched-roof cottages and friendly inhabitants",
        ["ashbrook", "village", "town", "settlement"],
        ["The village square has a central well", "Smoke rises from cottage chimneys", "Children play near the community hall"]
    )
    
    location_system.add_location(
        "village_tavern",
        "The Rusty Sword Tavern",
        "A warm, inviting tavern filled with the scent of ale and hearty stew",
        ["tavern", "inn", "rusty sword", "pub"],
        ["A large fireplace crackles at one end", "The bartender polishes mugs behind the counter", "Patrons share stories at wooden tables"]
    )
    
    # Add connections
    location_system.add_connection("village_outskirts", "ashbrook_village", 0)
    location_system.add_connection("ashbrook_village", "village_tavern", 0)
    
    # Set current location
    location_system.set_current_location("village_outskirts")
    
    # Test location detection
    print("Testing location detection:")
    
    # Good response that indicates movement
    good_response = """
    You walk along the path, following Emberlyn's guidance. After a short journey, 
    you arrive at Ashbrook Village. The quaint cottages with their thatched roofs 
    come into view, and you can see villagers going about their daily business in 
    the village square.
    """
    
    # Bad response that doesn't clearly indicate location
    bad_response = """
    You continue on your journey. The path winds through some trees, and you can 
    see buildings in the distance. Emberlyn flutters ahead, eager to reach the 
    destination.
    """
    
    # Test good response
    location_system.advance_turn()
    good_result = location_system.detect_location_change(good_response, "I walk to the village")
    print("\nGood Response Result:")
    for key, value in good_result.items():
        print(f"  {key}: {value}")
    
    # Test bad response
    location_system.advance_turn()
    bad_result = location_system.detect_location_change(bad_response, "I continue walking")
    print("\nBad Response Result:")
    for key, value in bad_result.items():
        print(f"  {key}: {value}")
    
    # Test location consistency
    consistent = location_system.check_location_consistency(good_response)
    print(f"\nLocation Consistency (Good): {consistent}")
    
    inconsistent = location_system.check_location_consistency(bad_response)
    print(f"Location Consistency (Bad): {inconsistent}")
    
    # Test enforcement
    if not inconsistent:
        enforcement_prompt, needs_enforcement = location_system.enforce_location_consistency(bad_response)
        if needs_enforcement:
            print("\nEnforcement Prompt:")
            print(enforcement_prompt[:300] + "...\n")
    
    # Test debug report
    debug_report = location_system.get_location_debug_report()
    print(debug_report)
    
    # Test force location change
    force_result = location_system.should_force_location_change()
    print("\nShould Force Location Change:")
    for key, value in force_result.items():
        print(f"  {key}: {value}")
    
    # Test location context
    context = location_system.generate_location_context("afternoon", "clear")
    print("\nLocation Context:")
    print(context)
    
    return True

def test_integrated_systems():
    """Test all systems working together"""
    print("\n🔄 TESTING INTEGRATED SYSTEMS")
    print("=" * 50)
    
    # Create all systems
    action_framework = ActionOutcomeFramework()
    coherence_system = NarrativeCoherenceSystem()
    
    story_arc = {
        "name": "The Crimson Prophecy",
        "type": "Epic Fantasy",
        "hook": "An ancient prophecy speaks of a crimson blade that will either save or doom the realm.",
        "elements": ["Rival seekers", "moral choices about power", "ancient weapon", "prophecy interpretation"],
        "climax": "Confrontation at the Sundering Peaks where the blade's true nature is revealed"
    }
    
    story_accelerator = StoryProgressionAccelerator(story_arc, target_climax_turn=20)
    location_system = EnhancedLocationSystem()
    
    # Set up locations
    location_system.add_location(
        "village_outskirts",
        "Village Outskirts",
        "A peaceful path leading to Ashbrook village, surrounded by autumn trees",
        ["outskirts", "path", "road", "outside village"]
    )
    
    location_system.add_location(
        "ashbrook_village",
        "Ashbrook Village",
        "A quaint village with thatched-roof cottages and friendly inhabitants",
        ["ashbrook", "village", "town", "settlement"]
    )
    
    location_system.add_connection("village_outskirts", "ashbrook_village", 10)  # DC 10
    
    # Set current location
    location_system.set_current_location("village_outskirts")
    coherence_system.set_current_location(
        "village_outskirts",
        {"name": "Village Outskirts", "description": "The path leading to Ashbrook village"}
    )
    
    # Register narrative elements
    coherence_system.register_element(
        "emberlyn", "character",
        {"name": "Emberlyn", "description": "A fairy companion with flame-colored wings"},
        importance=5
    )
    
    coherence_system.register_element(
        "shadow_blight", "threat",
        {"name": "Shadow Blight", "description": "A corruption spreading through the shadows"},
        importance=4
    )
    
    # Simulate a turn
    print("Simulating a game turn:")
    
    # 1. Advance turn in all systems
    coherence_system.advance_turn()
    story_accelerator.advance_turn()
    location_system.advance_turn()
    
    # 2. Process player action
    player_action = "I carefully investigate the shadows for signs of the corruption"
    action_type = "investigate"
    risk_level = "moderate"
    roll_result = 15
    difficulty_class = 12
    
    # 3. Resolve action outcome
    outcome = action_framework.resolve_action(action_type, risk_level, roll_result, difficulty_class)
    
    print("\nAction Outcome:")
    print(f"Action: {action_type} ({risk_level} risk)")
    print(f"Roll: {roll_result} vs DC: {difficulty_class}")
    print(f"Outcome: {outcome['outcome_type']}")
    
    # 4. Add story progress based on outcome
    progress_amount = outcome['state_changes'].get('progress_bonus', 0.0)
    progress_result = story_accelerator.add_progress(progress_amount, "player_action")
    
    print("\nStory Progress:")
    print(f"Added: {progress_amount * 100:.1f}%")
    print(f"Total: {story_accelerator.get_progress_percentage():.1f}%")
    print(f"Phase: {story_accelerator.current_phase.name}")
    
    # 5. Generate AI response (simulated)
    ai_response = """
    *Emberlyn hovers anxiously nearby as you carefully examine the writhing shadows*
    
    "You've found something important!" she exclaims. "See how the Shadow Blight 
    recoils from your touch? It's not fully manifested here yet, which means we 
    still have time to stop it."
    
    *The path through the Village Outskirts seems darker than before, with shadows 
    pooling unnaturally beneath the autumn trees. In the distance, you can see 
    the first buildings of Ashbrook Village.*
    """
    
    # 6. Check for location change
    location_result = location_system.detect_location_change(ai_response, player_action)
    
    print("\nLocation Check:")
    print(f"Location Changed: {location_result['location_changed']}")
    print(f"Current Location: {location_system.current_location_id}")
    
    # 7. Check narrative coherence
    coherence_system.update_mentions(ai_response)
    violations = coherence_system.check_continuity_violations(ai_response)
    
    print("\nNarrative Coherence:")
    print(f"Violations: {violations}")
    
    # 8. Generate next turn prompt
    character = {
        "name": "Bob",
        "race": "Human",
        "class": "Warrior"
    }
    
    location = {
        "name": location_system.get_current_location().name,
        "brief_description": location_system.get_current_location().description
    }
    
    story_state = {
        "current_phase": story_accelerator.current_phase.name
    }
    
    # Generate AI prompt for next turn
    ai_prompt = action_framework.generate_ai_prompt(outcome, character, location, story_state)
    
    print("\nNext Turn AI Prompt:")
    print(ai_prompt[:300] + "...\n")
    
    return True

def run_all_tests():
    """Run all gameplay improvement tests"""
    print("\n🧪 RUNNING GAMEPLAY IMPROVEMENT TESTS\n" + "=" * 50)
    
    test_action_outcome_framework()
    test_narrative_coherence_system()
    test_story_progression_accelerator()
    test_enhanced_location_system()
    test_integrated_systems()
    
    print("\n✅ ALL GAMEPLAY IMPROVEMENT TESTS COMPLETED")

if __name__ == "__main__":
    run_all_tests()