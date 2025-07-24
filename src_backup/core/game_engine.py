"""
Fire Whisper Game Engine - Code-Managed Game State
AI handles ONLY narrative generation, Code handles EVERYTHING else
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import time

class LocationId(Enum):
    VILLAGE_OUTSKIRTS = "village_outskirts"
    CRYSTAL_CAVE_ENTRANCE = "crystal_cave_entrance"
    CRYSTAL_CAVE_INTERIOR = "crystal_cave_interior"
    ASHBROOK_VILLAGE = "ashbrook_village"
    VILLAGE_TAVERN = "village_tavern"
    SACRED_GROVE = "sacred_grove"
    WHISPERING_GROVE = "whispering_grove"
    FIRE_SPRITE_CLEARING = "fire_sprite_clearing"
    UNDERGROUND_CHAMBER = "underground_chamber"

class ActionType(Enum):
    EXAMINE = "examine"
    MOVE = "move"
    COMBAT = "combat"
    SOCIAL = "social"
    USE_ITEM = "use_item"
    WAIT = "wait"

@dataclass
class GameLocation:
    id: LocationId
    name: str
    description: str
    enemies: List[str] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    items: List[str] = field(default_factory=list)
    exits: List[LocationId] = field(default_factory=list)
    visited: bool = False
    special_features: List[str] = field(default_factory=list)

@dataclass
class ActionResult:
    success: bool
    action_type: ActionType
    description: str
    discoveries: List[str] = field(default_factory=list)
    state_changes: Dict[str, Any] = field(default_factory=dict)
    narrative_focus: List[str] = field(default_factory=list)
    next_options: List[str] = field(default_factory=list)
    requires_dice_roll: bool = False
    dice_result: Optional[Dict] = None

class FireWhisperGameEngine:
    """Code-managed game engine - AI only writes narrative"""
    
    def __init__(self):
        self.current_location = LocationId.VILLAGE_OUTSKIRTS
        self.turn_count = 0
        self.game_flags = {
            "met_emberlyn": True,
            "knows_about_crystal": False,
            "cave_explored": False,
            "beetle_defeated": False,
            "crystal_obtained": False
        }
        
        # Initialize world
        self.locations = self._create_world()
        self.character_stats = {
            "hp": 20,
            "max_hp": 20,
            "level": 1,
            "xp": 0
        }
        
        # Track story elements for AI
        self.story_context = {
            "current_situation": "Beginning adventure with Emberlyn",
            "immediate_threat": None,
            "active_npcs": ["emberlyn"],
            "mood": "curious_exploration"
        }
    
    def _create_world(self) -> Dict[LocationId, GameLocation]:
        """Create the game world with all locations"""
        return {
            LocationId.VILLAGE_OUTSKIRTS: GameLocation(
                id=LocationId.VILLAGE_OUTSKIRTS,
                name="Village Outskirts",
                description="A peaceful path leading toward Ashbrook village, surrounded by autumn trees",
                exits=[LocationId.ASHBROOK_VILLAGE, LocationId.CRYSTAL_CAVE_ENTRANCE],
                special_features=["autumn_trees", "cobblestone_path"]
            ),
            
            LocationId.CRYSTAL_CAVE_ENTRANCE: GameLocation(
                id=LocationId.CRYSTAL_CAVE_ENTRANCE,
                name="Crystal Cave Entrance",
                description="A narrow cave entrance with mysterious sounds echoing from within",
                enemies=["fire_beetle"],
                exits=[LocationId.VILLAGE_OUTSKIRTS, LocationId.CRYSTAL_CAVE_INTERIOR],
                special_features=["glowing_crystals", "beetle_tracks", "ominous_sounds"],
                items=["small_crystal_shard"]
            ),
            
            LocationId.CRYSTAL_CAVE_INTERIOR: GameLocation(
                id=LocationId.CRYSTAL_CAVE_INTERIOR,
                name="Crystal Cave Interior",
                description="A glittering cavern filled with fire essence crystals",
                exits=[LocationId.CRYSTAL_CAVE_ENTRANCE],
                items=["fire_essence_crystal"],
                special_features=["crystal_formations", "magical_warmth"]
            ),
            
            LocationId.ASHBROOK_VILLAGE: GameLocation(
                id=LocationId.ASHBROOK_VILLAGE,
                name="Ashbrook Village",
                description="A cozy village with thatched roofs and friendly villagers",
                npcs=["village_elder", "concerned_farmer"],
                exits=[LocationId.VILLAGE_OUTSKIRTS, LocationId.VILLAGE_TAVERN],
                special_features=["market_square", "village_well"]
            ),
            
            LocationId.VILLAGE_TAVERN: GameLocation(
                id=LocationId.VILLAGE_TAVERN,
                name="The Rusty Sword Inn",
                description="A warm tavern with crackling fireplace and spiced cider",
                npcs=["innkeeper_martha"],
                exits=[LocationId.ASHBROOK_VILLAGE],
                items=["healing_potion", "travel_rations"]
            ),
            
            LocationId.SACRED_GROVE: GameLocation(
                id=LocationId.SACRED_GROVE,
                name="Sacred Grove",
                description="An ancient grove with a dimming sacred flame",
                exits=[LocationId.VILLAGE_OUTSKIRTS],
                special_features=["sacred_flame", "ancient_stones"]
            )
        }
    
    def get_current_location(self) -> GameLocation:
        """Get current location data"""
        return self.locations[self.current_location]
    
    def get_available_actions(self) -> List[Dict[str, Any]]:
        """Get available actions based on current location and state"""
        location = self.get_current_location()
        actions = []
        
        # Always available actions
        actions.extend([
            {
                "id": "examine_area",
                "text": "Examine the area carefully",
                "type": ActionType.EXAMINE,
                "risk": "low"
            },
            {
                "id": "ask_emberlyn",
                "text": "Ask Emberlyn for guidance",
                "type": ActionType.SOCIAL,
                "risk": "none"
            },
            {
                "id": "wait_observe",
                "text": "Wait and observe",
                "type": ActionType.WAIT,
                "risk": "low"
            }
        ])
        
        # Location-specific actions
        if location.enemies:
            actions.append({
                "id": "prepare_combat",
                "text": "Take defensive stance against threats",
                "type": ActionType.COMBAT,
                "risk": "medium"
            })
        
        if location.exits:
            for exit_id in location.exits:
                exit_location = self.locations[exit_id]
                actions.append({
                    "id": f"move_to_{exit_id.value}",
                    "text": f"Move to {exit_location.name}",
                    "type": ActionType.MOVE,
                    "risk": "low"
                })
        
        if location.special_features:
            for feature in location.special_features:
                actions.append({
                    "id": f"examine_{feature}",
                    "text": f"Examine {feature.replace('_', ' ')}",
                    "type": ActionType.EXAMINE,
                    "risk": "low"
                })
        
        return actions
    
    def process_action(self, action_input: str) -> ActionResult:
        """Process player action and return structured result"""
        
        self.turn_count += 1
        location = self.get_current_location()
        
        # Parse action input
        action_id = self._parse_action_input(action_input)
        
        # Process specific actions
        if action_id == "examine_area":
            return self._handle_examine_area()
        elif action_id == "ask_emberlyn":
            return self._handle_ask_emberlyn()
        elif action_id == "wait_observe":
            return self._handle_wait_observe()
        elif action_id == "prepare_combat":
            return self._handle_prepare_combat()
        elif action_id.startswith("move_to_"):
            target_location = action_id.replace("move_to_", "")
            return self._handle_movement(target_location)
        elif action_id.startswith("examine_"):
            feature = action_id.replace("examine_", "")
            return self._handle_examine_feature(feature)
        else:
            # Default action
            return self._handle_general_action(action_input)
    
    def _parse_action_input(self, action_input: str) -> str:
        """Parse player input into action ID"""
        
        input_lower = action_input.lower().strip()
        
        # Handle numbered choices (1, 2, 3, 4)
        if input_lower in ['1', '2', '3', '4', '5']:
            available_actions = self.get_available_actions()
            choice_index = int(input_lower) - 1
            if 0 <= choice_index < len(available_actions):
                return available_actions[choice_index]["id"]
        
        # Handle text input
        if any(word in input_lower for word in ['examine', 'look', 'investigate']):
            if any(word in input_lower for word in ['area', 'around', 'surroundings']):
                return "examine_area"
            else:
                return "examine_area"  # Default examine
        
        if any(word in input_lower for word in ['emberlyn', 'ask', 'guidance', 'help']):
            return "ask_emberlyn"
        
        if any(word in input_lower for word in ['wait', 'observe', 'watch']):
            return "wait_observe"
        
        if any(word in input_lower for word in ['combat', 'fight', 'defensive', 'stance']):
            return "prepare_combat"
        
        if any(word in input_lower for word in ['move', 'go', 'travel']):
            # Try to determine destination
            location = self.get_current_location()
            for exit_id in location.exits:
                exit_name = self.locations[exit_id].name.lower()
                if any(word in input_lower for word in exit_name.split()):
                    return f"move_to_{exit_id.value}"
        
        return "general_action"
    
    def _handle_examine_area(self) -> ActionResult:
        """Handle examining the current area"""
        location = self.get_current_location()
        discoveries = []
        narrative_focus = ["environmental_details", "emberlyn_observations"]
        
        # Mark location as visited
        location.visited = True
        
        # Discover things based on location
        if location.enemies and not self.game_flags.get("aware_of_enemies", False):
            discoveries.extend(location.enemies)
            self.game_flags["aware_of_enemies"] = True
            narrative_focus.append("threat_awareness")
        
        if location.special_features:
            discoveries.extend(location.special_features[:2])  # Discover first 2 features
            narrative_focus.append("special_discoveries")
        
        if location.items and not self.game_flags.get("items_spotted", False):
            discoveries.extend(location.items)
            self.game_flags["items_spotted"] = True
            narrative_focus.append("item_discovery")
        
        # Update story context
        if discoveries:
            self.story_context["current_situation"] = f"Discovered {', '.join(discoveries)} at {location.name}"
        
        return ActionResult(
            success=True,
            action_type=ActionType.EXAMINE,
            description=f"Carefully examined {location.name}",
            discoveries=discoveries,
            narrative_focus=narrative_focus,
            next_options=["investigate_discoveries", "ask_emberlyn", "proceed_cautiously"]
        )
    
    def _handle_ask_emberlyn(self) -> ActionResult:
        """Handle asking Emberlyn for guidance"""
        location = self.get_current_location()
        narrative_focus = ["emberlyn_wisdom", "fairy_insights"]
        
        # Emberlyn provides context-appropriate guidance
        guidance_topics = []
        
        if location.enemies:
            guidance_topics.append("combat_advice")
            narrative_focus.append("tactical_guidance")
        
        if location.special_features:
            guidance_topics.append("feature_explanation")
            narrative_focus.append("magical_knowledge")
        
        if not location.visited:
            guidance_topics.append("area_overview")
            narrative_focus.append("exploration_tips")
        
        # Update story context
        self.story_context["current_situation"] = f"Consulting with Emberlyn at {location.name}"
        self.story_context["mood"] = "seeking_guidance"
        
        return ActionResult(
            success=True,
            action_type=ActionType.SOCIAL,
            description="Asked Emberlyn for her wisdom and guidance",
            discoveries=guidance_topics,
            narrative_focus=narrative_focus,
            next_options=["follow_advice", "ask_more_questions", "take_action"]
        )
    
    def _handle_wait_observe(self) -> ActionResult:
        """Handle waiting and observing"""
        location = self.get_current_location()
        discoveries = []
        narrative_focus = ["patient_observation", "subtle_details"]
        
        # Waiting reveals different things based on location
        if location.enemies:
            discoveries.append("enemy_behavior_patterns")
            narrative_focus.append("threat_assessment")
            self.story_context["mood"] = "cautious_observation"
        else:
            discoveries.append("peaceful_atmosphere")
            narrative_focus.append("serene_moments")
            self.story_context["mood"] = "peaceful_contemplation"
        
        # Sometimes waiting reveals hidden things
        if location.special_features and len(location.special_features) > 2:
            discoveries.append(location.special_features[-1])  # Reveal last feature
            narrative_focus.append("hidden_discovery")
        
        return ActionResult(
            success=True,
            action_type=ActionType.WAIT,
            description=f"Waited and observed at {location.name}",
            discoveries=discoveries,
            narrative_focus=narrative_focus,
            next_options=["act_on_observations", "continue_waiting", "move_forward"]
        )
    
    def _handle_prepare_combat(self) -> ActionResult:
        """Handle preparing for combat"""
        location = self.get_current_location()
        
        if not location.enemies:
            return ActionResult(
                success=False,
                action_type=ActionType.COMBAT,
                description="No immediate threats detected",
                narrative_focus=["false_alarm", "overly_cautious"],
                next_options=["relax_stance", "examine_area", "ask_emberlyn"]
            )
        
        # Prepare for combat with known enemies
        self.story_context["current_situation"] = f"Preparing for combat with {', '.join(location.enemies)}"
        self.story_context["immediate_threat"] = location.enemies[0]
        self.story_context["mood"] = "combat_ready"
        
        return ActionResult(
            success=True,
            action_type=ActionType.COMBAT,
            description=f"Prepared for combat against {', '.join(location.enemies)}",
            discoveries=["tactical_advantage", "enemy_weaknesses"],
            narrative_focus=["combat_preparation", "tactical_assessment", "emberlyn_support"],
            next_options=["attack", "defensive_strategy", "attempt_negotiation"],
            requires_dice_roll=True
        )
    
    def _handle_movement(self, target_location_id: str) -> ActionResult:
        """Handle movement between locations"""
        
        try:
            target_id = LocationId(target_location_id)
        except ValueError:
            return ActionResult(
                success=False,
                action_type=ActionType.MOVE,
                description="Invalid destination",
                narrative_focus=["confusion", "emberlyn_correction"]
            )
        
        current_location = self.get_current_location()
        
        if target_id not in current_location.exits:
            return ActionResult(
                success=False,
                action_type=ActionType.MOVE,
                description=f"Cannot reach {self.locations[target_id].name} from here",
                narrative_focus=["blocked_path", "alternative_routes"],
                next_options=["find_another_way", "examine_area", "ask_emberlyn"]
            )
        
        # Successful movement
        old_location = self.current_location
        self.current_location = target_id
        new_location = self.get_current_location()
        
        # Update story context
        self.story_context["current_situation"] = f"Moved from {self.locations[old_location].name} to {new_location.name}"
        self.story_context["mood"] = "exploration"
        
        # Reset some location-specific flags
        self.game_flags["aware_of_enemies"] = False
        self.game_flags["items_spotted"] = False
        
        return ActionResult(
            success=True,
            action_type=ActionType.MOVE,
            description=f"Moved to {new_location.name}",
            discoveries=["new_location", "travel_experience"],
            state_changes={"location": target_id.value},
            narrative_focus=["journey_description", "new_environment", "emberlyn_commentary"],
            next_options=["examine_new_area", "ask_emberlyn", "continue_exploring"]
        )
    
    def _handle_examine_feature(self, feature: str) -> ActionResult:
        """Handle examining specific features"""
        location = self.get_current_location()
        
        if feature not in location.special_features:
            return ActionResult(
                success=False,
                action_type=ActionType.EXAMINE,
                description=f"No {feature.replace('_', ' ')} found here",
                narrative_focus=["search_failure", "emberlyn_suggestion"]
            )
        
        # Feature-specific discoveries
        discoveries = [feature]
        narrative_focus = ["detailed_examination", "emberlyn_knowledge"]
        
        if feature == "glowing_crystals":
            discoveries.extend(["magical_energy", "fire_essence"])
            narrative_focus.append("magical_discovery")
            self.game_flags["knows_about_crystal"] = True
        
        elif feature == "beetle_tracks":
            discoveries.extend(["recent_tracks", "creature_size"])
            narrative_focus.append("threat_assessment")
            self.game_flags["beetle_location_known"] = True
        
        elif feature == "sacred_flame":
            discoveries.extend(["dimming_flame", "ancient_magic"])
            narrative_focus.append("quest_revelation")
        
        return ActionResult(
            success=True,
            action_type=ActionType.EXAMINE,
            description=f"Examined {feature.replace('_', ' ')}",
            discoveries=discoveries,
            narrative_focus=narrative_focus,
            next_options=["investigate_further", "ask_emberlyn", "take_action"]
        )
    
    def _handle_general_action(self, action_input: str) -> ActionResult:
        """Handle general/unrecognized actions"""
        
        return ActionResult(
            success=True,
            action_type=ActionType.EXAMINE,
            description=f"Attempted: {action_input}",
            discoveries=["creative_approach"],
            narrative_focus=["player_creativity", "emberlyn_response"],
            next_options=["try_different_approach", "ask_emberlyn", "examine_area"]
        )
    
    def get_ai_context(self) -> Dict[str, Any]:
        """Get structured context for AI narrative generation"""
        location = self.get_current_location()
        
        return {
            "location": {
                "name": location.name,
                "description": location.description,
                "visited": location.visited
            },
            "situation": self.story_context,
            "game_state": {
                "turn": self.turn_count,
                "flags": self.game_flags,
                "character": self.character_stats
            },
            "immediate_context": {
                "enemies_present": location.enemies,
                "npcs_present": location.npcs,
                "items_available": location.items,
                "special_features": location.special_features
            }
        }
    
    def get_game_state_summary(self) -> str:
        """Get human-readable game state summary"""
        location = self.get_current_location()
        
        summary_parts = [
            f"Turn {self.turn_count}",
            f"Location: {location.name}",
            f"Situation: {self.story_context['current_situation']}"
        ]
        
        if location.enemies:
            summary_parts.append(f"Threats: {', '.join(location.enemies)}")
        
        if self.story_context.get("immediate_threat"):
            summary_parts.append(f"Immediate threat: {self.story_context['immediate_threat']}")
        
        return " | ".join(summary_parts)