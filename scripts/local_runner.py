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

# ===== INTEGRATED FEATURES =====
# Story Arc Integration, Location Debugging, Dynamic Options

# FEATURE 1: STORY ARC INTEGRATION
STORY_ARCS = [
    {
        "name": "The Sacred Flame Restoration",
        "type": "Nature Magic",
        "hook": "The Sacred Flame that protects the village is dimming, and you must find a Fire Essence crystal to restore it before darkness consumes the land.",
        "elements": ["Sacred duty", "elemental magic", "village protection", "ancient rituals"],
        "climax": "Restoring the Sacred Flame and banishing the encroaching darkness",
        "difficulty": 2,
        "turns": 8
    },
    {
        "name": "The Last Dragon's Quest",
        "type": "Classic Fantasy",
        "hook": "A young dragon, believed to be the last of its kind, seeks the player's protection from dragon hunters while searching for others of its race.",
        "elements": ["Protecting an innocent", "dragon hunters", "ancient dragon lairs", "species preservation"],
        "climax": "Discovery of a hidden dragon sanctuary and final battle with the Hunter King",
        "difficulty": 3,
        "turns": 12
    },
    {
        "name": "Songs of the Silent Stones",
        "type": "Musical Mystery",
        "hook": "Ancient stones that once sang beautiful melodies have fallen silent, and the local village's crops are failing as a result.",
        "elements": ["Musical puzzles", "environmental harmony", "corrupted magic", "restoring balance"],
        "climax": "Conducting a ritual to reharmonize the stones and restore the land's fertility",
        "difficulty": 2,
        "turns": 10
    },
    {
        "name": "The Memory Thief",
        "type": "Psychological Mystery",
        "hook": "People in a town are losing their most precious memories, and the player must track down the entity responsible before they forget who they are.",
        "elements": ["Identity themes", "memory puzzles", "emotional connections", "abstract enemy"],
        "climax": "Confronting the Memory Thief in a realm of stolen thoughts and recollections",
        "difficulty": 3,
        "turns": 11
    },
    {
        "name": "The Crimson Prophecy",
        "type": "Epic Fantasy",
        "hook": "An ancient prophecy speaks of a crimson blade that will either save or doom the realm. Multiple factions seek the weapon, and the player must decide its fate.",
        "elements": ["Rival seekers", "moral choices about power", "ancient weapon", "prophecy interpretation"],
        "climax": "Confrontation at the Sundering Peaks where the blade's true nature is revealed",
        "difficulty": 4,
        "turns": 15
    }
]

active_story_arc = None
arc_progress = 0

def select_story_arc(character_level, current_location, story_context):
    """Select appropriate story arc based on context"""
    global active_story_arc
    
    if active_story_arc:
        return active_story_arc  # Already have active arc
    
    # Filter arcs by difficulty
    suitable_arcs = [arc for arc in STORY_ARCS if arc['difficulty'] <= character_level + 1]
    
    # Context-based selection
    if 'sacred' in current_location.lower() or 'flame' in story_context:
        for arc in suitable_arcs:
            if 'Sacred Flame' in arc['name']:
                return arc
    
    # Default to first suitable arc
    return suitable_arcs[0] if suitable_arcs else STORY_ARCS[0]

def activate_story_arc(arc, log_file):
    """Activate a story arc"""
    global active_story_arc, arc_progress
    active_story_arc = arc
    arc_progress = 0
    
    activation_msg = f"\n🎭 STORY ARC ACTIVATED: {arc['name']}\n📖 {arc['hook']}\n🎯 Key Elements: {', '.join(arc['elements'][:3])}..."
    log_to_file(log_file, activation_msg)
    return activation_msg

def advance_story_arc(player_action, ai_response, log_file):
    """Advance story arc progress"""
    global arc_progress
    
    if not active_story_arc:
        return None
    
    # Check for progress indicators
    progress_keywords = ['discover', 'find', 'solve', 'defeat', 'complete', 'restore', 'save']
    if any(keyword in player_action.lower() or keyword in ai_response.lower() for keyword in progress_keywords):
        arc_progress += 1
        progress_ratio = arc_progress / active_story_arc['turns']
        
        if progress_ratio >= 1.0:
            completion_msg = f"\n🏆 STORY ARC COMPLETED: {active_story_arc['name']}!\n🎊 {active_story_arc['climax']}"
            log_to_file(log_file, completion_msg)
            return {'completed': True, 'message': completion_msg}
        elif progress_ratio >= 0.75:
            phase_msg = f"\n⚡ Story Arc Approaching Climax! ({arc_progress}/{active_story_arc['turns']})"
            log_to_file(log_file, phase_msg)
            return {'phase': 'climax', 'message': phase_msg}
        elif progress_ratio >= 0.5:
            phase_msg = f"\n🔥 Story Arc Intensifying! ({arc_progress}/{active_story_arc['turns']})"
            log_to_file(log_file, phase_msg)
            return {'phase': 'complications', 'message': phase_msg}
    
    return None

