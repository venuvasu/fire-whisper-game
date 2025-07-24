"""
Smart Action Analyzer - Determines when dice rolls are actually needed
Only rolls for meaningful, uncertain outcomes with consequences
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from .game_state_manager import ActionType

class ActionCategory(Enum):
    TRIVIAL = "trivial"          # No roll needed - automatic success
    MEANINGFUL = "meaningful"     # Roll needed - uncertain outcome
    IMPOSSIBLE = "impossible"     # No roll needed - automatic failure
    SOCIAL = "social"            # Roll for social interactions
    EXPLORATION = "exploration"   # Roll for discovery/investigation

class SmartActionAnalyzer:
    """Analyzes player actions to determine if dice rolls are needed"""
    
    def __init__(self):
        # Actions that should NEVER require rolls (trivial/automatic)
        self.trivial_actions = [
            'look around', 'examine', 'walk', 'move', 'go to', 'enter',
            'talk to', 'speak with', 'say', 'tell', 'ask',
            'take', 'pick up', 'grab', 'put down', 'drop',
            'open door', 'close door', 'sit down', 'stand up',
            'eat', 'drink', 'rest', 'sleep', 'wake up'
        ]
        
        # Actions that should ALWAYS require rolls (meaningful/risky)
        self.meaningful_actions = [
            'attack', 'fight', 'strike', 'charge', 'battle', 'combat',
            'cast spell', 'use magic', 'heal', 'channel divine',
            'sneak', 'hide', 'stealth', 'pickpocket', 'steal',
            'climb', 'jump', 'leap', 'swim', 'run fast',
            'persuade', 'convince', 'intimidate', 'deceive', 'lie',
            'pick lock', 'disable trap', 'break down door',
            'track', 'hunt', 'search for hidden', 'investigate clues'
        ]
        
        # Context keywords that indicate risk/uncertainty
        self.risk_indicators = [
            'dangerous', 'risky', 'difficult', 'challenging', 'guarded',
            'trapped', 'hidden', 'secret', 'locked', 'enemy', 'hostile',
            'time pressure', 'quickly', 'quietly', 'carefully', 'precisely'
        ]
        
        # Keywords that indicate no risk (safe situations)
        self.safe_indicators = [
            'safe', 'peaceful', 'friendly', 'open', 'obvious', 'easy',
            'plenty of time', 'no rush', 'no danger', 'alone', 'private'
        ]
    
    def analyze_action(self, player_input: str, situation_context: str, 
                      character: Dict, battle_active: bool = False) -> Dict:
        """
        Analyze if an action needs a dice roll based on:
        1. Action type (trivial vs meaningful)
        2. Context (safe vs risky)
        3. Character capabilities
        4. Battle state
        """
        
        player_lower = player_input.lower().strip()
        context_lower = situation_context.lower()
        
        analysis = {
            'requires_roll': False,
            'action_category': ActionCategory.TRIVIAL,
            'action_type': ActionType.SKILL_CHECK,
            'stat_used': 'charisma',
            'skill_used': 'Persuasion',
            'difficulty': 'normal',
            'xp_eligible': False,
            'reasoning': '',
            'auto_success': False,
            'auto_failure': False
        }
        
        # BATTLE ACTIONS - Always meaningful if in battle
        if battle_active:
            if any(word in player_lower for word in ['attack', 'fight', 'strike', 'charge', 'cast', 'heal']):
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.COMBAT,
                    'stat_used': 'strength',
                    'skill_used': 'Combat',
                    'difficulty': 'normal',
                    'xp_eligible': True,
                    'reasoning': 'Combat action in battle - outcome uncertain'
                })
                return analysis
        
        # MOVEMENT/BASIC ACTIONS - Usually trivial
        if any(phrase in player_lower for phrase in ['walk', 'go to', 'move to', 'enter', 'leave', 'approach']):
            # Check if movement is risky
            if any(risk in context_lower for risk in ['trap', 'guard', 'dangerous', 'cliff', 'unstable']):
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.SKILL_CHECK,
                    'stat_used': 'dexterity',
                    'skill_used': 'Athletics',
                    'difficulty': 'normal',
                    'xp_eligible': True,
                    'reasoning': 'Movement in dangerous area - risk of failure'
                })
            else:
                analysis.update({
                    'auto_success': True,
                    'reasoning': 'Simple movement - no roll needed'
                })
            return analysis
        
        # SOCIAL ACTIONS - Roll if outcome uncertain
        if any(word in player_lower for word in ['persuade', 'convince', 'negotiate', 'intimidate', 'deceive']):
            # Check if target is friendly/hostile
            if any(word in context_lower for word in ['friendly', 'ally', 'helpful', 'agrees']):
                analysis.update({
                    'auto_success': True,
                    'reasoning': 'Social action with friendly target - automatic success'
                })
            elif any(word in context_lower for word in ['hostile', 'enemy', 'angry', 'refuses']):
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.SOCIAL,
                    'stat_used': 'charisma',
                    'skill_used': 'Persuasion',
                    'difficulty': 'hard',
                    'xp_eligible': True,
                    'reasoning': 'Social action with hostile target - difficult but possible'
                })
            else:
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.SOCIAL,
                    'stat_used': 'charisma',
                    'skill_used': 'Persuasion',
                    'difficulty': 'normal',
                    'xp_eligible': True,
                    'reasoning': 'Social action with uncertain outcome'
                })
            return analysis
        
        # MAGIC ACTIONS - Always meaningful
        if any(word in player_lower for word in ['cast', 'spell', 'magic', 'heal', 'divine', 'channel']):
            analysis.update({
                'requires_roll': True,
                'action_category': ActionCategory.MEANINGFUL,
                'action_type': ActionType.MAGIC,
                'stat_used': 'charisma' if character.get('class') == 'Cleric' else 'intelligence',
                'skill_used': 'Healing' if 'heal' in player_lower else 'Magic',
                'difficulty': 'normal',
                'xp_eligible': True,
                'reasoning': 'Magic use - outcome depends on skill and circumstances'
            })
            return analysis
        
        # STEALTH ACTIONS - Meaningful if detection possible
        if any(word in player_lower for word in ['sneak', 'hide', 'stealth', 'quietly']):
            if any(word in context_lower for word in ['guard', 'enemy', 'patrol', 'watching']):
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.SKILL_CHECK,
                    'stat_used': 'dexterity',
                    'skill_used': 'Stealth',
                    'difficulty': 'normal',
                    'xp_eligible': True,
                    'reasoning': 'Stealth with detection risk - roll needed'
                })
            else:
                analysis.update({
                    'auto_success': True,
                    'reasoning': 'Stealth with no observers - automatic success'
                })
            return analysis
        
        # INVESTIGATION/SEARCH - Roll if something might be hidden
        if any(word in player_lower for word in ['search', 'investigate', 'examine', 'look for', 'find']):
            # Check for hidden/secret things in either player input or context
            hidden_keywords = ['hidden', 'secret', 'concealed', 'clue', 'trap', 'mystery', 'detect']
            searching_for_hidden = any(word in player_lower for word in hidden_keywords) or any(word in context_lower for word in hidden_keywords)
            
            if searching_for_hidden:
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.SKILL_CHECK,
                    'stat_used': 'intelligence',
                    'skill_used': 'Investigation',
                    'difficulty': 'normal',
                    'xp_eligible': True,
                    'reasoning': 'Searching for hidden things - success not guaranteed'
                })
            else:
                analysis.update({
                    'auto_success': True,
                    'reasoning': 'Examining obvious things - no roll needed'
                })
            return analysis
        
        # SKILL CHALLENGES - Check if actually challenging
        if any(word in player_lower for word in ['climb', 'jump', 'swim', 'balance', 'acrobatics']):
            if any(word in context_lower for word in ['high', 'far', 'difficult', 'dangerous', 'slippery']):
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.SKILL_CHECK,
                    'stat_used': 'dexterity',
                    'skill_used': 'Athletics',
                    'difficulty': 'normal',
                    'xp_eligible': True,
                    'reasoning': 'Challenging physical action - failure possible'
                })
            else:
                analysis.update({
                    'auto_success': True,
                    'reasoning': 'Simple physical action - no roll needed'
                })
            return analysis
        
        # COMBAT ACTIONS - Always meaningful
        if any(word in player_lower for word in ['attack', 'fight', 'strike', 'charge', 'battle']):
            analysis.update({
                'requires_roll': True,
                'action_category': ActionCategory.MEANINGFUL,
                'action_type': ActionType.COMBAT,
                'stat_used': 'strength',
                'skill_used': 'Combat',
                'difficulty': 'normal',
                'xp_eligible': True,
                'reasoning': 'Combat action - hit/miss uncertain'
            })
            return analysis
        
        # CREATIVE/UNUSUAL ACTIONS - Analyze based on context
        if any(word in player_lower for word in ['creative', 'innovative', 'unusual', 'try', 'attempt']):
            # Creative actions usually need rolls since outcome is uncertain
            analysis.update({
                'requires_roll': True,
                'action_category': ActionCategory.MEANINGFUL,
                'action_type': ActionType.SKILL_CHECK,
                'stat_used': 'intelligence',
                'skill_used': 'Problem Solving',
                'difficulty': 'normal',
                'xp_eligible': True,
                'reasoning': 'Creative solution - outcome uncertain'
            })
            return analysis
        
        # ESCAPE/FLEE ACTIONS
        if any(word in player_lower for word in ['run away', 'flee', 'escape', 'retreat']):
            if any(word in context_lower for word in ['chase', 'pursuit', 'fast', 'catch']):
                analysis.update({
                    'requires_roll': True,
                    'action_category': ActionCategory.MEANINGFUL,
                    'action_type': ActionType.SKILL_CHECK,
                    'stat_used': 'dexterity',
                    'skill_used': 'Athletics',
                    'difficulty': 'normal',
                    'xp_eligible': False,  # No XP for running away
                    'reasoning': 'Escape attempt with pursuit - success uncertain'
                })
            else:
                analysis.update({
                    'auto_success': True,
                    'reasoning': 'Leaving safe area - no roll needed'
                })
            return analysis
        
        # DEFAULT - Simple actions that don't need rolls
        analysis.update({
            'auto_success': True,
            'reasoning': 'Simple action with no meaningful risk or uncertainty'
        })
        
        return analysis
    
    def should_award_xp(self, analysis: Dict, success: bool) -> bool:
        """Determine if XP should be awarded for this action"""
        
        # Only award XP for meaningful actions
        if analysis['action_category'] != ActionCategory.MEANINGFUL:
            return False
        
        # Don't award XP for fleeing
        if 'run away' in analysis.get('reasoning', '').lower():
            return False
        
        # Award XP for attempts at meaningful actions, more for success
        return True
    
    def get_xp_amount(self, analysis: Dict, success: bool) -> int:
        """Calculate XP amount based on action and outcome"""
        
        if not self.should_award_xp(analysis, success):
            return 0
        
        base_amounts = {
            ActionType.COMBAT: 25,
            ActionType.MAGIC: 20,
            ActionType.SOCIAL: 15,
            ActionType.SKILL_CHECK: 10,
            ActionType.EXPLORATION: 10
        }
        
        base = base_amounts.get(analysis['action_type'], 5)
        
        # Reduce XP for failure, but still give some for trying
        if not success:
            base = max(3, base // 3)
        
        # Bonus for difficult actions
        if analysis.get('difficulty') == 'hard':
            base = int(base * 1.5)
        elif analysis.get('difficulty') == 'extreme':
            base = int(base * 2)
        
        return base