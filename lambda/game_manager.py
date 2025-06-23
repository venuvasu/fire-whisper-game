import boto3
import uuid
from game_record_schema import build_chat_record
from user_record_schema import build_user_record
from claude_haiku_30.claude_haiku_30 import name_game

def create_new_game(user_id, prompt, text, game_name):
    unique_game_id = str(uuid.uuid4())

    game_record = build_chat_record(unique_game_id, game_name, [prompt, text])
    print(f"Game record: {game_record}")

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FW_Sagas_Dev')
    table.put_item(Item=game_record)

    return game_record

def get_game_by_id(game_id):
    # Retrieve the game record from DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FW_Sagas_Dev')
    response = table.get_item(Key={'game_id': game_id})

    if 'Item' not in response:
        return None

    game_record = response['Item']
    return game_record

def append_message_to_game(game_record, message):
    messages = game_record.get('messages', [])
    messages.append(message)
    game_record['messages'] = messages
    return game_record

def update_game_messages(game_id, messages, game_active=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FW_Sagas_Dev')

    update_expr = "SET messages = :m"
    expr_attrs = {':m': messages}

    if game_active is not None:
        update_expr += ", game_active = :g"
        expr_attrs[':g'] = game_active

    table.update_item(
        Key={'game_id': game_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attrs
    )

def get_game_summary(game_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName="FW_Sagas_Dev",
        Key={'game_id': {'S': game_id}},
        ProjectionExpression='game_name, messages'
    )
    item = response.get('Item')
    if not item:
        return {
            'game_id': game_id,
            'game_name': None,
            'message_count': 0
        }
    
    game_name = item.get('game_name', {}).get('S', '')
    message_count = len(item.get('messages', {}).get('L', []))

    return {
        'game_id': game_id,
        'game_name': game_name,
        'message_count': message_count
    }


def get_games_for_character(user_id, target_character_id):
    dynamodb = boto3.client('dynamodb')
    response = dynamodb.get_item(
        TableName='FW_UserData_Dev',
        Key={'user_id': {'S': user_id}}
    )
    
    item = response.get('Item')
    if not item:
        return None

    characters = item.get('characters', {}).get('L', [])
    
    game_object = {
        'character_id': target_character_id,
        'active_games': [],
        'completed_games': []
    }
    for char_entry in characters:
        char = char_entry.get('M', {})
        char_id = char.get('character_id', {}).get('S')
        if char_id == target_character_id:
            active_games = [g['S'] for g in char.get('active_games', {}).get('L', [])]
            completed_games = [g['S'] for g in char.get('completed_games', {}).get('L', [])]
            game_object = {
                'character_id': char_id,
                'active_games': active_games,
                'completed_games': completed_games
            }

    hydrated_games = {
        'character_id': game_object['character_id'],
        'active_games': [],
        'completed_games': []
    }

    for game_id in game_object.get('active_games', []):
        hydrated_games['active_games'].append(get_game_summary(game_id))

    for game_id in game_object.get('completed_games', []):
        hydrated_games['completed_games'].append(get_game_summary(game_id))

    game_object = hydrated_games

    return game_object