# FEATURE 2: LOCATION PROGRESSION DEBUG
LOCATION_CONNECTIONS = {
    'village_outskirts': ['ashbrook_village', 'ember_woods'],
    'ashbrook_village': ['village_outskirts', 'village_tavern'],
    'village_tavern': ['ashbrook_village'],
    'ember_woods': ['village_outskirts', 'crystal_cave', 'sacred_grove'],
    'crystal_cave': ['ember_woods'],
    'sacred_grove': ['ember_woods']
}

LOCATION_PATTERNS = {
    'ashbrook_village': ['ashbrook', 'village', 'town'],
    'village_outskirts': ['outskirts', 'path', 'road'],
    'crystal_cave': ['cave', 'cavern', 'crystal'],
    'ember_woods': ['woods', 'forest', 'trees'],
    'sacred_grove': ['grove', 'sacred', 'shrine'],
    'village_tavern': ['tavern', 'inn', 'rusty sword']
}

current_location = 'village_outskirts'
location_debug_history = []

def detect_location_change(ai_response, dice_rolls=None):
    """Debug and detect location changes from AI response"""
    global current_location
    
    ai_lower = ai_response.lower()
    movement_words = ['move', 'walk', 'travel', 'head', 'go', 'enter', 'arrive', 'reach']
    
    # Check if movement is indicated
    has_movement = any(word in ai_lower for word in movement_words)
    
    if not has_movement:
        return {'location_changed': False, 'debug_info': 'No movement detected'}
    
    # Detect target location
    detected_location = None
    for location, patterns in LOCATION_PATTERNS.items():
        if any(pattern in ai_lower for pattern in patterns):
            detected_location = location
            break
    
    if not detected_location or detected_location == current_location:
        return {'location_changed': False, 'debug_info': f'No valid location change detected (current: {current_location})'}
    
    # Validate connection
    if detected_location not in LOCATION_CONNECTIONS.get(current_location, []):
        debug_msg = f'Invalid transition: {current_location} -> {detected_location}. Valid: {LOCATION_CONNECTIONS.get(current_location, [])}'
        return {'location_changed': False, 'debug_info': debug_msg, 'error': 'invalid_connection'}
    
    # Check if dice roll needed (for certain locations)
    dice_required_locations = ['crystal_cave', 'ember_woods']
    if detected_location in dice_required_locations and not dice_rolls:
        return {
            'location_changed': False, 
            'debug_info': f'Dice roll required for {detected_location}',
            'dice_needed': True,
            'target_location': detected_location
        }
    
    # Valid transition
    old_location = current_location
    current_location = detected_location
    
    transition_record = {
        'from': old_location,
        'to': detected_location,
        'turn': len(location_debug_history) + 1,
        'dice_used': bool(dice_rolls)
    }
    location_debug_history.append(transition_record)
    
    return {
        'location_changed': True,
        'old_location': old_location,
        'new_location': detected_location,
        'debug_info': f'Valid transition: {old_location} -> {detected_location}'
    }

def get_location_debug_report():
    """Get location debugging report"""
    if not location_debug_history:
        return "No location transitions recorded."
    
    report = f"\n🗺️  LOCATION DEBUG REPORT ({len(location_debug_history)} transitions):\n"
    for i, transition in enumerate(location_debug_history[-5:], 1):  # Last 5 transitions
        dice_indicator = "🎲" if transition['dice_used'] else "🚶"
        report += f"  {i}. {transition['from']} -> {transition['to']} {dice_indicator}\n"
    
    return report

