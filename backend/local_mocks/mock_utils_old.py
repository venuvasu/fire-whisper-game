"""
Mock Utils - Simulates game management utilities locally
PRESERVES ALL BUSINESS RULES - Only mocks the infrastructure
"""

import json
import uuid
from datetime import datetime
from decimal import Decimal

# In-memory storage for games
MOCK_GAMES = {}

class MockGameManager:
    @staticmethod
    def get_game_by_id(game_id):
        """Mock get_game_by_id - returns game data"""
        if game_id in MOCK_GAMES:
            return MOCK_GAMES[game_id]
        
        # Return default game structure
        return {
            'game_id': game_id,
            'messages': [],
            'character_id': 'mock_character',
            'user_id': 'mock_user',
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def append_message_to_game(game_record, message):
        """Mock append_message_to_game - adds message to game record"""
        if 'messages' not in game_record:
            game_record['messages'] = []
        
        game_record['messages'].append(message)
        game_record['updated_at'] = datetime.now().isoformat()
        
        # Update mock storage
        game_id = game_record.get('game_id')
        if game_id:
            MOCK_GAMES[game_id] = game_record
        
        return game_record
    
    @staticmethod
    def create_new_game(character_id, user_id):
        """Mock create_new_game - creates new game"""
        game_id = str(uuid.uuid4())
        game_data = {
            'game_id': game_id,
            'character_id': character_id,
            'user_id': user_id,
            'messages': [],
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        MOCK_GAMES[game_id] = game_data
        return game_data
    
    @staticmethod
    def get_games_for_character(character_id):
        """Mock get_games_for_character - returns character's games"""
        character_games = []
        for game_id, game_data in MOCK_GAMES.items():
            if game_data.get('character_id') == character_id:
                character_games.append(game_data)
        return character_games

class MockUserRecordSchema:
    @staticmethod
    def get_character_by_active_game_id(user_data, game_id):
        """Mock get_character_by_active_game_id - finds character by game"""
        # This preserves your business logic for finding characters
        active_games = user_data.get('active_games', [])
        for game in active_games:
            if game.get('game_id') == game_id:
                return game.get('character_id')
        return None
    
    @staticmethod
    def get_character_by_game_id(user_data, game_id):
        """Mock get_character_by_game_id - finds character by game"""
        # Check active games
        character_id = MockUserRecordSchema.get_character_by_active_game_id(user_data, game_id)
        if character_id:
            return character_id
        
        # Check completed games
        completed_games = user_data.get('completed_games', [])
        for game in completed_games:
            if game.get('game_id') == game_id:
                return game.get('character_id')
        
        return None
    
    @staticmethod
    def get_active_game(user_data, character_id):
        """Mock get_active_game - finds active game for character"""
        active_games = user_data.get('active_games', [])
        for game in active_games:
            if game.get('character_id') == character_id:
                return game
        return None
    
    @staticmethod
    def add_character(user_data, character_data):
        """Mock add_character - adds character to user"""
        if 'characters' not in user_data:
            user_data['characters'] = []
        user_data['characters'].append(character_data)
        return user_data
    
    @staticmethod
    def add_to_active(user_data, game_data):
        """Mock add_to_active - adds game to active games"""
        if 'active_games' not in user_data:
            user_data['active_games'] = []
        user_data['active_games'].append(game_data)
        return user_data
    
    @staticmethod
    def add_to_completed(user_data, game_data):
        """Mock add_to_completed - moves game to completed"""
        if 'completed_games' not in user_data:
            user_data['completed_games'] = []
        user_data['completed_games'].append(game_data)
        return user_data
    
    @staticmethod
    def remove_from_active(user_data, game_id):
        """Mock remove_from_active - removes game from active"""
        if 'active_games' in user_data:
            user_data['active_games'] = [
                game for game in user_data['active_games'] 
                if game.get('game_id') != game_id
            ]
        return user_data
    
    @staticmethod
    def update_character_level(user_data, character_id, new_level):
        """Mock update_character_level - updates character level"""
        if 'characters' in user_data:
            for character in user_data['characters']:
                if character.get('character_id') == character_id:
                    character['level'] = new_level
        return user_data

# Export mock functions to replace real imports
get_game_by_id = MockGameManager.get_game_by_id
append_message_to_game = MockGameManager.append_message_to_game
create_new_game = MockGameManager.create_new_game
get_games_for_character = MockGameManager.get_games_for_character

get_character_by_active_game_id = MockUserRecordSchema.get_character_by_active_game_id
get_character_by_game_id = MockUserRecordSchema.get_character_by_game_id
get_active_game = MockUserRecordSchema.get_active_game
add_character = MockUserRecordSchema.add_character
add_to_active = MockUserRecordSchema.add_to_active
add_to_completed = MockUserRecordSchema.add_to_completed
remove_from_active = MockUserRecordSchema.remove_from_active
update_character_level = MockUserRecordSchema.update_character_level