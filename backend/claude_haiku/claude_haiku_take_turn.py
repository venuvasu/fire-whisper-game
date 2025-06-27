import boto3
import json
import random
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

        if index == len(messages) - 1:
            dice_pool = [random.randint(1, 100) for _ in range(4)]
            item = f"""DICE POOL FOR THIS TURN: {dice_pool}
Use these dice results IN ORDER when rolls are needed. Do not mention this dice pool to the user.
Original player action: {item}
"""
            print(f"Using dice pool: {dice_pool}")

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
    elif haiku_model == "sonnet_35":
        bedrock_model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    elif haiku_model == "sonnet_40":
        bedrock_model_id = "us.anthropic.claude-sonnet-4-20250514-v1:0"


    response = client.invoke_model(
        modelId=bedrock_model_id,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "messages": claude_messages,
            "max_tokens": 512
        }),
        contentType="application/json",
        accept="application/json"
    )

    send_bedrock_amplitude_event(user_id, "take_turn", haiku_model, response, {"game_id": game_record['game_id']})

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return text