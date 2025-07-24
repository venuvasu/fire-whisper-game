"""
Mock Game Manager - Preserves business logic, mocks AWS infrastructure
"""

import uuid
from datetime import datetime

# Mock game storage (in real AWS this would be DynamoDB)
mock_games = {}

def get_game_by_id(game_id):
    """Mock get game by ID - preserves your business logic"""
    
    # In real AWS: Queries DynamoDB
    # Mock: Return structure that matches your real game data
    
    if game_id not in mock_games:
        # Create new game with structure matching your real system
        mock_games[game_id] = {
            'game_id': game_id,
            'messages': [],
            'game_active': True,
            'created_at': datetime.now().isoformat(),
            'game_name': 'Fire Whisper Adventure'
        }
    
    print(f"🎮 Mock Game Manager: Retrieved game {game_id}")
    return mock_games[game_id]

def append_message_to_game(game_record, message):
    """Mock append message - preserves your business logic EXACTLY"""
    
    # This is CRITICAL business logic - must work exactly like your real system
    if 'messages' not in game_record:
        game_record['messages'] = []
    
    game_record['messages'].append(message)
    
    # Update the mock storage
    game_id = game_record.get('game_id')
    if game_id:
        mock_games[game_id] = game_record
    
    print(f"💬 Mock Game Manager: Added message to game {game_id} (total: {len(game_record['messages'])})")
    return game_record

def create_new_game(user_id, character_id):
    """Mock create new game - preserves your business logic"""
    
    game_id = str(uuid.uuid4())
    
    game_record = {
        'game_id': game_id,
        'user_id': user_id,
        'character_id': character_id,
        'messages': [],
        'game_active': True,
        'created_at': datetime.now().isoformat(),
        'game_name': 'Fire Whisper Adventure'
    }
    
    mock_games[game_id] = game_record
    
    print(f"🆕 Mock Game Manager: Created new game {game_id}")
    return game_record