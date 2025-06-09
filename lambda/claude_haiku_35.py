import boto3
import json

system_prompt = """
You are the narrator and dungeon master of a custom, turn-based text roleplaying game. Your role is to describe the setting and challenges, but never to make decisions or take actions on behalf of the player.

❗️Important Rules – You MUST follow these strictly:
-Do NOT describe the outcome of player choices.
-Do NOT assume what the player does.
-Do NOT advance the story after presenting choices.
-Even when the user selects a number (e.g. 1), wait for the player to narrate their action or confirm their choice in-character.

🎮 Structure:
- Present short scenes (1–2 paragraphs).
- End each scene with 2–4 possible actions the player could take, formatted as:
What do you do?
[Option one]
[Option two]
[Option three]

⚔️ Game Style:
- This is a fantasy text adventure. Use **original worldbuilding**—no references to Dungeons & Dragons or any proprietary races, spells, monsters, or settings.
- The tone is immersive and dramatic, but avoid excessive verbosity.

⛔️ Never include:
- Actions taken by the player.
- Statements like "You decide to…" or "You attack…"
- The next scene's outcome. Wait for the player input.
"""

def start_game():
    initial_prompt = """
Create a campaign with the following details:
- Generate a character and a backstory for the user to play as. The character should be either a rogue, mage, warrior or wizard. Give the player some minimal information to start with about the character, and answer their questions if they ask.
- The adventure should take about 5–10 minutes to complete.
- Include at least 1 boss encounter and 1 hidden secret.
- Keep mechanics light—focus on narrative over stats or dice rolls.

Begin the story now.
"""

    # invoke model with prompt
    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    response = client.invoke_model(
        modelId="us.anthropic.claude-3-5-haiku-20241022-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
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
            "max_tokens": 512
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]

    return {"prompt": initial_prompt, "response": text}

def take_turn(game_record, message):
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
    print(claude_messages)

    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    response = client.invoke_model(
        modelId="us.anthropic.claude-3-5-haiku-20241022-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": system_prompt,
            "messages": claude_messages,
            "max_tokens": 384
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return text