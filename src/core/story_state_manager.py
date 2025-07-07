"""
Story State Management System - Tracks all game world state
Replaces AI memory with reliable code-based state tracking
"""
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import json
import time

class LocationType(Enum):
    VILLAGE = "village"
    FOREST = "forest"
    CAVE = "cave"
    SHRINE = "shrine"
    RUINS = "ruins"
    TAVERN = "tavern"
    SHOP = "shop"
    ROAD = "road"

class WeatherType(Enum):
    CLEAR = "clear"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    FOGGY = "foggy"
    STORMY = "stormy"

class TimeOfDay(Enum):
    DAWN = "dawn"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    MIDNIGHT = "midnight"

@dataclass
class NPC:
    name: str
    role: str  # "merchant", "guard", "villager", etc.
    location: str
    disposition: str  # "friendly", "neutral", "hostile", "afraid"
    dialogue_state: str = "initial"  # tracks conversation progress
    quest_giver: bool = False
    shop_keeper: bool = False
    inventory: List[str] = field(default_factory=list)

@dataclass
class Location:
    name: str
    type: LocationType
    description: str
    connected_locations: List[str] = field(default_factory=list)
    npcs_present: List[str] = field(default_factory=list)
    enemies_present: List[str] = field(default_factory=list)
    items_available: List[str] = field(default_factory=list)
    environmental_features: List[str] = field(default_factory=list)
    visited: bool = False
    safe_zone: bool = True

@dataclass
class Quest:
    id: str
    name: str
    description: str
    giver: str
    status: str = "available"  # "available", "active", "completed", "failed"
    objectives: List[str] = field(default_factory=list)
    completed_objectives: Set[str] = field(default_factory=set)
    rewards: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EnvironmentalConditions:
    weather: WeatherType = WeatherType.CLEAR
    time_of_day: TimeOfDay = TimeOfDay.AFTERNOON
    lighting: str = "normal"  # "bright", "normal", "dim", "dark"
    temperature: str = "comfortable"  # "hot", "warm", "comfortable", "cool", "cold"
    special_conditions: List[str] = field(default_factory=list)

