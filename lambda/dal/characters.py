import boto3

dynamodb = boto3.resource('dynamodb')
characters_table = dynamodb.Table('FW_Characters_Dev')

def get_character(character_id):
    response = characters_table.get_item(Key={'character_id': character_id})
    character_data = response.get('Item', {})
    return character_data

def put_character(character_record):
    characters_table.put_item(Item=character_record)