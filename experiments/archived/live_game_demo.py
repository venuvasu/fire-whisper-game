#!/usr/bin/env python3
"""
Live Game Demo - Stream the enhanced Fire Whisper experience to terminal
Watch the AI play with full narrative integration + YAML output generation
"""

import sys
import os
import time
import yaml
import gzip
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.ai_integration import AIIntegrationLayer


class GameSession:
    """Track and record game session data"""
    
    def __init__(self):
        self.session_data = {
            'session_info': {
                'timestamp': datetime.now().isoformat(),
                'system_version': 'enhanced_v1.0',
                'character': None,
                'total_turns': 0,
                'total_xp_gained': 0,
                'total_loot_found': 0
            },
            'turns': [],
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
    
    def add_turn(self, turn_data):
        """Add a turn to the session"""
        self.session_data['turns'].append(turn_data)
        self.session_data['session_info']['total_turns'] += 1
        
        # Update metrics
        if turn_data.get('xp_gained', 0) > 0:
            self.session_data['session_info']['total_xp_gained'] += turn_data['xp_gained']
            self.session_data['enhancements_detected']['xp_integration'] += 1
        
        if turn_data.get('loot_found', 0) > 0:
            self.session_data['session_info']['total_loot_found'] += turn_data['loot_found']
            self.session_data['enhancements_detected']['loot_discoveries'] += 1
        
        if turn_data.get('has_dice_integration', False):
            self.session_data['enhancements_detected']['dice_integration'] += 1
        
        if turn_data.get('has_emberlyn_moment', False):
            self.session_data['enhancements_detected']['emberlyn_moments'] += 1
        
        if turn_data.get('behavior_warning_level', 0) > 0:
            self.session_data['enhancements_detected']['behavior_warnings'] += 1
        
        if turn_data.get('stakes_level', 'medium') == 'high':
            self.session_data['enhancements_detected']['stakes_escalations'] += 1
        
        # Performance tracking
        response_time = turn_data.get('response_time', 0)
        self.session_data['performance_metrics']['total_response_time'] += response_time
        self.session_data['performance_metrics']['api_calls'] += 1
        self.session_data['performance_metrics']['average_response_time'] = (
            self.session_data['performance_metrics']['total_response_time'] / 
            self.session_data['performance_metrics']['api_calls']
        )
    
    def set_character(self, character_data):
        """Set initial character data"""
        self.session_data['session_info']['character'] = character_data
    
    def save_yaml(self, filename=None):
        """Save session data as compressed YAML"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fire_whisper_session_{timestamp}.yaml.gz"
        
        # Convert to YAML
        yaml_content = yaml.dump(self.session_data, default_flow_style=False, indent=2)
        
        # Compress and save
        with gzip.open(filename, 'wt', encoding='utf-8') as f:
            f.write(yaml_content)
        
        return filename


def print_separator(title=""):
    print("\n" + "="*80)
    if title:
        print(f"🎮 {title}")
    print("="*80)


def print_response(response, title="", session=None):
    if title:
        print(f"\n🎯 {title}")
        print("-" * 60)
    
    narrative = response['narrative']
    print(narrative)
    
    # Analyze enhancements
    turn_data = {
        'title': title,
        'player_action': getattr(print_response, 'last_action', ''),
        'narrative': narrative,
        'xp_gained': 0,
        'loot_found': 0,
        'has_dice_integration': False,
        'has_emberlyn_moment': False,
        'behavior_warning_level': 0,
        'stakes_level': 'medium',
        'response_time': getattr(print_response, 'last_response_time', 0),
        'mechanical_results': {},
        'character_status': {}
    }
    
    # Show mechanical results if any
    if response.get('mechanical_results'):
        mech = response['mechanical_results']
        turn_data['mechanical_results'] = {
            'dice_rolls': [],
            'xp_awards': [],
            'loot_discovered': []
        }
        
        if mech.get('dice_rolls'):
            print(f"\n🎲 DICE MECHANICS:")
            for roll in mech['dice_rolls']:
                roll_info = {
                    'type': roll.roll_type,
                    'base_roll': roll.base_roll,
                    'modifiers': dict(roll.modifiers),
                    'total': roll.base_roll + sum(roll.modifiers.values()),
                    'target': roll.target,
                    'success': roll.success
                }
                turn_data['mechanical_results']['dice_rolls'].append(roll_info)
                print(f"   {roll.roll_type}: {roll.base_roll} + {sum(roll.modifiers.values())} = {roll.base_roll + sum(roll.modifiers.values())} vs {roll.target} → {'SUCCESS' if roll.success else 'FAILURE'}")
            
            turn_data['has_dice_integration'] = True
        
        if mech.get('xp_awards'):
            print(f"\n✨ XP REWARDS:")
            for xp in mech['xp_awards']:
                xp_info = {
                    'amount': xp['xp_awarded'],
                    'reason': xp['reason'],
                    'new_total': xp['new_xp'],
                    'level_up': xp.get('level_up', False)
                }
                turn_data['mechanical_results']['xp_awards'].append(xp_info)
                turn_data['xp_gained'] += xp['xp_awarded']
                print(f"   +{xp['xp_awarded']} XP for {xp['reason']} (Total: {xp['new_xp']})")
                if xp.get('level_up'):
                    print(f"   🎉 LEVEL UP! Now Level {xp['new_level']}!")
        
        if mech.get('loot_discovered'):
            print(f"\n💎 LOOT FOUND:")
            for loot in mech['loot_discovered']:
                loot_info = {
                    'name': loot['name'],
                    'type': loot['type'],
                    'effect': loot['effect']
                }
                turn_data['mechanical_results']['loot_discovered'].append(loot_info)
                turn_data['loot_found'] += 1
                print(f"   {loot['name']} - {loot['effect']}")
    
    # Check for narrative enhancements
    narrative_lower = narrative.lower()
    
    # Dice integration check
    dice_indicators = ['strength', 'combat', 'charisma', 'skilled', 'drawing', 'natural', 'approach']
    if any(indicator in narrative_lower for indicator in dice_indicators):
        turn_data['has_dice_integration'] = True
    
    # Emberlyn moment check
    if 'emberlyn' in narrative_lower:
        turn_data['has_emberlyn_moment'] = True
    
    # Show behavior tracking
    if response.get('behavior_info'):
        behavior = response['behavior_info']
        turn_data['behavior_warning_level'] = behavior.get('warning_level', 0)
        turn_data['stakes_level'] = behavior.get('stakes_level', 'medium')
        
        if behavior.get('warning_level', 0) > 0:
            print(f"\n⚠️ BEHAVIOR WARNING: Level {behavior['warning_level']}")
        print(f"🎚️ Stakes Level: {behavior.get('stakes_level', 'medium').upper()}")
    
    # Character status
    if response.get('character'):
        char = response['character']
        turn_data['character_status'] = {
            'level': char['level'],
            'xp': char['xp'],
            'hp': f"{char['resources']['hp']}/{char['resources']['max_hp']}",
            'energy': f"{char['resources']['energy']}/{char['resources']['max_energy']}"
        }
    
    # Add to session
    if session:
        session.add_turn(turn_data)


def live_demo(save_yaml=True):
    """Run a live demo of the enhanced Fire Whisper system"""
    
    # Initialize session tracking
    session = GameSession() if save_yaml else None
    
    print_separator("FIRE WHISPER ENHANCED SYSTEM DEMO")
    print("🧚‍♀️ Starting enhanced RPG experience...")
    print("📊 Watch for narrative integration of mechanics!")
    if save_yaml:
        print("💾 Session will be saved as compressed YAML file")
    
    # Load API key
    from dotenv import load_dotenv
    load_dotenv('.env.local')
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        print("❌ No API key found!")
        return
    
    # Create character
    character_data = {
        'name': 'Kira the Bold',
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
    
    if session:
        session.set_character(character_data)
    
    print(f"\n👤 CHARACTER: {character_data['name']} - Level {character_data['level']} {character_data['class']}")
    print(f"💪 STR: {character_data['stats']['strength']} | 🏃 DEX: {character_data['stats']['dexterity']} | 🧠 INT: {character_data['stats']['intelligence']} | 💬 CHA: {character_data['stats']['charisma']}")
    print(f"❤️ HP: {character_data['resources']['hp']}/{character_data['resources']['max_hp']} | ⚡ Energy: {character_data['resources']['energy']}/{character_data['resources']['max_energy']}")
    
    try:
        # Initialize game
        ai_integration = AIIntegrationLayer(api_key)
        print("\n🔧 Enhanced AI Integration loaded...")
        
        # Start game
        print("\n⏳ Starting new adventure...")
        start_time = time.time()
        game_result = ai_integration.start_new_game(character_data)
        print_response.last_response_time = time.time() - start_time
        print_response.last_action = "Game Start"
        
        print_separator("GAME START")
        print_response(game_result, "Emberlyn's Introduction", session)
        
        # Play through several actions
        actions = [
            "I attack the enemy with my weapon",
            "I try to heal myself with divine magic", 
            "I search the area for useful items",
            "I attempt to negotiate with the next opponent",
            "I use my knowledge to assess the situation"
        ]
        
        for i, action in enumerate(actions, 1):
            print_separator(f"TURN {i}")
            print(f"🎮 PLAYER ACTION: {action}")
            print("\n⏳ Processing enhanced response...")
            
            # Track response time
            start_time = time.time()
            response = ai_integration.process_player_action(action)
            response_time = time.time() - start_time
            
            print_response.last_response_time = response_time
            print_response.last_action = action
            
            print_response(response, f"Enhanced Response #{i}", session)
            
            # Show character progression
            char = response['character']
            print(f"\n📊 CHARACTER STATUS:")
            print(f"   Level: {char['level']} | XP: {char['xp']} | HP: {char['resources']['hp']}/{char['resources']['max_hp']} | Energy: {char['resources']['energy']}/{char['resources']['max_energy']}")
            print(f"   Response Time: {response_time:.2f}s")
            
            # Pause between actions
            print("\n⏸️ [Pausing for 2 seconds...]")
            time.sleep(2)
        
        print_separator("DEMO COMPLETE")
        print("🎉 Enhanced Fire Whisper system demonstration complete!")
        
        if session:
            # Save YAML file
            filename = session.save_yaml()
            print(f"\n💾 Session saved as: {filename}")
            
            # Show session summary
            print(f"\n📊 SESSION SUMMARY:")
            print(f"   Total Turns: {session.session_data['session_info']['total_turns']}")
            print(f"   Total XP Gained: {session.session_data['session_info']['total_xp_gained']}")
            print(f"   Total Loot Found: {session.session_data['session_info']['total_loot_found']}")
            print(f"   Average Response Time: {session.session_data['performance_metrics']['average_response_time']:.2f}s")
            
            print(f"\n✨ ENHANCEMENTS DETECTED:")
            enhancements = session.session_data['enhancements_detected']
            print(f"   🎲 Dice Integration: {enhancements['dice_integration']} times")
            print(f"   ✨ XP Integration: {enhancements['xp_integration']} times")
            print(f"   💎 Loot Discoveries: {enhancements['loot_discoveries']} times")
            print(f"   🧚‍♀️ Emberlyn Moments: {enhancements['emberlyn_moments']} times")
            print(f"   🎚️ Stakes Escalations: {enhancements['stakes_escalations']} times")
            print(f"   ⚠️ Behavior Warnings: {enhancements['behavior_warnings']} times")
        
        print("\n🎯 RESULT: Premium RPG experience ready for players!")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Fire Whisper Live Demo')
    parser.add_argument('--no-yaml', action='store_true', help='Skip YAML output generation')
    args = parser.parse_args()
    
    live_demo(save_yaml=not args.no_yaml)