"""
Game Management Handler  
Purpose: Handle game/saga creation and state management

Functions:
- create_saga: Create new game/saga with AI generation
- get_game: Retrieve game state and data
- update_game: Update game state
"""

import json
from ..ai.providers.claude_haiku_create_saga import create_saga_with_character
from ..data.characters import get_character
from ..data.user_data import get_user_record, put_user_record
from ..utils.game_manager import create_new_game
from ..utils.user_record_schema import add_to_active

def create_saga_handler(event, context):
    """
    Create new game/saga with AI-generated content
    Purpose: Initialize new game session for character
    """
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    # Get parameters from the event body
    body = json.loads(event.get("body", "{}"))
    character_id = body.get("characterId")
    setting = body.get("setting")
    difficulty = body.get("difficulty")
    
    character_dict = get_character(character_id)  # Ensure character exists

    start_response = create_saga_with_character(user_id, character_dict, setting, difficulty, "claude_haiku_35")
    prompt = start_response['prompt']
    response = start_response['response']
    game_name = start_response['game_name']

    # Generate a new game record and attach to user
    game_record = create_new_game(user_id, prompt, response, game_name)

    # Safely get user data
    user_data = get_user_record(user_id)

    # Append to existing characters active
    add_to_active(user_data, character_id, game_record["game_id"], game_name)

    # Write back to table
    put_user_record(user_data)

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def handler(event, context):
    """Main game handler - routes to appropriate function"""
    
    # Ensure character exists
    character_dict = get_character(character_id)
    if not character_dict:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Character not found'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Generate saga using AI
    start_response = create_saga_with_character(
        user_id, character_dict, setting, difficulty
    )
    
    prompt = start_response['prompt']
    response = start_response['response']
    game_name = start_response['game_name']

    # Generate a new game record and attach to user
    game_record = create_new_game(user_id, prompt, response, game_name)

    # Update user data with active game
    user_data = get_user_record(user_id)
    add_to_active(user_data, character_id, game_record["game_id"], game_name)
    put_user_record(user_data)

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def get_game_handler(event, context):
    """
    Retrieve game state and data
    Purpose: Get current game information for display or continuation
    """
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')
    
    game_id = event['pathParameters']['game_id']
    
    # Get game data (implementation depends on storage method)
    # This would typically retrieve from DynamoDB or similar
    game_data = get_game_data(game_id)
    
    if not game_data:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Game not found'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(game_data),
        'headers': {'Content-Type': 'application/json'}
    }

# Lambda handler exports
handler = create_saga_handler  # Default export for create_saga Lambda