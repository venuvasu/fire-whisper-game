"""
Enhanced AI Integration Layer - Integrates narrative enhancement with game mechanics
"""
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from .game_state_manager import GameStateManager, ActionType
from .enhanced_narrative_integration import NarrativeEnhancer
from .option_generator import generate_contextual_options
from .battle_system import BattleSystem
from .smart_action_analyzer import SmartActionAnalyzer
from .story_state_manager import StoryStateManager
from .action_result_processor import ActionResultProcessor
from .narrative_template_engine import NarrativeTemplateEngine
# Import experimental Looma patterns
sys.path.append(str(Path(__file__).parent.parent.parent / "experiments" / "looma"))
from core.context_continuity import ContextContinuityEnforcer


class AIIntegrationLayer:
    def __init__(self, api_key: str = None):
        # Use environment variable if no API key provided
        if api_key is None:
            import os
            api_key = os.getenv('CLAUDE_API_KEY')
            if not api_key:
                raise ValueError("CLAUDE_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=api_key)
        self.game_manager: Optional[GameStateManager] = None
        self.narrative_enhancer = NarrativeEnhancer()
        self.battle_system = BattleSystem()
        self.action_analyzer = SmartActionAnalyzer()
        self.story_manager = StoryStateManager()
        self.action_processor = ActionResultProcessor(self.story_manager)
        self.narrative_engine = NarrativeTemplateEngine()
        self.continuity_enforcer = ContextContinuityEnforcer(self.story_manager)
        
    def start_new_game(self, character_data: Dict = None) -> Dict:
        """Initialize a new game with deterministic state management"""
        self.game_manager = GameStateManager(character_data)
        
        # Get initial narrative from AI
        initial_prompt = self._build_game_start_prompt()
        response = self._call_ai(initial_prompt)
        
        # Enhance with character status integration
        enhanced_response = self.narrative_enhancer.enhance_response(
            response, 
            {'dice_rolls': [], 'xp_awards': []},
            self.game_manager.character,
            {'status_requested': True}
        )
        
        # Initialize story state
        initial_context = self.story_manager.get_current_context()
        
        # Generate initial options
        story_context = {
            'turn_number': 1,
            'corruption_level': 'low',
            'character_health_ratio': 1.0
        }
        
        contextual_options = generate_contextual_options(
            enhanced_response, 
            self.game_manager.character, 
            story_context
        )
        
        # Append options to initial narrative
        enhanced_response += f"\n\n**What would you like to do?**\n{contextual_options}"
        
        return {
            'narrative': enhanced_response,
            'character': self.game_manager.character,
            'game_state': self.game_manager.get_current_state()
        }
    
    def process_player_action(self, player_input: str) -> Dict:
        """Process player action with enhanced narrative integration"""
        if not self.game_manager:
            raise ValueError("Game not initialized")
        
        # Get session ID for behavior tracking
        session_id = self.game_manager.session_data.get('session_id', 'default')
        
        # Increment turn and check for context refresh
        needs_refresh = self.game_manager.increment_turn()
        
        # Increment turn in story manager
        self.story_manager.increment_turn()
        
        # Get current story context (replaces AI memory)
        story_context = self.story_manager.get_current_context()
        current_situation = self.story_manager.get_narrative_context_summary()
        
        # Get progression context to prevent loops
        progression_context = self.game_manager.get_progression_context()
        
        # Check if we should force progression
        if progression_context['should_force_progression']['should_force']:
            print(f"🔄 FORCING PROGRESSION: {progression_context['should_force_progression']['reason']}")
            # Add progression context to story context
            story_context['force_progression'] = progression_context['should_force_progression']
        
        # Use smart analyzer to determine if dice roll is needed
        action_analysis = self.action_analyzer.analyze_action(
            player_input, 
            current_situation, 
            self.game_manager.character,
            self.battle_system.battle_state.value != 'no_battle'
        )
        
        # Check if battle should be triggered or is ongoing
        battle_results = {}
        
        # Force battle start if player chooses combat action and no battle active
        combat_keywords = ['charge', 'attack', 'fight', 'battle', 'strike']
        wants_combat = any(word in player_input.lower() for word in combat_keywords)
        
        if wants_combat and self.battle_system.battle_state.value == 'no_battle':
            # Create a default enemy encounter
            battle_situation = current_situation + " A hostile creature appears!"
            battle_results = self.battle_system.start_battle(battle_situation)
        
        # Process combat if battle is active
        if self.battle_system.battle_state.value != 'no_battle':
            combat_results = self.battle_system.process_combat_action(
                player_input, 
                self.game_manager.character['stats']
            )
            battle_results.update(combat_results)
        
        # Execute mechanics only if needed
        mechanical_results = self._execute_smart_mechanics(action_analysis, battle_results)
        
        # Debug output
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            print(f"\n🔍 DEBUG - Action Analysis:")
            print(f"   Player Input: {player_input}")
            print(f"   Requires Roll: {action_analysis['requires_roll']}")
            print(f"   Auto Success: {action_analysis.get('auto_success', False)}")
            print(f"   Reasoning: {action_analysis['reasoning']}")
            if battle_results:
                print(f"   Battle Active: {battle_results.get('battle_status', {}).get('in_battle', False)}")
            print(f"   Dice Rolls Made: {len(mechanical_results['dice_rolls'])}")
        
        # Build AI prompt with pre-calculated results and battle status
        ai_prompt = self._build_action_prompt(
            player_input, 
            action_analysis, 
            mechanical_results,
            battle_results,
            needs_refresh
        )
        
        # Add continuity enforcement to prompt
        enhanced_prompt = self.continuity_enforcer.generate_continuity_prompt_addition(story_context)
        if enhanced_prompt:
            ai_prompt += enhanced_prompt
            print(f"🧵 CONTINUITY ENFORCEMENT ACTIVE")
        
        # Get narrative response from AI
        ai_response = self._call_ai(ai_prompt)
        
        # Validate context continuity
        continuity_check = self.continuity_enforcer.validate_context_continuity(ai_response, story_context)
        if not continuity_check["valid"]:
            print(f"🚨 CONTINUITY VIOLATIONS: {continuity_check['violations']}")
            # Apply corrective measures
            if len(continuity_check['violations']) >= 2:  # Multiple violations
                print("🔧 APPLYING CONTINUITY CORRECTION...")
                # Generate corrected response
                correction_prompt = ai_prompt + f"""

IMPORTANT CORRECTION NEEDED:
Your previous response violated story continuity: {continuity_check['violations']}
Please provide a response that maintains the established context and story elements.
"""
                ai_response = self._call_ai(correction_prompt)
                print("✅ CONTINUITY CORRECTION APPLIED")
        
        # Create context anchor for next turn
        self.continuity_enforcer.create_context_anchor(ai_response, story_context)
        
        # Update behavior tracking
        behavior_info = self.narrative_enhancer.update_behavior_tracking(
            player_input, ai_response, session_id
        )
        
        # Parse AI response and validate compliance
        parsed_response = self._parse_ai_response(ai_response)
        
        # Check for location changes in AI response
        new_location = self.game_manager.parse_location_from_response(ai_response)
        if new_location:
            location_update = self.game_manager.update_location(new_location, "ai_narrative")
            if location_update['location_changed']:
                print(f"📍 LOCATION CHANGED: {location_update['old_location']} → {location_update['new_location']}")
        else:
            # Update turn count at current location
            self.game_manager.update_location(self.game_manager.progression_state['current_location'])
        
        # Advance story progress for meaningful actions
        if self._is_meaningful_action(player_input, action_analysis):
            event_description = f"player_{action_analysis.get('action_type', 'action').value}_{self.game_manager.session_data['turn_count']}"
            if self.game_manager.advance_story_progress(event_description):
                print(f"📈 STORY PROGRESS: Advanced to {self.game_manager.progression_state['story_progress']}")
        
        # Handle violations
        if parsed_response['violations']:
            self.game_manager.add_rule_violation(f"AI Hallucination: {parsed_response['violations']}")
        
        # Enhance response with integrated mechanics
        context = {
            'level_up': any(award.get('level_up') for award in mechanical_results.get('xp_awards', [])),
            'low_resources': self._check_low_resources(),
            'behavior_warning': behavior_info.get('warning_level', 0),
            'stakes_level': behavior_info.get('stakes_level', 'medium')
        }
        
        enhanced_narrative = self.narrative_enhancer.enhance_response(
            parsed_response['narrative'],
            mechanical_results,
            self.game_manager.character,
            context
        )
        
        # Generate and append contextual options
        story_context = {
            'turn_number': self.game_manager.session_data['turn_count'],
            'corruption_level': 'medium',  # Could be dynamic based on story
            'character_health_ratio': self.game_manager.character['resources']['hp'] / self.game_manager.character['resources']['max_hp']
        }
        
        contextual_options = generate_contextual_options(
            enhanced_narrative, 
            self.game_manager.character, 
            story_context
        )
        
        # Add battle status to narrative if active
        battle_status_text = self.battle_system.get_battle_summary()
        if battle_status_text:
            enhanced_narrative += battle_status_text
        
        # Update story manager with the narrative result
        self.story_manager.add_recent_event(f"player_action_{player_input.replace(' ', '_')[:20]}")
        self._last_narrative = enhanced_narrative
        
        # Don't append options to narrative since local runner handles them separately
        # enhanced_narrative += f"\n\n**What would you like to do?**\n{contextual_options}"
        
        # Clear used mechanics
        self.game_manager.clear_pending_rolls()
        
        # Get current game state for debug info
        current_state = self.game_manager.get_current_state()
        
        return {
            'narrative': enhanced_narrative,
            'mechanical_results': mechanical_results,
            'battle_results': battle_results,
            'character': self.game_manager.character,
            'game_state': current_state,
            'context_refreshed': needs_refresh,
            'behavior_info': behavior_info,
            # Add fields expected by local runner
            'LOCATION': current_state.get('current_location', 'Unknown'),
            'choices': contextual_options.split('\n') if contextual_options else [],
            'debug_info': {
                'location': current_state.get('current_location', 'unknown'),
                'story_progress': current_state.get('story_progress', 0),
                'turn': current_state.get('turn_count', 0)
            }
        }
    
    def _check_low_resources(self) -> bool:
        """Check if character has low resources"""
        char = self.game_manager.character
        hp_ratio = char['resources']['hp'] / char['resources']['max_hp']
        energy_ratio = char['resources']['energy'] / char['resources']['max_energy']
        return hp_ratio < 0.4 or energy_ratio < 0.4
    
    def _is_meaningful_action(self, player_input: str, action_analysis: Dict) -> bool:
        """Determine if an action should advance story progress"""
        # Every few turns should advance story to prevent stagnation
        turn_count = self.game_manager.session_data['turn_count']
        if turn_count % 3 == 0:  # Every 3rd turn advances story
            return True
        
        # Specific action types that always advance story
        meaningful_actions = ['COMBAT', 'MAGIC', 'SOCIAL']
        if action_analysis.get('action_type') and action_analysis['action_type'].value in meaningful_actions:
            return True
        
        # Combat-related keywords
        combat_keywords = ['attack', 'fight', 'battle', 'charge', 'strike']
        if any(word in player_input.lower() for word in combat_keywords):
            return True
        
        # Investigation keywords
        investigation_keywords = ['investigate', 'search', 'examine', 'explore']
        if any(word in player_input.lower() for word in investigation_keywords):
            return True
        
        return False
    
    # Copy all other methods from original AIIntegrationLayer
    def _analyze_player_action(self, player_input: str) -> Dict:
        """Analyze what mechanics the player action requires"""
        # Default analysis
        action_analysis = {
            'requires_roll': True,  # Most actions require rolls
            'action_type': ActionType.SKILL_CHECK,
            'stat_used': 'charisma',  # Default for clerics
            'skill_used': 'Persuasion',
            'difficulty': 'normal',
            'xp_eligible': True
        }
        
        # Handle numbered choices (1, 2, 3, 4)
        if player_input.strip() in ['1', '2', '3', '4']:
            choice_num = int(player_input.strip())
            
            # Map choices to common RPG actions
            if choice_num == 1:  # Usually combat/direct action
                action_analysis.update({
                    'action_type': ActionType.COMBAT,
                    'stat_used': 'strength',
                    'skill_used': 'Combat',
                    'difficulty': 'normal'
                })
            elif choice_num == 2:  # Usually magic/special ability
                action_analysis.update({
                    'action_type': ActionType.MAGIC,
                    'stat_used': 'charisma',  # For clerics
                    'skill_used': 'Healing',
                    'difficulty': 'normal'
                })
            elif choice_num == 3:  # Usually stealth/skill
                action_analysis.update({
                    'action_type': ActionType.SKILL_CHECK,
                    'stat_used': 'dexterity',
                    'skill_used': 'Stealth',
                    'difficulty': 'normal'
                })
            elif choice_num == 4:  # Usually knowledge/investigation
                action_analysis.update({
                    'action_type': ActionType.SKILL_CHECK,
                    'stat_used': 'intelligence',
                    'skill_used': 'Knowledge',
                    'difficulty': 'normal'
                })
        
        # Combat keywords
        elif any(word in player_input.lower() for word in ['attack', 'fight', 'strike', 'combat', 'battle', 'charge', 'swing', 'flame']):
            action_analysis.update({
                'action_type': ActionType.COMBAT,
                'stat_used': 'strength',
                'skill_used': 'Combat',
                'difficulty': 'normal'
            })
        
        # Magic keywords
        elif any(word in player_input.lower() for word in ['heal', 'magic', 'spell', 'divine', 'channel', 'sacred', 'barrier']):
            action_analysis.update({
                'action_type': ActionType.MAGIC,
                'stat_used': 'charisma',
                'skill_used': 'Healing',
                'difficulty': 'normal'
            })
        
        # Stealth keywords
        elif any(word in player_input.lower() for word in ['sneak', 'hide', 'stealth', 'quietly', 'silent']):
            action_analysis.update({
                'action_type': ActionType.SKILL_CHECK,
                'stat_used': 'dexterity',
                'skill_used': 'Stealth',
                'difficulty': 'normal'
            })
        
        # Social keywords
        elif any(word in player_input.lower() for word in ['persuade', 'convince', 'talk', 'negotiate', 'intimidate']):
            action_analysis.update({
                'action_type': ActionType.SOCIAL,
                'stat_used': 'charisma',
                'skill_used': 'Persuasion',
                'difficulty': 'normal'
            })
        
        # Investigation/Knowledge keywords
        elif any(word in player_input.lower() for word in ['examine', 'investigate', 'study', 'detect', 'guidance', 'assess']):
            action_analysis.update({
                'action_type': ActionType.SKILL_CHECK,
                'stat_used': 'intelligence',
                'skill_used': 'Knowledge',
                'difficulty': 'normal'
            })
        
        return action_analysis
    
    def _execute_mechanics(self, action_analysis: Dict) -> Dict:
        """Execute all required mechanics before AI call"""
        results = {
            'dice_rolls': [],
            'xp_awards': [],
            'state_changes': {},
            'loot_discovered': []  # NEW: Add loot system
        }
        
        # Execute dice roll if required
        if action_analysis['requires_roll']:
            roll = self.game_manager.execute_dice_roll(
                stat=action_analysis['stat_used'],
                skill=action_analysis['skill_used'],
                difficulty=action_analysis['difficulty'],
                context=action_analysis['action_type'].value
            )
            results['dice_rolls'].append(roll)
            
            # Award XP based on success and action type
            if action_analysis['xp_eligible']:
                if roll.success:
                    xp_amount = self._calculate_xp_reward(action_analysis['action_type'], True)
                    xp_result = self.game_manager.award_xp(
                        xp_amount, 
                        f"Successful {action_analysis['action_type'].value}",
                        action_analysis['action_type'].value
                    )
                    results['xp_awards'].append(xp_result)
                    
                    # Chance for loot on successful actions
                    loot = self._check_loot_discovery(action_analysis, roll)
                    if loot:
                        results['loot_discovered'].append(loot)
                        
                else:
                    # Small XP for attempt
                    xp_amount = 5
                    xp_result = self.game_manager.award_xp(
                        xp_amount,
                        f"Learning from {action_analysis['action_type'].value} attempt",
                        "learning"
                    )
                    results['xp_awards'].append(xp_result)
        
        return results
    
    def _execute_smart_mechanics(self, action_analysis: Dict, battle_results: Dict) -> Dict:
        """Execute mechanics only when actually needed based on smart analysis"""
        results = {
            'dice_rolls': [],
            'xp_awards': [],
            'state_changes': {},
            'loot_discovered': [],
            'battle_results': battle_results
        }
        
        # Only roll dice if analysis says it's needed
        if action_analysis['requires_roll']:
            roll = self.game_manager.execute_dice_roll(
                stat=action_analysis['stat_used'],
                skill=action_analysis['skill_used'],
                difficulty=action_analysis['difficulty'],
                context=action_analysis['action_type'].value
            )
            results['dice_rolls'].append(roll)
            
            # Award XP based on smart analysis
            if action_analysis['xp_eligible']:
                xp_amount = self.action_analyzer.get_xp_amount(action_analysis, roll.success)
                if xp_amount > 0:
                    xp_result = self.game_manager.award_xp(
                        xp_amount, 
                        f"{'Successful' if roll.success else 'Attempted'} {action_analysis['action_type'].value}",
                        action_analysis['action_type'].value
                    )
                    results['xp_awards'].append(xp_result)
        
        elif action_analysis['auto_success']:
            # Auto-success actions might still give small XP for story progression
            if action_analysis.get('story_progression', False):
                xp_result = self.game_manager.award_xp(
                    5, 
                    "Story progression",
                    "exploration"
                )
                results['xp_awards'].append(xp_result)
        
        # Handle battle damage to player
        if battle_results.get('enemy_damage_taken', 0) > 0:
            damage = battle_results['enemy_damage_taken']
            self.game_manager.character['resources']['hp'] = max(
                0, 
                self.game_manager.character['resources']['hp'] - damage
            )
            results['state_changes']['hp_damage'] = damage
        
        # Handle loot from battle
        if battle_results.get('loot_gained'):
            results['loot_discovered'].extend(battle_results['loot_gained'])
        
        return results
    
    def _check_loot_discovery(self, action_analysis: Dict, roll) -> Dict:
        """Check for loot discovery on successful actions"""
        import random
        
        # 30% chance for loot on successful combat/exploration
        if action_analysis['action_type'] in [ActionType.COMBAT, ActionType.EXPLORATION] and random.random() < 0.3:
            loot_types = [
                {'name': 'Healing Potion', 'type': 'consumable', 'effect': 'Restores 10 HP'},
                {'name': 'Energy Crystal', 'type': 'consumable', 'effect': 'Restores 5 Energy'},
                {'name': 'Silver Coins', 'type': 'currency', 'effect': '25 silver pieces'},
                {'name': 'Magic Scroll', 'type': 'consumable', 'effect': 'Single-use spell'},
                {'name': 'Blessed Charm', 'type': 'accessory', 'effect': '+1 to next roll'}
            ]
            return random.choice(loot_types)
        
        return None
    
    def _calculate_xp_reward(self, action_type: ActionType, success: bool) -> int:
        """Calculate XP reward based on action type and success"""
        base_rewards = {
            ActionType.COMBAT: 25,
            ActionType.SKILL_CHECK: 15,
            ActionType.SOCIAL: 20,
            ActionType.EXPLORATION: 10,
            ActionType.MAGIC: 20
        }
        
        base = base_rewards.get(action_type, 10)
        return base if success else max(5, base // 3)
    
    def _build_game_start_prompt(self) -> str:
        """Build initial game start prompt"""
        character = self.game_manager.character
        
        return f"""You are Emberlyn, a wise fairy companion in the Fire Whisper RPG.

CURRENT CHARACTER:
Name: {character['name']}
Class: {character['class']}
Level: {character['level']}
Stats: STR {character['stats']['strength']}, DEX {character['stats']['dexterity']}, INT {character['stats']['intelligence']}, CHA {character['stats']['charisma']}
HP: {character['resources']['hp']}/{character['resources']['max_hp']}
XP: {character['xp']}/100

CRITICAL RULES:
- You provide ONLY narrative and dialogue
- ALL dice rolls are pre-calculated and provided to you
- ALL XP awards are pre-calculated and provided to you
- NEVER modify character stats, XP, or HP yourself
- NEVER use commanding phrases like 'you must', 'you decide to', 'you automatically'
- NEVER mention dice rolls, XP gains, or mechanical calculations
- Use suggestive language like 'you could', 'perhaps', 'Emberlyn suggests'
- DO NOT include action choices or options in your response - these will be added automatically
- End your response with the narrative only, no choices or options

Start the adventure with Emberlyn introducing herself and presenting the first challenge."""
    
    def _build_action_prompt(self, player_input: str, action_analysis: Dict, 
                           mechanical_results: Dict, battle_results: Dict, needs_refresh: bool) -> str:
        """Build prompt for processing player action"""
        character = self.game_manager.character
        
        # Get structured context from story manager
        story_context = self.story_manager.get_current_context()
        context_summary = self.story_manager.get_narrative_context_summary()
        
        # Get progression context to prevent loops
        progression_context = self.game_manager.get_progression_context()
        
        # Debug context info
        if os.getenv("DEBUG_MODE", "false").lower() == "true":
            print(f"🌍 CONTEXT: {context_summary[:100]}...")
            print(f"📍 LOCATION: {story_context['location']['name']}")
        
        prompt = f"""You are Emberlyn, the fairy companion in Fire Whisper RPG.

STORY CONTEXT: {context_summary}
LOCATION: {story_context['location']['name']} - {story_context['location']['description']}
PROGRESSION STATE: Story Progress {progression_context['story_progress']}, Turn {progression_context['total_turns']}, {progression_context['turns_at_location']} turns at current location
ENEMIES PRESENT: {', '.join(story_context['enemies_present']) if story_context['enemies_present'] else 'None'}
NPCs PRESENT: {', '.join([npc['name'] for npc in story_context['npcs_present']]) if story_context['npcs_present'] else 'None'}
RECENT EVENTS: {', '.join(story_context['recent_events'][-2:]) if story_context['recent_events'] else 'None'}

CURRENT CHARACTER STATE:
Name: {character['name']} (Level {character['level']} {character['class']})
Stats: STR {character['stats']['strength']} (+{max(0, (character['stats']['strength']-10)//2)}), DEX {character['stats']['dexterity']} (+{max(0, (character['stats']['dexterity']-10)//2)}), INT {character['stats']['intelligence']} (+{max(0, (character['stats']['intelligence']-10)//2)}), CHA {character['stats']['charisma']} (+{max(0, (character['stats']['charisma']-10)//2)})
Resources: {character['resources']['hp']}/{character['resources']['max_hp']} HP, {character['resources']['energy']}/{character['resources']['max_energy']} Energy
XP: {character['xp']} (Level {character['level']})

PLAYER ACTION: {player_input}

BATTLE STATUS:"""
        
        # Add battle status if active
        if battle_results.get('battle_status', {}).get('in_battle', False):
            battle_status = battle_results['battle_status']
            prompt += f"""
⚔️ BATTLE ACTIVE - Round {battle_status['round']}"""
            for enemy in battle_status['enemies']:
                if enemy['alive']:
                    health_bar = "█" * (enemy['health_percent'] // 10)
                    health_bar += "░" * (10 - len(health_bar))
                    prompt += f"""
🔴 {enemy['name']}: {enemy['hp']}/{enemy['max_hp']} HP [{health_bar}]"""
                else:
                    prompt += f"""
💀 {enemy['name']}: DEFEATED"""
            
            # Add battle results
            if battle_results.get('player_damage_dealt', 0) > 0:
                prompt += f"""
⚔️ You dealt {battle_results['player_damage_dealt']} damage!"""
            
            if battle_results.get('enemy_damage_taken', 0) > 0:
                prompt += f"""
💔 You took {battle_results['enemy_damage_taken']} damage!"""
            
            if battle_results.get('enemies_defeated'):
                prompt += f"""
🏆 Defeated: {', '.join(battle_results['enemies_defeated'])}"""
            
            if battle_results.get('loot_gained'):
                for loot in battle_results['loot_gained']:
                    prompt += f"""
💎 Loot gained: {loot['name']}"""
        else:
            prompt += """
No active battle."""
        
        prompt += """

MECHANICAL RESULTS (ALREADY CALCULATED):"""
        
        # Add dice roll results
        for roll in mechanical_results['dice_rolls']:
            modifiers_text = " + ".join([f"{k} +{v}" for k, v in roll.modifiers.items()])
            result_text = "SUCCESS" if roll.success else "FAILURE"
            prompt += f"""
🎲 {roll.roll_type.title()} Roll: {roll.base_roll} + {sum(roll.modifiers.values())} ({modifiers_text}) = {roll.base_roll + sum(roll.modifiers.values())} vs {roll.target}
Result: {result_text}"""
        
        # Add XP awards
        for xp_award in mechanical_results['xp_awards']:
            prompt += f"""
✨ XP Award: +{xp_award['xp_awarded']} for {xp_award['reason']}
New XP Total: {xp_award['new_xp']}"""
            
            if xp_award['level_up']:
                prompt += f"""
🎉 LEVEL UP! Now Level {xp_award['new_level']}!
New Abilities: {', '.join(xp_award['new_abilities'])}"""
        
        # Add loot discoveries
        for loot in mechanical_results.get('loot_discovered', []):
            prompt += f"""
💎 LOOT DISCOVERED: {loot['name']} - {loot['effect']}"""
        
        prompt += f"""

CRITICAL CONSTRAINTS (NEVER VIOLATE):
- NEVER describe dice rolls, XP calculations, or mechanical processes
- NEVER use phrases like 'you must', 'you decide to', 'you automatically', 'you walk', 'you attack', 'you cast'
- NEVER mention rolling, calculating, or game mechanics
- NEVER say things like 'rolling 15+3=18' or 'you gain 25 XP' or 'level up'
- WAIT for player input - do not assume their actions
- Use phrases like 'Emberlyn suggests', 'you could', 'perhaps', 'you might consider'
- If asked about mechanics, redirect to narrative only
- Focus ONLY on story, dialogue, and atmosphere
- DO NOT include action choices or options in your response - these will be added automatically
- End your response with narrative only, no player choices
- MAINTAIN STORY CONTINUITY - continue from the current situation, don't restart or ignore context
- RESPOND TO THE PLAYER'S ACTUAL ACTION - don't give generic responses
- DO NOT repeat the same introduction over and over - the story should progress
- ACKNOWLEDGE what the player just did and build on it
- If player takes defensive stance, describe what they observe from that position
- If enemies are present, focus on them; if not, focus on the current location details

Generate response now:"""
        
        if needs_refresh:
            prompt += "\n\n[CONTEXT REFRESH: This is a fresh context to prevent rule drift]"
        
        return prompt
    
    def _call_ai(self, prompt: str) -> str:
        """Make API call to Claude"""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"AI Error: {str(e)}"
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse AI response and validate compliance"""
        violations = []
        
        # Check for hallucination patterns (AI mentioning mechanics)
        import re
        hallucination_patterns = [
            r'you gain \d+ xp',
            r'rolling.*\d+.*\+.*\d+',
            r'your level increases',
            r'you now have \d+ hp',
            r'dice.*result.*\d+',
            r'xp.*awarded',
            r'level.*up',
            r'your.*stat.*is now'
        ]
        
        response_lower = response.lower()
        for pattern in hallucination_patterns:
            if re.search(pattern, response_lower):
                violations.append(f"Hallucination detected: '{pattern}' in response")
        
        # Check for agency violation patterns
        agency_violation_patterns = [
            'you decide to',
            'you automatically', 
            'without thinking',
            'you have no choice',
            'you must',
            'you walk',
            'you attack',
            'you cast'
        ]
        
        for pattern in agency_violation_patterns:
            if pattern in response_lower:
                violations.append(f"Agency violation: '{pattern}' in response")
        
        # Clean response if violations found
        cleaned_response = response
        if violations:
            cleaned_response = self._generate_fallback_response()
        
        return {
            'narrative': cleaned_response,
            'violations': violations
        }
    
    def _generate_fallback_response(self) -> str:
        """Generate a safe fallback response when AI violates constraints"""
        return "*Emberlyn flutters her wings thoughtfully, considering the situation carefully.*\n\n\"Let me think about this for a moment,\" she says softly. \"There are several paths we could explore here.\"\n\n*She gestures toward different directions, her magical glow illuminating the possibilities.*\n\n**What would you like to do?**\n1. Take a direct approach\n2. Try a more careful strategy\n3. Look for alternative solutions\n4. Ask Emberlyn for guidance"
    
    def get_character_sheet(self) -> str:
        """Get formatted character sheet"""
        if not self.game_manager:
            return "No active game"
        
        char = self.game_manager.character
        return f"""
📊 **{char['name']}** - Level {char['level']} {char['class']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💪 STR: {char['stats']['strength']} (+{max(0, (char['stats']['strength']-10)//2)}) | 🏃 DEX: {char['stats']['dexterity']} (+{max(0, (char['stats']['dexterity']-10)//2)})
🧠 INT: {char['stats']['intelligence']} (+{max(0, (char['stats']['intelligence']-10)//2)}) | 💬 CHA: {char['stats']['charisma']} (+{max(0, (char['stats']['charisma']-10)//2)})

❤️ HP: {char['resources']['hp']}/{char['resources']['max_hp']} | ⚡ Energy: {char['resources']['energy']}/{char['resources']['max_energy']}
✨ XP: {char['xp']} | 🧚‍♀️ Emberlyn Bond: Level {char['emberlyn_bond']}

🎯 SKILLS:
{chr(10).join([f"   {skill}: Level {level}" for skill, level in char['skills'].items()])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""