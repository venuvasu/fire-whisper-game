import boto3
import json
import uuid

from claude_haiku_30 import update_character as update_character_haiku_30

def handler(event, context):
    body = json.loads(event.get('body', '{}'))
    game_id = body.get('game_id')
    character_id = body.get('character_id')

    character_template = update_character_haiku_30(game_id, character_id)
    print(f"Generated character template: {character_template}")
    character_dict = json.loads(character_template)

    return {
        'statusCode': 200,
        'body': json.dumps(character_dict),
        'headers': {
            'Content-Type': 'application/json'
        }
    }