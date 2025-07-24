"""
Action System with Real Consequences
Processes player actions with dice-based outcomes and meaningful consequences
"""
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from .dice_system import get_dice_system, DiceResult, RollResult, DifficultyClass
from .game_engine import LocationId, ActionType

@dataclass
class ActionConsequence:
    """Represents the consequence of a player action"""
    success: bool
    narrative_outcome: str
    mechanical_effects: Dict[str, Any]
    state_changes: Dict[str, Any]
    roll_result: Optional[RollResult] = None

class ActionProcessor:
    """
    Processes player actions with real consequences
    Uses dice system for randomness, applies results to game state
    """
    
    def __init__(self):
        self.dice_system = get_dice_system()
    
    def process_action(self, action_type: str, character: Dict[str, Any], 
                      game_state: Dict[str, Any], context: Dict[str, Any] = None) -> ActionConsequence:
        """
        Process a player action with dice-based consequences
        Returns concrete outcomes that affect the game world
        """
        context = context or {}
        
        # Make the dice roll
        roll_result = self.dice_system.make_action_check(
            character.get('stats', {}), 
            action_type, 
            context
        )
        
        # Process consequences based on roll result
        if roll_result.result == DiceResult.CRITICAL_SUCCESS:
            return self._handle_critical_success(action_type, roll_result, character, game_state, context)
        elif roll_result.result == DiceResult.SUCCESS:
            return self._handle_success(action_type, roll_result, character, game_state, context)
        elif roll_result.result == DiceResult.FAILURE:
            return self._handle_failure(action_type, roll_result, character, game_state, context)
        else:  # CRITICAL_FAILURE
            return self._handle_critical_failure(action_type, roll_result, character, game_state, context)
    
    def _handle_critical_success(self, action_type: str, roll_result: RollResult, 
                                character: Dict[str, Any], game_state: Dict[str, Any], 
                                context: Dict[str, Any]) -> ActionConsequence:
        """Handle critical success outcomes"""
        base_outcome = self._get_base_success_outcome(action_type, game_state, context)
        
        # Enhance the outcome for critical success
        enhanced_effects = base_outcome['mechanical_effects'].copy()
        enhanced_state = base_outcome['state_changes'].copy()
        
        if action_type == 'examine':
            enhanced_effects['bonus_discovery'] = True
            enhanced_effects['hidden_secrets_revealed'] = True
            enhanced_state['investigation_bonus'] = 2
            narrative = f"🎯 CRITICAL SUCCESS! {base_outcome['narrative']} You notice details that others would miss entirely!"
            
        elif action_type == 'move':
            enhanced_effects['fast_travel'] = True
            enhanced_effects['no_random_encounters'] = True
            enhanced_state['movement_bonus'] = True
            narrative = f"🎯 CRITICAL SUCCESS! {base_outcome['narrative']} You find the perfect path and make excellent time!"
            
        elif action_type == 'social':
            enhanced_effects['reputation_boost'] = True
            enhanced_effects['future_advantage'] = True
            enhanced_state['social_standing'] = enhanced_state.get('social_standing', 0) + 2
            narrative = f"🎯 CRITICAL SUCCESS! {base_outcome['narrative']} Your words resonate perfectly - people will remember this!"
            
        elif action_type == 'magic':
            enhanced_effects['spell_enhancement'] = True
            enhanced_effects['mana_efficiency'] = True
            enhanced_state['magical_resonance'] = True
            narrative = f"🎯 CRITICAL SUCCESS! {base_outcome['narrative']} The magic flows through you with unprecedented clarity!"
            
        else:
            enhanced_effects['exceptional_outcome'] = True
            narrative = f"🎯 CRITICAL SUCCESS! {base_outcome['narrative']} Everything goes better than you could have hoped!"
        
        return ActionConsequence(
            success=True,
            narrative_outcome=narrative,
            mechanical_effects=enhanced_effects,
            state_changes=enhanced_state,
            roll_result=roll_result
        )
    
    def _handle_success(self, action_type: str, roll_result: RollResult, 
                       character: Dict[str, Any], game_state: Dict[str, Any], 
                       context: Dict[str, Any]) -> ActionConsequence:
        """Handle regular success outcomes"""
        outcome = self._get_base_success_outcome(action_type, game_state, context)
        
        narrative = f"✅ SUCCESS! {outcome['narrative']}"
        
        return ActionConsequence(
            success=True,
            narrative_outcome=narrative,
            mechanical_effects=outcome['mechanical_effects'],
            state_changes=outcome['state_changes'],
            roll_result=roll_result
        )
    
    def _handle_failure(self, action_type: str, roll_result: RollResult, 
                       character: Dict[str, Any], game_state: Dict[str, Any], 
                       context: Dict[str, Any]) -> ActionConsequence:
        """Handle failure outcomes with meaningful consequences"""
        
        if action_type == 'examine':
            return ActionConsequence(
                success=False,
                narrative_outcome="❌ FAILURE! You look around but miss important details. The area seems ordinary to you.",
                mechanical_effects={'missed_clues': True, 'time_wasted': True},
                state_changes={'investigation_penalty': -1},
                roll_result=roll_result
            )
            
        elif action_type == 'move':
            return ActionConsequence(
                success=False,
                narrative_outcome="❌ FAILURE! You stumble or take a wrong turn. Progress is slow and you feel disoriented.",
                mechanical_effects={'movement_penalty': True, 'potential_danger': True},
                state_changes={'movement_setback': True, 'time_lost': 1},
                roll_result=roll_result
            )
            
        elif action_type == 'social':
            return ActionConsequence(
                success=False,
                narrative_outcome="❌ FAILURE! Your words don't land well. The conversation becomes awkward and tense.",
                mechanical_effects={'social_penalty': True, 'trust_decreased': True},
                state_changes={'social_standing': -1, 'conversation_difficulty': 1},
                roll_result=roll_result
            )
            
        elif action_type == 'magic':
            return ActionConsequence(
                success=False,
                narrative_outcome="❌ FAILURE! The magic fizzles out. You feel the energy drain away without effect.",
                mechanical_effects={'mana_wasted': True, 'spell_failure': True},
                state_changes={'magical_fatigue': 1, 'confidence_shaken': True},
                roll_result=roll_result
            )
            
        else:
            return ActionConsequence(
                success=False,
                narrative_outcome="❌ FAILURE! Your attempt doesn't work out as planned. You'll need to try a different approach.",
                mechanical_effects={'action_failed': True, 'time_wasted': True},
                state_changes={'frustration': 1},
                roll_result=roll_result
            )
    
    def _handle_critical_failure(self, action_type: str, roll_result: RollResult, 
                                character: Dict[str, Any], game_state: Dict[str, Any], 
                                context: Dict[str, Any]) -> ActionConsequence:
        """Handle critical failure with serious consequences"""
        
        if action_type == 'examine':
            return ActionConsequence(
                success=False,
                narrative_outcome="💥 CRITICAL FAILURE! You're so focused on looking that you miss obvious dangers. Something bad is about to happen!",
                mechanical_effects={'danger_triggered': True, 'vulnerability': True, 'major_oversight': True},
                state_changes={'investigation_penalty': -3, 'danger_level': 1},
                roll_result=roll_result
            )
            
        elif action_type == 'move':
            return ActionConsequence(
                success=False,
                narrative_outcome="💥 CRITICAL FAILURE! You trip, fall, or get completely lost. This is going to cause problems!",
                mechanical_effects={'injury_risk': True, 'lost': True, 'equipment_damage': True},
                state_changes={'hp_damage': 2, 'location_confusion': True, 'time_lost': 3},
                roll_result=roll_result
            )
            
        elif action_type == 'social':
            return ActionConsequence(
                success=False,
                narrative_outcome="💥 CRITICAL FAILURE! You say exactly the wrong thing at the wrong time. People are now actively hostile!",
                mechanical_effects={'hostility_triggered': True, 'reputation_damaged': True, 'future_disadvantage': True},
                state_changes={'social_standing': -3, 'enemies_made': 1, 'conversation_ended': True},
                roll_result=roll_result
            )
            
        elif action_type == 'magic':
            return ActionConsequence(
                success=False,
                narrative_outcome="💥 CRITICAL FAILURE! The magic backfires spectacularly! Dangerous magical energy surges uncontrolled!",
                mechanical_effects={'magical_backlash': True, 'area_damage': True, 'mana_burn': True},
                state_changes={'hp_damage': 3, 'mana_damage': 5, 'magical_instability': 2},
                roll_result=roll_result
            )
            
        else:
            return ActionConsequence(
                success=False,
                narrative_outcome="💥 CRITICAL FAILURE! Not only does your action fail, but it makes everything worse!",
                mechanical_effects={'catastrophic_failure': True, 'complications_added': True},
                state_changes={'situation_worsened': 2, 'morale_damage': 1},
                roll_result=roll_result
            )
    
    def _get_base_success_outcome(self, action_type: str, game_state: Dict[str, Any], 
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Get base success outcome for action type"""
        
        current_location = game_state.get('location', LocationId.VILLAGE_OUTSKIRTS)
        
        if action_type == 'examine':
            return {
                'narrative': "You carefully examine your surroundings and notice important details.",
                'mechanical_effects': {'clues_discovered': True, 'area_knowledge': True},
                'state_changes': {'investigation_progress': 1, 'location_familiarity': 1}
            }
            
        elif action_type == 'move':
            # Actually progress to next location
            next_location = self._determine_next_location(current_location, context)
            return {
                'narrative': f"You successfully move forward, making real progress on your journey.",
                'mechanical_effects': {'location_changed': True, 'progress_made': True},
                'state_changes': {'location': next_location, 'story_progress': 1}
            }
            
        elif action_type == 'social':
            return {
                'narrative': "Your social interaction goes well. People respond positively to you.",
                'mechanical_effects': {'information_gained': True, 'relationships_improved': True},
                'state_changes': {'social_standing': 1, 'trust_gained': True}
            }
            
        elif action_type == 'magic':
            return {
                'narrative': "Your magical attempt succeeds. The arcane energies respond to your will.",
                'mechanical_effects': {'spell_success': True, 'magical_effect': True},
                'state_changes': {'magical_progress': 1, 'confidence_boosted': True}
            }
            
        else:
            return {
                'narrative': "Your action succeeds as intended.",
                'mechanical_effects': {'action_completed': True},
                'state_changes': {'general_progress': 1}
            }
    
    def _determine_next_location(self, current_location: LocationId, context: Dict[str, Any]) -> LocationId:
        """Determine where the player moves to based on current location and context"""
        
        # Define location progression paths
        location_paths = {
            LocationId.VILLAGE_OUTSKIRTS: [LocationId.ASHBROOK_VILLAGE, LocationId.CRYSTAL_CAVE_ENTRANCE],
            LocationId.ASHBROOK_VILLAGE: [LocationId.VILLAGE_TAVERN, LocationId.SACRED_GROVE, LocationId.VILLAGE_OUTSKIRTS],
            LocationId.CRYSTAL_CAVE_ENTRANCE: [LocationId.CRYSTAL_CAVE_INTERIOR, LocationId.VILLAGE_OUTSKIRTS],
            LocationId.VILLAGE_TAVERN: [LocationId.ASHBROOK_VILLAGE],
            LocationId.SACRED_GROVE: [LocationId.WHISPERING_GROVE, LocationId.ASHBROOK_VILLAGE],
            LocationId.WHISPERING_GROVE: [LocationId.SACRED_GROVE, LocationId.FIRE_SPRITE_CLEARING],
            LocationId.FIRE_SPRITE_CLEARING: [LocationId.WHISPERING_GROVE],
            LocationId.CRYSTAL_CAVE_INTERIOR: [LocationId.CRYSTAL_CAVE_ENTRANCE, LocationId.UNDERGROUND_CHAMBER]
        }
        
        available_paths = location_paths.get(current_location, [LocationId.ASHBROOK_VILLAGE])
        
        # For now, take the first available path (can be made smarter later)
        if available_paths:
            return available_paths[0]
        else:
            return LocationId.ASHBROOK_VILLAGE  # Fallback

# Global action processor instance
_action_processor = None

def get_action_processor() -> ActionProcessor:
    """Get global action processor instance"""
    global _action_processor
    if _action_processor is None:
        _action_processor = ActionProcessor()
    return _action_processor