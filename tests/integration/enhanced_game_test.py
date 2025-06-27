#!/usr/bin/env python3
"""
Enhanced Fire Whisper Game - Implementing Core RPG Psychology
"""
import sys
import os

# Add backend to path
sys.path.append('backend')

from claude_direct.enhanced_claude_api import take_turn_enhanced, create_character_creation_prompt, process_character_creation
from utils.character_sheet import CharacterSheet

class EnhancedFireWhisperGame:
    def __init__(self):
        self.character = None
        self.game_record = {
            "game_id": "enhanced-test",
            "messages": [],
            "game_active": True
        }
        self.model = "sonnet_35"
        self.session_xp = 0
        
    def start_game(self):
        """Start the enhanced game experience"""
        print("🔥 FIRE WHISPER - Enhanced RPG Experience 🔥")
        print("=" * 60)
        print("Implementing core RPG psychology for maximum engagement!")
        print("=" * 60)
        
        # Model selection
        model_input = input("Choose AI model (sonnet_35/claude_haiku_35/claude_haiku_30) [sonnet_35]: ").strip()
        valid_models = ["sonnet_35", "claude_haiku_35", "claude_haiku_30"]
        self.model = model_input if model_input in valid_models else "sonnet_35"
        print(f"🎯 Using model: {self.model}")
        
        # Character creation
        self.create_character()
        
        # Start adventure
        self.game_loop()
    
    def create_character(self):
        """Enhanced character creation experience"""
        print("\n" + "=" * 60)
        print(create_character_creation_prompt())
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-4): "))
                if 1 <= choice <= 4:
                    break
                else:
                    print("Please choose 1, 2, 3, or 4")
            except ValueError:
                print("Please enter a number")
        
        name = input("What is your character's name? [Adventurer]: ").strip() or "Adventurer"
        
        # Process character creation
        creation_result = process_character_creation(choice, name)
        if creation_result:
            self.character = creation_result['character']
            print("\n" + "=" * 60)
            print(creation_result['intro'])
            
            # Initialize game messages
            self.game_record['messages'] = [
                "You are Emberlyn, starting an adventure with this new character. Use their character sheet and respond to their choice.",
                creation_result['intro']
            ]
        else:
            print("Character creation failed, using default character")
            self.character = CharacterSheet()
    
    def game_loop(self):
        """Main game loop with enhanced feedback"""
        print("\n" + "🎮 GAME COMMANDS:")
        print("- Type your action normally")
        print("- 'sheet' - View character sheet")
        print("- 'quit' - Exit game")
        print("- 'restart' - Start new character")
        print("-" * 40)
        
        while True:
            user_input = input("\n🎮 Your action: ").strip()
            
            if user_input.lower() == 'quit':
                self.end_game()
                break
            elif user_input.lower() == 'restart':
                self.start_game()
                return
            elif user_input.lower() == 'sheet':
                self.show_character_sheet()
                continue
            elif not user_input:
                print("Please enter an action!")
                continue
            
            # Process turn
            self.process_turn(user_input)
    
    def process_turn(self, user_input):
        """Process a game turn with enhanced feedback"""
        try:
            # Add user input to game record
            self.game_record['messages'].append(user_input)
            
            # Get AI response with character context
            result = take_turn_enhanced(
                "enhanced-user", 
                self.game_record, 
                self.model, 
                self.character.to_dict()
            )
            
            # Update character from AI response (if modified)
            if 'character' in result:
                old_xp = self.character.xp
                self.character = CharacterSheet(result['character'])
                
                # Track XP gains for session
                if self.character.xp > old_xp:
                    xp_gained = self.character.xp - old_xp
                    self.session_xp += xp_gained
                    print(f"🌟 +{xp_gained} XP! (Session total: +{self.session_xp} XP)")
            
            # Display AI response
            print(f"\n🧚‍♀️ Emberlyn: {result['response']}")
            
            # Add AI response to game record
            self.game_record['messages'].append(result['response'])
            
            # Check for completion
            if "Congratulations, you have completed this Saga!" in result['response']:
                self.complete_saga()
                
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Try again or type 'quit' to exit")
    
    def show_character_sheet(self):
        """Display current character sheet"""
        print("\n" + "=" * 60)
        print("📊 CHARACTER SHEET")
        print(self.character.get_display_sheet())
        
        if self.character.skills:
            print("🎯 SKILLS:")
            for skill, level in self.character.skills.items():
                print(f"   {skill}: Level {level}")
        
        if self.character.achievements:
            print("\n🏆 ACHIEVEMENTS:")
            for achievement in self.character.achievements:
                print(f"   ✓ {achievement}")
        
        print("=" * 60)
    
    def complete_saga(self):
        """Handle saga completion"""
        print("\n" + "🎉" * 20)
        print("SAGA COMPLETED!")
        print("🎉" * 20)
        
        print(f"\n📊 FINAL STATS:")
        print(f"Character: {self.character.name} (Level {self.character.level})")
        print(f"Total XP: {self.character.xp}")
        print(f"Session XP Gained: +{self.session_xp}")
        print(f"Emberlyn Bond: Level {self.character.emberlyn_bond}")
        
        if self.character.achievements:
            print(f"\n🏆 ACHIEVEMENTS UNLOCKED:")
            for achievement in self.character.achievements:
                print(f"   ✓ {achievement}")
        
        print("\n💡 In the full version, you would unlock:")
        print("   • New character classes and abilities")
        print("   • Advanced campaigns and storylines") 
        print("   • Multiplayer features and sharing")
        print("   • Exclusive Emberlyn personalities")
        
        choice = input("\nStart a new adventure? (y/n): ").lower()
        if choice == 'y':
            self.start_game()
    
    def end_game(self):
        """End game with retention messaging"""
        print("\n" + "👋" * 15)
        print("Thanks for playing Fire Whisper!")
        
        if self.session_xp > 0:
            print(f"\n📈 SESSION SUMMARY:")
            print(f"XP Gained: +{self.session_xp}")
            print(f"Final Level: {self.character.level}")
            print(f"Time well spent building your legend!")
        
        print("\n💡 Remember: Your character and progress would be saved")
        print("in the full version, ready for your next adventure!")
        print("👋" * 15)

if __name__ == "__main__":
    game = EnhancedFireWhisperGame()
    game.start_game()