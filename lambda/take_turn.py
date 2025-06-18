import boto3
import decimal
import json
import os
from game_manager import get_game_by_id, append_message_to_game, update_game_messages
from mistral.mistral import take_turn as take_turn_mistral
from claude_haiku_35.claude_haiku_35 import take_turn as take_turn_claude_haiku
from claude_haiku_30.claude_haiku_30 import take_turn as take_turn_claude_haiku_30
from claude_haiku_30.claude_haiku_30 import update_character as update_character_haiku_30
from claude_haiku.claude_haiku_take_turn import take_turn

model_type = "claude_haiku_35"

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    # Get API parameters
    body = json.loads(event.get("body", "{}"))
    game_id = body.get("game_id")
    message = body.get("message")

    if not game_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing game_id"})
        }

    # Get game record by game_id
    game_record = get_game_by_id(game_id)
    if not game_record:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Game not found'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    # Append the new message to the game record
    game_record = append_message_to_game(game_record, message)

    # Take the turn using the Mistral model
    text = ""
    if(model_type == "mistral"):
        text = take_turn_mistral(game_record, message)
    elif(model_type == "amazon_titan"):
        text = "Take turn using Amazon Titan model is not implemented yet."
    elif(model_type == "claude_haiku_35"):
        text = take_turn(user_id, game_record, "claude_haiku_35")
    elif(model_type == "claude_haiku_30"):
        text = take_turn(user_id, game_record, "claude_haiku_30")

    # Append the AI response to the game record
    game_record = append_message_to_game(game_record, text)

    # Retrieve user data from DynamoDB
    dynamodb = boto3.resource('dynamodb')
    user_table = dynamodb.Table('FW_UserData_Dev')
    user_data_response = user_table.get_item(Key={'user_id': user_id})
    user_record = user_data_response['Item']
    
    character_profile = None
    for character in user_record.get('characters', []):
        if character.get('active_games') and character['active_games'][0] == game_id:
            character_profile = character

    if character_profile is None:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Character profile not found for this game'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    # Handle if this is the final turn in the game
    if "Congratulations, you have completed this Saga!" in text:
        print("Game completed, updating game record status.")
        # Mark game_record as no longer active
        game_record['game_active'] = False

        # Append game_id to completed_games
        if 'completed_games' not in character_profile or not isinstance(character_profile['completed_games'], list):
            character_profile['completed_games'] = []
        if game_id not in character_profile['completed_games']:
            character_profile['completed_games'].append(game_id)

        if 'active_games' in character_profile and isinstance(character_profile['active_games'], list):
            character_profile['active_games'] = [
                g for g in character_profile['active_games'] if g != game_id
            ]

        for idx, character in enumerate(user_record.get('characters', [])):
            if character.get('character_id') == character_profile.get('character_id'):
                user_record['characters'][idx] = character_profile
                break

        # Update game in dynamo db
        user_table.put_item(Item=user_record)

    # Update game in dynamo db
    if 'game_active' not in game_record:
        game_record['game_active'] = True
    update_game_messages(game_id, game_record['messages'], game_record['game_active'])

    game_record['character_profile'] = character_profile

    print(game_record)

    # Invoke an async update character if games completed
    if "Congratulations, you have completed this Saga!" in text:
        update_fn = os.environ["UPDATE_CHARACTER_ARN"]
        lambda_client = boto3.client("lambda")

        payload = {
            "user_id": user_id,
            "character_id": character_profile.get('character_id'),
            "game_id": game_id
        }

        lambda_client.invoke(
            FunctionName=update_fn,
            InvocationType="Event",
            Payload=json.dumps(payload)
        )

    return {
        'statusCode': 200,
        'body': json.dumps(game_record, default=decimal_default),
        'headers': {
            'Content-Type': 'application/json'
        }
    }