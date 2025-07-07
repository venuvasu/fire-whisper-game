#!/usr/bin/env python3
"""
Modular Architecture Demo
Shows how to swap components and test different AI/Code configurations.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from looma.core.modular_architecture import (
    ModularGameArchitecture, GameState, ComponentMode
)

def create_test_state() -> GameState:
    """Create a test game state"""
    return GameState(
        player_hp=80,
        location="forest clearing",
        inventory=["sword", "health potion"],
        npcs_met=["village elder"],
        quests=[{"name": "Find the lost artifact", "status": "active"}],
        story_context="You are on a quest to find the lost artifact of power."
    )

def test_architecture_configuration(name: str, config: dict):
    """Test a specific architecture configuration"""
    print(f"\n🧪 Testing {name} Architecture")
    print("=" * 40)
    
    # Initialize architecture
    architecture = ModularGameArchitecture(config)
    
    # Show configuration
    info = architecture.get_architecture_info()
    print(f"State Management: {info['state_management']}")
    print(f"Narrative Generation: {info['narrative_generation']}")
    
    # Create test state
    state = create_test_state()
    
    # Test different actions
    test_actions = ["attack", "explore", "rest"]
    
    for action in test_actions:
        print(f"\n🎮 Action: {action}")
        result = architecture.process_game_turn(state, action)
        
        print(f"Success: {result.success}")
        print(f"Narrative: {result.narrative}")
        print(f"New Choices: {result.new_choices[:3]}...")  # Show first 3
        
        if result.state_changes:
            print(f"State Changes: {result.state_changes}")

def main():
    """Demo different architecture configurations"""
    
    print("🎯 Modular Architecture Demo")
    print("Testing different AI/Code responsibility splits")
    
    # Define test configurations
    configurations = {
        "AI Heavy": {
            "state_management": ComponentMode.AI,
            "narrative_generation": ComponentMode.AI
        },
        "Balanced": {
            "state_management": ComponentMode.CODE,
            "narrative_generation": ComponentMode.AI
        },
        "Code Heavy": {
            "state_management": ComponentMode.CODE,
            "narrative_generation": ComponentMode.CODE
        },
        "Hybrid": {
            "state_management": ComponentMode.CODE,
            "narrative_generation": ComponentMode.HYBRID
        }
    }
    
    # Test each configuration
    for name, config in configurations.items():
        test_architecture_configuration(name, config)
    
    print("\n✅ Demo complete!")
    print("\nNext steps:")
    print("1. Run architecture_balance_test.py to find optimal configuration")
    print("2. Use results to configure your production game architecture")
    print("3. A/B test different configurations with real players")

if __name__ == "__main__":
    main()