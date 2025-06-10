import boto3
import json

def start_game():
    prompt = """
You are the Dungeon Master for a turn-based, fantasy text adventure game.
Your job is to describe the world and situation, then present choices.
Do not describe what the player does—only describe the setting and options.

📜 Rules:
-NEVER describe the player's actions or decisions.
-NEVER continue the story after offering choices.
-ALWAYS end your response with a prompt for the player to choose or act.
-If the player asks a question, answer briefly, then stop.

🎮 Format:
Describe a short scene (1–2 paragraphs).

End with 2–4 clear, numbered choices. Format them like:
What do you do?
1. [First option]
2. [Second option]
3. [Optional third]

⚔️ Game Setup:
-The player is a level 5 rogue named Nightshade.
-The game includes 1 boss fight, 1 hidden secret, and ends on a cliffhanger.
-Mechanics are light—focus on immersive story over stats.

Start the game now.
"""

    # invoke model with prompt
    client = boto3.client('bedrock-runtime')

    response = client.invoke_model(
        modelId="amazon.titan-text-lite-v1",
        body=json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.7,
                "topP": 0.9,
                "stopSequences": []
            },
        }),
        contentType="application/json",
        accept="application/json"
    )

    # Parse the response
    response_body = response["body"].read().decode("utf-8")
    parsed_response = json.loads(response_body)
    text = parsed_response.get("results", [{}])[0].get("outputText", "No response received")

    return {"prompt": prompt, "response": text}

def name_game(initial_prompt):
    # invoke model with prompt
    client = boto3.client('bedrock-runtime')

    prompt = f"""You are an AI game-naming assistant.

Only reply with a game name that is:
- No more than 40 characters long
- Based on the following prompt: {initial_prompt}
- Returned as plain text only, with no explanation or formatting
- The name should have capitalization and punctuation as appropriate for a title

Example format (don't use this name, it's just an example):
Shadow of the Ember Queen

Now, give the name:"""

    response = client.invoke_model(
        modelId="amazon.titan-text-lite-v1",
        body=json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.7,
                "topP": 0.9,
                "stopSequences": []
            },
        }),
        contentType="application/json",
        accept="application/json"
    )

    # Parse the response
    response_body = response["body"].read().decode("utf-8")
    parsed_response = json.loads(response_body)
    text = parsed_response.get("results", [{}])[0].get("outputText", "No Name Game")

    return text.strip()[:40].title()