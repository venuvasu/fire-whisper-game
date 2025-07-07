import boto3
import json
try:
    from amplitude.amplitude_handler import send_bedrock_amplitude_event
except ImportError:
    def send_bedrock_amplitude_event(*args, **kwargs):
        print(f"📊 Analytics Event: {args[1] if len(args) > 1 else 'unknown'}")
        pass
from src.data.sagas import get_saga

# Fix file path for console
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
update_prompt_file = project_root / "src" / "ai" / "prompts" / "claude_system_prompt_update_character.txt"

with open(update_prompt_file, "r") as f:
    character_system_prompt = f.read()

def update_character(user_id, game_id, character_id, haiku_model="claude_haiku_30"):
    # Retrieve the game record from DynamoDB
    game_record = get_saga(game_id)

    messages = game_record.get('messages', [])
    messages.append("Return an updated character sheet in the same format as the original character sheet, with any changes made during the turn. Do not return any other text or explanation, just the updated character sheet.")

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
            "system": character_system_prompt,
            "messages": claude_messages,
            "max_tokens": 3072
        }),
        contentType="application/json",
        accept="application/json"
    )

    send_bedrock_amplitude_event(user_id, "update_character", haiku_model, response)

    response_body = json.loads(response["body"].read())
    content = response_body.get("content", [])
    if not content or not isinstance(content, list) or "text" not in content[0]:
        raise ValueError(f"Claude API returned no content: {response_body}")
    text = content[0]["text"]

    return text.strip()