#!/usr/bin/env python3
"""
Interactive Full Game - Complete Fire Whisper RPG session with mixed input types
Live terminal streaming with YAML output at completion
"""

import sys
import os
import time
import yaml
import random
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.ai_integration import AIIntegrationLayer
from engine.option_generator import generate_contextual_options


class InteractiveGameSession:
    """Manages a complete interactive game session"""
    
    def __init__(self):
        self.session_data = {
            'session_info': {
                'timestamp': datetime.now().isoformat(),
                'system_version': 'interactive_full_game_v1.0',
                'character': None,
                'total_turns': 0,
                'total_xp_gained': 0,
                'total_loot_found': 0,
                'story_arc': 'Interactive Adventure',
                'input_types_used': {'options': 0, 'freeform': 0},
                'game_completed': False,
                'forced_exit': False
            },
            'turns': [],
            'story_progression': {
                'act_1_discovery': False,
                'act_2_investigation': False,
                'act_3_confrontation': False,
                'story_completed': False
            },
            'enhancements_detected': {
                'dice_integration': 0,
                'xp_integration': 0,
                'loot_discoveries': 0,
                'emberlyn_moments': 0,
                'stakes_escalations': 0,
                'behavior_warnings': 0
            },
            'performance_metrics': {
                'average_response_time': 0,
                'total_response_time': 0,
                'api_calls': 0
            }
        }
        
        self.ai_integration = None
        self.max_turns = 30
        
    def save_yaml(self, filename=None):
        """Save complete session as YAML"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"results/interactive_full_game_{timestamp}.yaml"
        
        os.makedirs('results', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(self.session_data, f, default_flow_style=False, indent=2)
        
        return filename
    
    def add_turn(self, turn_data):
        """Add turn data to session"""
        self.session_data['turns'].append(turn_data)
        self.session_data['session_info']['total_turns'] += 1
        
        # Update metrics
        if turn_data.get('xp_gained', 0) > 0:
            self.session_data['session_info']['total_xp_gained'] += turn_data['xp_gained']
        
        if turn_data.get('loot_found', 0) > 0:
            self.session_data['session_info']['total_loot_found'] += turn_data['loot_found']
            self.session_data['enhancements_detected']['loot_discoveries'] += 1
        
        # Enhancement detection
        if turn_data.get('has_dice_integration', False):
            self.session_data['enhancements_detected']['dice_integration'] += 1
        
        if turn_data.get('has_xp_integration', False):
            self.session_data['enhancements_detected']['xp_integration'] += 1
        
        if turn_data.get('has_emberlyn_moment', False):
            self.session_data['enhancements_detected']['emberlyn_moments'] += 1
        
        # Input type tracking
        if turn_data.get('input_type') == 'option':
            self.session_data['session_info']['input_types_used']['options'] += 1
        elif turn_data.get('input_type') == 'freeform':
            self.session_data['session_info']['input_types_used']['freeform'] += 1
        
        # Performance tracking
        response_time = turn_data.get('response_time', 0)
        self.session_data['performance_metrics']['total_response_time'] += response_time
        self.session_data['performance_metrics']['api_calls'] += 1
        if self.session_data['performance_metrics']['api_calls'] > 0:
            self.session_data['performance_metrics']['average_response_time'] = (
                self.session_data['performance_metrics']['total_response_time'] / 
                self.session_data['performance_metrics']['api_calls']
            )
    
    def enhanced_ai_prompt_with_options(self, player_input, action_analysis, mechanical_results, needs_refresh):
        """Create AI prompt with dynamic options"""
        
        character = self.ai_integration.game_manager.character
        
        # Generate contextual options
        story_context = {
            'turn_number': self.session_data['session_info']['total_turns'],
            'corruption_level': 'medium' if self.session_data['session_info']['total_turns'] < 15 else 'high',
            'character_health_ratio': character['resources']['hp'] / character['resources']['max_hp']
        }
        
        contextual_options = generate_contextual_options(
            f"Current situation after: {player_input}", 
            character, 
            story_context
        )
        
        prompt = f"""You are Emberlyn, the fairy companion in Fire Whisper RPG.

