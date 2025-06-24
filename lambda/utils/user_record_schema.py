from decimal import Decimal

def build_user_record(user_id, characters):
    if not isinstance(user_id, str):
        raise ValueError("user_id must be a string")
    
    if not isinstance(characters, list):
        raise ValueError("characters must be a list")
    
    # Validate each character object
    for char in characters:
        if not isinstance(char, dict):
            raise ValueError("each character must be a dict")
        
        # Check required fields
        required_fields = ['name', 'profession', 'character_id', 'level']
        for field in required_fields:
            if field not in char:
                raise ValueError(f"character missing required field: {field}")
        
        # Validate required field types
        if not isinstance(char['name'], str):
            raise ValueError("character 'name' must be a string")
        if not isinstance(char['profession'], str):
            raise ValueError("character 'profession' must be a string")
        if not isinstance(char['character_id'], str):
            raise ValueError("character 'character_id' must be a string")
        if not isinstance(char['level'], (int, Decimal)):
            raise ValueError("character 'level' must be an int or Decimal")
        
        # Set default empty arrays for optional fields and validate if they exist
        if 'completed_games' not in char:
            char['completed_games'] = []
        elif not isinstance(char['completed_games'], list) or not all(isinstance(g, str) for g in char['completed_games']):
            raise ValueError("character 'completed_games' must be a list of strings")
        
        if 'active_games' not in char:
            char['active_games'] = []
        elif not isinstance(char['active_games'], list) or not all(isinstance(g, str) for g in char['active_games']):
            raise ValueError("character 'active_games' must be a list of strings")
        
        if 'active' not in char:
            char['active'] = []
        else:
            if not isinstance(char['active'], list):
                raise ValueError("character 'active' must be a list")
            for game in char['active']:
                if not isinstance(game, dict):
                    raise ValueError("each item in 'active' must be a dict")
                if not isinstance(game.get('game_id'), str):
                    raise ValueError("'active' game objects must have 'game_id' as string")
                if not isinstance(game.get('game_name'), str):
                    raise ValueError("'active' game objects must have 'game_name' as string")
        
        if 'completed' not in char:
            char['completed'] = []
        else:
            if not isinstance(char['completed'], list):
                raise ValueError("character 'completed' must be a list")
            for game in char['completed']:
                if not isinstance(game, dict):
                    raise ValueError("each item in 'completed' must be a dict")
                if not isinstance(game.get('game_id'), str):
                    raise ValueError("'completed' game objects must have 'game_id' as string")
                if not isinstance(game.get('game_name'), str):
                    raise ValueError("'completed' game objects must have 'game_name' as string")
    
    return {
        "user_id": user_id,
        "characters": characters
    }

def parse_user_record(record):
    return {
        "user_id": record.get("user_id", ""),
        "characters": record.get("characters", []),
    }

def get_user_record_character(user_record, character_id):
    """
    Returns a character from the user record based on character_id.
    
    Args:
        user_record (dict): The user record containing characters
        character_id (str): The character_id to search for
    
    Returns:
        dict: The character object if found, None otherwise
    """
    if not isinstance(user_record, dict):
        raise ValueError("user_record must be a dict")
    if not isinstance(character_id, str):
        raise ValueError("character_id must be a string")
    
    characters = user_record.get("characters", [])
    
    for character in characters:
        if isinstance(character, dict) and character.get("character_id") == character_id:
            return character
    
    return None

def add_to_active(user_record, character_id, game_id, game_name):
    """
    Adds a game to a character's active games list.
    
    Args:
        user_record (dict): The user record containing characters
        character_id (str): The character_id to add the game to
        game_id (str): The game_id to add
        game_name (str): The game_name to add
    
    Returns:
        dict: The updated user_record
    
    Raises:
        ValueError: If character not found
    """
    if not isinstance(user_record, dict):
        raise ValueError("user_record must be a dict")
    if not isinstance(character_id, str):
        raise ValueError("character_id must be a string")
    if not isinstance(game_id, str):
        raise ValueError("game_id must be a string")
    if not isinstance(game_name, str):
        raise ValueError("game_name must be a string")
    
    character = get_user_record_character(user_record, character_id)
    if character is None:
        raise ValueError(f"Character with id '{character_id}' not found")
    
    # Ensure active field exists
    if 'active' not in character:
        character['active'] = []
    
    # Check if game_id already exists in active games
    for game in character['active']:
        if game.get('game_id') == game_id:
            # Update existing game name
            game['game_name'] = game_name
            return user_record
    
    # Add new game
    character['active'].append({'game_id': game_id, 'game_name': game_name})
    return user_record

