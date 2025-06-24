import boto3
import json
from utils.game_manager import create_new_game
from claude_haiku.claude_haiku_create_saga import create_saga_with_character
from utils.user_record_schema import add_to_active

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    # Get parameters from the event body
    body = json.loads(event.get("body", "{}"))
    character_id = body.get("characterId")
    setting = body.get("setting")
    difficulty = body.get("difficulty")

    # Retrieve character dict from FW_Characters_Dev table
    dynamodb = boto3.resource('dynamodb')
    characters_table = dynamodb.Table('FW_Characters_Dev')
    response = characters_table.get_item(Key={'character_id': character_id})
    character_dict = response.get('Item')
    
    start_response = create_saga_with_character(user_id, character_dict, setting, difficulty, "claude_haiku_35")
    prompt = start_response['prompt']
    response = start_response['response']
    game_name = start_response['game_name']

    # Generate a new game record and attach to user
    game_record = create_new_game(user_id, prompt, response, game_name)

    # Safely get user data
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('FW_UserData_Dev')
    response = user_table.get_item(Key={'user_id': user_id})
    user_data = response.get('Item', {})

    # Append to existing characters active
    add_to_active(user_data, character_id, game_record["game_id"], game_name)

    # Write back to table
    user_table.put_item(Item=user_data)

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }