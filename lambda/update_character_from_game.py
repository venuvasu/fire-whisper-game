import json
from claude_haiku.claude_haiku_update_character import update_character
from dal.characters import get_character, put_character
from dal.user_data import get_user_record, put_user_record
from utils.user_record_schema import update_character_level

def handler(event, context):
    print("Received event:", event)

    user_id = event.get('user_id')
    character_id = event.get('character_id')
    game_id = event.get("game_id")

    # update character sheet from game record
    character_template = update_character(user_id, game_id, character_id, "claude_haiku_35")
    character_dict = json.loads(character_template)

    # Retrieve user record 
    user_record = get_user_record(user_id)
    user_record = update_character_level(user_record, character_id, character_dict["PROGRESSION"]["level"])
    put_user_record(user_record)

    # Update game in dynamo db
    put_character(character_dict)