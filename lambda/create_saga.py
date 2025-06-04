import boto3
import json
from game_manager import create_new_game
from claude_haiku_30 import create_saga_with_character as create_saga_with_character_haiku_30

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    # Get parameters from the event body
    body = json.loads(event.get("body", "{}"))
    character_id = body.get("characterId")
    print("character_id:", character_id)
    setting = body.get("setting")
    difficulty = body.get("difficulty")
    length = body.get("length")

    # Retrieve character dict from FW_Characters_Dev table
    dynamodb = boto3.resource('dynamodb')
    characters_table = dynamodb.Table('FW_Characters_Dev')
    response = characters_table.get_item(Key={'character_id': character_id})
    character_dict = response.get('Item')
    print("character_dict:", repr(character_dict))
    
    start_response = create_saga_with_character_haiku_30(character_dict, setting, difficulty, length)
    prompt = start_response['prompt']
    response = start_response['response']

    # Generate a new game record and attach to user
    game_record = create_new_game(user_id, prompt, response)

    # Safely get user data
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('FW_UserData_Dev')
    response = user_table.get_item(Key={'user_id': user_id})
    user_data = response.get('Item', {})

    # Append to existing characters active_games or create new list
    characters = user_data.get('characters', [])

    # Find and update the correct character's active_games
    for char in characters:
        if char.get('character_id') == character_id:
            if 'active_games' not in char:
                char['active_games'] = []
            char['active_games'].append(game_record["game_id"])
            break

    # Rebuild full item
    user_data['user_id'] = user_id
    user_data['characters'] = characters

    # Write back to table
    user_table.put_item(Item=user_data)

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }