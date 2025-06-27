import json
from claude_haiku.claude_haiku_create_saga import create_saga_with_character
from dal.characters import get_character
from dal.user_data import get_user_record, put_user_record
from utils.game_manager import create_new_game
from utils.user_record_schema import add_to_active

def handler(event, context):
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