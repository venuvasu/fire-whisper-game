import boto3
import decimal
import json
import random
from amplitude.amplitude_handler import send_bedrock_amplitude_event

with open("prompts/claude_system_prompt_start.txt", "r") as f:
    system_prompt = f.read()

with open("prompts/story_arcs.txt", "r") as f:
    story_arcs_file = f.read()
    story_arcs_list = [line.strip() for line in story_arcs_file.split('\n') if line.strip()]


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
        difficulty_prompt = "Easy"
    elif difficulty.strip() == "Story":
        difficulty_prompt = "Easy"
    elif difficulty.strip() == "Adventurer":
        difficulty_prompt = "Normal"
    elif difficulty.strip() == "Hero":
        difficulty_prompt = "Hard"
    else:
        difficulty_prompt = "Easy"
    return difficulty_prompt


def create_saga_with_character(user_id, character_data, setting, difficulty, length, haiku_model="claude_haiku_30"):
    # Retrieve character dict from FW_Characters_Dev table
    dynamodb = boto3.resource('dynamodb')
    characters_table = dynamodb.Table('FW_Characters_Dev')
    response = characters_table.get_item(Key={'character_id': character_data['character_id']})
    character_dict = response.get('Item')
    character_dict_str = json.dumps(character_dict, default=decimal_default)

    story_arc = random.choice(story_arcs_list)
    print("Selected story arc:", story_arc)

    story_prompt = f"""Begin a Fire Whisper adventure for this character. Track progress in this format:
{character_dict_str}

## QUEST PARAMETERS
- Duration: {length}
- Setting: {setting}
- Difficulty: {difficulty}

## STORY ARC
{story_arc}

## GENERATION RULES
- Create appropriate backstory connecting the character to this crisis
- Establish clear objective in opening scene via SPARK method
- This is a SINGLE-SESSION story that MUST reach "Congratulations, you have completed this Saga!" 
- Scale complexity to match duration:
  - Short: Direct path, 1 major obstacle
  - Medium: Some exploration, 2-3 major challenges  
  - Long: Multiple paths, subplots, 4+ major encounters
- Adjust challenge based on difficulty:
  - Story: Narrative focus, forgiving combat
  - Adventurer: Balanced challenge
  - Hero: Tactical thinking required - Death is a real possibility

Begin immediately with the opening crisis. Emberlyn should introduce herself naturally within the action.
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
            "max_tokens": 512
        }),
        contentType="application/json",
        accept="application/json"
    )

    send_bedrock_amplitude_event(user_id, "create_saga", haiku_model, response)

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return {"prompt": story_prompt, "response": text.strip()}