# FEATURE 3: DYNAMIC OPTIONS GENERATION
def generate_dynamic_options(situation, character, current_location, recent_actions):
    """Generate 4 structured options: Safe -> Moderate -> Risky High-Reward -> Emberlyn"""
    
    char_class = character.get('class', 'Cleric')
    
    # OPTION 1: SAFE APPROACH (Low risk, reliable outcome)
    safe_options = {
        'combat': "🛡️ Take a defensive stance and carefully assess the situation",
        'exploration': "🔍 Cautiously examine the area for important details",
        'social': "👂 Listen carefully and observe before taking action",
        'mystery': "📚 Look for clues and gather information methodically",
        'default': "🤔 Take a moment to carefully consider your options"
    }
    
    situation_type = 'default'
    if any(word in situation.lower() for word in ['enemy', 'hostile', 'fight', 'battle', 'goblin']):
        situation_type = 'combat'
    elif any(word in situation.lower() for word in ['explore', 'search', 'find', 'path', 'tree']):
        situation_type = 'exploration'
    elif any(word in situation.lower() for word in ['talk', 'speak', 'villager', 'people']):
        situation_type = 'social'
    elif any(word in situation.lower() for word in ['puzzle', 'mystery', 'secret', 'ancient']):
        situation_type = 'mystery'
    
    safe_option = safe_options.get(situation_type, safe_options['default'])
    
    # OPTION 2: MODERATE APPROACH (Medium risk, good outcome)
    moderate_options = {
        'Cleric': {
            'combat': "✨ Channel divine energy to protect yourself and allies",
            'exploration': "🔥 Use your divine connection to sense sacred energies",
            'social': "🙏 Offer spiritual guidance and comfort to those in need",
            'mystery': "📿 Pray for divine insight to reveal hidden truths",
            'default': "✨ Call upon your deity's blessing to guide your actions"
        },
        'Warrior': {
            'combat': "⚔️ Execute a tactical strike with calculated precision",
            'exploration': "🏃 Use your combat experience to navigate dangers",
            'social': "💪 Use your presence to command respect and attention",
            'mystery': "🗡️ Apply warrior instincts to uncover tactical advantages",
            'default': "⚔️ Use your warrior training to handle this challenge"
        },
        'Berserker': {
            'combat': "🔥 Channel controlled fury for a powerful but measured attack",
            'exploration': "💥 Use your primal instincts to sense danger and opportunity",
            'social': "😤 Let your passionate nature inspire others to action",
            'mystery': "🐺 Trust your wild intuition to guide you",
            'default': "🔥 Channel your berserker instincts with focused control"
        },
        'Mage': {
            'combat': "🔮 Cast a protective spell while preparing for action",
            'exploration': "⚡ Use magical senses to detect hidden properties",
            'social': "🌟 Demonstrate your magical knowledge to gain respect",
            'mystery': "📜 Apply arcane knowledge to decipher the situation",
            'default': "🔮 Use your magical abilities to understand the situation"
        }
    }
    
    class_options = moderate_options.get(char_class, moderate_options['Warrior'])
    moderate_option = class_options.get(situation_type, class_options['default'])
    
    # OPTION 3: RISKY HIGH-REWARD (High risk, potentially great outcome)
    risky_options = {
        'combat': "⚡ Launch a bold all-out attack to end the threat quickly",
        'exploration': "🚀 Venture boldly into the unknown despite the dangers",
        'social': "👑 Take charge and make a dramatic declaration or demand",
        'mystery': "💎 Attempt to unlock the mystery through direct magical interaction",
        'default': "🎯 Take a bold, decisive action that could change everything"
    }
    
    # Add location-specific risky options
    if current_location == 'crystal_cave':
        risky_option = "💎 Touch the crystal formations directly to absorb their power"
    elif current_location == 'sacred_grove':
        risky_option = "🌿 Attempt to commune directly with the ancient grove spirits"
    elif current_location == 'ember_woods':
        risky_option = "🔥 Use the forest's wild magic to enhance your abilities"
    else:
        risky_option = risky_options.get(situation_type, risky_options['default'])
    
    # OPTION 4: EMBERLYN ASSISTANCE (Safe with unique fairy perspective)
    emberlyn_options = {
        'combat': "🧚 Ask Emberlyn to use her fire magic to help in the fight",
        'exploration': "🧚 Ask Emberlyn to scout ahead with her fairy abilities",
        'social': "🧚 Ask Emberlyn to charm others with her fairy charisma",
        'mystery': "🧚 Ask Emberlyn about fairy knowledge of ancient magic",
        'default': "🧚 Ask Emberlyn for her fairy wisdom and unique perspective"
    }
    
    emberlyn_option = emberlyn_options.get(situation_type, emberlyn_options['default'])
    
    return [
        safe_option,
        moderate_option, 
        risky_option,
        emberlyn_option
    ]

