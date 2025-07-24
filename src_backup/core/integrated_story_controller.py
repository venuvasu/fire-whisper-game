"""
Integrated Story Controller - Combines story arcs, location debugging, and dynamic options
"""
from typing import Dict, List, Any, Optional, Tuple
import json
import time

from .story_arc_manager import StoryArcManager, StoryArc
from .location_progression_debugger import LocationProgressionDebugger
from .option_generator import DynamicOptionGenerator
from .game_state_manager import GameStateManager
from .story_state_manager import StoryStateManager

class IntegratedStoryController:
    """Main controller that integrates all story systems"""
    
    def __init__(self, game_state_manager: GameStateManager = None, 
                 story_state_manager: StoryStateManager = None):
        self.game_state_manager = game_state_manager or GameStateManager()
        self.story_state_manager = story_state_manager or StoryStateManager()
        
        # Initialize subsystems
        self.story_arc_manager = StoryArcManager()
        self.location_debugger = LocationProgressionDebugger()
        self.option_generator = DynamicOptionGenerator()
        
        # Integration state
        self.integration_active = True
        self.debug_mode = True
        self.last_ai_response = ""
        self.pending_location_change = None
        
    def process_turn(self, player_action: str, ai_response: str, 
                    dice_rolls: List[Dict] = None) -> Dict[str, Any]:
        """Process a complete turn with all integrated systems"""
        
        turn_result = {
            'turn_processed': True,
            'systems_active': {
                'story_arcs': True,
                'location_debugging': True,
                'dynamic_options': True
            },
            'integration_data': {}
        }
        
        # Store AI response for analysis
        self.last_ai_response = ai_response
        
        # 1. Process location transitions with debugging
        location_result = self._process_location_transitions(ai_response, dice_rolls)
        turn_result['integration_data']['location_processing'] = location_result
        
        # 2. Update story arc progress
        arc_result = self._process_story_arc_progression(player_action, ai_response)
        turn_result['integration_data']['story_arc_processing'] = arc_result
        
        # 3. Update option generator with recent action
        self.option_generator.update_recent_actions(player_action)
        
        # 4. Increment turn counters
        self.game_state_manager.increment_turn()
        self.story_state_manager.increment_turn()
        
        # 5. Check for story arc activation
        arc_activation_result = self._check_story_arc_activation()
        if arc_activation_result.get('arc_activated'):
            turn_result['integration_data']['new_arc_activated'] = arc_activation_result
        
        return turn_result
    
    def _process_location_transitions(self, ai_response: str, 
                                    dice_rolls: List[Dict] = None) -> Dict[str, Any]:
        """Process location transitions with debugging"""
        
        current_location = self.story_state_manager.current_location
        turn_number = self.story_state_manager.turn_count
        
        # Debug location transition
        debug_result = self.location_debugger.debug_location_transition(
            ai_response, current_location, dice_rolls, turn_number
        )
        
        result = {
            'debug_result': debug_result,
            'location_changed': False,
            'old_location': current_location,
            'new_location': current_location
        }
        
        # Apply location change if valid
        if debug_result['transition_detected'] and debug_result['transition_valid']:
            new_location = debug_result['new_location']
            
            # Update story state manager
            move_result = self.story_state_manager.move_to_location(new_location)
            
            # Update game state manager
            game_move_result = self.game_state_manager.update_location(
                new_location, "ai_narrative_transition"
            )
            
            result.update({
                'location_changed': True,
                'new_location': new_location,
                'story_state_result': move_result,
                'game_state_result': game_move_result
            })
        
        # Handle fixes if needed
        elif debug_result['fixes_applied']:
            result['fixes_applied'] = debug_result['fixes_applied']
            
            # If a dice roll was suggested, store it for next turn
            if debug_result.get('suggested_dice_roll'):
                self.pending_location_change = {
                    'target_location': debug_result['new_location'],
                    'suggested_roll': debug_result['suggested_dice_roll'],
                    'reason': 'location_transition_fix'
                }
        
        return result
    
    def _process_story_arc_progression(self, player_action: str, ai_response: str) -> Dict[str, Any]:
        """Process story arc progression"""
        
        result = {'arc_progression': False}
        
        # Check if we have an active arc
        current_arc_context = self.story_arc_manager.get_current_arc_context()
        
        if current_arc_context.get('no_active_arc'):
            result['no_active_arc'] = True
            return result
        
        # Determine if significant progress was made
        progress_indicators = [
            'quest', 'discovery', 'revelation', 'conflict', 'resolution',
            'important', 'significant', 'breakthrough', 'climax'
        ]
        
        ai_response_lower = ai_response.lower()
        player_action_lower = player_action.lower()
        
        progress_made = any(
            indicator in ai_response_lower or indicator in player_action_lower
            for indicator in progress_indicators
        )
        
        if progress_made:
            arc_progress_result = self.story_arc_manager.advance_arc_progress(1)
            result.update({
                'arc_progression': True,
                'progress_result': arc_progress_result
            })
            
            # Check if arc completed
            if arc_progress_result.get('arc_completed'):
                result['arc_completed'] = True
                result['completed_arc'] = arc_progress_result['completed_arc']
        
        return result
    
    def _check_story_arc_activation(self) -> Dict[str, Any]:
        """Check if a new story arc should be activated"""
        
        # Don't activate if we already have an active arc
        current_arc = self.story_arc_manager.get_current_arc_context()
        if not current_arc.get('no_active_arc'):
            return {'no_activation': 'arc_already_active'}
        
        # Get context for arc selection
        character = self.game_state_manager.character
        character_level = character.get('level', 1)
        
        story_context = {
            'character_level': character_level,
            'turn_count': self.story_state_manager.turn_count,
            'story_flags': self.story_state_manager.story_flags,
            'themes': self._extract_current_themes()
        }
        
        current_location = self.story_state_manager.current_location
        
        # Select appropriate arc
        selected_arc = self.story_arc_manager.select_arc_for_context(
            character_level, story_context, current_location
        )
        
        if selected_arc:
            activation_result = self.story_arc_manager.activate_arc(selected_arc)
            return activation_result
        
        return {'no_activation': 'no_suitable_arc'}
    
    def _extract_current_themes(self) -> List[str]:
        """Extract current story themes from recent events"""
        
        themes = []
        recent_events = self.story_state_manager.recent_events
        
        # Analyze recent events for themes
        theme_keywords = {
            'corruption': ['corruption', 'blight', 'dark', 'evil'],
            'restoration': ['restore', 'heal', 'fix', 'repair'],
            'exploration': ['discover', 'explore', 'find', 'search'],
            'conflict': ['fight', 'battle', 'enemy', 'hostile'],
            'mystery': ['mystery', 'unknown', 'secret', 'hidden']
        }
        
        for theme, keywords in theme_keywords.items():
            if any(any(keyword in event.lower() for keyword in keywords) 
                  for event in recent_events):
                themes.append(theme)
        
        return themes
    
    def generate_enhanced_context_for_ai(self) -> str:
        """Generate comprehensive context for AI including all systems"""
        
        context_parts = []
        
        # 1. Story Arc Context
        arc_context = self.story_arc_manager.get_current_arc_context()
        if not arc_context.get('no_active_arc'):
            context_parts.append("=== ACTIVE STORY ARC ===")
            active_arc = arc_context['active_arc']
            context_parts.extend([
                f"Arc: {active_arc['name']} ({active_arc['type']})",
                f"Phase: {arc_context['phase_guidance']}",
                f"Progress: {active_arc['progress']}/{active_arc['estimated_turns']} turns",
                f"Key Elements: {', '.join(active_arc['key_elements'])}"
            ])
            
            if arc_context.get('climax_direction'):
                context_parts.append(f"Approaching Climax: {arc_context['climax_direction']}")
            
            context_parts.append("")
        
        # 2. Location Context with Debug Info
        current_location_context = self.story_state_manager.get_current_context()
        location = current_location_context['location']
        
        context_parts.append("=== LOCATION CONTEXT ===")
        context_parts.extend([
            f"Current Location: {location['name']} ({location['type']})",
            f"Description: {location['description']}",
            f"Safe Zone: {'Yes' if location['safe_zone'] else 'No'}"
        ])
        
        if current_location_context['connected_locations']:
            connected_names = [loc['name'] for loc in current_location_context['connected_locations']]
            context_parts.append(f"Connected Locations: {', '.join(connected_names)}")
        
        if current_location_context['npcs_present']:
            npc_names = [npc['name'] for npc in current_location_context['npcs_present']]
            context_parts.append(f"NPCs Present: {', '.join(npc_names)}")
        
        context_parts.append("")
        
        # 3. Game State Context
        game_state = self.game_state_manager.get_current_state()
        character = game_state['character']
        
        context_parts.append("=== CHARACTER STATUS ===")
        context_parts.extend([
            f"Name: {character['name']} (Level {character['level']} {character['class']})",
            f"HP: {character['resources']['hp']}/{character['resources']['max_hp']}",
            f"Energy: {character['resources']['energy']}/{character['resources']['max_energy']}",
            f"XP: {character['xp']}"
        ])
        
        # 4. Pending Issues
        if self.pending_location_change:
            context_parts.append("=== PENDING LOCATION TRANSITION ===")
            pending = self.pending_location_change
            context_parts.extend([
                f"Target: {pending['target_location']}",
                f"Requires: {pending['suggested_roll']['skill_used']} check (difficulty: {pending['suggested_roll']['difficulty']})",
                f"Reason: {pending['reason']}"
            ])
            context_parts.append("")
        
        # 5. Debug Information (if enabled)
        if self.debug_mode:
            debug_report = self.location_debugger.get_transition_debug_report()
            if not debug_report.get('no_transitions'):
                context_parts.append("=== DEBUG INFO ===")
                context_parts.append(f"Location Transition Success Rate: {debug_report['success_rate']:.1%}")
                if debug_report['common_issues']:
                    context_parts.append(f"Common Issues: {', '.join(debug_report['common_issues'])}")
                context_parts.append("")
        
        return "\n".join(context_parts)
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of all integrated systems"""
        
        return {
            'integration_active': self.integration_active,
            'debug_mode': self.debug_mode,
            'systems_status': {
                'story_arc_manager': {
                    'active_arc': self.story_arc_manager.active_arc.name if self.story_arc_manager.active_arc else None,
                    'completed_arcs': len(self.story_arc_manager.completed_arcs),
                    'available_arcs': len(self.story_arc_manager.available_arcs)
                },
                'location_debugger': {
                    'transitions_logged': len(self.location_debugger.transition_history),
                    'debug_report': self.location_debugger.get_transition_debug_report()
                },
                'option_generator': {
                    'recent_actions_tracked': len(self.option_generator.recent_actions)
                }
            },
            'current_state': {
                'location': self.story_state_manager.current_location,
                'turn_count': self.story_state_manager.turn_count,
                'character_level': self.game_state_manager.character.get('level', 1)
            },
            'pending_issues': {
                'location_change': self.pending_location_change is not None
            }
        }
    
    def force_story_progression(self, reason: str = "manual_override") -> Dict[str, Any]:
        """Force story progression when needed"""
        
        result = {'forced_progression': True, 'reason': reason, 'actions_taken': []}
        
        # 1. Check if we need to activate a story arc
        if self.story_arc_manager.get_current_arc_context().get('no_active_arc'):
            activation_result = self._check_story_arc_activation()
            if activation_result.get('arc_activated'):
                result['actions_taken'].append('activated_story_arc')
                result['new_arc'] = activation_result
        
        # 2. Check if location progression is stuck
        progression_check = self.game_state_manager.should_force_progression()
        if progression_check['should_force']:
            # Suggest location change
            current_location = self.story_state_manager.current_location
            connectivity = self.location_debugger.get_location_connectivity_map()
            
            available_destinations = connectivity['connections'].get(current_location, {}).get('connected_to', [])
            if available_destinations:
                suggested_destination = available_destinations[0]  # Take first available
                
                result['actions_taken'].append('suggested_location_change')
                result['suggested_location'] = suggested_destination
                result['progression_reason'] = progression_check['reason']
        
        # 3. Advance story arc if stalled
        arc_context = self.story_arc_manager.get_current_arc_context()
        if not arc_context.get('no_active_arc'):
            active_arc = arc_context['active_arc']
            if active_arc['progress_ratio'] < 0.1:  # Very little progress
                arc_progress = self.story_arc_manager.advance_arc_progress(2)  # Double progress
                result['actions_taken'].append('advanced_story_arc')
                result['arc_progress'] = arc_progress
        
        return result
    
    def save_integrated_state(self) -> Dict[str, Any]:
        """Save state of all integrated systems"""
        
        return {
            'game_state': json.loads(self.game_state_manager.save_state()),
            'story_state': self.story_state_manager.save_state(),
            'story_arc_state': {
                'active_arc': self.story_arc_manager.active_arc.name if self.story_arc_manager.active_arc else None,
                'arc_progress': self.story_arc_manager.arc_progress,
                'completed_arcs': self.story_arc_manager.completed_arcs,
                'available_arcs': self.story_arc_manager.available_arcs
            },
            'integration_state': {
                'pending_location_change': self.pending_location_change,
                'recent_actions': self.option_generator.recent_actions
            },
            'timestamp': time.time()
        }
    
    def load_integrated_state(self, state_data: Dict[str, Any]):
        """Load state of all integrated systems"""
        
        # Load game state
        if 'game_state' in state_data:
            self.game_state_manager = GameStateManager.load_state(
                json.dumps(state_data['game_state'])
            )
        
        # Load story state
        if 'story_state' in state_data:
            self.story_state_manager.load_state(state_data['story_state'])
        
        # Load story arc state
        if 'story_arc_state' in state_data:
            arc_state = state_data['story_arc_state']
            if arc_state.get('active_arc'):
                # Reactivate arc
                arc = self.story_arc_manager.story_arcs.get(arc_state['active_arc'])
                if arc:
                    self.story_arc_manager.activate_arc(arc)
                    self.story_arc_manager.arc_progress = arc_state.get('arc_progress', 0)
            
            self.story_arc_manager.completed_arcs = arc_state.get('completed_arcs', [])
            self.story_arc_manager.available_arcs = arc_state.get('available_arcs', [])
        
        # Load integration state
        if 'integration_state' in state_data:
            integration_state = state_data['integration_state']
            self.pending_location_change = integration_state.get('pending_location_change')
            self.option_generator.recent_actions = integration_state.get('recent_actions', [])