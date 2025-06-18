import boto3
import decimal
import json
from amplitude.amplitude_handler import send_bedrock_amplitude_event

with open("prompts/claude_system_prompt_start.txt", "r") as f:
    system_prompt = f.read()

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def get_length_prompt(length):
    length_prompt = ""
    if not length or not length.strip() or length.strip() == "Short":
        length_prompt = "The duration of this story should be short, consisting of simple puzzle followed by a combat encounter leading to a conclusion."
    elif length.strip() == "Medium":
        length_prompt = "The duration of this story should be medium, consisting of puzzle followed by 2-3 combat encounters leading to a conclusion."
    elif length.strip() == "Long":
        length_prompt = "The duration of this story should be longer, consisting of 3 clear quest milestones that cascade to a conclusion. Each milestone should consist of a puzzle, 1-2 combat encounters, or a boss fight. There should be a heavy bias to using a Boss fight for the third milestone. NPCs should be encouraged to adventure alongside the player in this story."
    else:
        length_prompt = "The duration of this story should be short, consisting of simple puzzle followed by a combat encounter leading to a conclusion."
    return length_prompt

def get_difficulty_prompt(difficulty):
    difficulty_prompt = ""
    if difficulty and difficulty.strip() != "":
        difficulty_prompt = "Story should focus on narrative and exploration, lighter challenges."
    elif difficulty.strip() == "Story":
        difficulty_prompt = "Story should focus on narrative and exploration, lighter challenges."
    elif difficulty.strip() == "Adventurer":
        difficulty_prompt = "Story should focus on narrative and exploration and combat should be moderately difficult and have the possibility of failure."
    elif difficulty.strip() == "Hero":
        difficulty_prompt = "Story should strive to challenge the player and mistakes should be punished."
    else:
        difficulty_prompt = "Story should focus on narrative and exploration, lighter challenges."
    return difficulty_prompt


def create_saga_with_character(user_id, character_data, setting, difficulty, length, haiku_model="claude_haiku_30"):
    # Retrieve character dict from FW_Characters_Dev table
    dynamodb = boto3.resource('dynamodb')
    characters_table = dynamodb.Table('FW_Characters_Dev')
    response = characters_table.get_item(Key={'character_id': character_data['character_id']})
    character_dict = response.get('Item')
    character_dict_str = json.dumps(character_dict, default=decimal_default)

    setting_prompt = ""
    if setting and setting.strip() != "":
        setting_prompt = "- The setting of the story should be " + setting + "."
    difficulty_prompt = get_difficulty_prompt(difficulty)
    length_prompt = get_length_prompt(length)
    
    story_prompt = f"""We want to generate a game story for the following character. Track characters progress in this format as we play: {character_dict_str}

The story should have the following characteristics:
- Give the character simple, relevant backstory and a specific goal (or quest) to achieve
- This is a SINGLE-SESSION story that MUST conclude after the goal is achieved.
- The story should END automatically after the goals are completed and NOT prompt for further input. This means to options and no questions, as the user won't be able to respond.
- {length_prompt}
- {setting_prompt}
- {difficulty_prompt}
"""

    if difficulty.strip() == "Tutorial":
        story_prompt = f"""We want to generate a game story for the following character. Track characters progress in this format as we play: {character_dict_str}

The story should have the following characteristics:
- Give the character simple, relevant backstory and a specific goal (or quest) to achieve
- This is a SINGLE-SESSION story that MUST conclude after the goal is achieved.
- The story should END automatically after the goals are completed and NOT prompt for further input. This means to options and no questions, as the user won't be able to respond.
- This is a tutorial story, so it should be very simple, consisting of a very simple puzzle followed by a combat encounter leading to a quick conclusion.
{setting_prompt}
"""

    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    bedrock_model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    if haiku_model == "claude_haiku_35":
        bedrock_model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

    print("Invoking model with prompt:", system_prompt)

    response = client.invoke_model(
        modelId=bedrock_model_id,
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": story_prompt
                        }
                    ]
                }
            ],
            "max_tokens": 384
        }),
        contentType="application/json",
        accept="application/json"
    )

    send_bedrock_amplitude_event(user_id, "create_saga", haiku_model, response)

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return {"prompt": story_prompt, "response": text.strip()}