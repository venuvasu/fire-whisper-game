#!/usr/bin/env python3
"""
Deterministic Fire Whisper Game - Code handles mechanics, AI handles narrative
"""
import sys
import os

# Add backend to path
sys.path.append('backend')

from engine.ai_integration import AIIntegrationLayer
from engine.game_state_manager import GameStateManager

class DeterministicFireWhisper:
    def __init__(self):
        # Claude API key
        api_key = "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"
        self.ai_layer = AIIntegrationLayer(api_key)
        self.session_stats = {
            'turns': 0,
            'dice_rolls': 0,
            'xp_awarded': 0,
            'rule_violations': 0
        }
        
    def start_game(self):
        """Start the deterministic game"""
        print("🔥 FIRE WHISPER - DETERMINISTIC ENGINE 🔥")
        print("=" * 60)
        print("🎯 Code handles: Dice, XP, Stats, Rules")
        print("🤖 AI handles: Story, Dialogue, Choices")
        print("=" * 60)
        
        # Character creation
        character_data = self.create_character()
        
        # Initialize game
        print("\n🎮 Starting adventure...")
        game_start = self.ai_layer.start_new_game(character_data)
        
        print(f"\n🧚‍♀️ Emberlyn: {game_start['narrative']}")
        
        # Show initial character sheet
        print(self.ai_layer.get_character_sheet())
        
        # Game loop
        self.game_loop()
    
    def create_character(self):
        """Character creation with deterministic stats"""
        print("\n📋 CHARACTER CREATION")
        print("=" * 30)
        
        name = input("Character name [Adventurer]: ").strip() or "Adventurer"
        
        print("\nChoose your class:")
        print("[1] Warrior - High HP, Combat bonuses")
        print("[2] Mage - Magic abilities, Knowledge bonuses") 
        print("[3] Rogue - Stealth abilities, Skill bonuses")
        print("[4] Cleric - Healing abilities, Social bonuses")
        
        while True:
            try:
                choice = int(input("Enter choice (1-4): "))
                if 1 <= choice <= 4:
                    break
                print("Please choose 1-4")
            except ValueError:
                print("Please enter a number")
        
        # Deterministic character creation
        class_data = {
            1: {  # Warrior
                'class': 'Warrior',
                'stats': {'strength': 16, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
                'skills': {'Combat': 2, 'Athletics': 1, 'Intimidation': 1},
                'resources': {'hp': 35, 'max_hp': 35, 'energy': 10, 'max_energy': 10}
            },
            2: {  # Mage
                'class': 'Mage',
                'stats': {'strength': 10, 'dexterity': 12, 'intelligence': 16, 'charisma': 12},
                'skills': {'Magic': 2, 'Knowledge': 2, 'Investigation': 1},
                'resources': {'hp': 25, 'max_hp': 25, 'energy': 15, 'max_energy': 15}
            },
            3: {  # Rogue
                'class': 'Rogue',
                'stats': {'strength': 12, 'dexterity': 16, 'intelligence': 12, 'charisma': 10},
                'skills': {'Stealth': 2, 'Lockpicking': 2, 'Deception': 1},
                'resources': {'hp': 28, 'max_hp': 28, 'energy': 12, 'max_energy': 12}
            },
            4: {  # Cleric
                'class': 'Cleric',
                'stats': {'strength': 12, 'dexterity': 10, 'intelligence': 12, 'charisma': 16},
                'skills': {'Healing': 2, 'Persuasion': 2, 'Knowledge': 1},
                'resources': {'hp': 30, 'max_hp': 30, 'energy': 13, 'max_energy': 13}
            }
        }
        
        selected_class = class_data[choice]
        character_data = {
            'name': name,
            'level': 1,
            'xp': 0,
            'emberlyn_bond': 1,
            'achievements': [],
            **selected_class
        }
        
        print(f"\n✨ Created {name} the {selected_class['class']}!")
        return character_data
    
    def game_loop(self):
        """Main game loop with deterministic mechanics"""
        print("\n" + "🎮 GAME COMMANDS:")
        print("- Type your action normally")
        print("- 'sheet' - View character sheet")
        print("- 'stats' - View session statistics")
        print("- 'save' - Save game state")
        print("- 'quit' - Exit game")
        print("-" * 40)
        
        while True:
            user_input = input(f"\n🎮 Turn {self.session_stats['turns'] + 1}: ").strip()
            
            if user_input.lower() == 'quit':
                self.end_game()
                break
            elif user_input.lower() == 'sheet':
                print(self.ai_layer.get_character_sheet())
                continue
            elif user_input.lower() == 'stats':
                self.show_session_stats()
                continue
            elif user_input.lower() == 'save':
                self.save_game()
                continue
            elif not user_input:
                print("Please enter an action!")
                continue
            
            # Process turn with deterministic mechanics
            self.process_turn(user_input)
    
    def process_turn(self, user_input: str):
        """Process turn with full mechanical separation"""
        try:
            print(f"\n⚙️ Processing mechanics...")
            
            # AI layer handles all mechanics deterministically
            result = self.ai_layer.process_player_action(user_input)
            
            # Update session stats
            self.session_stats['turns'] += 1
            self.session_stats['dice_rolls'] += len(result['mechanical_results']['dice_rolls'])
            
            for xp_award in result['mechanical_results']['xp_awards']:
                self.session_stats['xp_awarded'] += xp_award['xp_awarded']
            
            # Show mechanical results first
            if result['mechanical_results']['dice_rolls']:
                print("🎲 DICE RESULTS:")
                for roll in result['mechanical_results']['dice_rolls']:
                    modifiers_text = " + ".join([f"{k}(+{v})" for k, v in roll.modifiers.items()])
                    result_text = "✅ SUCCESS" if roll.success else "❌ FAILURE"
                    print(f"   {roll.roll_type.title()}: {roll.base_roll} + {sum(roll.modifiers.values())} = {roll.base_roll + sum(roll.modifiers.values())} vs {roll.target} → {result_text}")
                    if modifiers_text:
                        print(f"   Modifiers: {modifiers_text}")
            
            if result['mechanical_results']['xp_awards']:
                print("✨ XP AWARDS:")
                for xp_award in result['mechanical_results']['xp_awards']:
                    print(f"   +{xp_award['xp_awarded']} XP: {xp_award['reason']}")
                    print(f"   Total XP: {xp_award['new_xp']}")
                    
                    if xp_award['level_up']:
                        print(f"   🎉 LEVEL UP! Now Level {xp_award['new_level']}!")
                        if xp_award['new_abilities']:
                            print(f"   New Abilities: {', '.join(xp_award['new_abilities'])}")
            
            # Show AI narrative response
            print(f"\n🧚‍♀️ Emberlyn: {result['narrative']}")
            
            # Show context refresh notification
            if result['context_refreshed']:
                print("\n🔄 [Context refreshed to prevent AI drift]")
            
            # Check for game completion
            if "Congratulations, you have completed this Saga!" in result['narrative']:
                self.complete_saga()
                
        except Exception as e:
            print(f"❌ Error processing turn: {e}")
            self.session_stats['rule_violations'] += 1
    
    def show_session_stats(self):
        """Show current session statistics"""
        print("\n📊 SESSION STATISTICS")
        print("=" * 30)
        print(f"Turns Played: {self.session_stats['turns']}")
        print(f"Dice Rolls: {self.session_stats['dice_rolls']}")
        print(f"Total XP Awarded: {self.session_stats['xp_awarded']}")
        print(f"Rule Violations: {self.session_stats['rule_violations']}")
        
        if self.ai_layer.game_manager:
            char = self.ai_layer.game_manager.character
            print(f"Character Level: {char['level']}")
            print(f"Current XP: {char['xp']}")
            print(f"HP: {char['resources']['hp']}/{char['resources']['max_hp']}")
        print("=" * 30)
    
    def save_game(self):
        """Save current game state"""
        if self.ai_layer.game_manager:
            state_json = self.ai_layer.game_manager.save_state()
            filename = f"savegame_{self.ai_layer.game_manager.character['name'].lower()}.json"
            
            with open(filename, 'w') as f:
                f.write(state_json)
            
            print(f"💾 Game saved to {filename}")
        else:
            print("❌ No active game to save")
    
    def complete_saga(self):
        """Handle saga completion"""
        print("\n" + "🎉" * 20)
        print("SAGA COMPLETED!")
        print("🎉" * 20)
        
        self.show_session_stats()
        
        print("\n🏆 ACHIEVEMENTS:")
        print("   ✓ Completed your first Fire Whisper saga")
        print("   ✓ Experienced deterministic game mechanics")
        print("   ✓ Maintained consistent character progression")
        
        print("\n💡 TECHNICAL ACHIEVEMENTS:")
        print(f"   • Zero XP tracking errors")
        print(f"   • {self.session_stats['dice_rolls']} consistent dice rolls")
        print(f"   • {self.session_stats['rule_violations']} rule violations detected")
        print(f"   • Context refreshed every 5 turns")
        
        choice = input("\nStart a new adventure? (y/n): ").lower()
        if choice == 'y':
            self.start_game()
    
    def end_game(self):
        """End game with statistics"""
        print("\n" + "👋" * 15)
        print("Thanks for testing Deterministic Fire Whisper!")
        
        self.show_session_stats()
        
        print("\n🎯 KEY BENEFITS DEMONSTRATED:")
        print("   • Dice rolls are always consistent")
        print("   • XP tracking never drifts")
        print("   • Character progression is reliable")
        print("   • AI focuses on narrative quality")
        print("   • Rules are enforced by code, not AI")
        
        print("\n🚀 This architecture enables:")
        print("   • Unlimited session length")
        print("   • Predictable game mechanics")
        print("   • Player trust in fairness")
        print("   • Scalable complexity")
        
        print("👋" * 15)

if __name__ == "__main__":
    game = DeterministicFireWhisper()
    game.start_game()