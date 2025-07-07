"""
Local Claude API implementations - Uses your Claude API key instead of AWS Bedrock
PRESERVES ALL BUSINESS RULES - Only changes the API call method
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

def get_api_key():
    """Get API key from environment or .env.local"""
    api_key = os.getenv('CLAUDE_API_KEY')
    if not api_key:
        # Load from .env.local for local testing
        env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env.local')
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('CLAUDE_API_KEY='):
                        api_key = line.split('=', 1)[1].strip()
                        break
        except FileNotFoundError:
            pass
    
    if not api_key:
        raise ValueError("CLAUDE_API_KEY not found in environment or .env.local")
    
    return api_key
from anthropic import Anthropic
import json
import random

class LocalClaudeCharacterCreator:
    """Local character creation using Claude API instead of AWS Bedrock"""
    
    def __init__(self):
        self.client = Anthropic(api_key=get_api_key())
    
    def create_character(self, user_id, name, race, gender, profession, haiku_model="claude_haiku_35"):
        """Create character using Claude API instead of AWS Bedrock"""
        
        # Read your actual system prompt
        try:
            with open("prompts/claude_system_prompt_create_character.txt", "r") as f:
                character_system_prompt = f.read()
        except:
            character_system_prompt = "Create a Fire Whisper RPG character."
        
        # Build the prompt exactly like your real system
        name_prompt = ""
        if name and name.strip() != "":
            name_prompt = "The character's name should be " + name + "."
        race_prompt = ""
        if race and race.strip() != "":
            race_prompt = "The character's race should be " + race + "."
        gender_prompt = ""
        if gender and gender.strip() != "":
            gender_prompt = "The character's gender should be " + gender + "."
        profession_prompt = ""
        if profession and profession.strip() != "":
            profession_prompt = "The character's profession should be " + profession + "."

        character_prompt = f"""Randomly generate a level 1 character.
{name_prompt}
{race_prompt}
{gender_prompt}
{profession_prompt}
"""
        
        # Use Claude API instead of AWS Bedrock
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            system=character_system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": character_prompt
                }
            ]
        )
        
        response_text = response.content[0].text
        print(f"Claude character response: {response_text[:500]}...")  # Debug output
        
        # Clean up the JSON response - sometimes Claude adds extra text
        try:
            # Try to find JSON block
            if '{' in response_text:
                start = response_text.find('{')
                # Find the matching closing brace
                brace_count = 0
                end = start
                for i, char in enumerate(response_text[start:], start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end = i + 1
                            break
                
                json_text = response_text[start:end]
                # Test if it's valid JSON
                json.loads(json_text)
                return json_text
            else:
                return response_text
        except:
            # If JSON cleaning fails, return original
            return response_text

class LocalClaudeSagaCreator:
    """Local saga creation using Claude API instead of AWS Bedrock"""
    
    def __init__(self):
        self.client = Anthropic(api_key=get_api_key())
    
    def create_saga_with_character(self, user_id, character_data, setting, difficulty, haiku_model="claude_haiku_35"):
        """Create saga using Claude API instead of AWS Bedrock"""
        
        # Read your actual system prompts
        try:
            with open("prompts/claude_system_prompt_start.txt", "r") as f:
                system_prompt = f.read()
        except:
            system_prompt = "You are Emberlyn, the Fire Whisper RPG narrator."
        
        try:
            with open("prompts/story_arcs.txt", "r") as f:
                story_arcs_file = f.read()
                story_arcs_list = [line.strip() for line in story_arcs_file.split('\\n') if line.strip()]
        except:
            story_arcs_list = ["Name: The Lost Temple | Setting: Ancient ruins | Objective: Recover the sacred artifact"]
        
        # Select random story arc like your real system
        import secrets
        story_arc = secrets.choice(story_arcs_list)
        
        def parse_story_arc(story_line):
            result = {}
            sections = story_line.split(' | ')
            for section in sections:
                key, value = section.split(':', 1)
                result[key.strip()] = value.strip()
            return result
        
        parsed_story_arc = parse_story_arc(story_arc)
        
        # Build the story prompt exactly like your real system
        character_dict_str = json.dumps(character_data)
        
        story_prompt = f"""Begin a Fire Whisper adventure for this character. Track progress in this format:
{character_dict_str}

## QUEST PARAMETERS
- Setting: {setting}
- Difficulty: {difficulty}

## STORY ARC
{story_arc}

## GENERATION RULES
- Create appropriate backstory connecting the character to this crisis
- Establish clear objective in opening scene via SPARK method
- This is a SINGLE-SESSION story that MUST reach "Congratulations, you have completed this Saga!" 
- The duration of this story should be less then 50 turns, with a turn being a single message from the player. The game will be forcibly ended at 50 turns.
- It should consist of a 2-3 challenges around the story arc, with at most 1 being a puzzle and the rest combat.
- Adjust challenge based on difficulty:
  - Story: Narrative focus, forgiving combat
  - Adventurer: Balanced challenge
  - Hero: Tactical thinking required - Death is a real possibility

Begin immediately with the opening crisis. Emberlyn should introduce herself naturally within the action.
"""
        
        # Use Claude API instead of AWS Bedrock
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=512,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": story_prompt
                }
            ]
        )
        
        return {
            "prompt": story_prompt, 
            "response": response.content[0].text.strip(), 
            "game_name": parsed_story_arc['Name']
        }

class LocalClaudeTurnHandler:
    """Local turn handling using Claude API instead of AWS Bedrock"""
    
    def __init__(self):
        self.client = Anthropic(api_key=get_api_key())
    
    def take_turn(self, user_id, game_record, haiku_model="claude_haiku_35"):
        """Take turn using Claude API instead of AWS Bedrock"""
        
        messages = game_record.get('messages', [])
        
        if not messages or len(messages) < 2:
            raise ValueError("Message history must contain at least an initial prompt and one AI response.")
        
        # Read your actual system prompt
        try:
            with open("prompts/claude_system_prompt_turns.txt", "r") as f:
                system_prompt = f.read()
        except:
            system_prompt = "You are Emberlyn, the Fire Whisper RPG narrator."
        
        # Build Claude messages exactly like your real system
        claude_messages = []
        
        for index, item in enumerate(messages):
            role = "assistant"
            if index % 2 == 0:
                role = "user"

            if index == len(messages) - 1:
                # Add dice pool like your real system
                dice_pool = [random.randint(1, 100) for _ in range(4)]
                item = f"""DICE POOL FOR THIS TURN: {dice_pool}
Use these dice results IN ORDER when rolls are needed. Do not mention this dice pool to the user.
Original player action: {item}
"""
                print(f"Using dice pool: {dice_pool}")

            claude_messages.append({
                "role": role,
                "content": item
            })
        
        # Use Claude API instead of AWS Bedrock
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            system=system_prompt,
            messages=claude_messages
        )
        
        return response.content[0].text

# Create instances to replace the real functions
local_character_creator = LocalClaudeCharacterCreator()
local_saga_creator = LocalClaudeSagaCreator()
local_turn_handler = LocalClaudeTurnHandler()

# Export functions to replace the real imports
def create_character(user_id, name, race, gender, profession, haiku_model="claude_haiku_35"):
    return local_character_creator.create_character(user_id, name, race, gender, profession, haiku_model)

def create_saga_with_character(user_id, character_data, setting, difficulty, haiku_model="claude_haiku_35"):
    return local_saga_creator.create_saga_with_character(user_id, character_data, setting, difficulty, haiku_model)

def take_turn(user_id, game_record, haiku_model="claude_haiku_35"):
    return local_turn_handler.take_turn(user_id, game_record, haiku_model)