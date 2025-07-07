#!/usr/bin/env python3
"""
Full Game Flow Test - Complete Fire Whisper RPG test with character creation
Includes: Character Creation (name, race, profession) → Saga Creation → Multiple Turns
Outputs full transcripts to YAML format
"""

import sys
import os
import json
import time
import random
import yaml
import uuid
from datetime import datetime
from typing import Dict, List, Any

# Setup paths
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
original_dir = os.getcwd()
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.dirname(backend_dir))

# Mock AWS dependencies
import local_mocks.mock_dal as mock_dal
import local_mocks.mock_utils as mock_utils
import local_mocks.mock_claude_local as mock_claude_local

sys.modules['dal.sagas'] = mock_dal
sys.modules['dal.user_data'] = mock_dal  
sys.modules['dal.characters'] = mock_dal
sys.modules['utils.game_manager'] = mock_utils
sys.modules['utils.user_record_schema'] = mock_utils
sys.modules['claude_haiku.claude_haiku_create_character'] = mock_claude_local
sys.modules['claude_haiku.claude_haiku_create_saga'] = mock_claude_local
sys.modules['claude_haiku.claude_haiku_take_turn'] = mock_claude_local

# Import backend handlers
from create_character import handler as create_character_handler
from create_saga import handler as create_saga_handler
from take_turn_enhanced import handler as take_turn_handler

from anthropic import Anthropic

# API key for testing
API_KEY = "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"

def estimate_tokens(text):
    """Rough token estimation"""
    return len(text) // 4

def full_context_strategy(messages):
    """Strategy A: Full Context (current approach)"""
    return messages.copy()

def hybrid_context_strategy(messages):
    """Strategy B: Hybrid Context (smart summarization)"""
    if len(messages) <= 6:
        return messages.copy()
    
    initial_prompt = messages[0]
    first_response = messages[1]
    recent_messages = messages[-4:]
    
    middle_count = (len(messages) - 6) // 2
    summary = f"[STORY SUMMARY]: Over {middle_count} previous turns, the player explored, made decisions, and progressed through the Fire Whisper adventure with Emberlyn's guidance."
    
    return [initial_prompt, first_response, summary] + recent_messages

def state_based_strategy(messages):
    """Strategy C: State-Based Context (minimal narrative)"""
    if len(messages) <= 4:
        return messages.copy()
    
    initial_prompt = messages[0]
    recent_messages = messages[-3:]
    
    state_summary = "[CURRENT STATE]: Fire Whisper RPG adventure in progress. Player has Emberlyn as fairy guide. Investigating threats and making story progress through choice-based gameplay."
    
    return [initial_prompt, state_summary] + recent_messages

class ContextAwareClaudeHandler:
    """Claude handler that applies context strategies"""
    
    def __init__(self, strategy_func, strategy_name):
        self.strategy_func = strategy_func
        self.strategy_name = strategy_name
        self.client = Anthropic(api_key=API_KEY)
        self.token_usage = []
        self.response_times = []
    
    def take_turn(self, user_id, game_record, haiku_model="claude_haiku_35"):
        """Take turn with context strategy applied"""
        
        messages = game_record.get('messages', [])
        
        if not messages or len(messages) < 2:
            raise ValueError("Message history must contain at least an initial prompt and one AI response.")
        
        # Apply context strategy
        filtered_messages = self.strategy_func(messages)
        
        # Estimate tokens
        total_text = " ".join(filtered_messages)
        estimated_tokens = estimate_tokens(total_text)
        self.token_usage.append(estimated_tokens)
        
        # Read system prompt
        try:
            with open("prompts/claude_system_prompt_turns.txt", "r") as f:
                system_prompt = f.read()
        except:
            system_prompt = "You are Emberlyn, the Fire Whisper RPG narrator."
        
        # Build Claude messages
        claude_messages = []
        for index, item in enumerate(filtered_messages):
            role = "assistant" if index % 2 == 1 else "user"

            if index == len(filtered_messages) - 1:
                dice_pool = [random.randint(1, 100) for _ in range(4)]
                item = f"""DICE POOL FOR THIS TURN: {dice_pool}
Use these dice results IN ORDER when rolls are needed. Do not mention this dice pool to the user.
Original player action: {item}
"""

            claude_messages.append({
                "role": role,
                "content": item
            })
        
        # Time the API call
        start_time = time.time()
        
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            system=system_prompt,
            messages=claude_messages
        )
        
        end_time = time.time()
        response_time = (end_time - start_time) * 1000
        self.response_times.append(response_time)
        
        return response.content[0].text

