"""
Looma Context Continuity - Prevents AI Context Amnesia
Pattern discovered from Fire Whisper RPG context loss issues
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .state_manager import StateManager

@dataclass
class ContextAnchor:
    """Key context elements that must be preserved across AI interactions"""
    primary_setting: str           # Main location/environment
    active_elements: List[str]     # NPCs, enemies, objects present
    immediate_situation: str       # What's happening right now
    recent_actions: List[str]      # Last few player actions
    story_momentum: str           # Current narrative direction

class ContextContinuityEnforcer:
    """Ensures AI responses maintain context continuity"""
    
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
        self.context_anchors: List[ContextAnchor] = []
        self.continuity_violations: List[str] = []
    
    def create_context_anchor(self, ai_response: str, context: Dict[str, Any]) -> ContextAnchor:
        """Create a context anchor from current situation"""
        
        # Extract key elements from AI response and context
        primary_setting = self._extract_primary_setting(ai_response, context)
        active_elements = self._extract_active_elements(ai_response, context)
        immediate_situation = self._extract_immediate_situation(ai_response)
        recent_actions = context.get("recent_events", [])[-3:]  # Last 3 actions
        story_momentum = self._determine_story_momentum(ai_response)
        
        anchor = ContextAnchor(
            primary_setting=primary_setting,
            active_elements=active_elements,
            immediate_situation=immediate_situation,
            recent_actions=recent_actions,
            story_momentum=story_momentum
        )
        
        self.context_anchors.append(anchor)
        
        # Keep only last 5 anchors to prevent memory bloat
        if len(self.context_anchors) > 5:
            self.context_anchors = self.context_anchors[-5:]
        
        return anchor
    
    def validate_context_continuity(self, new_ai_response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that new AI response maintains context continuity"""
        
        if not self.context_anchors:
            return {"valid": True, "violations": []}
        
        latest_anchor = self.context_anchors[-1]
        violations = []
        
        # Check if primary setting is maintained or properly transitioned
        new_setting = self._extract_primary_setting(new_ai_response, context)
        if new_setting != latest_anchor.primary_setting:
            if not self._is_valid_setting_transition(latest_anchor.primary_setting, new_setting):
                violations.append(f"Invalid setting change: {latest_anchor.primary_setting} -> {new_setting}")
        
        # Check if active elements are acknowledged or explained
        for element in latest_anchor.active_elements:
            if element not in new_ai_response and not self._element_properly_handled(element, new_ai_response):
                violations.append(f"Active element '{element}' disappeared without explanation")
        
        # Check if immediate situation is continued or resolved
        if latest_anchor.immediate_situation and not self._situation_addressed(latest_anchor.immediate_situation, new_ai_response):
            violations.append(f"Immediate situation '{latest_anchor.immediate_situation}' was ignored")
        
        # Check story momentum consistency
        new_momentum = self._determine_story_momentum(new_ai_response)
        if not self._momentum_consistent(latest_anchor.story_momentum, new_momentum):
            violations.append(f"Story momentum inconsistent: {latest_anchor.story_momentum} -> {new_momentum}")
        
        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "anchor_used": latest_anchor,
            "continuity_score": self._calculate_continuity_score(violations)
        }
    
    def generate_continuity_prompt_addition(self, context: Dict[str, Any]) -> str:
        """Generate additional prompt text to enforce continuity"""
        
        if not self.context_anchors:
            return ""
        
        latest_anchor = self.context_anchors[-1]
        
        prompt_addition = f"""
CONTEXT CONTINUITY REQUIREMENTS:
- Current Setting: {latest_anchor.primary_setting}
- Active Elements: {', '.join(latest_anchor.active_elements)}
- Immediate Situation: {latest_anchor.immediate_situation}
- Story Momentum: {latest_anchor.story_momentum}

CRITICAL: Your response MUST acknowledge and continue from this established context.
Do NOT introduce new settings or ignore active elements without proper narrative transition.
"""
        
        return prompt_addition
    
    def _extract_primary_setting(self, ai_response: str, context: Dict[str, Any]) -> str:
        """Extract the primary setting from AI response"""
        
        # Look for location keywords in response
        location_keywords = {
            "village": "village",
            "forest": "forest", 
            "cave": "cave",
            "shrine": "shrine",
            "thornbush": "corrupted_grove",
            "shadow": "shadow_area",
            "blight": "blighted_area"
        }
        
        response_lower = ai_response.lower()
        for keyword, setting in location_keywords.items():
            if keyword in response_lower:
                return setting
        
        # Fallback to context
        return context.get("current_location", "unknown")
    
    def _extract_active_elements(self, ai_response: str, context: Dict[str, Any]) -> List[str]:
        """Extract active elements mentioned in AI response"""
        
        elements = []
        
        # Common element patterns
        element_patterns = {
            "thornbush": r"thorn\w*",
            "shadow_blight": r"shadow\w*|blight\w*",
            "fairy_shrine": r"shrine\w*",
            "enemies": r"enemy|enemies|hostile",
            "npcs": r"villager\w*|merchant\w*|guard\w*"
        }
        
        import re
        response_lower = ai_response.lower()
        
        for element_name, pattern in element_patterns.items():
            if re.search(pattern, response_lower):
                elements.append(element_name)
        
        # Add from context
        elements.extend(context.get("enemies_present", []))
        elements.extend([npc["name"] for npc in context.get("npcs_present", [])])
        
        return list(set(elements))  # Remove duplicates
    
    def _extract_immediate_situation(self, ai_response: str) -> str:
        """Extract the immediate situation from AI response"""
        
        # Look for action-oriented phrases
        situation_indicators = [
            "blocking", "twisted", "pulsing", "creeping", "approaching",
            "waiting", "watching", "threatening", "glowing", "moving"
        ]
        
        response_lower = ai_response.lower()
        for indicator in situation_indicators:
            if indicator in response_lower:
                # Extract sentence containing the indicator
                sentences = ai_response.split('.')
                for sentence in sentences:
                    if indicator in sentence.lower():
                        return sentence.strip()
        
        return ""
    
    def _determine_story_momentum(self, ai_response: str) -> str:
        """Determine the story momentum from AI response"""
        
        response_lower = ai_response.lower()
        
        if any(word in response_lower for word in ["danger", "threat", "shadow", "blight", "hostile"]):
            return "tension_building"
        elif any(word in response_lower for word in ["peaceful", "calm", "gentle", "lovely"]):
            return "peaceful_exploration"
        elif any(word in response_lower for word in ["mystery", "strange", "curious", "investigate"]):
            return "mystery_unfolding"
        else:
            return "neutral_progression"
    
    def _is_valid_setting_transition(self, old_setting: str, new_setting: str) -> bool:
        """Check if setting transition is narratively valid"""
        
        # Define valid transitions
        valid_transitions = {
            "corrupted_grove": ["village", "forest", "shrine"],
            "village": ["forest", "road"],
            "forest": ["village", "cave", "shrine"],
            "cave": ["forest"],
            "shrine": ["forest", "corrupted_grove"]
        }
        
        return new_setting in valid_transitions.get(old_setting, [new_setting])
    
    def _element_properly_handled(self, element: str, ai_response: str) -> bool:
        """Check if an active element is properly handled in response"""
        
        # Element is properly handled if it's mentioned or there's a transition word
        transition_words = ["after", "once", "having", "beyond", "past", "leaving"]
        
        response_lower = ai_response.lower()
        element_lower = element.lower()
        
        # Direct mention
        if element_lower in response_lower:
            return True
        
        # Transition indicated
        for word in transition_words:
            if word in response_lower:
                return True
        
        return False
    
    def _situation_addressed(self, situation: str, ai_response: str) -> bool:
        """Check if immediate situation is addressed in response"""
        
        if not situation:
            return True
        
        # Extract key words from situation
        situation_words = situation.lower().split()
        response_lower = ai_response.lower()
        
        # Check if any key words are mentioned
        for word in situation_words:
            if len(word) > 3 and word in response_lower:  # Skip short words
                return True
        
        return False
    
    def _momentum_consistent(self, old_momentum: str, new_momentum: str) -> bool:
        """Check if story momentum is consistent"""
        
        # Some momentum changes are valid
        valid_momentum_changes = {
            "tension_building": ["tension_building", "mystery_unfolding"],
            "peaceful_exploration": ["peaceful_exploration", "mystery_unfolding", "tension_building"],
            "mystery_unfolding": ["mystery_unfolding", "tension_building"],
            "neutral_progression": ["peaceful_exploration", "mystery_unfolding", "tension_building"]
        }
        
        return new_momentum in valid_momentum_changes.get(old_momentum, [new_momentum])
    
    def _calculate_continuity_score(self, violations: List[str]) -> float:
        """Calculate continuity score (0.0 to 1.0)"""
        
        if not violations:
            return 1.0
        
        # Each violation reduces score
        score = 1.0 - (len(violations) * 0.2)
        return max(0.0, score)
    
    def get_continuity_report(self) -> Dict[str, Any]:
        """Get detailed continuity report"""
        
        return {
            "total_anchors": len(self.context_anchors),
            "recent_violations": self.continuity_violations[-10:],  # Last 10
            "current_anchor": self.context_anchors[-1] if self.context_anchors else None,
            "average_continuity": self._calculate_average_continuity()
        }
    
    def _calculate_average_continuity(self) -> float:
        """Calculate average continuity score"""
        
        if not self.continuity_violations:
            return 1.0
        
        # Simple calculation - could be more sophisticated
        violation_rate = len(self.continuity_violations) / max(1, len(self.context_anchors))
        return max(0.0, 1.0 - violation_rate)

# Integration helper for existing AI systems
def create_continuity_enforced_prompt(base_prompt: str, continuity_enforcer: ContextContinuityEnforcer, 
                                    context: Dict[str, Any]) -> str:
    """Create a prompt with continuity enforcement"""
    
    continuity_addition = continuity_enforcer.generate_continuity_prompt_addition(context)
    
    if continuity_addition:
        return f"{base_prompt}\n{continuity_addition}"
    else:
        return base_prompt