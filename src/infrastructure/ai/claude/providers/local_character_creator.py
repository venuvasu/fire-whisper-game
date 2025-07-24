"""
Local Character Creator - Uses direct Anthropic API instead of AWS Bedrock
For local development and testing
Identical business logic to claude_haiku_create_character.py
"""
import json
import os
from pathlib import Path
from anthropic import Anthropic

# Analytics fallback for local development
try:
    from amplitude.amplitude_handler import send_bedrock_amplitude_event
except ImportError:
    def send_bedrock_amplitude_event(*args, **kwargs):
        print(f"📊 Analytics Event: {args[1] if len(args) > 1 else 'unknown'}")
        pass

# Fix file path for console
prompt_dir = Path(__file__).parent.parent / "prompts"
prompt_file = prompt_dir / "claude_system_prompt_create_character.txt"

with open(prompt_file, "r") as f:
    character_system_prompt = f.read()

def create_character_console(user_id, name, race, gender, profession, haiku_model="claude_haiku_35"):
    """IDENTICAL business logic to Bedrock version, only AI calling mechanism differs"""
    
    # IDENTICAL prompt building logic
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
    
    # DIFFERENT: Use direct Anthropic API instead of Bedrock
    api_key = os.getenv('CLAUDE_API_KEY')
    if not api_key:
        raise ValueError("CLAUDE_API_KEY not found")
    
    client = Anthropic(api_key=api_key)
    
    # Map model names
    anthropic_model = "claude-3-haiku-20240307"
    if haiku_model == "claude_haiku_35":
        anthropic_model = "claude-3-5-haiku-20241022"
    
    response = client.messages.create(
        model=anthropic_model,
        max_tokens=3072,
        system=character_system_prompt,
        messages=[
            {
                "role": "user",
                "content": character_prompt
            }
        ]
    )
    
    # IDENTICAL analytics call
    send_bedrock_amplitude_event(user_id, "create_character", haiku_model, response)
    
    # IDENTICAL response processing
    text = response.content[0].text
    return text.strip()