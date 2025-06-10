import json
from game_manager import get_game_by_id, append_message_to_game, update_game_messages
from mistral.mistral import take_turn as take_turn_mistral
from claude_haiku_35 import take_turn as take_turn_claude_haiku
from claude_haiku_30 import take_turn as take_turn_claude_haiku_30

model_type = "claude_haiku_35"

def handler(event, context):
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
        text = take_turn_claude_haiku(game_record, message)
    elif(model_type == "claude_haiku_30"):
        text = take_turn_claude_haiku_30(game_record, message)

    # Append the AI response to the game record and update dynamodb
    game_record = append_message_to_game(game_record, text)
    update_game_messages(game_id, game_record['messages'])

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }