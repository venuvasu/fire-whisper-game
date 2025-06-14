import boto3
import json
import uuid

from claude_haiku_30 import create_character as create_character_haiku_30

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    body = json.loads(event.get('body', '{}'))
    body_name = body.get('name')
    body_gender = body.get('gender')
    body_profession = body.get('profession')

    character_template = create_character_haiku_30(user_id, body_name, body_gender, body_profession)
    print(f"Generated character template: {character_template}")
    character_dict = json.loads(character_template)

    character_id = str(uuid.uuid4())
    character_dict['character_id'] = character_id

    profile_character = {
        'character_id': character_id,
        'name': character_dict["IDENTITY"]["name"],
        'level': character_dict["PROGRESSION"]["level"],
        'profession': character_dict["IDENTITY"]["profession"],
        'active_games': [],
        'completed_games': []
    }

    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('FW_UserData_Dev')

    # Safely get user data
    response = user_table.get_item(Key={'user_id': user_id})
    user_data = response.get('Item', {})

    # Append to existing characters or create new list
    characters = user_data.get('characters', [])
    characters.append(profile_character)

    # Rebuild full item
    user_data['user_id'] = user_id
    user_data['characters'] = characters

    # Write back to table
    user_table.put_item(Item=user_data)

    # Write character to the characters table
    characters_table = dynamodb.Table('FW_Characters_Dev')
    characters_table.put_item(Item=character_dict)

    return {
        'statusCode': 200,
        'body': json.dumps(character_dict),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
