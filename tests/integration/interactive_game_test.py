#!/usr/bin/env python3
"""
Interactive Fire Whisper Game Tester
"""
import sys
import os

# Add backend to path
sys.path.append('backend')

from claude_direct.claude_direct_api import take_turn_direct

def start_interactive_game():
    """Start an interactive game session"""
    print("🔥 Fire Whisper - Interactive Game Test")
    print("=" * 50)
    print("Type 'quit' to exit, 'restart' to start over")
    print("=" * 50)
    
    # Initialize game
    game_record = {
        "game_id": "interactive-test",
        "messages": [
            "You are Emberlyn, a wise fairy serving as the Dungeon Master for Fire Whisper, a fantasy RPG. Start an adventure for the player.",
            "Welcome, brave adventurer! You stand at the entrance of a mysterious cave with glowing runes..."
        ],
        "game_active": True
    }
    
    model_input = input("Choose model (sonnet_35/claude_haiku_35/claude_haiku_30) [sonnet_35]: ").strip()
    valid_models = ["sonnet_35", "claude_haiku_35", "claude_haiku_30"]
    model = model_input if model_input in valid_models else "sonnet_35"
    print(f"\n🎯 Using model: {model}")
    print("=" * 50)
    
    # Get initial response
    try:
        response = take_turn_direct("interactive-user", game_record, model)
        print(f"\n🧚‍♀️ Emberlyn: {response}")
        game_record["messages"].append(response)
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Game loop
    while True:
        print("\n" + "-" * 30)
        user_input = input("\n🎮 Your action: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Thanks for playing!")
            break
        elif user_input.lower() == 'restart':
            start_interactive_game()
            return
        elif not user_input:
            print("Please enter an action!")
            continue
        
        # Add user input to game
        game_record["messages"].append(user_input)
        
        try:
            # Get AI response
            response = take_turn_direct("interactive-user", game_record, model)
            print(f"\n🧚‍♀️ Emberlyn: {response}")
            game_record["messages"].append(response)
            
            # Check for game completion
            if "Congratulations, you have completed this Saga!" in response:
                print("\n🎉 Game completed! Starting new adventure...")
                input("Press Enter to continue...")
                start_interactive_game()
                return
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Try again or type 'quit' to exit")

if __name__ == "__main__":
    start_interactive_game()