class FullGameFlowTester:
    """Complete Fire Whisper RPG test with full character creation flow"""
    
    def __init__(self):
        self.strategies = {
            "Full Context": full_context_strategy,
            "Hybrid Context": hybrid_context_strategy,
            "State-Based Context": state_based_strategy
        }
        
        # Detailed character templates with full creation data
        self.character_templates = [
            {
                "name": "Aria Moonwhisper",
                "race": "Elf",
                "gender": "Female", 
                "profession": "Ranger",
                "background": "Forest Guardian",
                "personality": "Wise and cautious, deeply connected to nature"
            },
            {
                "name": "Theron Brightblade", 
                "race": "Human",
                "gender": "Male",
                "profession": "Paladin",
                "background": "Noble Knight",
                "personality": "Honorable and brave, devoted to justice"
            },
            {
                "name": "Zara Ironforge",
                "race": "Dwarf", 
                "gender": "Female",
                "profession": "Fighter",
                "background": "Mountain Warrior",
                "personality": "Fierce and loyal, master of combat"
            },
            {
                "name": "Lyra Starweaver",
                "race": "Elf",
                "gender": "Female", 
                "profession": "Mage",
                "background": "Scholar of Ancient Arts",
                "personality": "Curious and intelligent, seeker of knowledge"
            },
            {
                "name": "Gareth Stormwind",
                "race": "Human",
                "gender": "Male",
                "profession": "Rogue", 
                "background": "Street Survivor",
                "personality": "Clever and resourceful, master of stealth"
            }
        ]
        
        # Detailed saga templates
        self.saga_templates = [
            {
                "setting": "Ancient Ruins",
                "difficulty": "Adventurer",
                "theme": "Archaeological Mystery",
                "description": "Explore forgotten ruins hiding ancient secrets"
            },
            {
                "setting": "Mystical Forest", 
                "difficulty": "Hero",
                "theme": "Nature's Balance",
                "description": "Restore harmony to a corrupted woodland realm"
            },
            {
                "setting": "Haunted Castle",
                "difficulty": "Story",
                "theme": "Gothic Horror", 
                "description": "Uncover the dark history of a cursed stronghold"
            },
            {
                "setting": "Mountain Peaks",
                "difficulty": "Adventurer",
                "theme": "Epic Quest",
                "description": "Scale treacherous heights to find legendary artifacts"
            },
            {
                "setting": "Desert Oasis",
                "difficulty": "Hero", 
                "theme": "Survival Adventure",
                "description": "Navigate harsh sands to reach a hidden sanctuary"
            }
        ]
        
        # Realistic player actions for different game phases
        self.player_actions = [
            # Early game actions
            "1", "2", "3", "4",
            "I examine my surroundings carefully",
            "I ask Emberlyn for guidance about what I'm seeing",
            "I approach cautiously with my weapon ready",
            "I search for hidden passages or secret doors",
            
            # Mid game actions  
            "I attempt to communicate peacefully",
            "I use my professional skills to solve this challenge",
            "I look for clues about the Crimson Prophecy",
            "I try to understand the source of this dark energy",
            
            # Late game actions
            "I prepare for the final confrontation",
            "I call upon all my training and experience",
            "I make a decisive move to end this threat",
            "I work with Emberlyn to overcome this obstacle"
        ]
    
    def create_mock_event(self, user_id, body_data):
        """Create mock Lambda event"""
        return {
            'requestContext': {
                'authorizer': {
                    'jwt': {
                        'claims': {
                            'sub': user_id
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
            'function_name': 'full_game_test',
            'memory_limit_in_mb': 512,
            'remaining_time_in_millis': lambda: 30000
        })()    

    def run_complete_game_test(self, strategy_name, strategy_func, game_num, turns=8):
        """Run complete game: Character Creation → Saga Creation → Multiple Turns"""
        
        print(f"  🎮 Game {game_num + 1} with {strategy_name}")
        
        user_id = f"test_{strategy_name.replace(' ', '_').lower()}_{game_num}_{int(time.time())}"
        
        game_transcript = {
            'test_metadata': {
                'strategy': strategy_name,
                'game_number': game_num + 1,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'target_turns': turns
            },
            'character_creation': {
                'input_data': {},
                'response_data': {},
                'metrics': {},
                'success': False
            },
            'saga_creation': {
                'input_data': {},
                'response_data': {},
                'metrics': {},
                'success': False
            },
            'gameplay_turns': [],
            'final_metrics': {},
            'full_transcript': [],
            'success': False
        }
        
        try:
            # Step 1: Detailed Character Creation
            char_template = self.character_templates[game_num % len(self.character_templates)]
            
            print(f"    👤 Creating {char_template['name']} ({char_template['race']} {char_template['profession']})")
            print(f"       Background: {char_template['background']}")
            print(f"       Personality: {char_template['personality']}")
            
            # Prepare character creation data
            char_creation_data = {
                'name': char_template['name'],
                'race': char_template['race'],
                'gender': char_template['gender'],
                'profession': char_template['profession']
            }
            
            char_event = self.create_mock_event(user_id, char_creation_data)
            char_context = self.create_mock_context()
            
            char_start_time = time.time()
            char_response = create_character_handler(char_event, char_context)
            char_end_time = time.time()
            
            if char_response['statusCode'] != 200:
                raise Exception(f"Character creation failed: {char_response}")
            
            character_data = json.loads(char_response['body'])
            character_id = character_data['character_id']
            
            # Store detailed character creation results
            game_transcript['character_creation'] = {
                'input_data': {
                    'template_used': char_template,
                    'creation_request': char_creation_data
                },
                'response_data': {
                    'character_id': character_id,
                    'full_character_sheet': character_data,
                    'identity': character_data.get('IDENTITY', {}),
                    'attributes': character_data.get('ATTRIBUTES', {}),
                    'progression': character_data.get('PROGRESSION', {}),
                    'equipment': character_data.get('EQUIPMENT', {}),
                    'abilities': character_data.get('ABILITIES', {})
                },
                'metrics': {
                    'creation_time_ms': (char_end_time - char_start_time) * 1000,
                    'response_size_chars': len(json.dumps(character_data))
                },
                'success': True
            }
            
            game_transcript['full_transcript'].append({
                'step': 'character_creation',
                'timestamp': datetime.now().isoformat(),
                'input': char_creation_data,
                'output': character_data,
                'duration_ms': (char_end_time - char_start_time) * 1000
            })
            
            # Step 2: Detailed Saga Creation
            saga_template = self.saga_templates[game_num % len(self.saga_templates)]
            saga_creation_data = {
                'characterId': character_id,
                'setting': saga_template['setting'],
                'difficulty': saga_template['difficulty']
            }
            
            print(f"    🏰 Creating saga: {saga_template['setting']} ({saga_template['difficulty']})")
            print(f"       Theme: {saga_template['theme']}")
            print(f"       Description: {saga_template['description']}")
            
            saga_event = self.create_mock_event(user_id, saga_creation_data)
            saga_context = self.create_mock_context()
            
            saga_start_time = time.time()
            saga_response = create_saga_handler(saga_event, saga_context)
            saga_end_time = time.time()
            
            if saga_response['statusCode'] != 200:
                raise Exception(f"Saga creation failed: {saga_response}")
            
            game_data = json.loads(saga_response['body'])
            game_id = game_data['game_id']
            
            # Store detailed saga creation results
            game_transcript['saga_creation'] = {
                'input_data': {
                    'template_used': saga_template,
                    'creation_request': saga_creation_data
                },
                'response_data': {
                    'game_id': game_id,
                    'game_name': game_data.get('game_name'),
                    'opening_scene': game_data.get('messages', [])[-1] if game_data.get('messages') else None,
                    'full_game_data': game_data
                },
                'metrics': {
                    'creation_time_ms': (saga_end_time - saga_start_time) * 1000,
                    'response_size_chars': len(json.dumps(game_data)),
                    'opening_scene_length': len(game_data.get('messages', [])[-1] if game_data.get('messages') else "")
                },
                'success': True
            }
            
            game_transcript['full_transcript'].append({
                'step': 'saga_creation',
                'timestamp': datetime.now().isoformat(),
                'input': saga_creation_data,
                'output': game_data,
                'duration_ms': (saga_end_time - saga_start_time) * 1000
            })
            
            # Step 3: Play Multiple Turns with Context Strategy
            print(f"    🎯 Playing {turns} turns with {strategy_name}")
            
            # Replace Claude handler with context-aware version
            original_take_turn = mock_claude_local.take_turn
            context_handler = ContextAwareClaudeHandler(strategy_func, strategy_name)
            mock_claude_local.take_turn = context_handler.take_turn
            
            try:
                for turn_num in range(turns):
                    # Select appropriate action based on game phase
                    if turn_num < 3:
                        # Early game - exploration actions
                        action_pool = self.player_actions[:8]
                    elif turn_num < 6:
                        # Mid game - investigation actions  
                        action_pool = self.player_actions[4:12]
                    else:
                        # Late game - decisive actions
                        action_pool = self.player_actions[8:]
                    
                    player_action = random.choice(action_pool)
                    
                    print(f"      Turn {turn_num + 1}: {player_action}")
                    
                    turn_event = self.create_mock_event(user_id, {
                        'game_id': game_id,
                        'message': player_action
                    })
                    turn_context = self.create_mock_context()
                    
                    turn_start_time = time.time()
                    turn_response = take_turn_handler(turn_event, turn_context)
                    turn_end_time = time.time()
                    
                    if turn_response['statusCode'] == 200:
                        body = json.loads(turn_response['body'])
                        ai_response = body.get('ai_response', body.get('response', 'No response'))
                        
                        # Analyze response quality
                        quality_scores = self.analyze_response_quality(ai_response)
                        
                        # Store detailed turn data
                        turn_data = {
                            'turn_number': turn_num + 1,
                            'player_input': {
                                'action': player_action,
                                'timestamp': datetime.now().isoformat()
                            },
                            'ai_response': {
                                'content': ai_response,
                                'length_chars': len(ai_response),
                                'word_count': len(ai_response.split())
                            },
                            'context_strategy': {
                                'strategy_name': strategy_name,
                                'tokens_used': context_handler.token_usage[-1] if context_handler.token_usage else 0,
                                'messages_in_context': len(context_handler.strategy_func(body.get('messages', []))) if hasattr(context_handler, 'strategy_func') else 0
                            },
                            'performance_metrics': {
                                'response_time_ms': (turn_end_time - turn_start_time) * 1000,
                                'api_response_time_ms': context_handler.response_times[-1] if context_handler.response_times else 0
                            },
                            'quality_analysis': quality_scores,
                            'game_state': {
                                'saga_completed': "Congratulations, you have completed this Saga!" in ai_response,
                                'choices_presented': ai_response.count('[') - ai_response.count('[['),
                                'dice_roll_occurred': '🎲' in ai_response
                            },
                            'success': True
                        }
                        
                        game_transcript['gameplay_turns'].append(turn_data)
                        
                        game_transcript['full_transcript'].append({
                            'step': f'turn_{turn_num + 1}',
                            'timestamp': datetime.now().isoformat(),
                            'input': player_action,
                            'output': ai_response,
                            'duration_ms': (turn_end_time - turn_start_time) * 1000,
                            'context_tokens': context_handler.token_usage[-1] if context_handler.token_usage else 0
                        })
                        
                        # Check for saga completion
                        if turn_data['game_state']['saga_completed']:
                            print(f"      🎊 Saga completed at turn {turn_num + 1}")
                            break
                            
                    else:
                        # Handle failed turn
                        turn_data = {
                            'turn_number': turn_num + 1,
                            'player_input': {
                                'action': player_action,
                                'timestamp': datetime.now().isoformat()
                            },
                            'error': {
                                'message': str(turn_response),
                                'status_code': turn_response.get('statusCode', 'unknown')
                            },
                            'success': False
                        }
                        game_transcript['gameplay_turns'].append(turn_data)
                        
                        game_transcript['full_transcript'].append({
                            'step': f'turn_{turn_num + 1}_failed',
                            'timestamp': datetime.now().isoformat(),
                            'input': player_action,
                            'error': str(turn_response),
                            'duration_ms': (turn_end_time - turn_start_time) * 1000
                        })
                        break
                
                # Calculate comprehensive metrics
                successful_turns = [t for t in game_transcript['gameplay_turns'] if t.get('success')]
                if successful_turns:
                    total_tokens = sum(t.get('context_strategy', {}).get('tokens_used', 0) for t in successful_turns)
                    total_response_time = sum(t.get('performance_metrics', {}).get('response_time_ms', 0) for t in successful_turns)
                    total_ai_words = sum(t.get('ai_response', {}).get('word_count', 0) for t in successful_turns)
                    avg_quality = sum(t.get('quality_analysis', {}).get('overall', 0) for t in successful_turns) / len(successful_turns)
                    
                    game_transcript['final_metrics'] = {
                        'gameplay_summary': {
                            'total_turns_attempted': len(game_transcript['gameplay_turns']),
                            'successful_turns': len(successful_turns),
                            'success_rate': len(successful_turns) / len(game_transcript['gameplay_turns']),
                            'saga_completed': any(t.get('game_state', {}).get('saga_completed', False) for t in successful_turns)
                        },
                        'performance_metrics': {
                            'total_tokens_used': total_tokens,
                            'avg_tokens_per_turn': total_tokens / len(successful_turns) if successful_turns else 0,
                            'total_response_time_ms': total_response_time,
                            'avg_response_time_ms': total_response_time / len(successful_turns) if successful_turns else 0,
                            'character_creation_time_ms': game_transcript['character_creation']['metrics']['creation_time_ms'],
                            'saga_creation_time_ms': game_transcript['saga_creation']['metrics']['creation_time_ms'],
                            'total_game_time_ms': game_transcript['character_creation']['metrics']['creation_time_ms'] + 
                                                 game_transcript['saga_creation']['metrics']['creation_time_ms'] + 
                                                 total_response_time
                        },
                        'content_analysis': {
                            'avg_quality_score': avg_quality,
                            'total_ai_words_generated': total_ai_words,
                            'avg_ai_words_per_turn': total_ai_words / len(successful_turns) if successful_turns else 0,
                            'total_choices_presented': sum(t.get('game_state', {}).get('choices_presented', 0) for t in successful_turns),
                            'dice_rolls_occurred': sum(1 for t in successful_turns if t.get('game_state', {}).get('dice_roll_occurred', False))
                        },
                        'context_strategy_analysis': {
                            'strategy_used': strategy_name,
                            'token_efficiency': {
                                'total_tokens': total_tokens,
                                'avg_per_turn': total_tokens / len(successful_turns) if successful_turns else 0
                            }
                        }
                    }
                    
                    game_transcript['success'] = True
                    
                    print(f"    ✅ Completed: {len(successful_turns)} turns, {total_tokens} tokens, {avg_quality:.1f}/10 quality")
                
            finally:
                # Restore original handler
                mock_claude_local.take_turn = original_take_turn
            
        except Exception as e:
            game_transcript['error'] = {
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"    ❌ Failed: {e}")
        
        return game_transcript
    
    def analyze_response_quality(self, response):
        """Comprehensive Fire Whisper RPG response quality analysis"""
        scores = {}
        
        # Choice format analysis (0-10)
        choice_count = response.count('[') - response.count('[[')
        has_question = 'what do you do' in response.lower()
        
        if has_question and choice_count >= 4:
            scores['choice_format'] = 10.0
        elif choice_count >= 3:
            scores['choice_format'] = 7.0
        elif choice_count >= 1:
            scores['choice_format'] = 4.0
        else:
            scores['choice_format'] = 0.0
        
        # Dice mechanics analysis (0-10)
        has_dice_emoji = '🎲' in response
        has_dice_result = any(word in response for word in ['needed', 'or higher', 'Success', 'Failure'])
        
        if has_dice_emoji and has_dice_result:
            scores['dice_mechanics'] = 10.0
        elif has_dice_emoji:
            scores['dice_mechanics'] = 5.0
        else:
            scores['dice_mechanics'] = 10.0  # No dice needed is acceptable
        
        # Story quality analysis (0-10)
        story_score = 5.0
        if 'emberlyn' in response.lower():
            story_score += 2.0
        if any(word in response.lower() for word in ['crimson', 'prophecy', 'fire whisper']):
            story_score += 1.0
        if len(response) > 200:
            story_score += 1.0
        if len(response) > 400:
            story_score += 1.0
        scores['story_quality'] = min(10.0, story_score)
        
        # Narrative engagement (0-10)
        engagement_score = 5.0
        if any(word in response.lower() for word in ['you', 'your']):
            engagement_score += 2.0
        if response.count('*') >= 2:  # Action descriptions
            engagement_score += 2.0
        if '!' in response:
            engagement_score += 1.0
        scores['narrative_engagement'] = min(10.0, engagement_score)
        
        # Technical format (0-10)
        format_score = 8.0
        if response.count('[') != response.count(']'):
            format_score -= 3.0
        if len(response) < 50:
            format_score -= 2.0
        scores['technical_format'] = max(0.0, format_score)
        
        # Overall score
        scores['overall'] = sum(scores.values()) / len(scores)
        
        return scores
    
    def run_comprehensive_test(self, games_per_strategy=2, turns_per_game=8):
        """Run comprehensive test across all strategies with full transcripts"""
        
        print("🧪 COMPREHENSIVE FIRE WHISPER RPG FULL GAME FLOW TEST")
        print("=" * 80)
        print("🎮 Complete Flow: Character Creation (Name/Race/Profession) → Saga Creation → Multiple Turns")
        print(f"📊 Testing {len(self.strategies)} strategies × {games_per_strategy} games × {turns_per_game} turns")
        print("📝 Outputting full transcripts with all details to YAML")
        print("🔍 Including character sheets, saga details, and turn-by-turn analysis")
        print()
        
        test_results = {
            'test_configuration': {
                'timestamp': datetime.now().isoformat(),
                'test_type': 'comprehensive_full_game_flow',
                'games_per_strategy': games_per_strategy,
                'turns_per_game': turns_per_game,
                'total_games_planned': len(self.strategies) * games_per_strategy,
                'strategies_tested': list(self.strategies.keys()),
                'character_templates_available': len(self.character_templates),
                'saga_templates_available': len(self.saga_templates)
            },
            'character_templates_used': self.character_templates,
            'saga_templates_used': self.saga_templates,
            'game_transcripts': [],
            'strategy_performance_summaries': {},
            'cross_strategy_analysis': {},
            'recommendations': {}
        }
        
        all_game_transcripts = []
        
        for strategy_name, strategy_func in self.strategies.items():
            print(f"🧪 Testing Strategy: {strategy_name}")
            print("-" * 60)
            
            strategy_games = []
            
            for game_num in range(games_per_strategy):
                game_transcript = self.run_complete_game_test(
                    strategy_name, strategy_func, game_num, turns_per_game
                )
                strategy_games.append(game_transcript)
                all_game_transcripts.append(game_transcript)
            
            # Calculate detailed strategy summary
            successful_games = [g for g in strategy_games if g.get('success')]
            
            if successful_games:
                # Aggregate all successful turns across games
                all_successful_turns = []
                for game in successful_games:
                    all_successful_turns.extend([t for t in game['gameplay_turns'] if t.get('success')])
                
                # Character creation metrics
                char_creation_times = [g['character_creation']['metrics']['creation_time_ms'] for g in successful_games]
                saga_creation_times = [g['saga_creation']['metrics']['creation_time_ms'] for g in successful_games]
                
                # Gameplay metrics
                total_tokens_all_games = sum(g['final_metrics']['performance_metrics']['total_tokens_used'] for g in successful_games)
                total_game_time_all_games = sum(g['final_metrics']['performance_metrics']['total_game_time_ms'] for g in successful_games)
                
                strategy_summary = {
                    'game_completion': {
                        'total_games_attempted': len(strategy_games),
                        'successful_games': len(successful_games),
                        'success_rate': len(successful_games) / len(strategy_games),
                        'sagas_completed': sum(1 for g in successful_games if g['final_metrics']['gameplay_summary']['saga_completed'])
                    },
                    'character_creation_performance': {
                        'avg_creation_time_ms': sum(char_creation_times) / len(char_creation_times),
                        'min_creation_time_ms': min(char_creation_times),
                        'max_creation_time_ms': max(char_creation_times),
                        'characters_created': len(successful_games)
                    },
                    'saga_creation_performance': {
                        'avg_creation_time_ms': sum(saga_creation_times) / len(saga_creation_times),
                        'min_creation_time_ms': min(saga_creation_times),
                        'max_creation_time_ms': max(saga_creation_times),
                        'sagas_created': len(successful_games)
                    },
                    'gameplay_performance': {
                        'total_turns_played': len(all_successful_turns),
                        'avg_turns_per_game': len(all_successful_turns) / len(successful_games) if successful_games else 0,
                        'total_tokens_used': total_tokens_all_games,
                        'avg_tokens_per_turn': total_tokens_all_games / len(all_successful_turns) if all_successful_turns else 0,
                        'avg_tokens_per_game': total_tokens_all_games / len(successful_games) if successful_games else 0,
                        'total_game_time_ms': total_game_time_all_games,
                        'avg_game_time_ms': total_game_time_all_games / len(successful_games) if successful_games else 0
                    },
                    'content_quality': {
                        'avg_quality_score': sum(t['quality_analysis']['overall'] for t in all_successful_turns) / len(all_successful_turns) if all_successful_turns else 0,
                        'avg_choice_format_score': sum(t['quality_analysis']['choice_format'] for t in all_successful_turns) / len(all_successful_turns) if all_successful_turns else 0,
                        'avg_story_quality_score': sum(t['quality_analysis']['story_quality'] for t in all_successful_turns) / len(all_successful_turns) if all_successful_turns else 0,
                        'total_ai_words_generated': sum(t['ai_response']['word_count'] for t in all_successful_turns),
                        'avg_ai_words_per_turn': sum(t['ai_response']['word_count'] for t in all_successful_turns) / len(all_successful_turns) if all_successful_turns else 0
                    },
                    'context_efficiency': {
                        'strategy_name': strategy_name,
                        'avg_context_tokens_per_turn': sum(t['context_strategy']['tokens_used'] for t in all_successful_turns) / len(all_successful_turns) if all_successful_turns else 0,
                        'total_context_tokens': sum(t['context_strategy']['tokens_used'] for t in all_successful_turns)
                    }
                }
                
                test_results['strategy_performance_summaries'][strategy_name] = strategy_summary
                
                print(f"  📊 Games: {len(successful_games)}/{len(strategy_games)} successful")
                print(f"  📊 Avg tokens/turn: {strategy_summary['gameplay_performance']['avg_tokens_per_turn']:.0f}")
                print(f"  📊 Avg quality: {strategy_summary['content_quality']['avg_quality_score']:.1f}/10")
                print(f"  📊 Avg game time: {strategy_summary['gameplay_performance']['avg_game_time_ms']/1000:.1f}s")
                print(f"  📊 Sagas completed: {strategy_summary['game_completion']['sagas_completed']}")
            else:
                print(f"  ❌ No successful games for {strategy_name}")
            
            print()
        
        # Add all game transcripts to results
        test_results['game_transcripts'] = all_game_transcripts
        
        # Cross-strategy analysis
        successful_strategies = {k: v for k, v in test_results['strategy_performance_summaries'].items() 
                               if v['game_completion']['successful_games'] > 0}
        
        if successful_strategies:
            # Find best performers in each category
            best_token_efficiency = min(successful_strategies.items(), 
                                      key=lambda x: x[1]['gameplay_performance']['avg_tokens_per_turn'])
            best_quality = max(successful_strategies.items(), 
                             key=lambda x: x[1]['content_quality']['avg_quality_score'])
            best_speed = min(successful_strategies.items(), 
                           key=lambda x: x[1]['gameplay_performance']['avg_game_time_ms'])
            best_completion_rate = max(successful_strategies.items(), 
                                     key=lambda x: x[1]['game_completion']['success_rate'])
            
            test_results['cross_strategy_analysis'] = {
                'best_performers': {
                    'token_efficiency': {
                        'strategy': best_token_efficiency[0],
                        'avg_tokens_per_turn': best_token_efficiency[1]['gameplay_performance']['avg_tokens_per_turn'],
                        'total_tokens_saved_vs_full_context': 0  # Will calculate below
                    },
                    'content_quality': {
                        'strategy': best_quality[0],
                        'avg_quality_score': best_quality[1]['content_quality']['avg_quality_score']
                    },
                    'response_speed': {
                        'strategy': best_speed[0],
                        'avg_game_time_ms': best_speed[1]['gameplay_performance']['avg_game_time_ms']
                    },
                    'completion_rate': {
                        'strategy': best_completion_rate[0],
                        'success_rate': best_completion_rate[1]['game_completion']['success_rate']
                    }
                },
                'comparative_metrics': {}
            }
            
            # Calculate token savings vs Full Context
            if 'Full Context' in successful_strategies:
                full_context_tokens = successful_strategies['Full Context']['gameplay_performance']['avg_tokens_per_turn']
                for strategy_name, summary in successful_strategies.items():
                    if strategy_name != 'Full Context':
                        tokens_saved = full_context_tokens - summary['gameplay_performance']['avg_tokens_per_turn']
                        savings_pct = (tokens_saved / full_context_tokens) * 100 if full_context_tokens > 0 else 0
                        test_results['cross_strategy_analysis']['comparative_metrics'][strategy_name] = {
                            'tokens_saved_per_turn': tokens_saved,
                            'token_savings_percentage': savings_pct
                        }
        
        # Generate recommendations
        test_results['recommendations'] = self.generate_comprehensive_recommendations(successful_strategies)
        
        # Save comprehensive results to YAML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        yaml_file = f"full_game_flow_test_results_{timestamp}.yaml"
        
        # Custom YAML representer for better formatting
        def represent_none(self, data):
            return self.represent_scalar('tag:yaml.org,2002:null', '')
        
        yaml.add_representer(type(None), represent_none)
        
        with open(yaml_file, 'w') as f:
            yaml.dump(test_results, f, default_flow_style=False, sort_keys=False, width=120, indent=2)
        
        # Print comprehensive summary
        self.print_comprehensive_summary(test_results, yaml_file)
        
        return test_results
    
    def generate_comprehensive_recommendations(self, strategies):
        """Generate detailed recommendations based on comprehensive analysis"""
        
        if not strategies:
            return {"error": "No successful strategies to analyze"}
        
        recommendations = {
            'primary_recommendation': '',
            'use_case_specific': {},
            'implementation_notes': [],
            'performance_tradeoffs': {}
        }
        
        # Find best balanced strategy
        best_balance_score = 0
        best_balance_strategy = None
        
        for name, summary in strategies.items():
            # Calculate composite score (efficiency + quality + speed)
            efficiency_score = 1000 / summary['gameplay_performance']['avg_tokens_per_turn'] if summary['gameplay_performance']['avg_tokens_per_turn'] > 0 else 0
            quality_score = summary['content_quality']['avg_quality_score']
            speed_score = 10000 / summary['gameplay_performance']['avg_game_time_ms'] if summary['gameplay_performance']['avg_game_time_ms'] > 0 else 0
            
            composite_score = (efficiency_score + quality_score + speed_score) / 3
            
            if composite_score > best_balance_score:
                best_balance_score = composite_score
                best_balance_strategy = name
        
        recommendations['primary_recommendation'] = f"Use {best_balance_strategy} for optimal balance of efficiency, quality, and performance"
        
        # Use case specific recommendations
        most_efficient = min(strategies.items(), key=lambda x: x[1]['gameplay_performance']['avg_tokens_per_turn'])
        highest_quality = max(strategies.items(), key=lambda x: x[1]['content_quality']['avg_quality_score'])
        fastest = min(strategies.items(), key=lambda x: x[1]['gameplay_performance']['avg_game_time_ms'])
        
        recommendations['use_case_specific'] = {
            'cost_optimization': f"Use {most_efficient[0]} to minimize token usage and API costs",
            'quality_priority': f"Use {highest_quality[0]} for maximum story and gameplay quality",
            'speed_priority': f"Use {fastest[0]} for fastest response times",
            'production_deployment': f"Use {best_balance_strategy} for production systems requiring balanced performance"
        }
        
        return recommendations
    
    def print_comprehensive_summary(self, results, yaml_file):
        """Print detailed summary of test results"""
        
        print("=" * 80)
        print("📊 COMPREHENSIVE FULL GAME FLOW TEST RESULTS")
        print("=" * 80)
        
        config = results['test_configuration']
        print(f"🎮 Total Games Tested: {config['total_games_planned']}")
        print(f"📝 Character Templates: {config['character_templates_available']}")
        print(f"🏰 Saga Templates: {config['saga_templates_available']}")
        print(f"🎯 Target Turns per Game: {config['turns_per_game']}")
        print()
        
        # Strategy comparison table
        print("📈 STRATEGY PERFORMANCE COMPARISON")
        print("-" * 100)
        print(f"{'Strategy':<18} {'Success':<8} {'Tokens/Turn':<12} {'Quality':<8} {'Game Time':<10} {'Sagas Done':<10}")
        print("-" * 100)
        
        for name, summary in results['strategy_performance_summaries'].items():
            success_rate = f"{summary['game_completion']['success_rate']:.1%}"
            tokens = f"{summary['gameplay_performance']['avg_tokens_per_turn']:.0f}"
            quality = f"{summary['content_quality']['avg_quality_score']:.1f}/10"
            game_time = f"{summary['gameplay_performance']['avg_game_time_ms']/1000:.1f}s"
            sagas = f"{summary['game_completion']['sagas_completed']}"
            
            print(f"{name:<18} {success_rate:<8} {tokens:<12} {quality:<8} {game_time:<10} {sagas:<10}")
        
        # Best performers
        if 'cross_strategy_analysis' in results and 'best_performers' in results['cross_strategy_analysis']:
            analysis = results['cross_strategy_analysis']['best_performers']
            print(f"\n🏆 CATEGORY WINNERS:")
            print(f"  • Most Token Efficient: {analysis['token_efficiency']['strategy']}")
            print(f"  • Highest Quality: {analysis['content_quality']['strategy']}")
            print(f"  • Fastest Response: {analysis['response_speed']['strategy']}")
            print(f"  • Best Completion Rate: {analysis['completion_rate']['strategy']}")
        
        # Recommendations
        if 'recommendations' in results:
            rec = results['recommendations']
            print(f"\n💡 RECOMMENDATIONS:")
            print(f"  🎯 Primary: {rec['primary_recommendation']}")
            if 'use_case_specific' in rec:
                print(f"  💰 Cost Optimization: {rec['use_case_specific'].get('cost_optimization', 'N/A')}")
                print(f"  🎨 Quality Priority: {rec['use_case_specific'].get('quality_priority', 'N/A')}")
                print(f"  ⚡ Speed Priority: {rec['use_case_specific'].get('speed_priority', 'N/A')}")
        
        print(f"\n💾 Complete results with full transcripts saved to: {yaml_file}")
        print("✅ Comprehensive full game flow test complete!")

def main():
    """Run the comprehensive full game flow test"""
    
    tester = FullGameFlowTester()
    results = tester.run_comprehensive_test(games_per_strategy=2, turns_per_game=8)
    
    return results

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    finally:
        os.chdir(original_dir)