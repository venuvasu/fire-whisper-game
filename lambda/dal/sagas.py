import boto3

dynamodb = boto3.resource('dynamodb')
sagas_table = dynamodb.Table('FW_Sagas_Dev')

def get_saga(game_id):
    response = sagas_table.get_item(Key={'game_id': game_id})
    saga_record = response.get('Item', {})
    return saga_record