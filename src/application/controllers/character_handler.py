"""
Character Management Handler
Purpose: Handle all character CRUD operations for Fire Whisper RPG

Functions:
- create_character: Create new character with AI generation
- get_character: Retrieve character data
- update_character: Update character from game progression
- delete_character: Remove character
"""

import json
import uuid
import decimal
from ...infrastructure.ai.claude.providers.claude_haiku_create_character import create_character as create_character_with_ai
from ...infrastructure.persistence.characters import create_character, get_character
from ...infrastructure.persistence.user_data import get_user_record, put_user_record
from ...shared.utils.user_record_schema import add_character_to_user
from ...shared.utils.game_manager import get_games_for_character

def default_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def create_character_handler(event, context):
    """Create a new character with AI generation"""
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    body = json.loads(event.get('body', '{}'))
    body_name = body.get('name')
    body_race = body.get('race')
    body_gender = body.get('gender')
    body_profession = body.get('profession')

    character_template = create_character_with_ai(user_id, body_name, body_race, body_gender, body_profession, haiku_model="claude_haiku_35")

    character_dict = json.loads(character_template)
    character_id = str(uuid.uuid4())
    character_dict['character_id'] = character_id

    # Get user data
    user_data = get_user_record(user_id)

    # Ensure user_id is present in user_data
    user_data["user_id"] = user_id

    # Add new character to user data
    add_character_to_user(user_data, character_dict["IDENTITY"]["name"], character_dict["IDENTITY"]["profession"], character_id, character_dict["PROGRESSION"]["level"])

    # Write back to table
    put_user_record(user_data)

    # Write character to the characters table
    create_character(character_dict)

    return {
        'statusCode': 200,
        'body': json.dumps(character_dict),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def handler(event, context):
    """
    Main character handler - routes to appropriate function
    Create new character with AI-generated attributes
    Purpose: Handle character creation requests from frontend
    """
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    body = json.loads(event.get('body', '{}'))
    body_name = body.get('name')
    body_race = body.get('race')
    body_gender = body.get('gender')
    body_profession = body.get('profession')

    # Generate character using AI
    character_template = create_character_with_ai(
        user_id, body_name, body_race, body_gender, body_profession
    )

    character_dict = json.loads(character_template)
    character_id = str(uuid.uuid4())
    character_dict['character_id'] = character_id

    # Get user data
    user_data = get_user_record(user_id)
    user_data["user_id"] = user_id

    # Add new character to user data
    add_character(
        user_data, 
        character_dict["IDENTITY"]["name"], 
        character_dict["IDENTITY"]["profession"], 
        character_id, 
        character_dict["PROGRESSION"]["level"]
    )

    # Write back to tables
    put_user_record(user_data)
    put_character(character_dict)

    return {
        'statusCode': 200,
        'body': json.dumps(character_dict),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def get_character_handler(event, context):
    """
    Retrieve character data
    Purpose: Get character information for display or gameplay
    """
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')
    
    character_id = event['pathParameters']['character_id']
    character_data = get_character_data(character_id)
    
    if not character_data:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Character not found'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(character_data),
        'headers': {'Content-Type': 'application/json'}
    }

def delete_character_handler(event, context):
    """
    Delete character
    Purpose: Remove character from user's collection
    """
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')
    
    character_id = event['pathParameters']['character_id']
    
    # Remove from user data
    user_data = get_user_record(user_id)
    remove_character(user_data, character_id)
    put_user_record(user_data)
    
    # Remove character data
    delete_character_data(character_id)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Character deleted successfully'}),
        'headers': {'Content-Type': 'application/json'}
    }

# Lambda handler exports
handler = create_character_handler  # Default export for create_character Lambda

def get_character_handler_v2(event, context):
    """Get character by ID with associated games"""
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    character_id = event.get("queryStringParameters", {}).get("character_id")

    # Retrieve character data by character_id
    character_data = get_character(character_id)

    if not character_data:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Character not found'}),
            'headers': {'Content-Type': 'application/json'}
        }

    games_object = get_games_for_character(user_id, character_id)
    if not games_object:
        games_object = {"active_games": [], "completed_games": []}

    character_data["active_games"] = games_object["active_games"]
    character_data["completed_games"] = games_object["completed_games"]

    return {
        'statusCode': 200,
        'body': json.dumps(character_data, default=default_serializer),
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def delete_character_handler(event, context):
    """Delete character by ID"""
    # Implementation will be moved from backend/delete_character.py
    pass