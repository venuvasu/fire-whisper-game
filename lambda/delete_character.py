import json
import boto3

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    character_id = None
    if event.get("queryStringParameters") and event["queryStringParameters"].get("character_id"):
        character_id = event["queryStringParameters"]["character_id"]

    if not character_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing character_id"})
        }
    
    # Get user data
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('FW_UserData_Dev')
    response = user_table.get_item(Key={'user_id': user_id})
    user_data = response.get('Item', {})
    characters = user_data.get('characters', [])

    for char in characters:
        if char.get('character_id') == character_id:
            characters.remove(char)
            break

    user_data['characters'] = characters

    # Write back to table
    user_table.put_item(Item=user_data)

    return {
        "statusCode": 200,
        "body": json.dumps({character_id: character_id})
    }
