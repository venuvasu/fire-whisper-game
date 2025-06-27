"""
AI Integration Layer - Manages AI interactions with deterministic game logic
"""
import json
from typing import Dict, List, Any, Optional
from anthropic import Anthropic
from .game_state_manager import GameStateManager, ActionType

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
        
    def start_new_game(self, character_data: Dict = None) -> Dict:
        """Initialize a new game with deterministic state management"""
        self.game_manager = GameStateManager(character_data)
        
        # Get initial narrative from AI
        initial_prompt = self._build_game_start_prompt()
        response = self._call_ai(initial_prompt)
        
        return {
            'narrative': response,
            'character': self.game_manager.character,
            'game_state': self.game_manager.get_current_state()
        }
    
    def process_player_action(self, player_input: str) -> Dict:
        """Process player action with deterministic mechanics"""
        if not self.game_manager:
            raise ValueError("Game not initialized")
        
        # Increment turn and check for context refresh
        needs_refresh = self.game_manager.increment_turn()
        
        # Parse player intent and determine required mechanics
        action_analysis = self._analyze_player_action(player_input)
        
        # Execute any required dice rolls BEFORE AI call
        mechanical_results = self._execute_mechanics(action_analysis)
        
        # Build AI prompt with pre-calculated results
        ai_prompt = self._build_action_prompt(
            player_input, 
            action_analysis, 
            mechanical_results,
            needs_refresh
        )
        
        # Get narrative response from AI
        ai_response = self._call_ai(ai_prompt)
        
        # Parse AI response and validate compliance
        parsed_response = self._parse_ai_response(ai_response)
        
        # Handle violations
        if parsed_response['violations']:
            self.game_manager.add_rule_violation(f"AI Hallucination: {parsed_response['violations']}")
            # Could regenerate response here in production
        
        # Clear used mechanics
        self.game_manager.clear_pending_rolls()
        
        return {
            'narrative': parsed_response['narrative'],
            'mechanical_results': mechanical_results,
            'character': self.game_manager.character,
            'game_state': self.game_manager.get_current_state(),
            'context_refreshed': needs_refresh
        }
    
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
            'state_changes': {}
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
- Present 3-4 action choices that use different character abilities

Start the adventure with Emberlyn introducing herself and presenting the first challenge."""
    
    def _build_action_prompt(self, player_input: str, action_analysis: Dict, 
                           mechanical_results: Dict, needs_refresh: bool) -> str:
        """Build prompt for processing player action"""
        character = self.game_manager.character
        
        prompt = f"""You are Emberlyn, the fairy companion in Fire Whisper RPG.

CURRENT CHARACTER STATE:
Name: {character['name']} (Level {character['level']} {character['class']})
Stats: STR {character['stats']['strength']} (+{max(0, (character['stats']['strength']-10)//2)}), DEX {character['stats']['dexterity']} (+{max(0, (character['stats']['dexterity']-10)//2)}), INT {character['stats']['intelligence']} (+{max(0, (character['stats']['intelligence']-10)//2)}), CHA {character['stats']['charisma']} (+{max(0, (character['stats']['charisma']-10)//2)})
Resources: {character['resources']['hp']}/{character['resources']['max_hp']} HP, {character['resources']['energy']}/{character['resources']['max_energy']} Energy
XP: {character['xp']} (Level {character['level']})

PLAYER ACTION: {player_input}
ACTION INTERPRETATION: The player chose option {player_input} from the previously presented choices.

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
- Present choices without commanding the player

ACTION DESCRIPTION:
The player chose option {player_input}.
Describe the narrative outcome of: {action_analysis['action_type'].value} using {action_analysis['stat_used']} + {action_analysis['skill_used']}

RESPONSE FORMAT:
1. Describe what happens in the story (no mechanics)
2. Give consequences based on success/failure
3. Present 4 new action choices
4. Stay purely narrative - no dice or XP mentions

FORBIDDEN:
- Do NOT change the scenario or setting
- Do NOT ignore the dice results
- Do NOT invent new magical effects
- Do NOT award different XP amounts
- Do NOT describe actions the player didn't choose

Your response must be EXACTLY about the action: {action_analysis['action_type'].value} with {action_analysis['stat_used']} + {action_analysis['skill_used']}

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