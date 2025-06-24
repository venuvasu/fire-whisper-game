import boto3
import json
import uuid
from claude_haiku.claude_haiku_create_character import create_character
from dal.user_data import get_user_record, put_user_record
from utils.user_record_schema import add_character

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    body = json.loads(event.get('body', '{}'))
    body_name = body.get('name')
    body_race = body.get('race')
    body_gender = body.get('gender')
    body_profession = body.get('profession')

    character_template = create_character(user_id, body_name, body_race, body_gender, body_profession, haiku_model="claude_haiku_35")

    character_dict = json.loads(character_template)
    character_id = str(uuid.uuid4())
    character_dict['character_id'] = character_id

    dynamodb = boto3.resource('dynamodb')

    # Get user data
    user_data = get_user_record(user_id)

    # Add new character to user data
    add_character(user_data, character_dict["IDENTITY"]["name"], character_dict["IDENTITY"]["profession"], character_id, character_dict["PROGRESSION"]["level"])

    # Write back to table
    put_user_record(user_data)

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
