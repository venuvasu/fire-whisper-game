#!/usr/bin/env python3
"""
Fire Whisper RPG - Local Development Runner

A complete text-based RPG with AI-powered narratives and deterministic mechanics.
Features three major integrated systems:

1. Story Arc Integration - 71 predefined story arcs with player saga selection
2. Location Progression Debug - Movement validation with dice integration  
3. Dynamic Options Generation - Context-aware, class-specific choices

Usage:
    python scripts/local_runner.py

Requires:
    - Python 3.8+
    - Claude API key in .env.local
    - src/ai/prompts/story_arcs.txt (71 predefined story arcs)

Version: 1.3.0.0
Author: Fire Whisper RPG Development Team
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

# ===== BILLION DOLLAR GAME FEATURES =====
# Enhanced Context Management, Session Hooks, Character Investment, Story Integration
# Implements the complete retention and engagement strategy

# ===== CORE SYSTEMS INTEGRATION =====
# 1. Enhanced Context Manager - Persistent context across sessions
# 2. Session Hooks Manager - Compelling reasons to return
# 3. Character Investment Manager - Progressive emotional attachment
# 4. Integrated Story Controller - All existing story systems
# 5. Billion Dollar Game Controller - Master orchestration

def initialize_billion_dollar_controller(character_data):
    """Initialize the billion dollar game controller with all systems"""
    try:
        from src.domain.fire_whisper_game.billion_dollar_game_controller import BillionDollarGameController
        return BillionDollarGameController(character_data)
    except ImportError as e:
        print(f"⚠️ Billion Dollar Controller not available: {e}")
        print("🔄 Falling back to integrated story controller...")
        return None

def load_story_arcs():
    """Load all story arcs from the story_arcs.txt and new story arcs files"""
    story_arcs_file = Path(__file__).parent.parent / "src" / "infrastructure" / "ai" / "claude" / "prompts" / "story_arcs.txt"
    new_story_arcs_file = Path(__file__).parent.parent / "src" / "infrastructure" / "ai" / "claude" / "prompts" / "new_story_arcs.txt"
    new_story_arcs_batch2_file = Path(__file__).parent.parent / "src" / "infrastructure" / "ai" / "claude" / "prompts" / "new_story_arcs_batch2.txt"
    new_story_arcs_batch3_file = Path(__file__).parent.parent / "src" / "infrastructure" / "ai" / "claude" / "prompts" / "new_story_arcs_batch3.txt"
    
    parsed_arcs = []
    new_arcs_count = 0
    
    # Load original arcs
    with open(story_arcs_file, "r") as f:
        story_arcs_content = f.read()
        story_arcs_list = [line.strip() for line in story_arcs_content.split('\n') if line.strip()]
    
    # Parse original arcs
    for story_line in story_arcs_list:
        if story_line.startswith('#'):  # Skip comment lines
            continue
            
        try:
            sections = story_line.split(' | ')
            arc_data = {}
            for section in sections:
                if ':' in section:
                    key, value = section.split(':', 1)
                    arc_data[key.strip()] = value.strip()
            
            if 'Name' in arc_data:
                parsed_arcs.append({
                    "name": arc_data['Name'],
                    "type": arc_data.get('Type', 'Adventure'),
                    "hook": arc_data.get('Hook', ''),
                    "elements": arc_data.get('Key Elements', '').split(', ') if arc_data.get('Key Elements') else [],
                    "climax": arc_data.get('Climax', ''),
                    "difficulty": 2,  # Default difficulty
                    "turns": 10,      # Default turns
                    "location_start": None,  # Default location
                    "character_level": "1-3"  # Default level range
                })
        except Exception as e:
            print(f"Warning: Could not parse story arc: {story_line[:50]}... Error: {e}")
    
    # Function to parse new arc files with enhanced format
    def parse_new_arc_file(file_path):
        nonlocal new_arcs_count
        
        if not file_path.exists():
            return []
            
        with open(file_path, "r") as f:
            new_arcs_content = f.read()
            new_arcs_list = [line.strip() for line in new_arcs_content.split('\n') if line.strip()]
        
        file_arcs = []
        for story_line in new_arcs_list:
            if story_line.startswith('#'):  # Skip comment lines
                continue
                
            try:
                sections = story_line.split(' | ')
                arc_data = {}
                for section in sections:
                    if ':' in section:
                        key, value = section.split(':', 1)
                        arc_data[key.strip()] = value.strip()
                
                if 'Name' in arc_data:
                    file_arcs.append({
                        "name": arc_data['Name'],
                        "type": arc_data.get('Type', 'Adventure'),
                        "hook": arc_data.get('Hook', ''),
                        "elements": arc_data.get('Key Elements', '').split(', ') if arc_data.get('Key Elements') else [],
                        "climax": arc_data.get('Climax', ''),
                        "difficulty": int(arc_data.get('Difficulty', 2)),
                        "turns": int(arc_data.get('Turns', 10)),
                        "location_start": arc_data.get('Location Start'),
                        "character_level": arc_data.get('Character Level', "1-3")
                    })
                    new_arcs_count += 1
            except Exception as e:
                print(f"Warning: Could not parse new story arc: {story_line[:50]}... Error: {e}")
        
        return file_arcs
    
    # Load and parse first batch of new arcs
    parsed_arcs.extend(parse_new_arc_file(new_story_arcs_file))
    
    # Load and parse second batch of new arcs
    parsed_arcs.extend(parse_new_arc_file(new_story_arcs_batch2_file))
    
    # Load and parse third batch of new arcs
    parsed_arcs.extend(parse_new_arc_file(new_story_arcs_batch3_file))
    
    print(f"📚 Loaded {len(parsed_arcs)} story arcs ({new_arcs_count} new arcs)")
    return parsed_arcs

STORY_ARCS = load_story_arcs()
# Debug: Uncomment next line to see arc loading confirmation
# print(f"📚 Loaded {len(STORY_ARCS)} story arcs from story_arcs.txt")

active_story_arc = None
arc_progress = 0

def select_story_arc(character_level, current_location, story_context, character_class=None):
    """Select appropriate story arc based on context, location, character level, and class"""
    global active_story_arc
    
    if active_story_arc:
        return active_story_arc  # Already have active arc
    
    # Parse character level range from arcs
    def in_level_range(arc, level):
        level_range = arc.get('character_level', '1-3')
        if not level_range or '-' not in level_range:
            return True  # Default to allowing if no valid range
        try:
            min_level, max_level = map(int, level_range.split('-'))
            return min_level <= level <= max_level
        except:
            return True  # Allow if parsing fails
    
    # Check if arc is suitable for character class
    def is_class_suitable(arc, char_class):
        if not char_class:
            return True  # No class restriction if character_class not provided
        
        required_class = None
        # Check if arc has a required class in its type
        if '/' in arc.get('type', ''):
            arc_type = arc['type'].split('/')
            if len(arc_type) > 1 and arc_type[0] == 'Class-Specific':
                required_class = arc_type[1]
        
        # Also check for explicit Required Class field
        if 'required_class' in arc:
            required_class = arc['required_class']
        
        # If no required class, arc is suitable for all classes
        if not required_class:
            return True
        
        # Check if character class matches required class
        return char_class.lower() == required_class.lower()
    
    # Filter arcs by difficulty, character level, and class
    suitable_arcs = [
        arc for arc in STORY_ARCS 
        if arc['difficulty'] <= character_level + 1 
        and in_level_range(arc, character_level)
        and is_class_suitable(arc, character_class)
    ]
    
    # Location-based selection (prioritize arcs that start in current location)
    location_arcs = [arc for arc in suitable_arcs if arc.get('location_start') == current_location]
    if location_arcs:
        import random
        return random.choice(location_arcs)  # Choose a random arc for this location for variety
    
    # Enhanced context-based selection
    context_keywords = {
        # Elements and nature
        'shadow': ['shadow', 'darkness', 'whisper', 'secret', 'night'],
        'fire': ['fire', 'flame', 'ember', 'burn', 'heat', 'ash'],
        'water': ['water', 'tide', 'river', 'ocean', 'flood', 'rain'],
        'earth': ['earth', 'stone', 'crystal', 'mountain', 'rock', 'gem'],
        'air': ['air', 'wind', 'sky', 'breath', 'cloud', 'storm'],
        
        # Creatures and beings
        'undead': ['undead', 'zombie', 'skeleton', 'ghost', 'spirit', 'haunt'],
        'monster': ['monster', 'beast', 'creature', 'dragon', 'giant', 'troll'],
        'fae': ['fairy', 'fae', 'elf', 'magical creature', 'sprite', 'pixie'],
        
        # Magic and mysticism
        'magic': ['magic', 'spell', 'arcane', 'mystic', 'enchant', 'wizard'],
        'ritual': ['ritual', 'ceremony', 'sacrifice', 'altar', 'offering', 'prayer'],
        'myth': ['myth', 'legend', 'fate', 'god', 'deity', 'divine'],
        
        # Historical and cultural
        'history': ['history', 'ancient', 'ruin', 'artifact', 'relic', 'tomb'],
        'culture': ['culture', 'tradition', 'custom', 'foreign', 'exotic', 'tribe'],
        
        # Character-focused
        'personal': ['personal', 'family', 'revenge', 'redemption', 'honor', 'duty'],
        'relationship': ['friend', 'enemy', 'rival', 'mentor', 'apprentice', 'companion']
    }
    
    story_context_lower = story_context.lower()
    
    # Score arcs based on context relevance
    arc_scores = {}
    for arc in suitable_arcs:
        arc_text = f"{arc['name']} {arc['type']} {arc['hook']}".lower()
        score = 0
        
        # Check for theme matches
        for theme, keywords in context_keywords.items():
            # Check if theme is in context
            theme_in_context = any(keyword in story_context_lower for keyword in keywords)
            # Check if theme is in arc
            theme_in_arc = any(keyword in arc_text for keyword in keywords)
            
            if theme_in_context and theme_in_arc:
                score += 3  # Strong match - both in context and arc
            elif theme_in_context:
                score += 1  # Context mentions theme but arc doesn't
            elif theme_in_arc:
                score += 1  # Arc has theme but context doesn't mention it
        
        # Bonus for location-specific arcs that match the current location type
        if current_location in arc_text:
            score += 2
        
        # Bonus for arcs with matching elements in key elements
        for element in arc['elements']:
            if element.lower() in story_context_lower:
                score += 1
        
        arc_scores[arc['name']] = score
    
    # Get arcs with highest scores
    if arc_scores:
        max_score = max(arc_scores.values())
        if max_score > 0:  # Only use score-based selection if we have meaningful matches
            best_arcs = [arc for arc in suitable_arcs if arc_scores[arc['name']] == max_score]
            import random
            return random.choice(best_arcs)
    
    # Special location-based selection as fallback
    location_type_arcs = []
    
    if 'sacred' in current_location.lower() or 'grove' in current_location.lower():
        location_type_arcs = [arc for arc in suitable_arcs if 
                             any(keyword in f"{arc['name']} {arc['type']}".lower() 
                                for keyword in ['sacred', 'grove', 'nature', 'spirit', 'druid'])]
    
    elif 'crystal' in current_location.lower() or 'cave' in current_location.lower():
        location_type_arcs = [arc for arc in suitable_arcs if 
                             any(keyword in f"{arc['name']} {arc['type']}".lower() 
                                for keyword in ['crystal', 'cave', 'stone', 'earth', 'underground'])]
    
    elif 'ember' in current_location.lower() or 'wood' in current_location.lower():
        location_type_arcs = [arc for arc in suitable_arcs if 
                             any(keyword in f"{arc['name']} {arc['type']}".lower() 
                                for keyword in ['ember', 'wood', 'forest', 'fire', 'tree'])]
    
    elif 'village' in current_location.lower():
        location_type_arcs = [arc for arc in suitable_arcs if 
                             any(keyword in f"{arc['name']} {arc['type']}".lower() 
                                for keyword in ['village', 'town', 'settlement', 'community'])]
    
    elif 'tavern' in current_location.lower():
        location_type_arcs = [arc for arc in suitable_arcs if 
                             any(keyword in f"{arc['name']} {arc['type']}".lower() 
                                for keyword in ['tavern', 'inn', 'drink', 'social', 'gathering'])]
    
    if location_type_arcs:
        import random
        return random.choice(location_type_arcs)
    
    # Special handling for high-level characters
    if character_level >= 5:
        # For high-level characters, prioritize high-level arcs
        high_level_arcs = [arc for arc in suitable_arcs if 'High-Level' in arc['type']]
        
        # If we have high-level arcs and the context suggests epic/cosmic themes, prioritize them
        if high_level_arcs and any(keyword in story_context.lower() for keyword in 
                                ['epic', 'cosmic', 'divine', 'godslayer', 'void', 'dragon']):
            import random
            print(f"DEBUG: Selecting from {len(high_level_arcs)} high-level arcs for level {character_level} character")
            return random.choice(high_level_arcs)
    
    # Category-based selection as another fallback
    character_level_category = "beginner" if character_level <= 2 else "intermediate" if character_level <= 4 else "advanced"
    
    if character_level_category == "beginner":
        # For beginners, prefer straightforward adventure arcs
        beginner_arcs = [arc for arc in suitable_arcs if 
                        any(keyword in arc['type'].lower() 
                           for keyword in ['classic', 'adventure', 'exploration'])]
        if beginner_arcs:
            import random
            return random.choice(beginner_arcs)
    
    elif character_level_category == "advanced":
        # For advanced players, prefer complex or challenging arcs
        advanced_arcs = [arc for arc in suitable_arcs if 
                        any(keyword in arc['type'].lower() 
                           for keyword in ['epic', 'cosmic', 'mythological', 'complex'])]
        if advanced_arcs:
            import random
            return random.choice(advanced_arcs)
    
    # Default to a random suitable arc for variety
    import random
    return random.choice(suitable_arcs) if suitable_arcs else STORY_ARCS[0]

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
    global arc_progress, active_story_arc
    
    if not active_story_arc:
        return None
    
    # Check for progress indicators
    progress_keywords = ['discover', 'find', 'solve', 'defeat', 'complete', 'restore', 'save', 'search', 'progress', 'ritual']
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
            return {'phase': 'development', 'message': phase_msg}
        else:
            # Early progress
            return {'phase': 'introduction', 'progress': arc_progress, 'total': active_story_arc['turns']}
    
    # No progress detected
    return {'phase': 'no_progress', 'progress': arc_progress, 'total': active_story_arc['turns']}

# ===== FEATURE 2: LOCATION PROGRESSION DEBUG =====
# Validates location transitions, prevents invalid movement, and integrates
# with dice system for challenging locations. Provides comprehensive debug reporting.

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

# ===== FEATURE 3: DYNAMIC OPTIONS GENERATION =====
# Generates context-aware, class-specific options with 4-tier risk structure:
# Safe → Moderate (class-specific) → Risky High-Reward → Emberlyn Assisted
# Options adapt based on narrative content, character class, and recent actions.

def generate_dynamic_options(situation, character, current_location, recent_actions):
    """Generate 4 structured options: Safe -> Moderate -> Risky High-Reward -> Emberlyn"""
    
    char_class = character.get('class', 'Cleric')
    
    # Analyze the current narrative situation for context
    situation_lower = situation.lower()
    
    # Detect key narrative elements
    has_magic = any(word in situation_lower for word in ['magic', 'spell', 'rune', 'energy', 'mystical', 'arcane', 'barrier'])
    has_danger = any(word in situation_lower for word in ['danger', 'threat', 'shadow', 'blight', 'dark', 'corrupt', 'hostile'])
    has_investigation = any(word in situation_lower for word in ['examine', 'investigate', 'clues', 'traces', 'markings', 'detect'])
    has_movement = any(word in situation_lower for word in ['path', 'ahead', 'village', 'continue', 'forward', 'travel'])
    has_social = any(word in situation_lower for word in ['villagers', 'people', 'talk', 'speak', 'ask', 'conversation'])
    has_mystery = any(word in situation_lower for word in ['mystery', 'strange', 'unusual', 'curious', 'puzzling', 'secret'])
    
    # Determine primary situation context
    if has_magic and has_danger:
        situation_type = 'magical_danger'
    elif has_investigation and has_mystery:
        situation_type = 'investigation'
    elif has_danger:
        situation_type = 'danger'
    elif has_magic:
        situation_type = 'magic'
    elif has_social:
        situation_type = 'social'
    elif has_movement:
        situation_type = 'exploration'
    else:
        situation_type = 'default'
    
    # OPTION 1: SAFE APPROACH (Low risk, reliable outcome)
    safe_options = {
        'magical_danger': "🛡️ Carefully assess the magical threat before taking action",
        'investigation': "🔍 Methodically examine the evidence for important clues",
        'danger': "🛡️ Take a defensive stance and assess the threat carefully",
        'magic': "🔮 Study the magical energies cautiously before proceeding",
        'social': "👂 Listen carefully and observe the social dynamics",
        'exploration': "🔍 Cautiously examine the area for important details",
        'default': "🤔 Take a moment to carefully consider your options"
    }
    
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
        'magical_danger': "⚡ Attempt to counter the magical threat with raw power",
        'investigation': "💎 Try to uncover the truth through direct magical probing",
        'danger': "⚡ Launch a bold preemptive strike against the threat",
        'magic': "🔥 Channel maximum magical energy to breakthrough barriers",
        'social': "👑 Make a dramatic declaration to rally or intimidate",
        'exploration': "🚀 Venture boldly into the unknown despite clear dangers",
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
        'magical_danger': "🧚 Ask Emberlyn to help identify and counter the magical threat",
        'investigation': "🧚 Ask Emberlyn to use her fairy senses to detect hidden clues",
        'danger': "🧚 Ask Emberlyn to scout ahead and assess the danger safely",
        'magic': "🧚 Ask Emberlyn about fairy knowledge of this type of magic",
        'social': "🧚 Ask Emberlyn to use her charm to ease social tensions",
        'exploration': "🧚 Ask Emberlyn to scout ahead with her fairy abilities",
        'default': "🧚 Ask Emberlyn for her fairy wisdom and unique perspective"
    }
    
    risky_option = risky_options.get(situation_type, risky_options['default'])
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
        from src.infrastructure.ai.claude.providers.local_character_creator import create_character_console
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
        from src.shared.utils.character_sheet import CharacterSheet
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
    
    # Handle MockLogFile objects for testing
    if hasattr(log_file, 'write'):
        log_file.write(content + '\n')
    else:
        # Regular file path
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(content + '\n')

def select_saga(log_file):
    """Let player select their preferred saga/story arc"""
    saga_header = "\n🎆 SAGA SELECTION\n" + "=" * 50 + "\n🎭 Choose your adventure! Each saga offers a unique story\nexperience with different themes and challenges.\n" + "=" * 50
    log_to_file(log_file, saga_header)
    
    # Show first 10 story arcs for selection
    print("\n📚 Available Sagas:")
    display_arcs = STORY_ARCS[:10]  # Show first 10 for now
    
    for i, arc in enumerate(display_arcs, 1):
        print(f"  {i}. {arc['name']} ({arc['type']})")
        print(f"     {arc['hook'][:80]}...")
    
    print(f"  {len(display_arcs) + 1}. Random Saga (Let fate decide!)")
    
    while True:
        try:
            choice_input = input(f"\nChoose saga (1-{len(display_arcs) + 1}) or 'quit' to exit: ").strip()
            if choice_input.lower() in ['quit', 'exit', 'q']:
                return None
            
            choice = int(choice_input)
            if 1 <= choice <= len(display_arcs):
                selected_arc = display_arcs[choice - 1]
                log_to_file(log_file, f"Selected Saga: {selected_arc['name']}")
                return selected_arc
            elif choice == len(display_arcs) + 1:
                import random
                selected_arc = random.choice(STORY_ARCS)
                log_to_file(log_file, f"Random Saga Selected: {selected_arc['name']}")
                return selected_arc
            else:
                print(f"Please choose a number between 1 and {len(display_arcs) + 1}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            return None

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
        from src.domain.fire_whisper_game.ai_integration import AIIntegrationLayer
        from src.shared.utils.character_sheet import CharacterSheet
        
        # Initialize game using existing architecture
        api_key = os.getenv("CLAUDE_API_KEY")
        ai_layer = AIIntegrationLayer(api_key)
        
        # Import your existing AI providers
        from src.infrastructure.ai.claude.providers.claude_direct_api import take_turn_direct
        from src.infrastructure.ai.claude.providers.local_character_creator import create_character_console as create_char_ai
        
        # Saga Selection
        selected_saga = select_saga(log_file)
        if not selected_saga:
            if handle_graceful_quit(log_file):
                return
        
        # Set the selected saga as the active story arc
        global active_story_arc, arc_progress
        active_story_arc = selected_saga
        arc_progress = 0
        
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
        
        # Initialize Billion Dollar Game Controller
        billion_dollar_controller = initialize_billion_dollar_controller(character)
        
        if billion_dollar_controller:
            # Start session with full context integration
            session_start = billion_dollar_controller.start_new_session()
            
            # Enhanced session start message
            session_msg = f"\n🎆 BILLION DOLLAR FEATURES ACTIVE:\n✅ Enhanced Context Management\n✅ Session Hooks & Cliffhangers\n✅ Progressive Character Investment\n✅ Integrated Story Systems\n\n📊 Session Context: {session_start['session_context']['session_number']} | Investment Score: {session_start['character_investment'].get('investment_score', 0):.2f}"
            log_to_file(log_file, session_msg)
            
            # Show session preview
            if session_start.get('session_preview'):
                preview_msg = f"\n🔮 Session Preview: {session_start['session_preview']}"
                log_to_file(log_file, preview_msg)
            
            # Show active hooks if any
            if session_start['active_hooks']['active_hooks']:
                hooks_msg = "\n🪝 ACTIVE STORY HOOKS:"
                for hook in session_start['active_hooks']['active_hooks'][:2]:
                    hooks_msg += f"\n• {hook['hook_text']}"
                    if hook['time_pressure']:
                        hooks_msg += " ⏰ URGENT"
                log_to_file(log_file, hooks_msg)
        
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
                # Process through billion dollar controller if available
                if billion_dollar_controller:
                    # Get enhanced AI context
                    enhanced_context = billion_dollar_controller._generate_comprehensive_ai_context()
                    
                    # TODO: Integrate enhanced context into AI layer properly
                    # For now, process action normally
                    result = ai_layer.process_player_action(player_input)
                    
                    # Process through billion dollar systems
                    bd_result = billion_dollar_controller.process_player_action(player_input, result.get('narrative', ''))
                    
                    # Show progression notifications
                    if bd_result.get('character_investment', {}).get('progressions_unlocked'):
                        progression_msg = "\n🎆 CHARACTER PROGRESSION UNLOCKED!"
                        for progression in bd_result['character_investment']['progressions_unlocked']:
                            progression_msg += f"\n✨ {progression['reward_description']}"
                            progression_msg += f"\n💭 {progression['emotional_impact']}"
                        log_to_file(log_file, progression_msg)
                    
                    # Show discovery notifications
                    if bd_result.get('discoveries'):
                        for discovery in bd_result['discoveries']:
                            if discovery.get('progression'):
                                discovery_msg = f"\n🔍 DISCOVERY MADE! Rarity: {'★' * discovery['rarity']}"
                                log_to_file(log_file, discovery_msg)
                    
                    # Check for forced progression if needed
                    force_check = billion_dollar_controller.force_progression_if_needed()
                    if force_check['progression_forced']:
                        force_msg = f"\n🚀 STORY PROGRESSION: {force_check['reason']}"
                        log_to_file(log_file, force_msg)
                else:
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
        
        # End session with billion dollar controller
        if billion_dollar_controller:
            session_end = billion_dollar_controller.end_session("max_turns_reached")
            
            # Show session end hook
            if session_end.get('session_hook'):
                hook_data = session_end['session_hook']
                hook_msg = f"\n🪝 SESSION END HOOK ({hook_data['intensity']}):\n{hook_data['hook_text']}\n\n🔮 {hook_data['next_session_preview']}\n💭 {hook_data['emotional_stakes']}"
                log_to_file(log_file, hook_msg)
            
            # Show retention metrics
            if session_end.get('retention_metrics'):
                metrics = session_end['retention_metrics']
                metrics_msg = f"\n📊 SESSION METRICS:\n• Overall Retention Score: {metrics['overall_retention_score']:.2f}/1.0\n• Character Investment: {metrics['character_investment_score']:.2f}/1.0\n• Context Richness: {metrics['context_richness_score']:.2f}/1.0\n• Hook Strength: {metrics['hook_strength_score']:.2f}/1.0"
                log_to_file(log_file, metrics_msg)
            
            # Show return motivation
            if session_end.get('return_motivation'):
                motivation = session_end['return_motivation']
                motivation_msg = f"\n🎯 RETURN MOTIVATION ({motivation['return_urgency'].upper()}):\n{motivation['anticipation_message']}"
                if motivation['motivation_factors']:
                    motivation_msg += "\n\nReasons to return:"
                    for factor in motivation['motivation_factors']:
                        motivation_msg += f"\n• {factor}"
                log_to_file(log_file, motivation_msg)
            
            # Show character progression preview
            if session_end.get('character_progression_preview'):
                preview_msg = f"\n🎆 {session_end['character_progression_preview']}"
                log_to_file(log_file, preview_msg)
        
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