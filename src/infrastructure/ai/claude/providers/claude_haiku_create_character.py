import boto3
import json
try:
    from amplitude.amplitude_handler import send_bedrock_amplitude_event
except ImportError:
    # Fallback for console/local development
    def send_bedrock_amplitude_event(*args, **kwargs):
        print(f"📊 Analytics Event: {args[1] if len(args) > 1 else 'unknown'}")
        pass

# Fix file path for console
import os
from pathlib import Path

# Get the correct path to the prompts directory
prompt_dir = Path(__file__).parent.parent / "prompts"
prompt_file = prompt_dir / "claude_system_prompt_create_character.txt"

with open(prompt_file, "r") as f:
    character_system_prompt = f.read()

def create_character(user_id, name, race, gender, profession, haiku_model="claude_haiku_30"):
    name_prompt = ""
    if name and name.strip() != "":
        name_prompt = "The character's name should be " + name + "."
    race_prompt = ""
    if race and race.strip() != "":
        race_prompt = "The character's race should be " + race + "."
    gender_prompt = ""
    if gender and gender.strip() != "":
        gender_prompt = "The character's gender should be " + gender + "."
    profession_prompt = ""
    if profession and profession.strip() != "":
        profession_prompt = "The character's profession should be " + profession + "."

    character_prompt = f"""Randomly generate a level 1 character.
{name_prompt}
{race_prompt}
{gender_prompt}
{profession_prompt}
"""
    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    bedrock_model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    if haiku_model == "claude_haiku_35":
        bedrock_model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

    response = client.invoke_model(
        modelId=bedrock_model_id,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": character_system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": character_prompt
                        }
                    ]
                }
            ],
            "max_tokens": 3072
        }),
        contentType="application/json",
        accept="application/json"
    )

    send_bedrock_amplitude_event(user_id, "create_character", haiku_model, response)

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return text.strip()