#!/usr/bin/env python3
"""
Action-Outcome Framework - Creates varied, meaningful consequences for player actions

This system replaces the binary success/failure model with a spectrum of outcomes:
- Spectacular Success: Exceeding DC by 5+, major benefits
- Success: Meeting DC, standard benefits
- Partial Success: Within 2 of DC, mixed results
- Failure: Below DC but not by much, minor setbacks
- Spectacular Failure: Far below DC, major setbacks but new opportunities

Each outcome type has specific narrative templates and game state changes.
"""
import random
from typing import Dict, List, Tuple, Any, Optional

class ActionOutcomeFramework:
    """Handles the resolution of player actions with varied, meaningful outcomes"""
    
    def __init__(self):
        # Define outcome categories and their thresholds relative to DC
        self.outcome_categories = {
            "spectacular_success": {
                "threshold_modifier": 5,  # DC + 5
                "probability_boost": 0.1,  # 10% chance boost for high-risk actions
                "state_changes": {
                    "progress_bonus": 2.0,  # Double progress
                    "reputation_bonus": 1.0,
                    "special_reward": True
                }
            },
            "success": {
                "threshold_modifier": 0,  # DC + 0
                "probability_boost": 0.0,
                "state_changes": {
                    "progress_bonus": 1.0,
                    "reputation_bonus": 0.5
                }
            },
            "partial_success": {
                "threshold_modifier": -2,  # DC - 2
                "probability_boost": 0.0,
                "state_changes": {
                    "progress_bonus": 0.5,
                    "minor_complication": True
                }
            },
            "failure": {
                "threshold_modifier": -5,  # DC - 5
                "probability_boost": 0.0,
                "state_changes": {
                    "minor_setback": True
                }
            },
            "spectacular_failure": {
                "threshold_modifier": -999,  # Default for anything below failure
                "probability_boost": 0.0,
                "state_changes": {
                    "major_setback": True,
                    "reputation_penalty": 1.0,
                    "unexpected_opportunity": True  # Even spectacular failures open new paths
                }
            }
        }
        
        # Narrative templates for each outcome type
        self.narrative_templates = self._initialize_narrative_templates()
        
        # Track outcome statistics
        self.outcome_stats = {category: 0 for category in self.outcome_categories.keys()}
        self.total_actions = 0
    
    def _initialize_narrative_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize narrative templates for different action types and outcomes"""
        templates = {
            "spectacular_success": {
                "combat": [
                    "Your attack lands with extraordinary precision! {spectacular_effect}",
                    "With exceptional skill, you execute a perfect strike! {spectacular_consequence}"
                ],
                "magic": [
                    "Your magical energies surge with unexpected power! {spectacular_effect}",
                    "The spell manifests with extraordinary potency! {spectacular_consequence}"
                ],
                "social": [
                    "Your words resonate perfectly, achieving far more than expected! {spectacular_effect}",
                    "Your charismatic approach wins them over completely! {spectacular_consequence}"
                ],
                "exploration": [
                    "You discover something extraordinary that others have missed! {spectacular_effect}",
                    "Your keen senses reveal a hidden secret of great value! {spectacular_consequence}"
                ],
                "general": [
                    "You succeed brilliantly, achieving far more than expected! {spectacular_effect}",
                    "Your exceptional skill turns this challenge into a remarkable triumph! {spectacular_consequence}"
                ]
            },
            "success": {
                "combat": [
                    "Your attack strikes true. {positive_effect}",
                    "You execute your combat maneuver successfully. {positive_consequence}"
                ],
                "magic": [
                    "Your spell works as intended. {positive_effect}",
                    "The magical energies respond to your command. {positive_consequence}"
                ],
                "social": [
                    "Your approach works well. {positive_effect}",
                    "Your words have the desired effect. {positive_consequence}"
                ],
                "exploration": [
                    "You find what you were looking for. {positive_effect}",
                    "Your careful examination reveals useful information. {positive_consequence}"
                ],
                "general": [
                    "You succeed in your task. {positive_effect}",
                    "Your efforts yield the desired result. {positive_consequence}"
                ]
            },
            "partial_success": {
                "combat": [
                    "Your attack partially connects. {mixed_effect}",
                    "You land a glancing blow, but {complication}."
                ],
                "magic": [
                    "Your spell works, but not quite as intended. {mixed_effect}",
                    "The magic responds, but {complication}."
                ],
                "social": [
                    "Your approach partially works. {mixed_effect}",
                    "You make some progress, but {complication}."
                ],
                "exploration": [
                    "You find something, though not exactly what you sought. {mixed_effect}",
                    "Your search reveals partial information, but {complication}."
                ],
                "general": [
                    "You partially succeed. {mixed_effect}",
                    "You make progress, but {complication}."
                ]
            },
            "failure": {
                "combat": [
                    "Your attack misses its mark. {negative_effect}",
                    "Your combat maneuver fails to execute properly. {negative_consequence}"
                ],
                "magic": [
                    "Your spell fizzles ineffectively. {negative_effect}",
                    "The magical energies dissipate without achieving your goal. {negative_consequence}"
                ],
                "social": [
                    "Your approach doesn't have the desired effect. {negative_effect}",
                    "Your words fail to persuade them. {negative_consequence}"
                ],
                "exploration": [
                    "Your search reveals nothing of value. {negative_effect}",
                    "You miss what you were looking for. {negative_consequence}"
                ],
                "general": [
                    "You fail to accomplish your goal. {negative_effect}",
                    "Your efforts don't yield the desired result. {negative_consequence}"
                ]
            },
            "spectacular_failure": {
                "combat": [
                    "Your attack goes dramatically wrong! {spectacular_negative_effect}",
                    "In a stroke of bad luck, your weapon {spectacular_failure_verb}! {spectacular_negative_consequence}"
                ],
                "magic": [
                    "Your spell backfires spectacularly! {spectacular_negative_effect}",
                    "The magical energies spiral out of control! {spectacular_negative_consequence}"
                ],
                "social": [
                    "Your approach has the opposite effect intended! {spectacular_negative_effect}",
                    "Your words inadvertently reveal something you didn't intend! {spectacular_negative_consequence}"
                ],
                "exploration": [
                    "Your search not only fails but alerts what you were trying to avoid! {spectacular_negative_effect}",
                    "You accidentally trigger something dangerous during your investigation! {spectacular_negative_consequence}"
                ],
                "general": [
                    "Your attempt goes dramatically wrong! {spectacular_negative_effect}",
                    "In an unfortunate turn of events, you {spectacular_failure_verb}! {spectacular_negative_consequence}"
                ]
            }
        }
        
        return templates
    
    def resolve_action(self, action_type: str, risk_level: str, roll_result: int, 
                      difficulty_class: int, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Resolve a player action and determine the outcome
        
        Args:
            action_type: Type of action (combat, magic, social, exploration, etc.)
            risk_level: Level of risk (low, moderate, high)
            roll_result: Result of the dice roll
            difficulty_class: Base difficulty class for the action
            context: Additional context for the action
            
        Returns:
            Dict containing outcome type, narrative template, and state changes
        """
        # Default context if none provided
        if context is None:
            context = {}
        
        # Adjust DC based on risk level
        adjusted_dc = self._adjust_dc_for_risk(difficulty_class, risk_level)
        
        # Apply probability modifications for high-risk actions
        # This ensures high-risk actions have a better chance of spectacular success
        if risk_level == "high":
            roll_result = self._apply_high_risk_probability_boost(roll_result, adjusted_dc)
        
        # Determine outcome category based on roll vs. adjusted DC
        outcome_type = self._determine_outcome_type(roll_result, adjusted_dc)
        
        # Get appropriate narrative template
        narrative = self._get_narrative_template(outcome_type, action_type)
        
        # Get state changes for this outcome
        state_changes = self.outcome_categories[outcome_type]["state_changes"].copy()
        
        # Update statistics
        self.outcome_stats[outcome_type] += 1
        self.total_actions += 1
        
        # Build result
        result = {
            "outcome_type": outcome_type,
            "narrative_template": narrative,
            "state_changes": state_changes,
            "roll_result": roll_result,
            "difficulty_class": adjusted_dc,
            "action_type": action_type,
            "risk_level": risk_level
        }
        
        return result
    
    def _adjust_dc_for_risk(self, base_dc: int, risk_level: str) -> int:
        """Adjust difficulty class based on risk level"""
        if risk_level == "high":
            return base_dc + 2  # Higher risk means higher difficulty
        elif risk_level == "low":
            return base_dc - 2  # Lower risk means lower difficulty
        else:  # moderate
            return base_dc
    
    def _apply_high_risk_probability_boost(self, roll_result: int, dc: int) -> int:
        """
        Apply probability boost for high-risk actions
        
        This ensures high-risk actions have a better chance of spectacular success,
        making them worth taking despite the higher difficulty.
        """
        # Check if we're close to a spectacular success
        if roll_result >= dc + 3 and roll_result < dc + 5:
            # 40% chance to boost to spectacular success
            if random.random() < 0.4:
                return dc + 5  # Boost to minimum spectacular success
        
        return roll_result
    
    def _determine_outcome_type(self, roll_result: int, dc: int) -> str:
        """Determine outcome category based on roll vs. DC"""
        # Check each outcome category in order from best to worst
        for outcome_type, data in sorted(
            self.outcome_categories.items(),
            key=lambda x: x[1]["threshold_modifier"],
            reverse=True
        ):
            threshold = dc + data["threshold_modifier"]
            if roll_result >= threshold:
                return outcome_type
        
        # Default to spectacular failure if nothing else matches
        return "spectacular_failure"
    
    def _get_narrative_template(self, outcome_type: str, action_type: str) -> str:
        """Get an appropriate narrative template for the outcome and action type"""
        # Normalize action type to one of our categories
        normalized_action_type = self._normalize_action_type(action_type)
        
        # Get templates for this outcome and action type
        templates = self.narrative_templates[outcome_type][normalized_action_type]
        
        # Return a random template
        return random.choice(templates)
    
    def _normalize_action_type(self, action_type: str) -> str:
        """Map specific action types to our general categories"""
        action_mapping = {
            # Combat actions
            "attack": "combat",
            "defend": "combat",
            "strike": "combat",
            "block": "combat",
            "dodge": "combat",
            
            # Magic actions
            "cast": "magic",
            "spell": "magic",
            "enchant": "magic",
            "ritual": "magic",
            
            # Social actions
            "persuade": "social",
            "intimidate": "social",
            "deceive": "social",
            "charm": "social",
            "negotiate": "social",
            
            # Exploration actions
            "search": "exploration",
            "investigate": "exploration",
            "examine": "exploration",
            "scout": "exploration",
            "explore": "exploration"
        }
        
        # Check if action type matches any of our mappings
        for key, value in action_mapping.items():
            if key in action_type.lower():
                return value
        
        # Default to general if no match
        return "general"
    
    def get_outcome_statistics(self) -> Dict[str, float]:
        """Get statistics on outcome distribution"""
        if self.total_actions == 0:
            return {category: 0.0 for category in self.outcome_categories.keys()}
        
        return {
            category: count / self.total_actions * 100
            for category, count in self.outcome_stats.items()
        }
    
    def generate_ai_prompt(self, outcome_data: Dict[str, Any], character: Dict[str, Any], 
                          location: Dict[str, Any], story_state: Dict[str, Any]) -> str:
        """
        Generate a prompt for AI to create varied, engaging action resolutions
        
        Args:
            outcome_data: Data from resolve_action
            character: Character data
            location: Location data
            story_state: Current story state
            
        Returns:
            Prompt for AI to generate a response
        """
        outcome_type = outcome_data["outcome_type"]
        action_type = outcome_data["action_type"]
        
        # Base prompt structure
        prompt = f"""
        Create an engaging, varied response for a {outcome_type} outcome to the player's {action_type} action.
        
        ## Action Context
        - Action: {action_type}
        - Character: {character['name']}, a {character['race']} {character['class']}
        - Location: {location['name']} - {location.get('brief_description', '')}
        - Story Phase: {story_state.get('current_phase', 'introduction')}
        
        ## Outcome Type: {outcome_type.upper()}
        
        ## Required Elements
        1. Describe the outcome with vivid, specific details (avoid generic descriptions)
        2. Include clear consequences that affect the game world
        3. Reference the specific location and its features
        4. Maintain continuity with previously established elements
        5. Include Emberlyn's reaction to the outcome
        
        ## Prohibited Patterns
        - DO NOT use phrases like "Despite your best efforts" or "The task tests the limits of your abilities"
        - DO NOT use generic failure descriptions
        - ALWAYS provide specific details about what happened and why
        - NEVER contradict established facts about the world or characters
        
        ## Tone Guidelines
        - {self._get_tone_for_outcome(outcome_type)}
        - Maintain the established fantasy atmosphere
        - Keep Emberlyn's personality consistent (helpful, slightly anxious, knowledgeable)
        
        ## Response Format
        *Emberlyn's reaction and description of the outcome*
        
        "Emberlyn's dialogue about what happened and its implications"
        
        *Additional environmental details and consequences*
        """
        
        # Add outcome-specific instructions
        if outcome_type == "spectacular_success":
            prompt += """
            ## Spectacular Success Guidelines
            - Describe how the character exceeds expectations dramatically
            - Include a significant positive consequence or reward
            - Show how this success advances the story in a meaningful way
            - Have Emberlyn express delighted surprise at the outcome
            """
        elif outcome_type == "success":
            prompt += """
            ## Success Guidelines
            - Describe a clear, satisfying success
            - Include a positive consequence or advantage gained
            - Show how this success helps the current situation
            - Have Emberlyn be encouraging and pleased
            """
        elif outcome_type == "partial_success":
            prompt += """
            ## Partial Success Guidelines
            - Describe a mixed outcome with both positive and negative elements
            - Include a complication that arises despite the partial success
            - Show how the character can still make progress despite setbacks
            - Have Emberlyn be optimistic but cautious about the mixed results
            """
        elif outcome_type == "failure":
            prompt += """
            ## Failure Guidelines
            - Describe a clear failure but avoid humiliation
            - Include a specific reason for the failure that makes sense
            - Show a minor setback that doesn't halt all progress
            - Have Emberlyn be supportive and suggest alternatives
            """
        elif outcome_type == "spectacular_failure":
            prompt += """
            ## Spectacular Failure Guidelines
            - Make the failure dramatic but NOT humiliating
            - Include an unexpected opportunity that arises from the failure
            - Ensure the story can still progress despite this setback
            - Have Emberlyn be supportive rather than critical
            - Add an element of humor or irony if appropriate
            """
        
        return prompt
    
    def _get_tone_for_outcome(self, outcome_type: str) -> str:
        """Get appropriate tone guidelines for different outcome types"""
        tone_guidelines = {
            "spectacular_success": "triumphant, exciting, and rewarding",
            "success": "positive, satisfying, and encouraging",
            "partial_success": "mixed, nuanced, and balanced",
            "failure": "challenging but not discouraging",
            "spectacular_failure": "dramatic but with a silver lining"
        }
        
        return tone_guidelines.get(outcome_type, "balanced and appropriate")


