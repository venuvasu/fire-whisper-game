import boto3
import json

def start_game():
    prompt = """
You are the narrator and dungeon master of a custom, turn-based text roleplaying game. Your role is to describe the setting and challenges, but never to make decisions or take actions on behalf of the player.

❗️Important Rules:
- DO NOT decide what the player character does.
- DO NOT continue the story past presenting choices.
- Always stop after offering a set of clear, numbered options (or wait for an open-ended player command).
- Your response should end with a prompt for the user to respond.
- If the player character asks a question or requests information, provide a brief answer but DO NOT advance the story.

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

📜 Campaign Details:
- The player is a level 5 rogue named **Nightshade**.
- The adventure should take about 5–10 minutes to complete.
- Include 1 boss encounter, 1 hidden secret (that can optionally be discovered), and end on a cliffhanger leading to the next episode.
- Keep mechanics light—focus on narrative over stats or dice rolls.

⛔️ Never include:
- Actions taken by the player.
- Statements like "You decide to…" or "You attack…"
- The next scene's outcome. Wait for the player input.

Begin the story now.
"""

    # invoke model with prompt
    client = boto3.client('bedrock-runtime')

    response = client.invoke_model(
        modelId="mistral.mixtral-8x7b-instruct-v0:1",
        body=json.dumps({
            "max_tokens": 512,
            "temperature": 0.8,
            "prompt": f"{prompt}"
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response['body'].read())
    text = response_body["outputs"][0]["text"]

    return {"prompt": prompt, "response": text}

def take_turn(game_record, message):
    messages = game_record.get('messages', [])

    if not messages or len(messages) < 2:
        raise ValueError("Message history must contain at least an initial prompt and one AI response.")

    prompt_lines = []

    # Initial setup
    prompt_lines.append(f"User: {messages[0]}")
    prompt_lines.append(f"Assistant: {messages[1]}")

    # Loop through the rest of the history
    for i in range(2, len(messages), 2):
        user_msg = messages[i]
        ai_msg = messages[i + 1] if i + 1 < len(messages) else ""
        prompt_lines.append(f"User: {user_msg}")
        prompt_lines.append(f"Assistant: {ai_msg}")

    prompt = "\n".join(prompt_lines)

    client = boto3.client('bedrock-runtime')

    response = client.invoke_model(
        modelId="mistral.mixtral-8x7b-instruct-v0:1",
        body=json.dumps({
            "max_tokens": 512,
            "temperature": 0.8,
            "prompt": f"{prompt}"
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response['body'].read())
    text = response_body["outputs"][0]["text"]
    return text