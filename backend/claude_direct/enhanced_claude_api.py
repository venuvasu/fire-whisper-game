import json
import random
import os
from anthropic import Anthropic
import sys
sys.path.append('..')
from utils.character_sheet import CharacterSheet
from utils.dice_system import DiceRoll

# Initialize Anthropic client
client = Anthropic(api_key="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")

# Enhanced system prompt with character awareness
ENHANCED_SYSTEM_PROMPT = """You are Emberlyn, a wise fairy serving as the Dungeon Master for "Fire Whisper," a turn-based text RPG.

CRITICAL RULES - CHARACTER OWNERSHIP:
- ALWAYS show the player's character sheet when relevant
- ALWAYS explain how their stats affect dice rolls
- ALWAYS give players meaningful choices that use different stats/skills
- ALWAYS show XP gains immediately when earned
- ALWAYS acknowledge player specialization and build choices

DICE SYSTEM RULES:
- When a roll is needed, ALWAYS show: "Rolling [Stat] + [Skill]..."
- ALWAYS show the math: "12 + 3 (STR) + 2 (Combat) = 17 vs Target 15"
- ALWAYS explain why they succeeded/failed based on their character
- Use player stats to determine bonuses, not arbitrary numbers

XP AWARD RULES (MANDATORY):
- Combat victory: 25-50 XP
- Skill success: 10-25 XP  
- Quest milestone: 50-100 XP
- Creative solution: 15-30 XP
- ALWAYS announce: "You gain X XP! (Total: Y/Z to next level)"

PROGRESSION FEEDBACK:
- Show character growth: "Your Combat skill increases to 3!"
- Acknowledge specialization: "Your Warrior training pays off here"
- Hint at future abilities: "At level 3, you'll unlock Power Attack"

CHOICE PRESENTATION:
Present choices that highlight different character approaches:
[1] Use Strength + Combat to break through
[2] Use Dexterity + Stealth to sneak around  
[3] Use Charisma + Persuasion to negotiate
[4] Describe your own approach

NEVER assume player actions. ALWAYS wait for their choice.
Keep responses under 300 words but include character sheet updates.
Make every choice feel meaningful and tied to their character build.
"""

def take_turn_enhanced(user_id, game_record, model="claude-3-5-sonnet-20241022", character_data=None):
    """Enhanced turn system with character awareness"""
    
    messages = game_record.get('messages', [])
    if not messages or len(messages) < 2:
        raise ValueError("Message history must contain at least an initial prompt and one AI response.")
    
    # Initialize or load character
    character = CharacterSheet(character_data) if character_data else CharacterSheet()
    
    # Prepare messages with character context
    claude_messages = []
    
    for index, item in enumerate(messages):
        role = "assistant" if index % 2 == 1 else "user"
        
        # Add character sheet context to user messages
        if role == "user" and index == len(messages) - 1:
            # This is the latest user input - add character context
            dice_pool = [random.randint(1, 20) for _ in range(4)]
            
            enhanced_message = f"""CURRENT CHARACTER STATE:
{character.get_display_sheet()}

AVAILABLE DICE FOR THIS TURN: {dice_pool}
(Use these dice results IN ORDER when rolls are needed. Do not mention this dice pool to the user.)

PLAYER ACTION: {item}

Remember to:
1. Show how their stats affect any rolls needed
2. Award XP for successes and milestones  
3. Present choices that use different character abilities
4. Update character progression when appropriate
"""
            claude_messages.append({
                "role": role,
                "content": enhanced_message.strip()
            })
            print(f"Using dice pool: {dice_pool}")
        else:
            claude_messages.append({
                "role": role,
                "content": item.strip()
            })
    
    # Map model names
    model_mapping = {
        "claude_haiku_35": "claude-3-5-haiku-20241022",
        "claude_haiku_30": "claude-3-haiku-20240307", 
        "sonnet_35": "claude-3-5-sonnet-20241022",
        "sonnet_40": "claude-3-5-sonnet-20241022"
    }
    
    api_model = model_mapping.get(model, "claude-3-5-sonnet-20241022")
    
    try:
        response = client.messages.create(
            model=api_model,
            max_tokens=800,  # Increased for character sheet display
            system=ENHANCED_SYSTEM_PROMPT,
            messages=claude_messages
        )
        
        print(f"✅ Enhanced Claude API call - Model: {api_model}, Character: {character.name}")
        
        result = {
            'response': response.content[0].text,
            'character': character.to_dict(),
            'model_used': api_model
        }
        
        return result
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        raise e

def create_character_creation_prompt():
    """Create an engaging character creation experience"""
    return """🔥 **Welcome to Fire Whisper!** 🔥

You're about to embark on an epic adventure with Emberlyn, your fairy companion and guide. But first, let's create your character!

**Choose your class:**
[1] **Warrior** - Master of combat, high HP, bonus to Strength and Combat skills
[2] **Mage** - Wielder of magic, high Intelligence, bonus to Magic and Knowledge  
[3] **Rogue** - Master of stealth, high Dexterity, bonus to Stealth and Lockpicking
[4] **Cleric** - Divine healer, balanced stats, bonus to Healing and Persuasion

Each class gets unique abilities as you level up, and your choice will affect how you approach challenges throughout your adventure.

What class calls to you?"""

def process_character_creation(choice, name="Adventurer"):
    """Process character creation choice"""
    
    class_templates = {
        1: {  # Warrior
            'class': 'Warrior',
            'strength': 16,
            'dexterity': 12, 
            'intelligence': 10,
            'charisma': 12,
            'skills': {'Combat': 2, 'Intimidation': 1, 'Survival': 1},
            'description': 'A mighty warrior, skilled in combat and intimidation'
        },
        2: {  # Mage
            'class': 'Mage',
            'strength': 10,
            'dexterity': 12,
            'intelligence': 16, 
            'charisma': 12,
            'skills': {'Magic': 2, 'Knowledge': 2, 'Investigation': 1},
            'description': 'A learned spellcaster, master of arcane knowledge'
        },
        3: {  # Rogue
            'class': 'Rogue', 
            'strength': 12,
            'dexterity': 16,
            'intelligence': 12,
            'charisma': 10,
            'skills': {'Stealth': 2, 'Lockpicking': 2, 'Deception': 1},
            'description': 'A nimble infiltrator, master of stealth and trickery'
        },
        4: {  # Cleric
            'class': 'Cleric',
            'strength': 12,
            'dexterity': 10,
            'intelligence': 12,
            'charisma': 16,
            'skills': {'Healing': 2, 'Persuasion': 2, 'Knowledge': 1},
            'description': 'A divine healer, blessed with holy power'
        }
    }
    
    if choice in class_templates:
        template = class_templates[choice]
        template['name'] = name
        character = CharacterSheet(template)
        
        return {
            'character': character,
            'intro': f"""✨ **{character.name} the {character.class_name}** ✨

{template['description']}

{character.get_display_sheet()}

*A shimmering light appears before you, and Emberlyn the fairy materializes with a warm smile.*

"Greetings, {character.name}! I sense great potential in you. I'll be your companion and guide on this journey. Together, we'll face whatever challenges await!"

*She flutters around you excitedly.*

"Are you ready to begin your first adventure? I know of an ancient mystery that needs solving..."

What do you say to Emberlyn?
[1] "I'm ready! What's this mystery about?"
[2] "Tell me more about yourself first, Emberlyn."
[3] "I want to test my abilities before we start."
[4] Say something else to your new companion"""
        }
    
    return None