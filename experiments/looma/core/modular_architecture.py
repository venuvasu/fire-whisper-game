"""
Modular Game Architecture
Swappable components for testing different AI/Code responsibility splits.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ComponentMode(Enum):
    AI = "ai"
    CODE = "code"
    HYBRID = "hybrid"

@dataclass
class GameState:
    """Standardized game state structure"""
    player_hp: int
    location: str
    inventory: List[str]
    npcs_met: List[str]
    quests: List[Dict[str, Any]]
    story_context: str
    last_action: Optional[str] = None

@dataclass
class ActionResult:
    """Standardized action result structure"""
    success: bool
    narrative: str
    state_changes: Dict[str, Any]
    new_choices: List[str]
    error_message: Optional[str] = None

# Abstract Interfaces for Swappable Components

class StateManager(ABC):
    """Abstract state management component"""
    
    @abstractmethod
    def update_state(self, current_state: GameState, action: str, result: Dict[str, Any]) -> GameState:
        pass
    
    @abstractmethod
    def validate_state(self, state: GameState) -> bool:
        pass

class NarrativeGenerator(ABC):
    """Abstract narrative generation component"""
    
    @abstractmethod
    def generate_narrative(self, state: GameState, action: str, result: Dict[str, Any]) -> str:
        pass
    
    @abstractmethod
    def generate_scene_description(self, state: GameState) -> str:
        pass

class ActionProcessor(ABC):
    """Abstract action processing component"""
    
    @abstractmethod
    def process_action(self, state: GameState, action: str) -> ActionResult:
        pass
    
    @abstractmethod
    def validate_action(self, state: GameState, action: str) -> bool:
        pass

class ChoiceGenerator(ABC):
    """Abstract choice generation component"""
    
    @abstractmethod
    def generate_choices(self, state: GameState) -> List[str]:
        pass

# AI-Based Implementations

class AIStateManager(StateManager):
    """AI-driven state management"""
    
    def update_state(self, current_state: GameState, action: str, result: Dict[str, Any]) -> GameState:
        # AI determines state changes based on context
        # This would integrate with your AI service
        
        # Simulate AI decision making
        new_state = GameState(
            player_hp=current_state.player_hp,
            location=current_state.location,
            inventory=current_state.inventory.copy(),
            npcs_met=current_state.npcs_met.copy(),
            quests=current_state.quests.copy(),
            story_context=current_state.story_context,
            last_action=action
        )
        
        # AI would analyze action and determine appropriate state changes
        if action == "attack" and result.get("success"):
            new_state.player_hp = max(0, current_state.player_hp - 10)  # AI decides damage
        elif action == "explore":
            new_state.story_context += f" Player explored and {result.get('discovery', 'found nothing')}."
            
        return new_state
    
    def validate_state(self, state: GameState) -> bool:
        # AI validates state consistency
        return state.player_hp >= 0 and len(state.location) > 0

class AINarrativeGenerator(NarrativeGenerator):
    """AI-driven narrative generation"""
    
    def generate_narrative(self, state: GameState, action: str, result: Dict[str, Any]) -> str:
        # AI generates creative, contextual narrative
        # This would call your AI service
        
        context = f"Player at {state.location}, HP: {state.player_hp}, last action: {action}"
        
        # Simulate AI narrative generation
        if action == "attack":
            return f"You swing your weapon with determination. The clash of steel rings through {state.location}. {result.get('outcome', 'The battle continues...')}"
        elif action == "explore":
            return f"You carefully examine your surroundings in {state.location}. The atmosphere is thick with mystery. {result.get('discovery', 'Nothing catches your eye immediately.')}"
        else:
            return f"You {action} in {state.location}. The world responds to your choice in unexpected ways."
    
    def generate_scene_description(self, state: GameState) -> str:
        return f"You find yourself in {state.location}, feeling the weight of your journey. Your health stands at {state.player_hp}. {state.story_context}"

# Code-Based Implementations

class CodeStateManager(StateManager):
    """Rule-based state management"""
    
    def __init__(self):
        self.state_rules = {
            "attack": {"hp_change": -5, "location_change": False},
            "heal": {"hp_change": 20, "location_change": False},
            "move": {"hp_change": 0, "location_change": True}
        }
    
    def update_state(self, current_state: GameState, action: str, result: Dict[str, Any]) -> GameState:
        # Code-based deterministic state changes
        new_state = GameState(
            player_hp=current_state.player_hp,
            location=current_state.location,
            inventory=current_state.inventory.copy(),
            npcs_met=current_state.npcs_met.copy(),
            quests=current_state.quests.copy(),
            story_context=current_state.story_context,
            last_action=action
        )
        
        # Apply predefined rules
        if action in self.state_rules:
            rule = self.state_rules[action]
            new_state.player_hp = max(0, min(100, current_state.player_hp + rule["hp_change"]))
            
            if rule["location_change"] and result.get("new_location"):
                new_state.location = result["new_location"]
        
        return new_state
    
    def validate_state(self, state: GameState) -> bool:
        return (0 <= state.player_hp <= 100 and 
                state.location is not None and 
                isinstance(state.inventory, list))

class CodeNarrativeGenerator(NarrativeGenerator):
    """Template-based narrative generation"""
    
    def __init__(self):
        self.templates = {
            "attack": "You attack the enemy. {outcome}",
            "defend": "You raise your guard. {outcome}",
            "explore": "You explore the area. {discovery}",
            "default": "You {action}. {result}"
        }
    
    def generate_narrative(self, state: GameState, action: str, result: Dict[str, Any]) -> str:
        template = self.templates.get(action, self.templates["default"])
        return template.format(
            action=action,
            outcome=result.get("outcome", "Something happens."),
            discovery=result.get("discovery", "You find nothing of interest."),
            result=result.get("description", "The action completes.")
        )
    
    def generate_scene_description(self, state: GameState) -> str:
        return f"Location: {state.location} | HP: {state.player_hp} | Items: {len(state.inventory)}"

# Hybrid Implementations

class HybridNarrativeGenerator(NarrativeGenerator):
    """Combines AI creativity with code reliability"""
    
    def __init__(self):
        self.ai_generator = AINarrativeGenerator()
        self.code_generator = CodeNarrativeGenerator()
    
    def generate_narrative(self, state: GameState, action: str, result: Dict[str, Any]) -> str:
        # Use AI for creative elements, code for structure
        try:
            ai_narrative = self.ai_generator.generate_narrative(state, action, result)
            # Add code-based validation and fallback
            if len(ai_narrative) < 10:  # AI failed
                return self.code_generator.generate_narrative(state, action, result)
            return ai_narrative
        except Exception:
            return self.code_generator.generate_narrative(state, action, result)
    
    def generate_scene_description(self, state: GameState) -> str:
        try:
            return self.ai_generator.generate_scene_description(state)
        except Exception:
            return self.code_generator.generate_scene_description(state)

# Modular Architecture Controller

class ModularGameArchitecture:
    """Main controller that orchestrates swappable components"""
    
    def __init__(self, config: Dict[str, ComponentMode]):
        self.config = config
        self.components = self._initialize_components(config)
    
    def _initialize_components(self, config: Dict[str, ComponentMode]) -> Dict[str, Any]:
        """Initialize components based on configuration"""
        components = {}
        
        # State Manager
        if config["state_management"] == ComponentMode.AI:
            components["state_manager"] = AIStateManager()
        else:  # CODE or HYBRID default to code for reliability
            components["state_manager"] = CodeStateManager()
        
        # Narrative Generator
        if config["narrative_generation"] == ComponentMode.AI:
            components["narrative_generator"] = AINarrativeGenerator()
        elif config["narrative_generation"] == ComponentMode.HYBRID:
            components["narrative_generator"] = HybridNarrativeGenerator()
        else:  # CODE
            components["narrative_generator"] = CodeNarrativeGenerator()
        
        return components
    
    def process_game_turn(self, current_state: GameState, player_action: str) -> ActionResult:
        """Process a complete game turn using configured components"""
        
        try:
            # Validate action (always use code for reliability)
            if not self._validate_action(current_state, player_action):
                return ActionResult(
                    success=False,
                    narrative="That action is not possible right now.",
                    state_changes={},
                    new_choices=[],
                    error_message="Invalid action"
                )
            
            # Process action result
            action_result = self._process_action_result(current_state, player_action)
            
            # Generate narrative
            narrative = self.components["narrative_generator"].generate_narrative(
                current_state, player_action, action_result
            )
            
            # Update state
            new_state = self.components["state_manager"].update_state(
                current_state, player_action, action_result
            )
            
            # Generate new choices
            new_choices = self._generate_choices(new_state)
            
            return ActionResult(
                success=True,
                narrative=narrative,
                state_changes=self._calculate_state_changes(current_state, new_state),
                new_choices=new_choices
            )
            
        except Exception as e:
            return ActionResult(
                success=False,
                narrative="Something unexpected happened.",
                state_changes={},
                new_choices=["try again", "continue"],
                error_message=str(e)
            )
    
    def _validate_action(self, state: GameState, action: str) -> bool:
        """Validate if action is possible in current state"""
        # Basic validation rules
        if state.player_hp <= 0 and action not in ["heal", "restart"]:
            return False
        return True
    
    def _process_action_result(self, state: GameState, action: str) -> Dict[str, Any]:
        """Determine the result of an action"""
        # This would contain your game logic
        if action == "attack":
            return {"success": True, "outcome": "You strike the enemy!", "damage": 15}
        elif action == "explore":
            return {"success": True, "discovery": "You find a hidden passage.", "new_location": None}
        else:
            return {"success": True, "description": f"You {action} successfully."}
    
    def _generate_choices(self, state: GameState) -> List[str]:
        """Generate available choices based on current state"""
        base_choices = ["explore", "rest", "check inventory"]
        
        if state.player_hp < 50:
            base_choices.append("heal")
        
        if state.location == "village":
            base_choices.extend(["talk to villagers", "visit shop"])
        elif state.location == "forest":
            base_choices.extend(["climb tree", "follow path"])
        
        return base_choices
    
    def _calculate_state_changes(self, old_state: GameState, new_state: GameState) -> Dict[str, Any]:
        """Calculate what changed between states"""
        changes = {}
        
        if old_state.player_hp != new_state.player_hp:
            changes["hp_change"] = new_state.player_hp - old_state.player_hp
        
        if old_state.location != new_state.location:
            changes["location_change"] = {"from": old_state.location, "to": new_state.location}
        
        return changes
    
    def get_architecture_info(self) -> Dict[str, str]:
        """Get information about current architecture configuration"""
        return {
            "state_management": self.config["state_management"].value,
            "narrative_generation": self.config["narrative_generation"].value,
            "components_loaded": list(self.components.keys())
        }