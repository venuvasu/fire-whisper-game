import boto3
import decimal
import json
from amplitude.amplitude_handler import send_bedrock_amplitude_event

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

with open("prompts/claude_system_prompt_turns.txt", "r") as f:
    system_prompt = f.read()

def name_game(initial_prompt):
    # invoke model with prompt
    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    name_system_prompt = f"""You are an AI game-naming assistant.

Only reply with a game name that is:
- No more than 40 characters long
- Returned as plain text only, with no explanation or formatting
- The name should have capitalization and punctuation as appropriate for a title

Example format (don't use this name, it's just an example):
Shadow of the Ember Queen"""
    
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": name_system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": initial_prompt
                        }
                    ]
                }
            ],
            "max_tokens": 64
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return text.strip()