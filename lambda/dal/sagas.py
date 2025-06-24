import boto3

dynamodb = boto3.resource('dynamodb')
sagas_table = dynamodb.Table('FW_Sagas_Dev')

def get_saga(game_id):
    response = sagas_table.get_item(Key={'game_id': game_id})
    saga_record = response.get('Item', {})
    return saga_record

def put_saga(saga_record):
    sagas_table.put_item(Item=saga_record)

def update_saga(game_id, messages, game_active=None):
    update_expr = "SET messages = :m"
    expr_attrs = {':m': messages}

    if game_active is not None:
        update_expr += ", game_active = :g"
        expr_attrs[':g'] = game_active

    sagas_table.update_item(
        Key={'game_id': game_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attrs
    )