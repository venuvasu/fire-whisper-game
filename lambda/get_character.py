import boto3
import decimal
import json
from game_manager import get_games_for_character

def default_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    character_id = event.get("queryStringParameters", {}).get("character_id")

    dynamodb = boto3.resource('dynamodb')
    characters_table = dynamodb.Table('FW_Characters_Dev')

    # Retrieve character data by character_id
    response = characters_table.get_item(Key={'character_id': character_id})
    character_data = response.get('Item')

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