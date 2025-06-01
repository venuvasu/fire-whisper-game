import boto3
import decimal
import json
import os

def default_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('FW_UserData_Dev')
    user_data = user_table.get_item(Key={'user_id': user_id})

    return {
        'statusCode': 200,
        'body': json.dumps(user_data, default=default_serializer),
        'headers': {
            'Content-Type': 'application/json'
        }
    }