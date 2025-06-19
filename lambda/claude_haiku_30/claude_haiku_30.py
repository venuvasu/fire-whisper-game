import boto3
import decimal
import json
from amplitude.amplitude_handler import send_bedrock_amplitude_event

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

with open("prompts/claude_system_prompt_turns.txt", "r") as f:
    system_prompt = f.read()

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

def update_character(game_id, character_id):
    character_system_prompt = """You are the dungeon master of a custom, turn-based text roleplaying game. Your job is to update a character sheet based on what happened during gameplay, which is passed as the messages.

What gets returned MUST match the JSON described below, with no extra words or anything, so the game can use it to save the character:
{
    IDENTITY: {
        name: "",                  // Player's chosen name
        gender: "",                // Male, Female, Transgender Male, Transgender Female, Non-Binary
        appearance: "",            // Physical description
        background: "",            // Origin story/personal history
        profession: "",            // Class equivalent (Warrior, Mage, etc.)
        race: "",
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

Players level up based on total experience points (XP). Use this XP table:
Level 2 = 1000 XP
Level 3 = 2000 XP
Level 4 = 5000 XP
Level 5 = 10000 XP
Level 6 = 15000 XP
Level 7 = 23000 XP
Level 8 = 34000 XP
Level 9 = 48000 XP
Level 10 = 64000 XP
Level 11 = 85000 XP
Level 12 = 100000 XP
Level 13 = 120000 XP
Level 14 = 140000 XP
Level 15 = 165000 XP
Level 16 = 195000 XP
Level 17 = 225000 XP
Level 18 = 265000 XP
Level 19 = 305000 XP
Level 20 = 355000 XP
Only increase level when XP meets or exceeds the threshold. Do not grant partial levels.

On leveling up, bestow benefits on the character such as:
- Increased attributes
- New skills or skill improvements
- New talents or spells
- Increased hit points and mana
- Special abilities at milestone levels
If the benefits were bestowed during the game, they should be reflected in the character sheet. Correct the character sheet to upgrade the character if the game failed to.
"""
    # Get messages from game record
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('FW_Sagas_Dev')

    # Retrieve the game record from DynamoDB
    response = table.get_item(Key={'game_id': game_id})
    game_record = response['Item']
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

    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "system": character_system_prompt,
            "messages": claude_messages,
            "max_tokens": 3072
        }),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    content = response_body.get("content", [])
    if not content or not isinstance(content, list) or "text" not in content[0]:
        raise ValueError(f"Claude API returned no content: {response_body}")
    text = content[0]["text"]

    return text.strip()