def remove_from_active(user_record, character_id, game_id):
    """
    Removes a game from a character's active games list based on game_id.
    
    Args:
        user_record (dict): The user record containing characters
        character_id (str): The character_id to remove the game from
        game_id (str): The game_id to remove
    
    Returns:
        dict: The updated user_record
    
    Raises:
        ValueError: If character not found or game not found
    """
    if not isinstance(user_record, dict):
        raise ValueError("user_record must be a dict")
    if not isinstance(character_id, str):
        raise ValueError("character_id must be a string")
    if not isinstance(game_id, str):
        raise ValueError("game_id must be a string")
    
    character = get_user_record_character(user_record, character_id)
    if character is None:
        raise ValueError(f"Character with id '{character_id}' not found")
    
    # Ensure active field exists
    if 'active' not in character:
        character['active'] = []
    
    # Find and remove the game
    for i, game in enumerate(character['active']):
        if game.get('game_id') == game_id:
            character['active'].pop(i)
            return user_record
    
    raise ValueError(f"Game with id '{game_id}' not found in character's active games")

def add_to_completed(user_record, character_id, game_id, game_name):
    """
    Adds a game to a character's completed games list.
    
    Args:
        user_record (dict): The user record containing characters
        character_id (str): The character_id to add the game to
        game_id (str): The game_id to add
        game_name (str): The game_name to add
    
    Returns:
        dict: The updated user_record
    
    Raises:
        ValueError: If character not found
    """
    if not isinstance(user_record, dict):
        raise ValueError("user_record must be a dict")
    if not isinstance(character_id, str):
        raise ValueError("character_id must be a string")
    if not isinstance(game_id, str):
        raise ValueError("game_id must be a string")
    if not isinstance(game_name, str):
        raise ValueError("game_name must be a string")
    
    character = get_user_record_character(user_record, character_id)
    if character is None:
        raise ValueError(f"Character with id '{character_id}' not found")
    
    # Ensure completed field exists
    if 'completed' not in character:
        character['completed'] = []
    
    # Check if game_id already exists in completed games
    for game in character['completed']:
        if game.get('game_id') == game_id:
            # Update existing game name
            game['game_name'] = game_name
            return user_record
    
    # Add new game
    character['completed'].append({'game_id': game_id, 'game_name': game_name})
    return user_record

def add_character(user_record, name, profession, character_id, level):
    """
    Creates a new character and adds it to the user record.
    
    Args:
        user_record (dict): The user record containing characters
        name (str): The character's name
        profession (str): The character's profession
        character_id (str): The unique character_id
        level (int or Decimal): The character's level
    
    Returns:
        dict: The updated user_record
    
    Raises:
        ValueError: If character_id already exists or invalid input types
    """
    if not isinstance(user_record, dict):
        raise ValueError("user_record must be a dict")
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    if not isinstance(profession, str):
        raise ValueError("profession must be a string")
    if not isinstance(character_id, str):
        raise ValueError("character_id must be a string")
    if not isinstance(level, (int, Decimal)):
        raise ValueError("level must be an int or Decimal")
    
    # Check if character_id already exists
    existing_character = get_user_record_character(user_record, character_id)
    if existing_character is not None:
        raise ValueError(f"Character with id '{character_id}' already exists")
    
    # Ensure characters field exists
    if 'characters' not in user_record:
        user_record['characters'] = []
    
    # Create new character with required fields and empty optional arrays
    new_character = {
        'name': name,
        'profession': profession,
        'character_id': character_id,
        'level': level,
        'completed_games': [],
        'active_games': [],
        'active': [],
        'completed': []
    }
    
    # Add character to the user record
    user_record['characters'].append(new_character)
    
    return user_record