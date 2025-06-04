import boto3
import decimal
import json

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

with open("prompts/claude_system_prompt.txt", "r") as f:
    system_prompt = f.read()

def start_game(body_params):
    initial_prompt = """Create a campaign with the following details:
- Generate a character and a backstory for the user to play as. The character should be either a rogue, mage, warrior or wizard. Give the player some minimal information to start with about the character, and answer their questions if they ask.
- The adventure should take about 5–10 minutes to complete.
- Include at least 1 boss encounter and 1 hidden secret.
- Keep mechanics light—focus on narrative over stats or dice rolls.

Begin the story now.
"""

    # TODO - move to it's own helper function
    if body_params is not None:        
        character_string = "You should choose a character name and tell the user."
        class_string = "You should choose a class for the character and tell the user from these options: Warrior, Berserker, Mage, Druid, Shaman, Cleric, Templar, Assassin, Thief, Bard."
        campaign_difficulty = "The campaign should be easy difficulty."
        story_keywords = ""
        story_tone = "The story tone should be fun but not silly."
        if "character_name" in body_params and body_params['character_name'].strip() != "":
            character_string = f"The characters name should be {body_params['character_name']}."  
        if "class" in body_params and body_params["class"].strip() != "" and body_params["class"].strip() != "<Random>":
            class_string = f"The characters class should be {body_params['class']}."
        if "character_name" in body_params and body_params["character_name"].strip() != "":
            campaign_difficulty = f"The campaign should be {body_params['difficulty']} difficulty."
        if "story_keywords" in body_params and body_params["story_keywords"].strip() != "":
            story_keywords = f"-The story should be inspired by the following keywords: {body_params['story_keywords']}."
        if "tone" in body_params and body_params["tone"]:
            story_tone = "The tone of the story should be based on balancing the following tones: " + ", ".join(body_params['tone']) + "."

        initial_prompt = f'''Create a campaign with the following details:
- Generate a character and a backstory for the user to play as.
- {character_string}
- {class_string}
- {campaign_difficulty}
- {story_tone}
{story_keywords}
'''
    print("Initial prompt:", initial_prompt)

    # invoke model with prompt
    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
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

    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
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

def name_game(initial_prompt):
    # invoke model with prompt
    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    name_system_prompt = f"""You are an AI game-naming assistant.

Only reply with a game name that is:
- No more than 40 characters long
- Returned as plain text only, with no explanation or formatting
- The name should have capitalization and punctuation as appropriate for a title

Example format (don't use this name, it's just an example):
Shadow of the Ember Queen"""
    
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": name_system_prompt,
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
            "max_tokens": 64
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return text.strip()

