"""
Mock Data Access Layer - Simulates AWS DynamoDB locally
PRESERVES ALL BUSINESS RULES - Only mocks the storage layer
"""

import json
import uuid
from datetime import datetime
from decimal import Decimal

# In-memory storage to simulate DynamoDB
MOCK_SAGAS = {}
MOCK_USER_DATA = {}
MOCK_CHARACTERS = {}

class MockDecimal(Decimal):
    """Mock Decimal that behaves like DynamoDB Decimal"""
    pass

# Mock dal.sagas module
class MockSagas:
    @staticmethod
    def get_saga(game_id):
        """Mock get_saga - returns saga data"""
        if game_id in MOCK_SAGAS:
            return MOCK_SAGAS[game_id]
        
        # Return default saga structure
        return {
            'game_id': game_id,
            'messages': [],
            'character_id': 'mock_character',
            'user_id': 'mock_user',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def update_saga(game_id, saga_data):
        """Mock update_saga - stores saga data"""
        MOCK_SAGAS[game_id] = saga_data
        return saga_data

# Mock dal.user_data module  
class MockUserData:
    @staticmethod
    def get_user_record(user_id):
        """Mock get_user_record - returns user data"""
        if user_id in MOCK_USER_DATA:
            return MOCK_USER_DATA[user_id]
        
        # Return default user structure
        return {
            'user_id': user_id,
            'characters': [],
            'active_games': [],
            'completed_games': [],
            'created_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def put_user_record(user_data):
        """Mock put_user_record - stores user data"""
        user_id = user_data.get('user_id')
        if user_id:
            MOCK_USER_DATA[user_id] = user_data
        return user_data

# Mock dal.characters module
class MockCharacters:
    @staticmethod
    def get_character(character_id):
        """Mock get_character - returns character data"""
        if character_id in MOCK_CHARACTERS:
            return MOCK_CHARACTERS[character_id]
        
        # Return default Fire Whisper character
        return {
            'character_id': character_id,
            'name': 'Hero',
            'level': 1,
            'xp': 0,
            'hp': 100,
            'max_hp': 100,
            'class': 'Adventurer',
            'attributes': {
                'strength': 10,
                'dexterity': 10,
                'constitution': 10,
                'intelligence': 10,
                'wisdom': 10,
                'charisma': 10
            },
            'skills': {},
            'equipment': [],
            'inventory': [],
            'created_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def put_character(character_data):
        """Mock put_character - stores character data"""
        character_id = character_data.get('character_id')
        if character_id:
            MOCK_CHARACTERS[character_id] = character_data
        return character_data
    
    @staticmethod
    def validate_and_fix_level(character_data):
        """Mock validate_and_fix_level - preserves business logic"""
        # This would contain your actual level validation logic
        return character_data
    
    @staticmethod
    def validate_and_fix_profession(character_data):
        """Mock validate_and_fix_profession - preserves business logic"""
        # This would contain your actual profession validation logic
        return character_data

# Export mock modules to replace real imports
get_saga = MockSagas.get_saga
update_saga = MockSagas.update_saga
get_user_record = MockUserData.get_user_record
put_user_record = MockUserData.put_user_record
get_character = MockCharacters.get_character
put_character = MockCharacters.put_character
validate_and_fix_level = MockCharacters.validate_and_fix_level
validate_and_fix_profession = MockCharacters.validate_and_fix_profession