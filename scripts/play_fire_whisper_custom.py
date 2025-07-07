#!/usr/bin/env python3
"""
Fire Whisper RPG - Custom Character Play
Create your own character and play with real Claude AI
"""

import sys
import os
import json
import uuid
from datetime import datetime

# Change to backend directory for proper imports
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
original_dir = os.getcwd()
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.dirname(backend_dir))

# Mock ONLY the AWS dependencies BEFORE importing backend modules
import local_mocks.mock_dal as mock_dal
import local_mocks.mock_utils as mock_utils
import local_mocks.mock_claude_local as mock_claude_local

# Replace ONLY the AWS infrastructure imports - Use local Claude API instead of AWS Bedrock
sys.modules['dal.sagas'] = mock_dal
sys.modules['dal.user_data'] = mock_dal  
sys.modules['dal.characters'] = mock_dal
sys.modules['utils.game_manager'] = mock_utils
sys.modules['utils.user_record_schema'] = mock_utils

# Replace AWS Bedrock Claude calls with local Claude API calls
sys.modules['claude_haiku.claude_haiku_create_character'] = mock_claude_local
sys.modules['claude_haiku.claude_haiku_create_saga'] = mock_claude_local
sys.modules['claude_haiku.claude_haiku_take_turn'] = mock_claude_local

# Now import your actual backend handlers (they will use local Claude API)
from create_character import handler as create_character_handler
from create_saga import handler as create_saga_handler
from take_turn_enhanced import handler as take_turn_handler