# Example usage
if __name__ == "__main__":
    # Create framework
    action_framework = ActionOutcomeFramework()
    
    # Test with different risk levels and rolls
    print("Testing Action-Outcome Framework with different scenarios:")
    
    # Test scenarios
    scenarios = [
        {"action_type": "attack", "risk_level": "high", "roll": 18, "dc": 15},
        {"action_type": "attack", "risk_level": "high", "roll": 5, "dc": 15},
        {"action_type": "investigate", "risk_level": "moderate", "roll": 15, "dc": 15},
        {"action_type": "persuade", "risk_level": "low", "roll": 10, "dc": 15},
        {"action_type": "cast spell", "risk_level": "high", "roll": 3, "dc": 15}
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        outcome = action_framework.resolve_action(
            scenario["action_type"], 
            scenario["risk_level"], 
            scenario["roll"], 
            scenario["dc"]
        )
        
        print(f"\nScenario {i}:")
        print(f"Action: {scenario['action_type']} (Risk: {scenario['risk_level']})")
        print(f"Roll: {scenario['roll']} vs DC: {scenario['dc']} (Adjusted: {outcome['difficulty_class']})")
        print(f"Outcome: {outcome['outcome_type']}")
        print(f"Narrative Template: {outcome['narrative_template']}")
        print(f"State Changes: {outcome['state_changes']}")
    
    # Print statistics
    print("\nOutcome Statistics:")
    stats = action_framework.get_outcome_statistics()
    for outcome_type, percentage in stats.items():
        print(f"{outcome_type}: {percentage:.1f}%")