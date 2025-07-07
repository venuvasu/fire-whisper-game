#!/usr/bin/env python3
"""
Local Development Runner for Fire Whisper RPG
Runs the game locally without AWS dependencies
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "backend"))

# Load environment variables
load_dotenv(project_root / ".env.local")

def create_character_console(log_file):
    """Character creation using your actual system (matching frontend flow)"""
    char_header = "\n🎭 CHARACTER CREATION\n" + "=" * 50 + "\n🌟 Time to breathe life into legend! Shape your hero below—choose\ntheir path, their spirit, and their spark. The world of Fire Whisper\nawaits your creation...\n" + "=" * 50
    log_to_file(log_file, char_header)
    
    # Name input (matching frontend)
    name = input("\n📝 Enter your character's name (or 'quit' to exit): ").strip()
    if name.lower() in ['quit', 'exit', 'q']:
        return None  # Signal to quit
    if not name:
        name = "Adventurer"
    log_to_file(log_file, f"Name: {name}")
    
    # Race selection (matching frontend options exactly)
    races = [
        "Human", "Elf", "Dwarf", "Halfling", "Orc", 
        "Catfolk", "Lizardfolk", "Giant", "Goblin", "Centaur"
    ]
    
    print(f"\n🧬 Choose your race:")
    for i, race in enumerate(races, 1):
        print(f"  {i}. {race}")
    
    while True:
        try:
            race_input = input(f"\nChoose race (1-{len(races)}) or 'quit' to exit: ").strip()
            if race_input.lower() in ['quit', 'exit', 'q']:
                return None  # Signal to quit
            race_choice = int(race_input)
            if 1 <= race_choice <= len(races):
                race = races[race_choice - 1]
                log_to_file(log_file, f"Race: {race}")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number or 'quit' to exit.")
    
    # Gender selection (matching frontend options exactly)
    genders = ["Male", "Female", "Transgender Male", "Transgender Female", "Non-Binary"]
    
    print(f"\n⚧ Choose your gender:")
    for i, gender in enumerate(genders, 1):
        print(f"  {i}. {gender}")
    
    while True:
        try:
            gender_input = input(f"\nChoose gender (1-{len(genders)}) or 'quit' to exit: ").strip()
            if gender_input.lower() in ['quit', 'exit', 'q']:
                return None  # Signal to quit
            gender_choice = int(gender_input)
            if 1 <= gender_choice <= len(genders):
                gender = genders[gender_choice - 1]
                log_to_file(log_file, f"Gender: {gender}")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number or 'quit' to exit.")
    
    # Profession selection (matching frontend options exactly)
    professions = [
        "Warrior", "Berserker", "Mage", "Druid", "Shaman",
        "Cleric", "Templar", "Assassin", "Thief", "Bard"
    ]
    
    print(f"\n⚔️ Choose your profession:")
    for i, prof in enumerate(professions, 1):
        print(f"  {i}. {prof}")
    
    while True:
        try:
            prof_input = input(f"\nChoose profession (1-{len(professions)}) or 'quit' to exit: ").strip()
            if prof_input.lower() in ['quit', 'exit', 'q']:
                return None  # Signal to quit
            prof_choice = int(prof_input)
            if 1 <= prof_choice <= len(professions):
                profession = professions[prof_choice - 1]
                log_to_file(log_file, f"Profession: {profession}")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number or 'quit' to exit.")
    
    creation_msg = f"\n✨ Creating {name} the {race} {profession}...\n🤖 Generating character with AI (this may take a moment)..."
    log_to_file(log_file, creation_msg)
    
    try:
        # Use your ACTUAL character creation system
        from src.ai.providers.local_character_creator import create_character_console
        import json
        import uuid
        
        # Generate character using your AI system (matching frontend flow)
        user_id = "console_user"  # Mock user ID for console
        character_json = create_character_console(user_id, name, race, gender, profession, "claude-3-5-sonnet-20241022")
        
        # Parse the generated character
        character_data = json.loads(character_json)
        
        # Debug: Show what AI actually returned
        print(f"\n🔍 DEBUG - AI Response Structure:")
        print(f"Keys: {list(character_data.keys())}")
        if 'IDENTITY' in character_data:
            print(f"IDENTITY keys: {list(character_data['IDENTITY'].keys())}")
        if 'VITALITY' in character_data:
            print(f"VITALITY keys: {list(character_data['VITALITY'].keys())}")
        else:
            print("❌ No VITALITY key found!")
            print(f"Available keys: {list(character_data.keys())}")
            # Show first few keys of each top-level section
            for key, value in character_data.items():
                if isinstance(value, dict):
                    print(f"{key} contains: {list(value.keys())[:5]}...")
        
        # Convert AI response to match your existing system format
        # The AI returns camelCase but your system expects snake_case
        vitality = character_data['VITALITY']
        
        # Convert camelCase to snake_case to match your existing system
        if 'hitPoints' in vitality:
            vitality['hit_points'] = vitality['hitPoints']
        if 'maxHitPoints' in vitality:
            vitality['max_hit_points'] = vitality['maxHitPoints']
        if 'maxMana' in vitality:
            vitality['max_mana'] = vitality['maxMana']
            
        hp = vitality.get('hit_points', 20)
        mana = vitality.get('mana', 10)
        
        # Handle both camelCase and snake_case for display
        attrs = character_data['ATTRIBUTES']
        success_msg = f"\n🎉 Character Created Successfully!\n🎭 {character_data['IDENTITY']['name']} the {character_data['IDENTITY']['race']} {character_data['IDENTITY']['profession']}\n📊 STR:{attrs['strength']} DEX:{attrs['dexterity']} CON:{attrs['constitution']}\n📊 INT:{attrs['intelligence']} WIS:{attrs['wisdom']} CHA:{attrs['charisma']}\n❤️  HP: {hp} | 🔮 Mana: {mana}"
        log_to_file(log_file, success_msg)
        
        # Show some equipment
        if character_data.get('EQUIPMENT', {}).get('weapon'):
            weapon = character_data['EQUIPMENT']['weapon']
            weapon_msg = f"⚔️  Weapon: {weapon['name']} ({weapon['damage']})"
            log_to_file(log_file, weapon_msg)
        
        character = {
            'name': character_data['IDENTITY']['name'],
            'class': character_data['IDENTITY']['profession'],
            'level': 1,
            'xp': 0,
            'stats': character_data['ATTRIBUTES'],
            'resources': {
                'hp': hp,
                'max_hp': hp,
                'energy': mana,
                'max_energy': mana
            },
            'skills': character_data.get('SKILLS', character_data.get('CAPABILITIES', {})),
            'achievements': [],
            'emberlyn_bond': 1,
            'character_id': str(uuid.uuid4()),
            'full_character_data': character_data  # Keep full data for reference
        }
        
        return character
        
    except Exception as e:
        print(f"❌ Error creating character with AI: {e}")
        print("🎮 Creating basic character for console play...")
        
        # Fallback to basic character if AI fails
        from src.utils.character_sheet import CharacterSheet
        char_sheet = CharacterSheet({
            'name': name,
            'class': profession,
            'race': race,
            'gender': gender
        })
        
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
        
        return character

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

def setup_gameplay_logging():
    """Setup gameplay logging to txt file"""
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    log_file = logs_dir / f"gameplay_{timestamp}.txt"
    
    return log_file

def handle_graceful_quit(log_file):
    """Handle graceful quit with log file save option"""
    quit_msg = "\n👋 Thanks for playing Fire Whisper RPG!"
    print(quit_msg)  # Print to console but don't write to file yet
    
    # Ask if user wants to save the log file
    save_choice = input("\n💾 Would you like to save this gameplay log? (y/n): ").strip().lower()
    
    if save_choice in ['n', 'no']:
        try:
            if log_file.exists():
                log_file.unlink()  # Delete the log file
                print(f"🗑️  Log file deleted: {log_file.name}")
            else:
                print(f"⚠️  Log file doesn't exist: {log_file.name}")
        except Exception as e:
            print(f"⚠️  Could not delete log file: {e}")
            import traceback
            traceback.print_exc()
    else:
        # Only write quit message to file if keeping it
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(quit_msg + '\n')
        print(f"💾 Log file saved: {log_file.name}")
    
    print("\n🔥 Fire Whisper RPG session ended.")
    return True  # Signal to exit

def log_to_file(log_file, content):
    """Write content to log file and print to console"""
    print(content)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(content + '\n')

def run_local_game():
    """Run the game in local mode with gameplay logging"""
    if not check_environment():
        return
    
    # Setup logging
    log_file = setup_gameplay_logging()
    
    # Log game start
    header = f"🔥 Fire Whisper RPG - Local Mode\n" + "=" * 40 + f"\n🏷️  Version: {get_version()}\n🔑 API Key: {'✅ Configured' if os.getenv('CLAUDE_API_KEY') else '❌ Missing'}\n🌍 Mode: Local Development\n📝 Log File: {log_file.name}\n" + "=" * 40
    log_to_file(log_file, header)
    
    try:
        # Import existing game components (fix the broken import)
        from src.core.ai_integration import AIIntegrationLayer
        from src.utils.character_sheet import CharacterSheet
        
        # Initialize game using existing architecture
        api_key = os.getenv("CLAUDE_API_KEY")
        ai_layer = AIIntegrationLayer(api_key)
        
        # Import your existing AI providers
        from src.ai.providers.claude_direct_api import take_turn_direct
        from src.ai.providers.local_character_creator import create_character_console as create_char_ai
        
        # Character Creation (matching frontend flow)
        character = create_character_console(log_file)
        if not character:
            # Handle quit during character creation
            if handle_graceful_quit(log_file):
                return
        
        start_msg = f"\n🎮 Starting new game with {character['name']} the {character['class']}"
        log_to_file(log_file, start_msg)
        
        # Start game using existing system
        game_start = ai_layer.start_new_game(character)
        narrative_msg = f"\n📖 {game_start['narrative']}"
        log_to_file(log_file, narrative_msg)
        
        # Show initial choices
        if game_start.get('choices'):
            choices_msg = "\n**What would you like to do?**"
            for choice in game_start['choices']:
                choices_msg += f"\n{choice}"
            log_to_file(log_file, choices_msg)
        
        # Game loop
        turn_count = 0
        max_turns = int(os.getenv("MAX_TURNS_PER_GAME", 100))
        
        while turn_count < max_turns:
            turn_header = f"\n{'='*50}\nTurn {turn_count + 1}\n{'='*50}"
            log_to_file(log_file, turn_header)
            
            # Get player input
            player_input = input("\n🎯 Your choice: ").strip()
            log_to_file(log_file, f"\n🎯 Player Input: {player_input}")
            
            if player_input.lower() in ['quit', 'exit', 'q']:
                if handle_graceful_quit(log_file):
                    break
            
            if player_input.lower() == 'character':
                char_sheet = ai_layer.get_character_sheet()
                log_to_file(log_file, char_sheet)
                continue
            
            if player_input.lower() in ['cost', 'costs', 'money', 'api']:
                cost_summary = ai_layer.get_cost_summary()
                log_to_file(log_file, cost_summary)
                continue
            
            # Process action with proper story progression
            try:
                result = ai_layer.process_player_action(player_input)
                
                # Show location and story progress
                if os.getenv("DEBUG_MODE", "false").lower() == "true":
                    debug_info = result.get('debug_info', {})
                    debug_msg = f"\n🔍 DEBUG - Game State: Location: {debug_info.get('location', 'unknown')} | Progress: {debug_info.get('story_progress', 0)} | Turn: {debug_info.get('turn', 0)}"
                    log_to_file(log_file, debug_msg)
                
                # Show narrative
                result_msg = f"\n📍 LOCATION: {result.get('LOCATION', 'Unknown')}"
                log_to_file(log_file, result_msg)
                
                narrative_msg = f"\n📖 {result['narrative']}"
                log_to_file(log_file, narrative_msg)
                
                # Show choices
                if result.get('choices'):
                    choices_msg = "\n**What would you like to do?**"
                    for choice in result['choices']:
                        choices_msg += f"\n{choice}"
                    log_to_file(log_file, choices_msg)
                
                # Show mechanical results if any
                if result.get('mechanical_results', {}).get('info'):
                    mech_msg = f"\n⚙️ {result['mechanical_results']['info']}"
                    log_to_file(log_file, mech_msg)
                
                turn_count += 1
                
            except Exception as e:
                error_msg = f"❌ Error processing action: {e}"
                log_to_file(log_file, error_msg)
                if os.getenv("DEBUG_MODE", "false").lower() == "true":
                    import traceback
                    traceback_msg = traceback.format_exc()
                    log_to_file(log_file, f"\nTraceback:\n{traceback_msg}")
        
        # Show final cost summary
        try:
            final_cost_summary = ai_layer.get_cost_summary()
            log_to_file(log_file, f"\n{final_cost_summary}")
        except:
            pass  # Don't fail if cost summary fails
        
        # Don't log completion message - it's handled in graceful quit
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