class CustomFireWhisperGame:
    """Custom Fire Whisper RPG with character creation"""
    
    def __init__(self):
        self.user_id = "player_" + str(uuid.uuid4())[:8]
        self.character_id = None
        self.game_id = None
        
        print("🔥 FIRE WHISPER RPG - CREATE YOUR HERO")
        print("=" * 60)
        print("🎭 Create your custom character")
        print("🌟 Choose your saga setting")
        print("🤖 Play with real Claude AI")
        print()
    
    def create_mock_event(self, body_data):
        """Create mock Lambda event"""
        return {
            'requestContext': {
                'authorizer': {
                    'jwt': {
                        'claims': {
                            'sub': self.user_id
                        }
                    }
                }
            },
            'body': json.dumps(body_data)
        }
    
    def create_mock_context(self):
        """Create mock Lambda context"""
        return type('MockContext', (), {
            'aws_request_id': str(uuid.uuid4()),
            'function_name': 'fire_whisper_game',
            'memory_limit_in_mb': 512,
            'remaining_time_in_millis': lambda: 30000
        })()
    
    def get_character_details(self):
        """Get character details from player"""
        
        print("🎭 CHARACTER CREATION")
        print("=" * 30)
        
        # Get character name
        while True:
            name = input("Character Name (or press Enter for random): ").strip()
            if not name:
                name = ""  # Let Claude generate random name
                break
            elif len(name) >= 2:
                break
            else:
                print("Name must be at least 2 characters long.")
        
        # Get race
        print("\\nAvailable Races:")
        races = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Tiefling", "Gnome", "Half-Elf", "Half-Orc"]
        for i, race in enumerate(races, 1):
            print(f"  {i}. {race}")
        
        while True:
            try:
                choice = input("\\nChoose race (1-9 or type custom): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 9:
                    race = races[int(choice) - 1]
                    break
                elif choice and not choice.isdigit():
                    race = choice.title()
                    break
                else:
                    race = ""  # Random
                    break
            except:
                print("Invalid choice. Try again.")
        
        # Get gender
        print("\\nGender:")
        genders = ["Male", "Female", "Non-binary", "Other"]
        for i, gender in enumerate(genders, 1):
            print(f"  {i}. {gender}")
        
        while True:
            try:
                choice = input("\\nChoose gender (1-4 or type custom): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 4:
                    gender = genders[int(choice) - 1]
                    break
                elif choice and not choice.isdigit():
                    gender = choice.title()
                    break
                else:
                    gender = ""  # Random
                    break
            except:
                print("Invalid choice. Try again.")
        
        # Get profession/class
        print("\\nAvailable Classes:")
        classes = ["Fighter", "Ranger", "Wizard", "Rogue", "Cleric", "Barbarian", "Bard", "Paladin", "Sorcerer", "Warlock"]
        for i, cls in enumerate(classes, 1):
            print(f"  {i}. {cls}")
        
        while True:
            try:
                choice = input("\\nChoose class (1-10 or type custom): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 10:
                    profession = classes[int(choice) - 1]
                    break
                elif choice and not choice.isdigit():
                    profession = choice.title()
                    break
                else:
                    profession = ""  # Random
                    break
            except:
                print("Invalid choice. Try again.")
        
        return name, race, gender, profession
    
    def get_saga_settings(self):
        """Get saga settings from player"""
        
        print("\\n🌟 SAGA CREATION")
        print("=" * 30)
        
        # Get setting
        print("Adventure Settings:")
        settings = [
            "Mystical Forest", "Ancient Ruins", "Haunted Castle", "Desert Oasis", 
            "Mountain Peaks", "Coastal Village", "Underground Caverns", "Floating Islands",
            "Frozen Wasteland", "Volcanic Realm"
        ]
        for i, setting in enumerate(settings, 1):
            print(f"  {i}. {setting}")
        
        while True:
            try:
                choice = input("\\nChoose setting (1-10 or type custom): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 10:
                    setting = settings[int(choice) - 1]
                    break
                elif choice and not choice.isdigit():
                    setting = choice.title()
                    break
                else:
                    setting = "Mystical Forest"  # Default
                    break
            except:
                print("Invalid choice. Try again.")
        
        # Get difficulty
        print("\\nDifficulty Levels:")
        difficulties = ["Story", "Adventurer", "Hero"]
        descriptions = [
            "Story - Narrative focus, forgiving combat",
            "Adventurer - Balanced challenge", 
            "Hero - Tactical thinking required, death is possible"
        ]
        for i, (diff, desc) in enumerate(zip(difficulties, descriptions), 1):
            print(f"  {i}. {desc}")
        
        while True:
            try:
                choice = input("\\nChoose difficulty (1-3): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= 3:
                    difficulty = difficulties[int(choice) - 1]
                    break
                else:
                    difficulty = "Adventurer"  # Default
                    break
            except:
                print("Invalid choice. Try again.")
        
        return setting, difficulty
    
    def create_character(self, name, race, gender, profession):
        """Create character with real Claude AI"""
        
        print("\\n⚡ Creating your character with Claude AI...")
        
        event = self.create_mock_event({
            'name': name,
            'race': race,
            'gender': gender,
            'profession': profession
        })
        
        context = self.create_mock_context()
        
        try:
            response = create_character_handler(event, context)
            
            if response['statusCode'] == 200:
                character_data = json.loads(response['body'])
                self.character_id = character_data['character_id']
                
                print("\\n✅ Character Created Successfully!")
                print("=" * 40)
                identity = character_data.get('IDENTITY', {})
                progression = character_data.get('PROGRESSION', {})
                attributes = character_data.get('ATTRIBUTES', {})
                
                print(f"Name: {identity.get('name', 'Unknown')}")
                print(f"Race: {identity.get('race', 'Unknown')}")
                print(f"Gender: {identity.get('gender', 'Unknown')}")
                print(f"Class: {identity.get('profession', 'Unknown')}")
                print(f"Level: {progression.get('level', 1)}")
                print(f"HP: {character_data.get('VITALITY', {}).get('hitPoints', 'Unknown')}")
                print("\\nAttributes:")
                for attr, value in attributes.items():
                    print(f"  {attr.title()}: {value}")
                
                return character_data
            else:
                print(f"❌ Character creation failed: {response}")
                return None
                
        except Exception as e:
            print(f"❌ Character creation error: {e}")
            return None
    
    def create_saga(self, setting, difficulty):
        """Create saga with real Claude AI"""
        
        print(f"\\n⚡ Creating your {setting} adventure with Claude AI...")
        
        event = self.create_mock_event({
            'characterId': self.character_id,
            'setting': setting,
            'difficulty': difficulty
        })
        
        context = self.create_mock_context()
        
        try:
            response = create_saga_handler(event, context)
            
            if response['statusCode'] == 200:
                game_data = json.loads(response['body'])
                self.game_id = game_data['game_id']
                
                print("\\n✅ Adventure Created Successfully!")
                print("=" * 40)
                print(f"Quest: {game_data.get('game_name', 'Unknown')}")
                print(f"Setting: {setting}")
                print(f"Difficulty: {difficulty}")
                
                # Show the opening scene
                messages = game_data.get('messages', [])
                if len(messages) >= 2:
                    print("\\n📖 YOUR ADVENTURE BEGINS")
                    print("=" * 50)
                    print(messages[1])  # The AI response (opening scene)
                    print("=" * 50)
                
                return game_data
            else:
                print(f"❌ Saga creation failed: {response}")
                return None
                
        except Exception as e:
            print(f"❌ Saga creation error: {e}")
            return None
    
    def take_turn(self, player_action):
        """Process turn with real Claude AI"""
        
        event = self.create_mock_event({
            'game_id': self.game_id,
            'message': player_action
        })
        
        context = self.create_mock_context()
        
        try:
            response = take_turn_handler(event, context)
            
            if response['statusCode'] == 200:
                body = json.loads(response['body'])
                ai_response = body.get('ai_response', body.get('response', 'No response'))
                
                print("\\n📖 " + "=" * 50)
                print(ai_response)
                print("=" * 52)
                
                return ai_response
            else:
                print(f"❌ Turn failed: {response}")
                return None
                
        except Exception as e:
            print(f"❌ Turn error: {e}")
            return None
    
    def play_game(self):
        """Main game loop"""
        
        # Character creation
        name, race, gender, profession = self.get_character_details()
        character_data = self.create_character(name, race, gender, profession)
        
        if not character_data:
            print("Failed to create character. Exiting.")
            return
        
        # Saga creation
        setting, difficulty = self.get_saga_settings()
        game_data = self.create_saga(setting, difficulty)
        
        if not game_data:
            print("Failed to create saga. Exiting.")
            return
        
        # Game loop
        print("\\n🎮 GAME COMMANDS:")
        print("  • Type your action or choose 1-4")
        print("  • 'quit' to exit")
        print("  • 'status' to see character info")
        print("  • 'help' for more commands")
        print()
        
        turn_count = 0
        while True:
            turn_count += 1
            print(f"\\n🎯 Turn {turn_count}")
            print("─" * 20)
            
            try:
                player_input = input("🎮 Your action: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            
            if player_input.lower() == 'quit':
                break
            elif player_input.lower() == 'status':
                self._show_character_status()
                continue
            elif player_input.lower() == 'help':
                self._show_help()
                continue
            elif not player_input:
                continue
            
            # Process turn
            response = self.take_turn(player_input)
            
            if not response:
                print("Failed to get response. Try again.")
                continue
            
            # Check for saga completion
            if "Congratulations, you have completed this Saga!" in response:
                print("\\n🎊 SAGA COMPLETED!")
                print("Your Fire Whisper adventure has reached its epic conclusion!")
                break
        
        print("\\n👋 Thanks for playing Fire Whisper RPG!")
    
    def _show_character_status(self):
        """Show character status"""
        if self.character_id:
            character = mock_dal.get_character(self.character_id)
            print(f"\\n👤 CHARACTER STATUS")
            print("-" * 20)
            identity = character.get('IDENTITY', {})
            progression = character.get('PROGRESSION', {})
            vitality = character.get('VITALITY', {})
            print(f"Name: {identity.get('name', 'Unknown')}")
            print(f"Race: {identity.get('race', 'Unknown')}")
            print(f"Class: {identity.get('profession', 'Unknown')}")
            print(f"Level: {progression.get('level', 1)}")
            print(f"XP: {progression.get('experience', 0)}")
            print(f"HP: {vitality.get('hitPoints', 'Unknown')}/{vitality.get('maxHitPoints', 'Unknown')}")
    
    def _show_help(self):
        """Show help"""
        print("\\n📚 FIRE WHISPER RPG - HELP")
        print("=" * 30)
        print("🎮 How to Play:")
        print("   • Choose from 4 options presented after each scene")
        print("   • Options 1-3 are curated choices")
        print("   • Option 4 lets you describe your own action")
        print("   • Dice rolls happen for risky actions")
        print("\\n🎯 Commands:")
        print("   • help - Show this help")
        print("   • status - Show character status")
        print("   • quit - End adventure")

def main():
    """Main function"""
    
    try:
        game = CustomFireWhisperGame()
        game.play_game()
    except KeyboardInterrupt:
        print("\\n\\n👋 Adventure interrupted. Thanks for playing!")
    finally:
        # Change back to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    main()