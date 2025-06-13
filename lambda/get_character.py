import boto3
import decimal
import json

def default_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    character_id = event.get("queryStringParameters", {}).get("character_id")
    print(f"Character ID: {character_id}")

    dynamodb = boto3.resource('dynamodb')
    characters_table = dynamodb.Table('FW_Characters_Dev')

    # Retrieve character data by character_id
    response = characters_table.get_item(Key={'character_id': character_id})
    character_data = response.get('Item')

    return {
        'statusCode': 200,
        'body': json.dumps(character_data, default=default_serializer),
        'headers': {
            'Content-Type': 'application/json'
        }
    }