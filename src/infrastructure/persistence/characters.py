import boto3

dynamodb = boto3.resource('dynamodb')
characters_table = dynamodb.Table('FW_Characters_Dev')

def get_character(character_id):
    response = characters_table.get_item(Key={'character_id': character_id})
    character_data = response.get('Item', {})
    return character_data

def put_character(character_record):
    characters_table.put_item(Item=character_record)

def validate_and_fix_profession(character_record):
    """
    Validate and fix the character profession if AI has augmented it incorrectly
    """
    valid_professions = [
        "Warrior", "Berserker", "Mage", "Druid", "Shaman", 
        "Cleric", "Templar", "Assassin", "Thief", "Bard"
    ]
    
    # Get current profession
    current_profession = character_record.get("IDENTITY", {}).get("profession")
    
    if not current_profession:
        return character_record
    
    # If it's already a valid profession, do nothing
    if current_profession in valid_professions:
        return character_record
    
    # Check if any valid profession is a substring of the current value
    for valid_prof in valid_professions:
        if valid_prof in current_profession:
            print(f"Fixed profession: '{current_profession}' -> '{valid_prof}'")
            character_record["IDENTITY"]["profession"] = valid_prof
            return character_record
    
    # Couldn't deduce a valid profession
    print(f"Couldn't deduce profession from: '{current_profession}'")
    return character_record

def validate_and_fix_level(character_record):
    """
    Validate and fix the character level based on experience points
    """
    xp_table = {
        1: 0,
        2: 1000,
        3: 2000,
        4: 5000,
        5: 10000,
        6: 15000,
        7: 23000,
        8: 34000,
        9: 48000,
        10: 64000,
        11: 85000,
        12: 100000,
        13: 120000,
        14: 140000,
        15: 165000,
        16: 195000,
        17: 225000,
        18: 265000,
        19: 305000,
        20: 355000
    }
    
    # Get current experience and level
    progression = character_record.get("PROGRESSION", {})
    current_xp = progression.get("experience")
    current_level = progression.get("level")
    
    if current_xp is None:
        return character_record
    
    # Calculate correct level based on experience
    correct_level = 1
    for level, required_xp in sorted(xp_table.items()):
        if current_xp >= required_xp:
            correct_level = level
        else:
            break
    
    # Fix level if it's wrong
    if current_level != correct_level:
        print(f"Fixed level: {current_level} -> {correct_level} (XP: {current_xp})")
        character_record["PROGRESSION"]["level"] = correct_level
    
    return character_record