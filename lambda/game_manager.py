import boto3
import uuid
from game_record_schema import build_chat_record
from user_record_schema import build_user_record
from claude_haiku_30 import name_game

def create_new_game(user_id, prompt, text):
    unique_game_id = str(uuid.uuid4())

    game_name = name_game(prompt)
    print(f"Game name: {game_name}")

    game_record = build_chat_record(unique_game_id, game_name, prompt, [prompt, text])
    print(f"Game record: {game_record}")

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TavernGames_Dev')
    table.put_item(Item=game_record)

    user_table = dynamodb.Table('FW_UserData_Dev')
    user_data = user_table.get_item(Key={'user_id': user_id})

    if 'Item' not in user_data:
        new_user_data = build_user_record(user_id, [{"id":unique_game_id, "name":game_name}])
        user_table.put_item(Item=new_user_data)
    else:
        games = user_data['Item'].get('active_games', [])
        games.append({"id":unique_game_id, "name":game_name})
        user_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression="SET active_games = :g",
            ExpressionAttributeValues={':g': games}
        )

    return game_record

def get_game_by_id(game_id):
    # Retrieve the game record from DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TavernGames_Dev')
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

def update_game_messages(game_id, messages):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TavernGames_Dev')

    table.update_item(
        Key={'game_id': game_id},
        UpdateExpression="SET messages = :m",
        ExpressionAttributeValues={':m': messages}
    )