def create_character(name, gender, profession):
    character_system_prompt = """
You are the dungeon master of a custom, turn-based text roleplaying game.

When generating a new character, keep the following in mind:
- ONLY return the JSON object as described below, with no extra words or formatting. This will return via an API and expects the JSON, and will error if there are any extraneous words or content.
- The relationships should be empty arrays, as the player will build them during the game through play.

Make sure when generating a character that the following are auto generated, unless the player has specified them in which case you should use the player's input:
- Make sure All IDENTITY fields are filled in based on comment next to field.
- All ATTRIBUTES fields
- All VITALITY fields
- Capabilities fields should be auto generated as appropriate for the profession
- Generate all the EQUIPMENT fields, including a weapon, armor, accessories, tools, and magical items
- Generate other fields as appropriate for the character, but do not include any extra fields that are not in the JSON below.

Right now, your job is to create a character for use in the game. What gets returned MUST match the JSON described below, with no extra words or anything, so the game can use it to save the character:

{
    IDENTITY: {
        name: "",                  // Player's chosen name
        gender: "",                // Male, Female, Transgender Male, Transgender Female, Non-Binary
        appearance: "",            // Physical description
        background: "",            // Origin story/personal history
        profession: "",            // Class equivalent (Warrior, Mage, etc.)
        path: {
            approach: "",          // Principled/Adaptable/Free-spirited
            ethos: ""              // Altruistic/Balanced/Pragmatic/Shadow-touched
        }
    },
    ATTRIBUTES: {
        strength: 0,               // Physical power
        dexterity: 0,              // Agility/reflexes
        constitution: 0,           // Stamina/health resilience
        intelligence: 0,           // Knowledge/reasoning
        wisdom: 0,                 // Intuition/perception
        charisma: 0                // Social influence
    },
    VITALITY: {
        hitPoints: 0,
        maxHitPoints: 0,
        mana: 0,
        maxMana: 0,
        recoveryRate: {
            hitpoints: 0,          // HP recovery per rest
            mana: 0              // Energy recovery per rest
        }
    },
    PROGRESSION: {
        experience: 0,             // XP accumulation - default should start at 0 xp and level 1
        level: 1,                  // Character advancement tier
        renown: 0,                 // Reputation in the world
        destinyPoints: 0           // Points for special abilities/fate manipulation
    },
    CAPABILITIES: {
        skills: [                  // Trained abilities with proficiency levels
            {name: "", proficiency: "", description: ""}
        ],
        talents: [                 // Special abilities unique to character
            {name: "", description: "", cooldown: 0}
        ],
        spellsTechniques: [        // Known spells or combat techniques
            {name: "", type: "", effect: "", energyCost: 0}
        ],
        passiveAbilities: [        // Always-active benefits
            {name: "", effect: ""}
        ]
    },
    EQUIPMENT: {
        weapon: {
            name: "",              // Primary offensive tool
            effect: "",            // Special properties
            damage: 0,             // Base damage
            durability: 0          // Condition (100 = perfect)
        },
        armor: {
            name: "",              // Protective gear
            protection: 0,         // Damage reduction
            durability: 0          // Condition (100 = perfect)
        },
        accessories: [             // Rings, amulets, etc.
            {name: "", effect: ""}
        ],
        tools: [                   // Utility items
            {name: "", use: ""}
        ],
        magicalItems: [            // Special enchanted possessions
            {name: "", power: "", charges: 0}
        ]
    },
    INVENTORY: {
        carriedItems: [            // List of possessions
            {name: "", quantity: 0, description: ""}
        ],
        currency: 0,               // Money amount
        questItems: [              // Special objects related to quests
            {name: "", quest: "", description: ""}
        ],
        consumables: [             // Potions, food, etc.
            {name: "", effect: "", quantity: 0}
        ]
    },
    RELATIONSHIPS: {
        allies: [                  // Friends and companions
            {name: "", attitude: 0, notes: ""}
        ],
        enemies: [                 // Hostile NPCs
            {name: "", threat: 0, notes: ""}
        ],
        factions: [                // Groups and their disposition
            {name: "", standing: 0, notes: ""}
        ],
        companionBond: 0           // Relationship with Emberlyn (0-100)
    },
    ADDITIONAL: {
        resistances: {             // Special protections
            physical: 0,
            magical: 0,
            elemental: {fire: 0, ice: 0, lightning: 0, poison: 0}
        },
        languages: [],             // What the character can speak/understand
        trainingProgress: {        // Advancement toward new skills
            current: "",
            progress: 0
        },
        injuryStatus: [],          // Persistent wounds affecting performance
        effects: {
            blessings: [],         // Positive supernatural effects
            curses: [],            // Negative supernatural effects
            temporary: []          // Short-term buffs/debuffs
        },
        craftingAbilities: [],     // Skills for creating items
        knowledgeAreas: [],        // Specific subjects character has studied
        culturalTraits: []         // Benefits/challenges from cultural background
    }
}
"""
    name_prompt = ""
    if name and name.strip() != "":
        name_prompt = "The character's name should be " + name + "."
    gender_prompt = ""
    if gender and gender.strip() != "":
        gender_prompt = "The character's gender should be " + gender + "."
    profession_prompt = ""
    if profession and profession.strip() != "":
        profession_prompt = "The character's profession should be " + profession + "."

    character_prompt = f"""Randomly generate a level 1 character.
{name_prompt}
{gender_prompt}
{profession_prompt}
"""

    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
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

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return text.strip()

def create_saga_with_character(character_data, setting, difficulty, length):
    # Retrieve character dict from FW_Characters_Dev table
    dynamodb = boto3.resource('dynamodb')
    characters_table = dynamodb.Table('FW_Characters_Dev')
    response = characters_table.get_item(Key={'character_id': character_data['character_id']})
    character_dict = response.get('Item')
    character_dict_str = json.dumps(character_dict, default=decimal_default)

    setting_prompt = ""
    if setting and setting.strip() != "":
        setting_prompt = "- The setting of the story should be " + setting + "."
    difficulty_prompt = ""
    if difficulty and difficulty.strip() != "":
        difficulty_prompt = "- The setting of the story should be " + difficulty + "."
    length_prompt = ""
    if length and length.strip() != "":
        length_prompt = "- The setting of the story should be " + length + "."

    print("Difficulty prompt:", difficulty_prompt)
    print("Length prompt:", length_prompt)

    story_prompt = f"""
We want to generate a game story for the following character. Track characters progress in this format as we play: {character_dict_str}

The story should have the following characteristics:
- Give the character simple, relevant backstory and a goal to achieve
- Mix combat, puzzle-solving, and exploration
{setting_prompt}
- STORY MODE - Lighter challenges, focus on narrative and exploration
- The duration should be: Short - 10 minutes
"""

    client = boto3.client('bedrock-runtime', region_name="us-east-1")

    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
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
            "max_tokens": 256
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    text = response_body["content"][0]["text"]
    return {"prompt": story_prompt, "response": text.strip()}