import json
from mistral import start_game as start_game_mistral
from amazon_titan import start_game as start_game_amazon_titan
from claude_haiku_35 import start_game as start_game_claude_haiku
from claude_haiku_30 import start_game as start_game_claude_haiku_30
from game_manager import create_new_game

model_type = "claude_haiku_30"

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')


    # Parse all fields from the request body
    body = event.get("body", "{}")
    try:
        body_json = json.loads(body)
    except Exception:
        body_json = {}

    print("Body JSON:", body_json)

    # Start the game
    prompt = ""
    if(model_type == "mistral"):
        mistral_response = start_game_mistral()
        prompt = mistral_response['prompt']
        response = mistral_response['response']
    elif(model_type == "amazon_titan"):
        amazon_titan_response = start_game_amazon_titan()
        prompt = amazon_titan_response['prompt']
        response = amazon_titan_response['response']
    elif(model_type == "claude_haiku_35"):
        claude_haiku_35_response = start_game_claude_haiku()
        prompt = claude_haiku_35_response['prompt']
        response = claude_haiku_35_response['response']
    elif(model_type == "claude_haiku_30"):
        claude_haiku_35_response = start_game_claude_haiku_30(body_json)
        prompt = claude_haiku_35_response['prompt']
        response = claude_haiku_35_response['response']

    # Generate a new game record and attach to user
    game_record = create_new_game(user_id, prompt, response)

    return {
        'statusCode': 200,
        'body': json.dumps(game_record),
        'headers': {
            'Content-Type': 'application/json'
        }
    }