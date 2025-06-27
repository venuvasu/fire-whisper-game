#!/usr/bin/env python3
"""
Local Development Runner for Fire Whisper RPG
Runs the game locally without AWS dependencies
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "backend"))

# Load environment variables
load_dotenv(project_root / ".env.local")

def check_environment():
    """Check if local environment is properly configured"""
    required_vars = ["CLAUDE_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Copy .env.example to .env.local and configure your API keys")
        return False
    
    return True

def run_local_game():
    """Run the game in local mode"""
    if not check_environment():
        return
    
    print("🔥 Fire Whisper RPG - Local Mode")
    print("=" * 40)
    print(f"🏷️  Version: {get_version()}")
    print(f"🔑 API Key: {'✅ Configured' if os.getenv('CLAUDE_API_KEY') else '❌ Missing'}")
    print(f"🌍 Mode: Local Development")
    print("=" * 40)
    
    try:
        # Import game components
        from engine.ai_integration import AIIntegrationLayer
        from utils.character_sheet import CharacterSheet
        
        # Initialize game
        api_key = os.getenv("CLAUDE_API_KEY")
        ai_layer = AIIntegrationLayer(api_key)
        
        # Create default character
        char_sheet = CharacterSheet()
        character = {
            'name': char_sheet.name,
            'class': char_sheet.class_name,
            'level': char_sheet.level,
            'xp': char_sheet.xp,
            'stats': {
                'strength': char_sheet.strength,
                'dexterity': char_sheet.dexterity,
                'intelligence': char_sheet.intelligence,
                'charisma': char_sheet.charisma
            },
            'resources': {
                'hp': char_sheet.hp,
                'max_hp': char_sheet.max_hp(),
                'energy': char_sheet.energy,
                'max_energy': char_sheet.max_energy()
            },
            'skills': char_sheet.skills,
            'achievements': char_sheet.achievements,
            'emberlyn_bond': char_sheet.emberlyn_bond
        }
        
        print(f"\n🎮 Starting new game with {character['name']} the {character['class']}")
        
        # Start game
        game_start = ai_layer.start_new_game(character)
        print(f"\n📖 {game_start['narrative']}")
        
        # Game loop
        turn_count = 0
        max_turns = int(os.getenv("MAX_TURNS_PER_GAME", 100))
        
        while turn_count < max_turns:
            print(f"\n{'='*50}")
            print(f"Turn {turn_count + 1}")
            print(f"{'='*50}")
            
            # Get player input
            player_input = input("\n🎯 Your choice: ").strip()
            
            if player_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for playing Fire Whisper RPG!")
                break
            
            if player_input.lower() == 'character':
                print(ai_layer.get_character_sheet())
                continue
            
            # Process action
            try:
                result = ai_layer.process_player_action(player_input)
                print(f"\n📖 {result['narrative']}")
                
                # Show mechanical results if debug mode
                if os.getenv("DEBUG_MODE", "false").lower() == "true":
                    if result.get('mechanical_results', {}).get('dice_rolls'):
                        print(f"\n🎲 Debug - Dice Results:")
                        for roll in result['mechanical_results']['dice_rolls']:
                            print(f"   {roll.roll_type}: {roll.base_roll} + {sum(roll.modifiers.values())} = {roll.base_roll + sum(roll.modifiers.values())} ({'SUCCESS' if roll.success else 'FAILURE'})")
                
                turn_count += 1
                
            except Exception as e:
                print(f"❌ Error processing action: {e}")
                if os.getenv("DEBUG_MODE", "false").lower() == "true":
                    import traceback
                    traceback.print_exc()
        
        print(f"\n🎉 Game completed after {turn_count} turns!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r backend/requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            import traceback
            traceback.print_exc()

def get_version():
    """Get current version from version.json"""
    try:
        import json
        with open(project_root / "version.json", 'r') as f:
            version_data = json.load(f)
        return version_data.get("version", "unknown")
    except:
        return "unknown"

if __name__ == "__main__":
    run_local_game()