class StoryStateManager:
    """Manages all persistent game world state"""
    
    def __init__(self):
        self.current_location = "village_outskirts"
        self.previous_location = None
        self.turn_count = 0
        self.story_flags: Dict[str, Any] = {}
        self.environmental_conditions = EnvironmentalConditions()
        
        # Initialize world data
        self.locations: Dict[str, Location] = {}
        self.npcs: Dict[str, NPC] = {}
        self.quests: Dict[str, Quest] = {}
        self.recent_events: List[str] = []  # Last 5 significant events
        
        self._initialize_world()
    
    def _initialize_world(self):
        """Set up the initial game world"""
        
        # Create locations
        self.locations = {
            "village_outskirts": Location(
                name="Village Outskirts",
                type=LocationType.ROAD,
                description="A peaceful path leading to Ashbrook village, surrounded by autumn trees",
                connected_locations=["ashbrook_village", "ember_woods_entrance"],
                environmental_features=["autumn_trees", "cobblestone_path", "village_smoke_visible"]
            ),
            "ashbrook_village": Location(
                name="Ashbrook Village",
                type=LocationType.VILLAGE,
                description="A cozy village with thatched roofs and friendly villagers",
                connected_locations=["village_outskirts", "village_tavern", "village_shop"],
                npcs_present=["village_elder", "concerned_farmer"],
                safe_zone=True
            ),
            "village_tavern": Location(
                name="The Rusty Sword Inn",
                type=LocationType.TAVERN,
                description="A warm tavern with crackling fireplace and the smell of spiced cider",
                connected_locations=["ashbrook_village"],
                npcs_present=["innkeeper_martha", "traveling_merchant"],
                safe_zone=True
            ),
            "ember_woods_entrance": Location(
                name="Ember Woods Entrance",
                type=LocationType.FOREST,
                description="The edge of ancient woods where magical creatures dwell",
                connected_locations=["village_outskirts", "sacred_grove", "crystal_cave_entrance"],
                environmental_features=["ancient_trees", "magical_atmosphere", "fairy_lights"]
            ),
            "crystal_cave_entrance": Location(
                name="Crystal Cave Entrance",
                type=LocationType.CAVE,
                description="A narrow cave entrance with the sound of skittering from within",
                connected_locations=["ember_woods_entrance", "crystal_cave_interior"],
                enemies_present=["fire_beetle"],
                environmental_features=["dim_lighting", "rocky_walls", "crystal_glints"],
                safe_zone=False
            ),
            "crystal_cave_interior": Location(
                name="Crystal Cave Interior",
                type=LocationType.CAVE,
                description="A glittering cavern filled with fire essence crystals",
                connected_locations=["crystal_cave_entrance"],
                items_available=["fire_essence_crystal"],
                environmental_features=["crystal_formations", "magical_glow", "warm_air"],
                safe_zone=False
            ),
            "sacred_grove": Location(
                name="Sacred Grove",
                type=LocationType.SHRINE,
                description="An ancient grove with a dimming sacred flame at its heart",
                connected_locations=["ember_woods_entrance"],
                environmental_features=["ancient_hearth", "sacred_flame", "stone_circle"],
                safe_zone=True
            )
        }
        
        # Create NPCs
        self.npcs = {
            "village_elder": NPC(
                name="Elder Thorne",
                role="village_leader",
                location="ashbrook_village",
                disposition="concerned",
                quest_giver=True
            ),
            "concerned_farmer": NPC(
                name="Farmer Willem",
                role="farmer",
                location="ashbrook_village", 
                disposition="worried",
                dialogue_state="worried_about_woods"
            ),
            "innkeeper_martha": NPC(
                name="Martha",
                role="innkeeper",
                location="village_tavern",
                disposition="friendly",
                shop_keeper=True,
                inventory=["healing_potion", "spiced_cider", "travel_rations"]
            ),
            "traveling_merchant": NPC(
                name="Gareth the Trader",
                role="merchant",
                location="village_tavern",
                disposition="neutral",
                shop_keeper=True,
                inventory=["silver_charm", "rope", "torch", "basic_sword"]
            )
        }
        
        # Create initial quest
        self.quests = {
            "restore_sacred_flame": Quest(
                id="restore_sacred_flame",
                name="Restore the Sacred Flame",
                description="Find a Fire Essence crystal to restore the dimming Sacred Flame",
                giver="village_elder",
                status="active",
                objectives=[
                    "find_fire_essence_crystal",
                    "defeat_cave_guardian", 
                    "return_to_sacred_grove",
                    "restore_the_flame"
                ],
                rewards={"xp": 100, "gold": 50, "reputation": "village_hero"}
            )
        }
        
        # Set initial story flags
        self.story_flags = {
            "met_emberlyn": True,
            "knows_about_sacred_flame": True,
            "cave_location_known": True,
            "has_fire_crystal": False,
            "sacred_flame_restored": False
        }
    
    def move_to_location(self, location_id: str) -> Dict[str, Any]:
        """Move player to a new location and return context"""
        if location_id not in self.locations:
            return {"error": f"Location {location_id} does not exist"}
        
        old_location = self.current_location
        self.previous_location = old_location
        self.current_location = location_id
        
        # Mark location as visited
        self.locations[location_id].visited = True
        
        # Add to recent events
        self.add_recent_event(f"moved_from_{old_location}_to_{location_id}")
        
        return self.get_current_context()
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get complete context for current situation"""
        location = self.locations[self.current_location]
        
        return {
            "location": {
                "id": self.current_location,
                "name": location.name,
                "type": location.type.value,
                "description": location.description,
                "safe_zone": location.safe_zone,
                "environmental_features": location.environmental_features
            },
            "npcs_present": [
                {
                    "id": npc_id,
                    "name": self.npcs[npc_id].name,
                    "role": self.npcs[npc_id].role,
                    "disposition": self.npcs[npc_id].disposition
                }
                for npc_id in location.npcs_present if npc_id in self.npcs
            ],
            "enemies_present": location.enemies_present,
            "items_available": location.items_available,
            "connected_locations": [
                {
                    "id": loc_id,
                    "name": self.locations[loc_id].name,
                    "type": self.locations[loc_id].type.value
                }
                for loc_id in location.connected_locations if loc_id in self.locations
            ],
            "environmental_conditions": {
                "weather": self.environmental_conditions.weather.value,
                "time_of_day": self.environmental_conditions.time_of_day.value,
                "lighting": self.environmental_conditions.lighting,
                "temperature": self.environmental_conditions.temperature,
                "special_conditions": self.environmental_conditions.special_conditions
            },
            "active_quests": [
                quest for quest in self.quests.values() 
                if quest.status == "active"
            ],
            "story_flags": self.story_flags.copy(),
            "recent_events": self.recent_events.copy(),
            "turn_count": self.turn_count
        }
    
    def add_recent_event(self, event: str):
        """Add an event to recent history"""
        self.recent_events.append(event)
        if len(self.recent_events) > 5:
            self.recent_events.pop(0)
    
    def set_story_flag(self, flag: str, value: Any):
        """Set a story flag"""
        self.story_flags[flag] = value
        self.add_recent_event(f"story_flag_{flag}_set_to_{value}")
    
    def get_story_flag(self, flag: str, default: Any = None) -> Any:
        """Get a story flag value"""
        return self.story_flags.get(flag, default)
    
    def update_quest_progress(self, quest_id: str, objective: str):
        """Mark a quest objective as completed"""
        if quest_id in self.quests:
            quest = self.quests[quest_id]
            quest.completed_objectives.add(objective)
            
            # Check if quest is complete
            if all(obj in quest.completed_objectives for obj in quest.objectives):
                quest.status = "completed"
                self.add_recent_event(f"quest_{quest_id}_completed")
    
    def add_npc_to_location(self, npc_id: str, location_id: str):
        """Move an NPC to a location"""
        if npc_id in self.npcs and location_id in self.locations:
            # Remove from old location
            for loc in self.locations.values():
                if npc_id in loc.npcs_present:
                    loc.npcs_present.remove(npc_id)
            
            # Add to new location
            self.locations[location_id].npcs_present.append(npc_id)
            self.npcs[npc_id].location = location_id
    
    def add_enemy_to_location(self, enemy_id: str, location_id: str):
        """Add an enemy to a location"""
        if location_id in self.locations:
            if enemy_id not in self.locations[location_id].enemies_present:
                self.locations[location_id].enemies_present.append(enemy_id)
                self.locations[location_id].safe_zone = False
    
    def remove_enemy_from_location(self, enemy_id: str, location_id: str):
        """Remove an enemy from a location"""
        if location_id in self.locations:
            if enemy_id in self.locations[location_id].enemies_present:
                self.locations[location_id].enemies_present.remove(enemy_id)
                
                # Check if location is now safe
                if not self.locations[location_id].enemies_present:
                    self.locations[location_id].safe_zone = True
    
    def advance_time(self, hours: int = 1):
        """Advance game time"""
        time_order = list(TimeOfDay)
        current_index = time_order.index(self.environmental_conditions.time_of_day)
        new_index = (current_index + hours) % len(time_order)
        self.environmental_conditions.time_of_day = time_order[new_index]
        
        self.add_recent_event(f"time_advanced_to_{self.environmental_conditions.time_of_day.value}")
    
    def change_weather(self, weather: WeatherType):
        """Change weather conditions"""
        old_weather = self.environmental_conditions.weather
        self.environmental_conditions.weather = weather
        self.add_recent_event(f"weather_changed_from_{old_weather.value}_to_{weather.value}")
    
    def get_narrative_context_summary(self) -> str:
        """Get a concise summary for AI narrative generation"""
        context = self.get_current_context()
        location = context["location"]
        
        summary_parts = [
            f"Location: {location['name']} ({location['type']})",
            f"Description: {location['description']}"
        ]
        
        if context["enemies_present"]:
            summary_parts.append(f"Enemies: {', '.join(context['enemies_present'])}")
        
        if context["npcs_present"]:
            npc_names = [npc["name"] for npc in context["npcs_present"]]
            summary_parts.append(f"NPCs: {', '.join(npc_names)}")
        
        if context["recent_events"]:
            recent = context["recent_events"][-2:]  # Last 2 events
            summary_parts.append(f"Recent: {', '.join(recent)}")
        
        env = context["environmental_conditions"]
        summary_parts.append(f"Time: {env['time_of_day']}, Weather: {env['weather']}")
        
        return " | ".join(summary_parts)
    
    def increment_turn(self):
        """Increment turn counter"""
        self.turn_count += 1
        
        # Advance time slightly each turn
        if self.turn_count % 3 == 0:  # Every 3 turns = 1 hour
            self.advance_time(1)
    
    def save_state(self) -> Dict[str, Any]:
        """Export state for saving"""
        return {
            "current_location": self.current_location,
            "previous_location": self.previous_location,
            "turn_count": self.turn_count,
            "story_flags": self.story_flags,
            "environmental_conditions": {
                "weather": self.environmental_conditions.weather.value,
                "time_of_day": self.environmental_conditions.time_of_day.value,
                "lighting": self.environmental_conditions.lighting,
                "temperature": self.environmental_conditions.temperature,
                "special_conditions": self.environmental_conditions.special_conditions
            },
            "recent_events": self.recent_events,
            "quest_states": {
                qid: {
                    "status": quest.status,
                    "completed_objectives": list(quest.completed_objectives)
                }
                for qid, quest in self.quests.items()
            }
        }
    
    def load_state(self, state_data: Dict[str, Any]):
        """Import state from save data"""
        self.current_location = state_data.get("current_location", "village_outskirts")
        self.previous_location = state_data.get("previous_location")
        self.turn_count = state_data.get("turn_count", 0)
        self.story_flags = state_data.get("story_flags", {})
        self.recent_events = state_data.get("recent_events", [])
        
        # Restore environmental conditions
        env_data = state_data.get("environmental_conditions", {})
        self.environmental_conditions.weather = WeatherType(env_data.get("weather", "clear"))
        self.environmental_conditions.time_of_day = TimeOfDay(env_data.get("time_of_day", "afternoon"))
        self.environmental_conditions.lighting = env_data.get("lighting", "normal")
        self.environmental_conditions.temperature = env_data.get("temperature", "comfortable")
        self.environmental_conditions.special_conditions = env_data.get("special_conditions", [])
        
        # Restore quest states
        quest_states = state_data.get("quest_states", {})
        for qid, qstate in quest_states.items():
            if qid in self.quests:
                self.quests[qid].status = qstate.get("status", "available")
                self.quests[qid].completed_objectives = set(qstate.get("completed_objectives", []))