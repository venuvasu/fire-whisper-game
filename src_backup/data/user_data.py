"""
Mock DAL User Data - Preserves business logic, mocks AWS infrastructure
"""

# Mock user data storage (in real AWS this would be DynamoDB)
mock_user_records = {}

def get_user_record(user_id):
    """Mock get user record - preserves your business logic"""
    
    # In real AWS: Queries DynamoDB
    # Mock: Return structure that matches your real data
    
    if user_id not in mock_user_records:
        # Create default user record matching your real structure
        mock_user_records[user_id] = {
            'user_id': user_id,
            'characters': [
                {
                    'character_id': f'char_{user_id}',
                    'character_name': 'Hero',
                    'character_class': 'Adventurer',
                    'level': 1,
                    'experience_points': 0,
                    'hit_points': 100,
                    'active_games': [],
                    'completed_games': []
                }
            ]
        }
    
    print(f"👤 Mock DAL: Retrieved user record for {user_id}")
    return mock_user_records[user_id]

def put_user_record(user_record):
    """Mock put user record - preserves your business logic"""
    
    # In real AWS: Updates DynamoDB
    # Mock: Store in memory
    
    user_id = user_record.get('user_id')
    if user_id:
        mock_user_records[user_id] = user_record
        print(f"💾 Mock DAL: Saved user record for {user_id}")
    
    return True