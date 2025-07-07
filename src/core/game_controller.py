"""
Game Controller - Orchestrates Code-Managed Game Engine + AI Narrative
This is the new main integration layer
"""
from typing import Dict, List, Any
from .game_engine import FireWhisperGameEngine, ActionResult
from .narrative_generator import NarrativeGenerator
import os

class GameController:
    """Main game controller - Code manages state, AI writes narrative"""
    
    def __init__(self):
        self.game_engine = FireWhisperGameEngine()
        self.narrative_generator = NarrativeGenerator()
        self.debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    
    def start_new_game(self) -> Dict[str, Any]:
        """Start a new game session"""
        
        if self.debug_mode:
            print("🎮 Starting new code-managed game...")
            print(f"📍 Initial location: {self.game_engine.get_current_location().name}")
        
        # Get game context
        game_context = self.game_engine.get_ai_context()
        
        # Generate opening narrative
        opening_narrative = self.narrative_generator.generate_game_start_narrative(game_context)
        
        # Get available actions
        available_actions = self.game_engine.get_available_actions()
        
        return {
            "narrative": opening_narrative,
            "actions": available_actions,
            "game_state": self.game_engine.get_game_state_summary(),
            "debug_info": game_context if self.debug_mode else {}
        }
    
    def process_player_action(self, player_input: str) -> Dict[str, Any]:
        """Process player action through code-managed engine"""
        
        if self.debug_mode:
            print(f"\n🎯 Processing action: {player_input}")
            print(f"📍 Current location: {self.game_engine.get_current_location().name}")
        
        # 1. Code determines what happens
        action_result = self.game_engine.process_action(player_input)
        
        if self.debug_mode:
            print(f"⚙️ Action result: {action_result.action_type.value} - {'Success' if action_result.success else 'Failed'}")
            if action_result.discoveries:
                print(f"🔍 Discoveries: {', '.join(action_result.discoveries)}")
        
        # 2. Get updated game context
        game_context = self.game_engine.get_ai_context()
        
        # 3. AI generates narrative based on code results
        narrative = self.narrative_generator.generate_narrative(action_result, game_context)
        
        # 4. Get new available actions
        available_actions = self.game_engine.get_available_actions()
        
        # 5. Handle dice rolls if needed
        dice_info = None
        if action_result.requires_dice_roll:
            dice_info = self._handle_dice_roll(action_result)
        
        return {
            "narrative": narrative,
            "actions": available_actions,
            "game_state": self.game_engine.get_game_state_summary(),
            "action_result": {
                "type": action_result.action_type.value,
                "success": action_result.success,
                "discoveries": action_result.discoveries
            },
            "dice_info": dice_info,
            "debug_info": {
                "game_context": game_context,
                "action_result": action_result
            } if self.debug_mode else {}
        }
    
    def _handle_dice_roll(self, action_result: ActionResult) -> Dict[str, Any]:
        """Handle dice rolling for actions that require it"""
        
        import random
        
        # Simple dice roll - could be enhanced
        roll = random.randint(1, 20)
        modifier = 2  # Base modifier
        total = roll + modifier
        
        # Determine success threshold based on action
        if action_result.action_type.value == "combat":
            threshold = 12
        else:
            threshold = 10
        
        success = total >= threshold
        
        dice_result = {
            "roll": roll,
            "modifier": modifier,
            "total": total,
            "threshold": threshold,
            "success": success
        }
        
        # Update action result with dice outcome
        action_result.dice_result = dice_result
        
        if self.debug_mode:
            print(f"🎲 Dice roll: {roll} + {modifier} = {total} vs {threshold} ({'SUCCESS' if success else 'FAILURE'})")
        
        return dice_result
    
    def get_character_sheet(self) -> str:
        """Get formatted character information"""
        
        stats = self.game_engine.character_stats
        location = self.game_engine.get_current_location()
        flags = self.game_engine.game_flags
        
        return f"""
📊 **Character Status**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❤️ HP: {stats['hp']}/{stats['max_hp']} | ⭐ Level: {stats['level']} | ✨ XP: {stats['xp']}

📍 **Current Location:** {location.name}
🎯 **Turn:** {self.game_engine.turn_count}

🏆 **Progress Flags:**
{chr(10).join([f"   {'✅' if value else '❌'} {key.replace('_', ' ').title()}" for key, value in flags.items()])}

🌍 **Game State:** {self.game_engine.get_game_state_summary()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def get_available_actions_formatted(self) -> str:
        """Get formatted list of available actions"""
        
        actions = self.game_engine.get_available_actions()
        
        formatted_actions = []
        for i, action in enumerate(actions, 1):
            risk_emoji = {"none": "🟢", "low": "🟡", "medium": "🟠", "high": "🔴"}.get(action.get("risk", "low"), "🟡")
            formatted_actions.append(f"{i}. {action['text']} {risk_emoji}")
        
        return "\n".join(formatted_actions)
    
    def save_game_state(self) -> Dict[str, Any]:
        """Export current game state for saving"""
        
        return {
            "current_location": self.game_engine.current_location.value,
            "turn_count": self.game_engine.turn_count,
            "game_flags": self.game_engine.game_flags,
            "character_stats": self.game_engine.character_stats,
            "story_context": self.game_engine.story_context,
            "locations_visited": {
                loc_id.value: loc.visited 
                for loc_id, loc in self.game_engine.locations.items()
            }
        }
    
    def load_game_state(self, save_data: Dict[str, Any]):
        """Load game state from save data"""
        
        from .game_engine import LocationId
        
        self.game_engine.current_location = LocationId(save_data["current_location"])
        self.game_engine.turn_count = save_data["turn_count"]
        self.game_engine.game_flags = save_data["game_flags"]
        self.game_engine.character_stats = save_data["character_stats"]
        self.game_engine.story_context = save_data["story_context"]
        
        # Restore location visited status
        for loc_id_str, visited in save_data.get("locations_visited", {}).items():
            loc_id = LocationId(loc_id_str)
            if loc_id in self.game_engine.locations:
                self.game_engine.locations[loc_id].visited = visited