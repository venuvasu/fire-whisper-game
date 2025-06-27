import json
from dal.user_data import get_user_record, put_user_record

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
    user_data = get_user_record(user_id)
    characters = user_data.get('characters', [])

    for char in characters:
        if char.get('character_id') == character_id:
            characters.remove(char)
            break

    user_data['characters'] = characters

    # Write back to table
    put_user_record(user_data)


    return {
        "statusCode": 200,
        "body": json.dumps({character_id: character_id})
    }
