import boto3

import json
from amplitude.amplitude_handler import send_bedrock_amplitude_event

with open("prompts/claude_system_prompt_turns.txt", "r") as f:
    system_prompt = f.read()

def take_turn(user_id, game_record, haiku_model="claude_haiku_30"):
    messages = game_record.get('messages', [])
    
    if not messages or len(messages) < 2:
        raise ValueError("Message history must contain at least an initial prompt and one AI response.")

    claude_messages = []

    for index, item in enumerate(messages):
        role = "assistant"
        if index % 2 == 0:
            role = "user"
        
        claude_messages.append({
            "role": role,
            "content": [
                {
                    "type": "text",
                    "text": item
                    }
            ]
        })

    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    bedrock_model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    if haiku_model == "claude_haiku_35":
        bedrock_model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

    response = client.invoke_model(
        modelId=bedrock_model_id,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "messages": claude_messages,
            "max_tokens": 384
        }),
        contentType="application/json",
        accept="application/json"
    )

    send_bedrock_amplitude_event(user_id, "take_turn", haiku_model, response)

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return text