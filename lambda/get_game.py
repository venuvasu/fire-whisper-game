import boto3
import decimal
import json
from dal.user_data import get_user_record
from utils.user_record_schema import get_character_by_game_id

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        # Convert to int if possible, else float
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    #  Get game_id from query parameters
    game_id = event.get("queryStringParameters", {}).get("game_id")
    if not game_id:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Game ID is required'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    # Get User Record
    user_record = get_user_record(user_id)
    character_profile = get_character_by_game_id(user_record, game_id)

    print(f"Character profile for game {game_id}: {character_profile}")

    # Retrieve the game record from DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FW_Sagas_Dev')
    response = table.get_item(Key={'game_id': game_id})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Game not found'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    game_record = response['Item']
    game_record['character_profile'] = character_profile
    print(f"Game record: {game_record}")

    return {
        'statusCode': 200,
        'body': json.dumps(game_record, default=decimal_default),
        'headers': {
            'Content-Type': 'application/json'
        }
    }