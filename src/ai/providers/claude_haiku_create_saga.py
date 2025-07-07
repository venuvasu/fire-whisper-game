import boto3
import decimal
import json
import secrets
try:
    from amplitude.amplitude_handler import send_bedrock_amplitude_event
except ImportError:
    def send_bedrock_amplitude_event(*args, **kwargs):
        print(f"📊 Analytics Event: {args[1] if len(args) > 1 else 'unknown'}")
        pass
from src.data.characters import get_character

# Fix file paths for console
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
start_prompt_file = project_root / "src" / "ai" / "prompts" / "claude_system_prompt_start.txt"
story_arcs_file_path = project_root / "src" / "ai" / "prompts" / "story_arcs.txt"

with open(start_prompt_file, "r") as f:
    system_prompt = f.read()

with open(story_arcs_file_path, "r") as f:
    story_arcs_file = f.read()
    story_arcs_list = [line.strip() for line in story_arcs_file.split('\n') if line.strip()]


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def parse_story_arc(story_line):
    result = {}
    sections = story_line.split(' | ')
    
    for section in sections:
        key, value = section.split(':', 1)
        result[key.strip()] = value.strip()
    
    return result

def create_saga_with_character(user_id, character_data, setting, difficulty, haiku_model="claude_haiku_30"):
    character_dict_str = json.dumps(character_data, default=decimal_default)

    story_arc = secrets.choice(story_arcs_list)
    parsed_story_arc = parse_story_arc(story_arc)
    print("Selected story arc:", parsed_story_arc['Name'])
    print("Length of story_arc string:", len(story_arcs_list))

    story_prompt = f"""Begin a Fire Whisper adventure for this character. Track progress in this format:
{character_dict_str}

## QUEST PARAMETERS
- Setting: {setting}
- Difficulty: {difficulty}

## STORY ARC
{story_arc}

## GENERATION RULES
- Create appropriate backstory connecting the character to this crisis
- Establish clear objective in opening scene via SPARK method
- This is a SINGLE-SESSION story that MUST reach "Congratulations, you have completed this Saga!" 
- The duration of this story should be less then 50 turns, with a turn being a single message from the player. The game will be forcibly ended at 50 turns.
- It should consist of a 2-3 challenges around the story arc, with at most 1 being a puzzle and the rest combat.
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

    send_bedrock_amplitude_event(user_id, "create_saga", haiku_model, response, {"game_name": parsed_story_arc['Name'], "character_id": character_data['character_id']})

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return {"prompt": story_prompt, "response": text.strip(), "game_name": parsed_story_arc['Name']}