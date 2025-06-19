import boto3
import json
from claude_haiku.claude_haiku_update_character import update_character

def handler(event, context):
    print("Received event:", event)

    user_id = event.get('user_id')
    character_id = event.get('character_id')
    game_id = event.get("game_id")

    # update character sheet from game record
    character_template = update_character(user_id, game_id, character_id, "claude_haiku_35")
    character_dict = json.loads(character_template)

    # Retrieve user data from DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('FW_UserData_Dev')
    user_data_response = user_table.get_item(Key={'user_id': user_id})
    user_record = user_data_response['Item']
    
    print("user_record:", user_record)

    character_profile = None
    for character in user_record.get('characters', []):
        print("character:", character)
        if character.get('completed_games') and game_id in character['completed_games']:
            character_profile = character

    print("character_profile:", character_profile)

    if character_profile is None:
        raise ValueError("No character_profile found")

    character_profile['level'] = character_dict["PROGRESSION"]["level"]

    for idx, character in enumerate(user_record.get('characters', [])):
        if character.get('character_id') == character_profile.get('character_id'):
            user_record['characters'][idx] = character_profile
            break

    # Update game in dynamo db
    user_table.put_item(Item=user_record)
    characters_table = dynamodb.Table('FW_Characters_Dev')
    characters_table.put_item(Item=character_dict)