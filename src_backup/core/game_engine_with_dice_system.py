"""
Enhanced Game Engine Adapter - Strangler Fig Pattern
Gradually replaces legacy AI integration with proper game engine
"""
from typing import Dict, Any, Optional
import json
from .experiment_manager import get_experiment_manager
from .game_engine import GameLocation, LocationId, ActionResult, ActionType
from ..ai.providers.local_character_creator import create_character_console as create_character_ai
from ..handlers.gameplay_handler import GamePerformanceMonitor
import time

class EnhancedGameEngineAdapter:
    """
    Adapter that uses Strangler Fig pattern to gradually replace legacy components
    Routes to new or legacy implementations based on experiment configuration
    """
    
    def __init__(self, user_id: str = "local_dev"):
        self.user_id = user_id
        self.experiment_manager = get_experiment_manager(user_id)
        self.performance_monitor = GamePerformanceMonitor()
        
        # Game state - managed by new engine if experiment enabled
        self.game_state = {
            'location': LocationId.VILLAGE_OUTSKIRTS,
            'story_progress': 0,
            'turn_count': 0,
            'world_state': {
                'shadow_blight_level': 1,
                'ashbrook_alert_level': 0,
                'emberlyn_bond': 0
            },
            'discovered_locations': [LocationId.VILLAGE_OUTSKIRTS],
            'completed_events': []
        }
        
        # Initialize locations if using new engine
        if self.experiment_manager.should_use_new_implementation("game_engine"):
            self._initialize_locations()
    
    def _initialize_locations(self):
        """Initialize game world locations"""
        self.locations = {
            LocationId.VILLAGE_OUTSKIRTS: GameLocation(
                id=LocationId.VILLAGE_OUTSKIRTS,
                name="Village Outskirts",
                description="A peaceful path leading to Ashbrook village, surrounded by autumn trees",
                exits=[LocationId.ASHBROOK_VILLAGE, LocationId.CRYSTAL_CAVE_ENTRANCE],
                special_features=["shadow_blight_traces", "weathered_signpost"]
            ),
            LocationId.ASHBROOK_VILLAGE: GameLocation(
                id=LocationId.ASHBROOK_VILLAGE,
                name="Ashbrook Village",
                description="A small farming village with thatched roofs and cobblestone streets",
                exits=[LocationId.VILLAGE_OUTSKIRTS, LocationId.VILLAGE_TAVERN, LocationId.SACRED_GROVE],
                npcs=["village_elder", "concerned_farmer", "traveling_merchant"]
            ),
            LocationId.CRYSTAL_CAVE_ENTRANCE: GameLocation(
                id=LocationId.CRYSTAL_CAVE_ENTRANCE,
                name="Crystal Cave Entrance",
                description="A mysterious cave entrance with strange crystalline formations",
                exits=[LocationId.VILLAGE_OUTSKIRTS, LocationId.CRYSTAL_CAVE_INTERIOR],
                special_features=["glowing_crystals", "shadow_blight_corruption"]
            ),
            LocationId.VILLAGE_TAVERN: GameLocation(
                id=LocationId.VILLAGE_TAVERN,
                name="Village Tavern",
                description="A cozy tavern with warm firelight and the smell of hearty stew",
                exits=[LocationId.ASHBROOK_VILLAGE],
                npcs=["tavern_keeper", "local_patrons", "mysterious_stranger"]
            ),
            LocationId.SACRED_GROVE: GameLocation(
                id=LocationId.SACRED_GROVE,
                name="Sacred Grove",
                description="An ancient grove where druids once gathered, now touched by shadow",
                exits=[LocationId.ASHBROOK_VILLAGE, LocationId.WHISPERING_GROVE],
                special_features=["ancient_stones", "shadow_corruption"]
            ),
            LocationId.WHISPERING_GROVE: GameLocation(
                id=LocationId.WHISPERING_GROVE,
                name="Whispering Grove",
                description="The grove mentioned in the opening - where the fire sprite awaits",
                exits=[LocationId.SACRED_GROVE, LocationId.FIRE_SPRITE_CLEARING],
                special_features=["mysterious_runes", "fire_sprite_presence"]
            ),
            LocationId.FIRE_SPRITE_CLEARING: GameLocation(
                id=LocationId.FIRE_SPRITE_CLEARING,
                name="Fire Sprite Clearing",
                description="A small clearing where the mischievous fire sprite dances among the flames",
                exits=[LocationId.WHISPERING_GROVE],
                npcs=["fire_sprite"],
                special_features=["dancing_flames", "sprite_magic"]
            ),
            LocationId.CRYSTAL_CAVE_INTERIOR: GameLocation(
                id=LocationId.CRYSTAL_CAVE_INTERIOR,
                name="Crystal Cave Interior",
                description="Deep within the cave, crystals pulse with otherworldly energy",
                exits=[LocationId.CRYSTAL_CAVE_ENTRANCE, LocationId.UNDERGROUND_CHAMBER],
                special_features=["pulsing_crystals", "magical_resonance"]
            ),
            LocationId.UNDERGROUND_CHAMBER: GameLocation(
                id=LocationId.UNDERGROUND_CHAMBER,
                name="Underground Chamber",
                description="A vast underground chamber with ancient secrets",
                exits=[LocationId.CRYSTAL_CAVE_INTERIOR],
                special_features=["ancient_murals", "hidden_treasure"]
            )
        }
    
    def start_new_game(self, character: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start new game - routes to new or legacy implementation
        """
        start_time = time.time()
        
        try:
            if self.experiment_manager.should_use_new_implementation("game_engine"):
                result = self._start_new_game_enhanced(character)
                self.experiment_manager.record_metric(
                    "local_game_engine_v2", 
                    "game_start_success", 
                    True,
                    {"method": "enhanced", "response_time": time.time() - start_time}
                )
            else:
                result = self._start_new_game_legacy(character)
                self.experiment_manager.record_metric(
                    "local_game_engine_v2", 
                    "game_start_success", 
                    True,
                    {"method": "legacy", "response_time": time.time() - start_time}
                )
            
            return result
            
        except Exception as e:
            # Fallback to legacy on error
            self.experiment_manager.record_metric(
                "local_game_engine_v2", 
                "game_start_error", 
                str(e),
                {"fallback_used": True}
            )
            return self._start_new_game_legacy(character)
    
    def _start_new_game_enhanced(self, character: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced game start with proper state management"""
        self.character = character
        current_location = self.locations[self.game_state['location']]
        
        # Generate contextual opening
        narrative = self._generate_location_narrative(current_location, is_opening=True)
        choices = self._generate_location_choices(current_location)
        
        return {
            'narrative': narrative,
            'choices': choices,
            'location': current_location.name,
            'debug_info': {
                'engine_version': 'enhanced_v2',
                'location_id': current_location.id.value,
                'story_progress': self.game_state['story_progress']
            }
        }
    
    def _start_new_game_legacy(self, character: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy game start - fallback implementation"""
        return {
            'narrative': f"Welcome {character['name']} the {character['class']}! Your adventure begins at the village outskirts. Emberlyn the fairy companion flutters beside you, ready to guide your journey.",
            'choices': [
                "1. Examine the surrounding area carefully",
                "2. Head towards Ashbrook village",
                "3. Look for signs of trouble or danger",
                "4. Ask Emberlyn for guidance"
            ],
            'location': "Village Outskirts",
            'debug_info': {'engine_version': 'legacy'}
        }
    
    def process_player_action(self, player_input: str) -> Dict[str, Any]:
        """
        Process player action - routes to new or legacy implementation
        """
        start_time = time.time()
        self.game_state['turn_count'] += 1
        
        try:
            if self.experiment_manager.should_use_new_implementation("choice_processor"):
                result = self._process_action_enhanced(player_input)
                self.experiment_manager.record_metric(
                    "local_game_engine_v2", 
                    "action_processing_success", 
                    True,
                    {"method": "enhanced", "response_time": time.time() - start_time}
                )
            else:
                result = self._process_action_legacy(player_input)
                self.experiment_manager.record_metric(
                    "local_game_engine_v2", 
                    "action_processing_success", 
                    True,
                    {"method": "legacy", "response_time": time.time() - start_time}
                )
            
            return result
            
        except Exception as e:
            # Fallback to legacy on error
            self.experiment_manager.record_metric(
                "local_game_engine_v2", 
                "action_processing_error", 
                str(e),
                {"fallback_used": True}
            )
            return self._process_action_legacy(player_input)
    
    def _process_action_enhanced(self, player_input: str) -> Dict[str, Any]:
        """Enhanced action processing with proper state management"""
        current_location = self.locations[self.game_state['location']]
        
        # Parse player choice
        action_result = self._parse_and_execute_action(player_input, current_location)
        
        # Update game state based on action
        if action_result.success:
            self._update_game_state(action_result)
        
        # Generate response narrative
        narrative = self._generate_action_response(action_result, current_location)
        
        # Get new location after potential movement
        new_location = self.locations[self.game_state['location']]
        choices = self._generate_location_choices(new_location)
        
        return {
            'narrative': narrative,
            'choices': choices,
            'location': new_location.name,
            'mechanical_results': {
                'action_success': action_result.success,
                'discoveries': action_result.discoveries,
                'state_changes': action_result.state_changes
            },
            'debug_info': {
                'engine_version': 'enhanced_v2',
                'location_id': new_location.id.value,
                'story_progress': self.game_state['story_progress'],
                'turn': self.game_state['turn_count']
            }
        }
    
    def _process_action_legacy(self, player_input: str) -> Dict[str, Any]:
        """Legacy action processing - basic fallback"""
        return {
            'narrative': f"You chose option {player_input}. The story continues as you explore the village outskirts. Emberlyn flutters nearby, offering guidance.",
            'choices': [
                "1. Continue exploring the area",
                "2. Head towards the village",
                "3. Look for clues about the shadow blight",
                "4. Rest and plan your next move"
            ],
            'location': "Village Outskirts",
            'debug_info': {'engine_version': 'legacy'}
        }
    
    def _parse_and_execute_action(self, player_input: str, location: GameLocation) -> ActionResult:
        """Parse player input and execute action with REAL dice-based consequences"""
        try:
            choice_num = int(player_input.strip())
        except ValueError:
            choice_num = 1  # Default to first choice
        
        # Import dice system
        from .action_system import get_action_processor
        action_processor = get_action_processor()
        
        # Map choice to action type
        action_mapping = {
            1: 'examine',
            2: 'move', 
            3: 'investigate',
            4: 'social'
        }
        
        action_type = action_mapping.get(choice_num, 'examine')
        
        # Process action with dice system
        consequence = action_processor.process_action(
            action_type, 
            self.character, 
            self.game_state,
            {'location': location, 'choice_number': choice_num}
        )
        
        # Apply consequences to game state
        self._apply_consequences(consequence)
        
        # Convert to ActionResult format
        return ActionResult(
            success=consequence.success,
            action_type=ActionType.EXAMINE if action_type == 'examine' else ActionType.MOVE,
            description=consequence.narrative_outcome,
            discoveries=list(consequence.mechanical_effects.keys()),
            state_changes=consequence.state_changes,
            dice_result={
                'roll': consequence.roll_result.description if consequence.roll_result else "No roll made",
                'success': consequence.success,
                'total': consequence.roll_result.total if consequence.roll_result else 0,
                'difficulty': consequence.roll_result.difficulty if consequence.roll_result else 0
            }
        )
    
    def _apply_consequences(self, consequence):
        """Apply action consequences to game state"""
        # Apply state changes from dice results
        for key, value in consequence.state_changes.items():
            if key == 'location':
                self.game_state['location'] = value
                if value not in self.game_state['discovered_locations']:
                    self.game_state['discovered_locations'].append(value)
            elif key == 'story_progress':
                self.game_state['story_progress'] = max(self.game_state['story_progress'], value)
            elif key == 'hp_damage' and hasattr(self, 'character'):
                current_hp = self.character.get('resources', {}).get('hp', 20)
                self.character['resources']['hp'] = max(0, current_hp - value)
            elif key == 'mana_damage' and hasattr(self, 'character'):
                current_mana = self.character.get('resources', {}).get('energy', 10)
                self.character['resources']['energy'] = max(0, current_mana - value)
            elif key in ['social_standing', 'investigation_progress', 'magical_progress']:
                # Track ongoing character development
                if not hasattr(self, 'character_progression'):
                    self.character_progression = {}
                self.character_progression[key] = self.character_progression.get(key, 0) + value
    

    

    

    
    def _update_game_state(self, action_result: ActionResult):
        """Update game state based on action result"""
        for key, value in action_result.state_changes.items():
            if key == 'story_progress':
                self.game_state['story_progress'] = value
            elif key == 'location_changed':
                # Location already updated in movement action
                pass
    
    def _generate_location_narrative(self, location: GameLocation, is_opening: bool = False) -> str:
        """Generate narrative for current location"""
        base_narrative = location.description
        
        if is_opening:
            return f"*Emberlyn flutters beside you as you arrive at {location.name}* {base_narrative}. The fairy's warm glow illuminates the path ahead, and you sense adventure awaiting."
        
        # Add contextual details based on game state
        if self.game_state['world_state']['shadow_blight_level'] > 1:
            base_narrative += " You notice signs of shadow blight corruption in the area."
        
        if location.special_features:
            feature_descriptions = {
                'shadow_blight_traces': "Dark tendrils creep along the ground",
                'weathered_signpost': "An old signpost points toward various destinations",
                'glowing_crystals': "Strange crystals emit an otherworldly light"
            }
            for feature in location.special_features:
                if feature in feature_descriptions:
                    base_narrative += f" {feature_descriptions[feature]}."
        
        return base_narrative
    
    def _generate_action_response(self, action_result: ActionResult, location: GameLocation) -> str:
        """Generate narrative response to player action with dice results"""
        base_response = action_result.description
        
        # Show dice roll results
        if action_result.dice_result:
            dice_info = action_result.dice_result
            base_response += f"\n\n🎲 DICE ROLL: {dice_info['roll']}"
        
        if action_result.discoveries:
            discovery_text = ", ".join(action_result.discoveries)
            base_response += f"\n\n🔍 MECHANICAL EFFECTS: {discovery_text}"
        
        if action_result.action_type == ActionType.MOVE and action_result.success:
            new_location = self.locations[self.game_state['location']]
            base_response += f"\n\n📍 NEW LOCATION: {self._generate_location_narrative(new_location)}"
        
        return base_response
    
    def _generate_location_choices(self, location: GameLocation) -> list:
        """Generate contextual choices for current location"""
        choices = []
        
        # Always have examine option
        choices.append(f"1. Examine {location.name} more carefully")
        
        # Movement options
        if location.exits:
            exit_location = self.locations[location.exits[0]]
            choices.append(f"2. Head towards {exit_location.name}")
        else:
            choices.append("2. Look for a way forward")
        
        # Investigation option
        if location.special_features:
            choices.append("3. Investigate the unusual features you notice")
        else:
            choices.append("3. Search for clues or hidden details")
        
        # Social option
        if location.npcs:
            choices.append("4. Speak with the people here")
        else:
            choices.append("4. Consult with Emberlyn about your next move")
        
        return choices
    
    def get_character_sheet(self) -> str:
        """Get character sheet information"""
        if not hasattr(self, 'character'):
            return "No character loaded"
        
        return f"""
🎭 CHARACTER SHEET
==================
Name: {self.character['name']}
Class: {self.character['class']}
Level: {self.character.get('level', 1)}

🌍 GAME STATE:
Location: {self.locations[self.game_state['location']].name}
Story Progress: {self.game_state['story_progress']}
Turn: {self.game_state['turn_count']}

🔬 EXPERIMENT INFO:
Engine: {'Enhanced V2' if self.experiment_manager.should_use_new_implementation('game_engine') else 'Legacy'}
Features: {list(self.experiment_manager.get_component_config('game_engine').keys())}
"""