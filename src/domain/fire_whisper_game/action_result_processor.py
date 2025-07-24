"""
Action Result Processor - Determines what happens when player takes actions
Replaces AI guesswork with structured, predictable outcomes
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from .story_state_manager import StoryStateManager

class ActionResultType(Enum):
    MOVEMENT = "movement"
    COMBAT_PREPARATION = "combat_preparation"
    INVESTIGATION = "investigation"
    SOCIAL_INTERACTION = "social_interaction"
    ENVIRONMENTAL_INTERACTION = "environmental_interaction"
    QUEST_PROGRESSION = "quest_progression"
    TACTICAL_ADVANTAGE = "tactical_advantage"
    INFORMATION_GATHERING = "information_gathering"

@dataclass
class ActionResult:
    result_type: ActionResultType
    success: bool
    description_template: str
    mechanical_effects: Dict[str, Any]
    story_updates: Dict[str, Any]
    narrative_focus: List[str]  # What AI should focus on in description
    next_options_hint: str = ""  # Suggestion for what options to show next

class ActionResultProcessor:
    """Processes player actions and determines structured outcomes"""
    
    def __init__(self, story_manager: StoryStateManager):
        self.story_manager = story_manager
        
        # Action templates for different situations
        self.action_templates = {
            "defensive_stance": {
                "with_enemies": {
                    "result_type": ActionResultType.TACTICAL_ADVANTAGE,
                    "description_template": "defensive_stance_vs_enemies",
                    "mechanical_effects": {"next_attack_bonus": 2, "damage_reduction": 1},
                    "narrative_focus": ["enemy_behavior", "tactical_observations", "environment_advantages"]
                },
                "without_enemies": {
                    "result_type": ActionResultType.COMBAT_PREPARATION,
                    "description_template": "defensive_stance_safe",
                    "mechanical_effects": {"alertness_bonus": 1},
                    "narrative_focus": ["area_assessment", "potential_threats", "strategic_positioning"]
                }
            },
            "examine_area": {
                "with_secrets": {
                    "result_type": ActionResultType.INVESTIGATION,
                    "description_template": "examination_reveals_secrets",
                    "mechanical_effects": {"investigation_bonus": 2},
                    "narrative_focus": ["hidden_details", "ancient_markings", "magical_traces"]
                },
                "without_secrets": {
                    "result_type": ActionResultType.INFORMATION_GATHERING,
                    "description_template": "examination_basic_info",
                    "mechanical_effects": {},
                    "narrative_focus": ["obvious_features", "general_atmosphere", "practical_details"]
                }
            },
            "ask_emberlyn": {
                "quest_related": {
                    "result_type": ActionResultType.QUEST_PROGRESSION,
                    "description_template": "emberlyn_quest_guidance",
                    "mechanical_effects": {"guidance_bonus": 1},
                    "narrative_focus": ["quest_hints", "fairy_wisdom", "magical_insights"]
                },
                "general": {
                    "result_type": ActionResultType.INFORMATION_GATHERING,
                    "description_template": "emberlyn_general_advice",
                    "mechanical_effects": {},
                    "narrative_focus": ["area_knowledge", "fairy_perspective", "encouragement"]
                }
            },
            "wait_and_observe": {
                "dangerous_area": {
                    "result_type": ActionResultType.TACTICAL_ADVANTAGE,
                    "description_template": "patient_observation_danger",
                    "mechanical_effects": {"surprise_bonus": 2, "initiative_bonus": 1},
                    "narrative_focus": ["enemy_patterns", "environmental_changes", "opportunity_timing"]
                },
                "safe_area": {
                    "result_type": ActionResultType.INFORMATION_GATHERING,
                    "description_template": "patient_observation_safe",
                    "mechanical_effects": {"perception_bonus": 1},
                    "narrative_focus": ["subtle_details", "atmospheric_changes", "peaceful_moments"]
                }
            },
            "stealth_approach": {
                "with_targets": {
                    "result_type": ActionResultType.TACTICAL_ADVANTAGE,
                    "description_template": "stealth_vs_targets",
                    "mechanical_effects": {"stealth_bonus": 2, "first_strike_advantage": True},
                    "narrative_focus": ["stealth_technique", "target_awareness", "positioning"]
                },
                "exploration": {
                    "result_type": ActionResultType.INVESTIGATION,
                    "description_template": "stealth_exploration",
                    "mechanical_effects": {"discovery_bonus": 1},
                    "narrative_focus": ["hidden_paths", "quiet_movement", "careful_observation"]
                }
            }
        }
    
    def process_action(self, player_input: str, dice_result: Optional[Dict] = None) -> ActionResult:
        """Process a player action and return structured result"""
        
        context = self.story_manager.get_current_context()
        action_type = self._classify_action(player_input)
        situation_type = self._analyze_situation(context)
        
        # Get base template
        template_key = self._get_template_key(action_type, situation_type)
        base_template = self._get_action_template(action_type, situation_type)
        
        # Determine success based on dice result or situation
        success = self._determine_success(dice_result, action_type, situation_type)
        
        # Build result
        result = ActionResult(
            result_type=base_template["result_type"],
            success=success,
            description_template=base_template["description_template"],
            mechanical_effects=base_template["mechanical_effects"].copy(),
            story_updates=self._determine_story_updates(action_type, success, context),
            narrative_focus=base_template["narrative_focus"].copy(),
            next_options_hint=self._suggest_next_options(action_type, success, context)
        )
        
        # Apply story updates
        self._apply_story_updates(result.story_updates)
        
        return result
    
    def _classify_action(self, player_input: str) -> str:
        """Classify the type of action player is taking"""
        
        input_lower = player_input.lower().strip()
        
        # Handle numbered choices
        if input_lower in ['1', '2', '3', '4', '5']:
            # Map common option numbers to actions based on context
            context = self.story_manager.get_current_context()
            if context["enemies_present"]:
                option_map = {
                    '1': 'defensive_stance',
                    '2': 'examine_area', 
                    '3': 'wait_and_observe',
                    '4': 'ask_emberlyn'
                }
            else:
                option_map = {
                    '1': 'defensive_stance',
                    '2': 'stealth_approach',
                    '3': 'wait_and_observe', 
                    '4': 'ask_emberlyn'
                }
            return option_map.get(input_lower, 'defensive_stance')
        
        # Direct action classification
        if any(word in input_lower for word in ['defensive', 'stance', 'assess', 'tactical']):
            return 'defensive_stance'
        elif any(word in input_lower for word in ['examine', 'look', 'investigate', 'runes', 'symbols']):
            return 'examine_area'
        elif any(word in input_lower for word in ['wait', 'observe', 'watch', 'patience']):
            return 'wait_and_observe'
        elif any(word in input_lower for word in ['emberlyn', 'guidance', 'advice', 'ask']):
            return 'ask_emberlyn'
        elif any(word in input_lower for word in ['sneak', 'stealth', 'quietly', 'careful']):
            return 'stealth_approach'
        elif any(word in input_lower for word in ['attack', 'charge', 'fight', 'combat']):
            return 'combat_action'
        elif any(word in input_lower for word in ['move', 'go', 'travel', 'enter']):
            return 'movement'
        else:
            return 'general_action'
    
    def _analyze_situation(self, context: Dict) -> str:
        """Analyze current situation to determine appropriate response"""
        
        if context["enemies_present"]:
            return "with_enemies"
        elif not context["location"]["safe_zone"]:
            return "dangerous_area"
        elif context["items_available"] or "hidden" in str(context["location"]["environmental_features"]):
            return "with_secrets"
        elif context["active_quests"]:
            return "quest_related"
        else:
            return "safe_area"
    
    def _get_action_template(self, action_type: str, situation_type: str) -> Dict:
        """Get the appropriate action template"""
        
        if action_type in self.action_templates:
            templates = self.action_templates[action_type]
            
            # Try specific situation first
            if situation_type in templates:
                return templates[situation_type]
            
            # Fall back to general templates
            if "with_enemies" in templates and situation_type in ["dangerous_area"]:
                return templates["with_enemies"]
            elif "without_enemies" in templates:
                return templates["without_enemies"]
            elif "general" in templates:
                return templates["general"]
            else:
                # Return first available template
                return list(templates.values())[0]
        
        # Default template for unknown actions
        return {
            "result_type": ActionResultType.INFORMATION_GATHERING,
            "description_template": "general_action_response",
            "mechanical_effects": {},
            "narrative_focus": ["player_intent", "current_situation", "available_options"]
        }
    
    def _determine_success(self, dice_result: Optional[Dict], action_type: str, situation_type: str) -> bool:
        """Determine if action succeeds based on dice result or situation"""
        
        if dice_result and 'success' in dice_result:
            return dice_result['success']
        
        # Some actions auto-succeed in certain situations
        auto_success_actions = ['ask_emberlyn', 'wait_and_observe', 'examine_area']
        if action_type in auto_success_actions:
            return True
        
        # Defensive actions usually succeed
        if action_type == 'defensive_stance':
            return True
        
        # Default to success for non-risky actions
        return True
    
    def _determine_story_updates(self, action_type: str, success: bool, context: Dict) -> Dict[str, Any]:
        """Determine what story state should be updated"""
        
        updates = {}
        
        # Track significant actions
        if action_type == 'examine_area' and success:
            location_id = context["location"]["id"]
            updates["story_flags"] = {f"examined_{location_id}": True}
        
        if action_type == 'defensive_stance' and context["enemies_present"]:
            updates["story_flags"] = {"took_defensive_stance": True}
        
        if action_type == 'ask_emberlyn':
            updates["story_flags"] = {"consulted_emberlyn": True}
        
        # Add recent event
        updates["recent_event"] = f"{action_type}_{'success' if success else 'failure'}"
        
        return updates
    
    def _suggest_next_options(self, action_type: str, success: bool, context: Dict) -> str:
        """Suggest what types of options should be available next"""
        
        if context["enemies_present"]:
            return "combat_options"
        elif context["items_available"]:
            return "exploration_options"
        elif context["npcs_present"]:
            return "social_options"
        else:
            return "general_options"
    
    def _apply_story_updates(self, updates: Dict[str, Any]):
        """Apply updates to story state"""
        
        if "story_flags" in updates:
            for flag, value in updates["story_flags"].items():
                self.story_manager.set_story_flag(flag, value)
        
        if "recent_event" in updates:
            self.story_manager.add_recent_event(updates["recent_event"])
    
    def _get_template_key(self, action_type: str, situation_type: str) -> str:
        """Get template key for narrative generation"""
        return f"{action_type}_{situation_type}"
    
    def get_narrative_prompt_data(self, action_result: ActionResult, context: Dict) -> Dict[str, Any]:
        """Get structured data for AI narrative generation"""
        
        return {
            "action_result": {
                "type": action_result.result_type.value,
                "success": action_result.success,
                "template": action_result.description_template,
                "focus_points": action_result.narrative_focus
            },
            "location_context": {
                "name": context["location"]["name"],
                "type": context["location"]["type"],
                "description": context["location"]["description"],
                "features": context["location"]["environmental_features"]
            },
            "situation_context": {
                "enemies": context["enemies_present"],
                "npcs": [npc["name"] for npc in context["npcs_present"]],
                "items": context["items_available"],
                "safe_zone": context["location"]["safe_zone"]
            },
            "mechanical_effects": action_result.mechanical_effects,
            "story_context": {
                "recent_events": context["recent_events"],
                "active_quests": [q.name for q in context["active_quests"]],
                "time": context["environmental_conditions"]["time_of_day"],
                "weather": context["environmental_conditions"]["weather"]
            }
        }