CURRENT CHARACTER STATE:
Name: {character['name']} (Level {character['level']} {character['class']})
Stats: STR {character['stats']['strength']} (+{max(0, (character['stats']['strength']-10)//2)}), DEX {character['stats']['dexterity']} (+{max(0, (character['stats']['dexterity']-10)//2)}), INT {character['stats']['intelligence']} (+{max(0, (character['stats']['intelligence']-10)//2)}), CHA {character['stats']['charisma']} (+{max(0, (character['stats']['charisma']-10)//2)})
Resources: {character['resources']['hp']}/{character['resources']['max_hp']} HP, {character['resources']['energy']}/{character['resources']['max_energy']} Energy
XP: {character['xp']} (Level {character['level']})

PLAYER ACTION: {player_input}

MECHANICAL RESULTS (ALREADY CALCULATED):"""
        
        # Add mechanical results
        for roll in mechanical_results.get('dice_rolls', []):
            result_text = "SUCCESS" if roll.success else "FAILURE"
            prompt += f"""
🎲 {roll.roll_type.title()} Roll: {roll.base_roll} + {sum(roll.modifiers.values())} = {roll.base_roll + sum(roll.modifiers.values())} vs {roll.target} → {result_text}"""
        
        for xp_award in mechanical_results.get('xp_awards', []):
            prompt += f"""
✨ XP Award: +{xp_award['xp_awarded']} for {xp_award['reason']} (Total: {xp_award['new_xp']})"""
            if xp_award.get('level_up'):
                prompt += f"""
🎉 LEVEL UP! Now Level {xp_award['new_level']}!"""
        
        for loot in mechanical_results.get('loot_discovered', []):
            prompt += f"""
💎 LOOT: {loot['name']} - {loot['effect']}"""
        
        prompt += f"""

RESPONSE REQUIREMENTS:
1. Describe what happens in the story (no explicit mechanics)
2. Give consequences based on success/failure
3. Present these contextual options:

{contextual_options}

4. End with: "What would you like to do?"

NEVER mention dice rolls, XP numbers, or mechanical calculations in your narrative.
Focus on story, dialogue, and atmosphere only."""
        
        return prompt
    
    def print_separator(self, title="", char="="):
        """Print formatted separator"""
        width = 80
        if title:
            print(f"\n{char * width}")
            print(f"🎮 {title}")
            print(f"{char * width}")
        else:
            print(f"{char * width}")
    
    def print_character_status(self, character):
        """Print current character status"""
        print(f"\n📊 CHARACTER STATUS:")
        print(f"   {character['name']} - Level {character['level']} {character['class']}")
        print(f"   HP: {character['resources']['hp']}/{character['resources']['max_hp']} | Energy: {character['resources']['energy']}/{character['resources']['max_energy']} | XP: {character['xp']}")
    
    def get_player_input(self, options_available=True):
        """Get player input - either option selection or freeform text"""
        
        if options_available:
            print(f"\n🎯 INPUT OPTIONS:")
            print(f"   • Enter 1-5 to select an option")
            print(f"   • Type anything else for custom action")
            print(f"   • Type 'quit' to end game")
        
        user_input = input(f"\n🎮 Your choice: ").strip()
        
        if user_input.lower() == 'quit':
            return None, 'quit'
        elif user_input in ['1', '2', '3', '4', '5']:
            return user_input, 'option'
        else:
            return user_input, 'freeform'
    
    def process_turn(self, player_input, input_type):
        """Process a single game turn"""
        
        turn_start = time.time()
        
        # Get action analysis and mechanical results
        action_analysis = self.ai_integration._analyze_player_action(player_input)
        mechanical_results = self.ai_integration._execute_mechanics(action_analysis)
        
        # Build enhanced prompt
        enhanced_prompt = self.enhanced_ai_prompt_with_options(
            player_input, action_analysis, mechanical_results, False
        )
        
        # Get AI response
        ai_response = self.ai_integration._call_ai(enhanced_prompt)
        response_time = time.time() - turn_start
        
        # Enhance with narrative integration
        behavior_info = {'warning_level': 0, 'stakes_level': 'medium'}
        context = {
            'level_up': any(award.get('level_up') for award in mechanical_results.get('xp_awards', [])),
            'low_resources': self.ai_integration._check_low_resources(),
            'behavior_warning': behavior_info.get('warning_level', 0),
            'stakes_level': behavior_info.get('stakes_level', 'medium')
        }
        
        enhanced_narrative = self.ai_integration.narrative_enhancer.enhance_response(
            ai_response,
            mechanical_results,
            self.ai_integration.game_manager.character,
            context
        )
        
        # Create turn data
        turn_data = {
            'turn_number': self.session_data['session_info']['total_turns'] + 1,
            'player_input': player_input,
            'input_type': input_type,
            'narrative': enhanced_narrative,
            'response_time': response_time,
            'xp_gained': sum(award['xp_awarded'] for award in mechanical_results.get('xp_awards', [])),
            'loot_found': len(mechanical_results.get('loot_discovered', [])),
            'has_dice_integration': any(word in enhanced_narrative.lower() for word in ['strength', 'charisma', 'skilled', 'drawing']),
            'has_xp_integration': any(word in enhanced_narrative.lower() for word in ['experience', 'understanding', 'stronger', 'wisdom']),
            'has_emberlyn_moment': 'emberlyn' in enhanced_narrative.lower(),
            'mechanical_results': {
                'dice_rolls': [{'type': roll.roll_type, 'result': roll.base_roll + sum(roll.modifiers.values()), 'success': roll.success} for roll in mechanical_results.get('dice_rolls', [])],
                'xp_awards': mechanical_results.get('xp_awards', []),
                'loot_discovered': mechanical_results.get('loot_discovered', [])
            }
        }
        
        self.add_turn(turn_data)
        
        return enhanced_narrative, mechanical_results, response_time
    
    def run_interactive_game(self):
        """Run the complete interactive game session"""
        
        self.print_separator("FIRE WHISPER - INTERACTIVE FULL GAME")
        print("🧚‍♀️ Welcome to Fire Whisper RPG!")
        print("🎯 Mix of option selection and freeform input")
        print("📊 Live streaming with YAML output at end")
        print("⏰ Maximum 30 turns (auto-exit if exceeded)")
        
        # Load API key
        from dotenv import load_dotenv
        load_dotenv('.env.local')
        api_key = os.getenv('CLAUDE_API_KEY')
        
        if not api_key:
            print("❌ No API key found!")
            return
        
        # Create character
        character_data = {
            'name': 'Kira Stormwind',
            'class': 'Cleric',
            'level': 1,
            'xp': 0,
            'stats': {
                'strength': 12,
                'dexterity': 14,
                'intelligence': 13,
                'charisma': 16
            },
            'resources': {
                'hp': 25,
                'max_hp': 25,
                'energy': 12,
                'max_energy': 12
            },
            'skills': {
                'Healing': 3,
                'Persuasion': 2,
                'Combat': 1
            },
            'achievements': [],
            'emberlyn_bond': 1
        }
        
        self.session_data['session_info']['character'] = character_data
        
        try:
            # Initialize game
            self.ai_integration = AIIntegrationLayer(api_key)
            print("\n🔧 Enhanced AI Integration loaded...")
            
            # Start game
            print("\n⏳ Starting interactive adventure...")
            game_result = self.ai_integration.start_new_game(character_data)
            
            self.print_separator("GAME START - EMBERLYN'S INTRODUCTION")
            print(game_result['narrative'])
            self.print_character_status(character_data)
            
            # Main game loop
            while self.session_data['session_info']['total_turns'] < self.max_turns:
                
                # Get player input
                player_input, input_type = self.get_player_input(True)
                
                if input_type == 'quit':
                    print("\n👋 Thanks for playing Fire Whisper!")
                    break
                
                # Process turn
                turn_number = self.session_data['session_info']['total_turns'] + 1
                self.print_separator(f"TURN {turn_number}", "-")
                
                if input_type == 'option':
                    print(f"🎯 SELECTED OPTION: {player_input}")
                else:
                    print(f"✍️ CUSTOM ACTION: {player_input}")
                
                print("\n⏳ Processing...")
                
                narrative, mechanical_results, response_time = self.process_turn(player_input, input_type)
                
                # Display results
                print(f"\n🎭 STORY RESPONSE:")
                print(narrative)
                
                # Show mechanical results
                if mechanical_results.get('dice_rolls'):
                    print(f"\n🎲 DICE RESULTS:")
                    for roll in mechanical_results['dice_rolls']:
                        print(f"   {roll.roll_type}: {roll.base_roll} + {sum(roll.modifiers.values())} = {roll.base_roll + sum(roll.modifiers.values())} vs {roll.target} → {'SUCCESS' if roll.success else 'FAILURE'}")
                
                if mechanical_results.get('xp_awards'):
                    print(f"\n✨ XP GAINED:")
                    for xp in mechanical_results['xp_awards']:
                        print(f"   +{xp['xp_awarded']} XP for {xp['reason']} (Total: {xp['new_xp']})")
                        if xp.get('level_up'):
                            print(f"   🎉 LEVEL UP! Now Level {xp['new_level']}!")
                
                if mechanical_results.get('loot_discovered'):
                    print(f"\n💎 LOOT DISCOVERED:")
                    for loot in mechanical_results['loot_discovered']:
                        print(f"   {loot['name']} - {loot['effect']}")
                
                # Show character status
                current_char = self.ai_integration.game_manager.character
                self.print_character_status(current_char)
                
                print(f"\n⏱️ Response Time: {response_time:.2f}s")
                print(f"📊 Turn {turn_number}/{self.max_turns} complete")
                
                # Check for story completion keywords
                if any(word in narrative.lower() for word in ['victory', 'complete', 'finished', 'end', 'triumph', 'success']):
                    print(f"\n🎉 STORY COMPLETION DETECTED!")
                    self.session_data['session_info']['game_completed'] = True
                    break
                
                # Brief pause
                time.sleep(1)
            
            # Handle max turns reached
            if self.session_data['session_info']['total_turns'] >= self.max_turns:
                print(f"\n⏰ MAXIMUM TURNS REACHED ({self.max_turns})")
                print("🚪 Forcing game exit...")
                self.session_data['session_info']['forced_exit'] = True
            
            # Game complete
            self.print_separator("GAME SESSION COMPLETE")
            
            # Save YAML
            filename = self.save_yaml()
            print(f"\n💾 Complete session saved as: {filename}")
            
            # Show final statistics
            print(f"\n📊 FINAL SESSION STATISTICS:")
            print(f"   Total Turns: {self.session_data['session_info']['total_turns']}")
            print(f"   Total XP Gained: {self.session_data['session_info']['total_xp_gained']}")
            print(f"   Total Loot Found: {self.session_data['session_info']['total_loot_found']}")
            print(f"   Average Response Time: {self.session_data['performance_metrics']['average_response_time']:.2f}s")
            
            print(f"\n🎮 INPUT TYPE BREAKDOWN:")
            print(f"   Option Selections: {self.session_data['session_info']['input_types_used']['options']}")
            print(f"   Freeform Text: {self.session_data['session_info']['input_types_used']['freeform']}")
            
            print(f"\n✨ ENHANCEMENTS DETECTED:")
            enhancements = self.session_data['enhancements_detected']
            print(f"   🎲 Dice Integration: {enhancements['dice_integration']} times")
            print(f"   ✨ XP Integration: {enhancements['xp_integration']} times")
            print(f"   💎 Loot Discoveries: {enhancements['loot_discoveries']} times")
            print(f"   🧚‍♀️ Emberlyn Moments: {enhancements['emberlyn_moments']} times")
            
            completion_status = "COMPLETED" if self.session_data['session_info']['game_completed'] else "FORCED EXIT" if self.session_data['session_info']['forced_exit'] else "USER QUIT"
            print(f"\n🎯 GAME STATUS: {completion_status}")
            print(f"💰 Premium RPG experience delivered!")
            
        except Exception as e:
            print(f"\n❌ Error during interactive game: {e}")
            import traceback
            traceback.print_exc()
            
            # Save partial session
            filename = self.save_yaml()
            print(f"💾 Partial session saved as: {filename}")


def main():
    """Run the interactive full game"""
    session = InteractiveGameSession()
    session.run_interactive_game()


if __name__ == "__main__":
    main()