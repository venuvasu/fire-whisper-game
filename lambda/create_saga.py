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
    
    start_response = create_saga_with_character_haiku_30(character_dict)
    prompt = start_response['prompt']
    response = start_response['response']

    # Generate a new game record and attach to user
    # TODO - update this to use saga creation logic
    game_record = create_new_game(user_id, prompt, response)

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }