import json
import random
import os
from anthropic import Anthropic
from utils.character_sheet import CharacterSheet
from utils.dice_system import DiceRoll, create_roll_choice_prompt

# Initialize Anthropic client with your API key
client = Anthropic(api_key="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")

# Load system prompt
try:
    with open("backend/prompts/claude_system_prompt_turns.txt", "r") as f:
        system_prompt = f.read()
except FileNotFoundError:
    # Fallback system prompt for testing
    system_prompt = """You are Emberlyn, a wise fairy serving as the Dungeon Master for "Fire Whisper," a turn-based text RPG.
    
Your job is to help the player play the roleplaying game and act as referee, narrator and storyteller.

CORE RULES:
- NEVER assume player actions or use phrases like "You decide to..."
- Wait for player input before advancing the story
- Keep responses under 200 tokens, ending with complete sentences
- Present 1-2 paragraph scenes ending with choices

Present scenes ending with:
What do you do?
[Action one]
[Action two]
[Action three]
[Describe your own action]"""

def take_turn_direct(user_id, game_record, model="claude-3-5-sonnet-20241022", character_data=None):
    """
    Take a turn using direct Claude API instead of AWS Bedrock
    """
    messages = game_record.get('messages', [])
    
    if not messages or len(messages) < 2:
        raise ValueError("Message history must contain at least an initial prompt and one AI response.")

    claude_messages = []

    for index, item in enumerate(messages):
        role = "assistant"
        if index % 2 == 0:
            role = "user"

        if index == len(messages) - 1:
            dice_pool = [random.randint(1, 100) for _ in range(4)]
            item = f"""DICE POOL FOR THIS TURN: {dice_pool}
Use these dice results IN ORDER when rolls are needed. Do not mention this dice pool to the user.
Original player action: {item}
"""
            print(f"Using dice pool: {dice_pool}")

        claude_messages.append({
            "role": role,
            "content": item.strip()
        })

    # Map model names to Claude API model IDs
    model_mapping = {
        "claude_haiku_35": "claude-3-5-haiku-20241022",
        "claude_haiku_30": "claude-3-haiku-20240307",
        "sonnet_35": "claude-3-5-sonnet-20241022",
        "sonnet_40": "claude-3-5-sonnet-20241022",  # Using 3.5 as 4.0 not available via API yet
        "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
        "claude-3-haiku-20240307": "claude-3-haiku-20240307"
    }
    
    api_model = model_mapping.get(model, "claude-3-5-sonnet-20241022")
    
    try:
        response = client.messages.create(
            model=api_model,
            max_tokens=512,
            system=system_prompt,
            messages=claude_messages
        )
        
        # Log usage for local testing
        print(f"✅ Claude API call successful - Model: {api_model}, User: {user_id}")
        
        return response.content[0].text
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        raise e

def list_available_models():
    """List available Claude models via direct API"""
    return [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022", 
        "claude-3-haiku-20240307"
    ]