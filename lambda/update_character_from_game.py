import boto3
import json
from claude_haiku.claude_haiku_update_character import update_character
from utils.user_record_schema import get_character_by_game_id, update_character_level

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
    character_profile = get_character_by_game_id(user_record, game_id)
    print("character_profile:", character_profile)

    user_record = update_character_level(user_record, character_id, character_dict["PROGRESSION"]["level"])

    # Update game in dynamo db
    user_table.put_item(Item=user_record)
    characters_table = dynamodb.Table('FW_Characters_Dev')
    characters_table.put_item(Item=character_dict)