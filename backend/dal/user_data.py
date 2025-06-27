import boto3

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('FW_UserData_Dev')

def get_user_record(user_id):
    response = user_table.get_item(Key={'user_id': user_id})
    user_record = response.get('Item', {})
    return user_record

def put_user_record(user_record):
    user_table.put_item(Item=user_record)