# Track recent player actions for adaptive options
recent_player_actions = []

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
    # Create logs directory if it doesn't exist (always in project root)
    project_root = Path(__file__).parent.parent  # Go up from scripts/ to project root
    logs_dir = project_root / "logs"
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
        
        # Show integrated features status
        features_msg = f"\n🎆 ENHANCED FEATURES ACTIVE:\n✅ Story Arc Integration ({len(STORY_ARCS)} arcs available)\n✅ Location Progression Debug ({len(LOCATION_CONNECTIONS)} locations mapped)\n✅ Dynamic Contextual Options\n🗺️ Starting Location: {current_location}"
        log_to_file(log_file, features_msg)
        
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
            
            # Special commands for integrated features
            if player_input.lower() in ['arc', 'story', 'storyline']:
                if active_story_arc:
                    arc_status = f"\n🎭 ACTIVE STORY ARC: {active_story_arc['name']}\n📖 {active_story_arc['hook']}\n📊 Progress: {arc_progress}/{active_story_arc['turns']} turns ({arc_progress/active_story_arc['turns']*100:.1f}%)\n🎯 Phase: {'Climax Approaching' if arc_progress/active_story_arc['turns'] >= 0.75 else 'Development' if arc_progress/active_story_arc['turns'] >= 0.5 else 'Introduction'}"
                else:
                    arc_status = "\n🎭 No active story arc"
                log_to_file(log_file, arc_status)
                continue
            
            if player_input.lower() in ['location', 'map', 'where']:
                location_status = f"\n🗺️ CURRENT LOCATION: {current_location}\n🚪 Connected Locations: {', '.join(LOCATION_CONNECTIONS.get(current_location, []))}\n{get_location_debug_report()}"
                log_to_file(log_file, location_status)
                continue
            
            if player_input.lower() in ['features', 'status', 'debug']:
                feature_status = f"\n🔧 INTEGRATED FEATURES STATUS:\n🎭 Story Arc: {active_story_arc['name'] if active_story_arc else 'None'} (Progress: {arc_progress})\n🗺️ Location: {current_location} (Transitions: {len(location_debug_history)})\n🎯 Dynamic Options: Active (Recent actions: {len(recent_player_actions)})\n📊 Turn: {turn_count + 1}"
                log_to_file(log_file, feature_status)
                continue
            
            # Track recent actions for dynamic options
            recent_player_actions.append(player_input)
            if len(recent_player_actions) > 5:
                recent_player_actions.pop(0)
            
            # Process action with proper story progression
            try:
                result = ai_layer.process_player_action(player_input)
                
                # === INTEGRATED FEATURES PROCESSING ===
                
                # 1. Story Arc Integration
                if not active_story_arc and turn_count == 0:
                    # Activate story arc on first turn
                    selected_arc = select_story_arc(character.get('level', 1), current_location, result.get('narrative', ''))
                    activate_story_arc(selected_arc, log_file)
                
                # Advance story arc based on AI response
                arc_result = advance_story_arc(player_input, result.get('narrative', ''), log_file)
                if arc_result:
                    # Log arc progress
                    pass  # Already logged in advance_story_arc
                
                # 2. Location Progression Debug
                location_result = detect_location_change(result.get('narrative', ''), result.get('dice_rolls'))
                if location_result['location_changed']:
                    location_msg = f"\n🗺️ LOCATION CHANGED: {location_result['old_location']} → {location_result['new_location']}"
                    log_to_file(log_file, location_msg)
                elif location_result.get('debug_info'):
                    if os.getenv("DEBUG_MODE", "false").lower() == "true":
                        debug_msg = f"\n🔧 LOCATION DEBUG: {location_result['debug_info']}"
                        log_to_file(log_file, debug_msg)
                
                # 3. Generate Dynamic Options (replace static choices)
                if result.get('choices'):
                    # Generate dynamic options based on current context
                    dynamic_options = generate_dynamic_options(
                        result.get('narrative', ''), 
                        character, 
                        current_location, 
                        recent_player_actions
                    )
                    
                    # Add risk indicators and numbering
                    risk_indicators = ['🟢', '🟡', '🔴', '🟣']  # Green, Yellow, Red, Purple
                    risk_labels = ['(Safe & Reliable)', '(Moderate Risk)', '(High Risk, High Reward)', '(Emberlyn Assisted)']
                    
                    formatted_options = []
                    for i, (option, indicator, label) in enumerate(zip(dynamic_options, risk_indicators, risk_labels), 1):
                        formatted_options.append(f"{i}. {option} {indicator} {label}")
                    
                    result['choices'] = formatted_options  # Replace with formatted dynamic options
                
                # Show location and story progress
                if os.getenv("DEBUG_MODE", "false").lower() == "true":
                    debug_info = result.get('debug_info', {})
                    debug_msg = f"\n🔍 DEBUG - Game State: Location: {current_location} | Arc: {active_story_arc['name'] if active_story_arc else 'None'} | Progress: {arc_progress} | Turn: {turn_count + 1}"
                    log_to_file(log_file, debug_msg)
                    
                    # Show location debug report every 5 turns
                    if (turn_count + 1) % 5 == 0:
                        location_debug = get_location_debug_report()
                        log_to_file(log_file, location_debug)
                
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