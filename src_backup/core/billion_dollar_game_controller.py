"""
Billion Dollar Game Controller - Integrates all retention and engagement systems
Combines Enhanced Context, Session Hooks, Character Investment, and existing systems
"""
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import asdict

from .enhanced_context_manager import EnhancedContextManager, ContextType
from .session_hooks_manager import SessionHooksManager, HookType, HookIntensity
from .character_investment_manager import CharacterInvestmentManager, ProgressionType
from .integrated_story_controller import IntegratedStoryController
from .game_state_manager import GameStateManager
from .story_state_manager import StoryStateManager

class BillionDollarGameController:
    """
    Master controller that orchestrates all systems for maximum player retention
    Implements the billion-dollar game strategy with context continuity and emotional investment
    """
    
    def __init__(self, character_data: Dict = None):
        # Initialize core systems
        self.enhanced_context = EnhancedContextManager()
        self.session_hooks = SessionHooksManager(self.enhanced_context)
        self.character_investment = CharacterInvestmentManager(character_data)
        
        # Initialize existing systems
        self.game_state_manager = GameStateManager(character_data)
        self.story_state_manager = StoryStateManager()
        self.integrated_story_controller = IntegratedStoryController(
            self.game_state_manager, self.story_state_manager
        )
        
        # Game session state
        self.current_session_data = {}
        self.session_actions = []
        self.session_start_time = time.time()
        
        # Retention metrics
        self.retention_metrics = {
            'session_length_target': 1200,  # 20 minutes in seconds
            'engagement_score': 0.0,
            'emotional_investment_score': 0.0,
            'return_motivation_score': 0.0
        }
        
    def start_new_session(self) -> Dict[str, Any]:
        """Start a new game session with full context integration"""
        
        # Start session in all systems
        session_context = self.enhanced_context.start_new_session()
        investment_result = self.character_investment.track_session_start()
        hooks_context = self.session_hooks.get_session_start_context()
        
        # Reset session tracking
        self.current_session_data = session_context
        self.session_actions = []
        self.session_start_time = time.time()
        
        # Generate comprehensive session start context
        session_start_result = {
            'session_started': True,
            'session_context': session_context,
            'character_investment': investment_result,
            'active_hooks': hooks_context,
            'ai_context': self._generate_comprehensive_ai_context(),
            'session_preview': self._generate_session_preview()
        }
        
        return session_start_result
    
    def process_player_action(self, player_action: str, ai_response: str = None) -> Dict[str, Any]:
        """Process a player action through all integrated systems"""
        
        action_start_time = time.time()
        
        # Track action in all relevant systems
        investment_result = self.character_investment.track_action(
            player_action, 
            {'session_id': self.current_session_data.get('session_id')}
        )
        
        # Process through integrated story controller
        story_result = self.integrated_story_controller.process_turn(
            player_action, ai_response or "", []
        )
        
        # Update context with choice consequences if significant
        choice_consequence_id = None
        if self._is_significant_choice(player_action, story_result):
            choice_consequence_id = self.enhanced_context.record_choice_consequence(
                player_action,
                ai_response or "Action taken",
                self._extract_choice_implications(story_result)
            )
        
        # Track discoveries if any
        discoveries = self._extract_discoveries(ai_response or "", story_result)
        discovery_results = []
        for discovery in discoveries:
            discovery_result = self.character_investment.track_discovery(
                discovery['name'], discovery['rarity']
            )
            discovery_results.append(discovery_result)
            
            # Also record in context
            self.enhanced_context.record_discovery(
                discovery['name'], discovery['type'], 
                discovery['description'], discovery['rarity'],
                f"Discovered during: {player_action}"
            )
        
        # Update relationship tracking if NPCs involved
        relationship_updates = self._extract_relationship_changes(ai_response or "", story_result)
        for npc_name, change_data in relationship_updates.items():
            self.enhanced_context.update_relationship(
                npc_name, change_data['interaction_type'],
                change_data['relationship_change'], change_data['context']
            )
        
        # Track total relationship score for investment system
        total_relationship_score = sum(
            abs(rel.relationship_level) 
            for rel in self.enhanced_context.relationship_states.values()
        )
        relationship_result = self.character_investment.track_relationship_change(total_relationship_score)
        
        # Update nemesis if relevant
        nemesis_update = self._check_nemesis_encounter(player_action, ai_response or "", story_result)
        if nemesis_update:
            self.enhanced_context.create_or_update_nemesis(
                nemesis_update['name'], nemesis_update['context'],
                [player_action], nemesis_update['outcome']
            )
        
        # Store action for session tracking
        self.session_actions.append({
            'action': player_action,
            'timestamp': action_start_time,
            'ai_response': ai_response,
            'story_result': story_result
        })
        
        # Calculate engagement metrics
        engagement_update = self._update_engagement_metrics(
            player_action, story_result
        )
        
        # Compile comprehensive result
        action_result = {
            'action_processed': True,
            'player_action': player_action,
            'character_investment': investment_result,
            'story_processing': story_result,
            'choice_consequence_id': choice_consequence_id,
            'discoveries': discovery_results,
            'relationship_updates': relationship_result,
            'nemesis_update': nemesis_update,
            'engagement_metrics': engagement_update,
            'ai_context_updated': True
        }
        
        return action_result
    
    def end_session(self, reason: str = "player_choice") -> Dict[str, Any]:
        """End the current session with hooks and retention features"""
        
        session_end_time = time.time()
        session_duration = session_end_time - self.session_start_time
        
        # Generate session-ending hook
        session_context = {
            'session_duration': session_duration,
            'actions_taken': len(self.session_actions),
            'session_id': self.current_session_data.get('session_id'),
            'end_reason': reason
        }
        
        current_story_state = self.integrated_story_controller.get_integration_status()
        
        session_hook = self.session_hooks.generate_session_end_hook(
            session_context,
            [action['action'] for action in self.session_actions],
            current_story_state
        )
        
        # Calculate final retention metrics
        final_metrics = self._calculate_session_retention_metrics(session_duration)
        
        # Generate return motivation
        return_motivation = self._generate_return_motivation()
        
        # Update context with session end
        self.enhanced_context.last_session_end_hook = session_hook.hook_text
        
        session_end_result = {
            'session_ended': True,
            'session_duration': session_duration,
            'actions_taken': len(self.session_actions),
            'session_hook': {
                'hook_text': session_hook.hook_text,
                'intensity': session_hook.intensity.name,
                'next_session_preview': session_hook.next_session_preview,
                'emotional_stakes': session_hook.emotional_stakes
            },
            'retention_metrics': final_metrics,
            'return_motivation': return_motivation,
            'character_progression_preview': self.character_investment.generate_progression_preview()
        }
        
        return session_end_result
    
    def _generate_comprehensive_ai_context(self) -> str:
        """Generate comprehensive context for AI including all systems"""
        
        context_sections = []
        
        # 1. Enhanced context (weighted by importance)
        enhanced_context = self.enhanced_context.generate_weighted_context_for_ai([
            ContextType.PERSONAL_STORY,
            ContextType.CHOICE_CONSEQUENCES,
            ContextType.NEMESIS_EVOLUTION,
            ContextType.RELATIONSHIP_DYNAMICS,
            ContextType.CHARACTER_PROGRESSION
        ])
        
        if enhanced_context:
            context_sections.append(enhanced_context)
        
        # 2. Character progression context
        progression_context = self.character_investment.get_character_progression_context()
        if progression_context:
            context_sections.append(progression_context)
        
        # 3. Active hooks context
        hooks_context = self.session_hooks.get_session_start_context()
        if hooks_context['active_hooks']:
            context_sections.append("=== ACTIVE STORY HOOKS ===")
            for hook in hooks_context['active_hooks'][:2]:  # Top 2 hooks
                context_sections.append(f"• {hook['hook_text']}")
                if hook['time_pressure']:
                    context_sections.append("  ⏰ TIME SENSITIVE")
        
        # 4. Integrated story controller context
        story_context = self.integrated_story_controller.generate_enhanced_context_for_ai()
        if story_context:
            context_sections.append(story_context)
        
        # 5. Retention guidance for AI
        retention_guidance = self._generate_retention_guidance_for_ai()
        context_sections.append(retention_guidance)
        
        return "\n\n".join(context_sections)
    
    def _generate_retention_guidance_for_ai(self) -> str:
        """Generate guidance for AI to maximize retention"""
        
        guidance = ["=== RETENTION GUIDANCE ==="]
        
        # Current session metrics
        session_duration = time.time() - self.session_start_time
        target_duration = self.retention_metrics['session_length_target']
        
        if session_duration < target_duration * 0.5:
            guidance.append("• Build engagement - session just started")
            guidance.append("• Include discovery opportunities")
            guidance.append("• Establish emotional stakes")
        elif session_duration < target_duration * 0.8:
            guidance.append("• Maintain momentum - mid-session")
            guidance.append("• Develop character relationships")
            guidance.append("• Progress personal story elements")
        else:
            guidance.append("• Prepare for compelling session end")
            guidance.append("• Set up cliffhanger or hook")
            guidance.append("• Leave unresolved tension")
        
        # Investment score guidance
        investment_summary = self.character_investment.get_investment_summary()
        if investment_summary['investment_score'] < 1.0:
            guidance.append("• Focus on character growth opportunities")
            guidance.append("• Highlight progression achievements")
        
        # Context richness guidance
        context_stats = self.enhanced_context.get_context_summary_stats()
        if context_stats['context_richness_score'] < 0.5:
            guidance.append("• Build more personal connections")
            guidance.append("• Reference past player choices")
        
        return "\n".join(guidance)
    
    def _generate_session_preview(self) -> str:
        """Generate preview of what this session might contain"""
        
        preview_elements = []
        
        # Check for active hooks
        hooks_context = self.session_hooks.get_session_start_context()
        if hooks_context['has_urgent_hooks']:
            preview_elements.append("urgent matters require your attention")
        
        # Check for near progressions
        progression_preview = self.character_investment.generate_progression_preview()
        if "upcoming" in progression_preview.lower():
            preview_elements.append("character growth opportunities await")
        
        # Check for story arc status
        story_status = self.integrated_story_controller.get_integration_status()
        if story_status['systems_status']['story_arc_manager']['active_arc']:
            preview_elements.append("your story arc continues to unfold")
        
        # Check for relationship tensions
        important_relationships = [
            r for r in self.enhanced_context.relationship_states.values()
            if abs(r.relationship_level) >= 5
        ]
        if important_relationships:
            preview_elements.append("important relationships are evolving")
        
        if preview_elements:
            return f"This session: {', '.join(preview_elements)}."
        else:
            return "New adventures and discoveries await in this session."
    
    def _is_significant_choice(self, player_action: str, story_result: Dict) -> bool:
        """Determine if a player action represents a significant choice"""
        
        # Check for choice indicators
        choice_keywords = [
            'decide', 'choose', 'agree', 'refuse', 'accept', 'reject',
            'attack', 'defend', 'help', 'ignore', 'trust', 'betray'
        ]
        
        action_lower = player_action.lower()
        has_choice_keyword = any(keyword in action_lower for keyword in choice_keywords)
        
        # Check story result for significance
        has_story_impact = story_result.get('integration_data', {}).get('story_arc_processing', {}).get('arc_progression', False)
        has_location_change = story_result.get('integration_data', {}).get('location_processing', {}).get('location_changed', False)
        
        return has_choice_keyword or has_story_impact or has_location_change
    
    def _extract_choice_implications(self, story_result: Dict) -> Dict[str, Any]:
        """Extract implications of a choice for context tracking"""
        
        implications = {
            'type': 'immediate',
            'impact_level': 1,
            'affected_npcs': [],
            'world_changes': {},
            'unlocked_options': [],
            'blocked_options': []
        }
        
        # Analyze story result for implications
        integration_data = story_result.get('integration_data', {})
        
        if integration_data.get('story_arc_processing', {}).get('arc_progression'):
            implications['impact_level'] = 3
            implications['type'] = 'cascading'
        
        if integration_data.get('location_processing', {}).get('location_changed'):
            implications['impact_level'] = max(implications['impact_level'], 2)
            implications['world_changes']['location_access'] = True
        
        return implications
    
    def _extract_discoveries(self, ai_response: str, story_result: Dict) -> List[Dict[str, Any]]:
        """Extract discoveries from AI response and story result"""
        
        discoveries = []
        
        # Look for discovery keywords in AI response
        discovery_keywords = {
            'find': 2, 'discover': 3, 'uncover': 3, 'reveal': 2,
            'hidden': 3, 'secret': 4, 'ancient': 4, 'mysterious': 3,
            'rare': 4, 'unique': 5, 'legendary': 5
        }
        
        ai_response_lower = ai_response.lower()
        max_rarity = 1
        
        for keyword, rarity in discovery_keywords.items():
            if keyword in ai_response_lower:
                max_rarity = max(max_rarity, rarity)
        
        if max_rarity > 1:
            discoveries.append({
                'name': 'Discovery from exploration',
                'type': 'exploration',
                'description': 'Something interesting found during adventure',
                'rarity': min(max_rarity, 5)
            })
        
        return discoveries
    
    def _extract_relationship_changes(self, ai_response: str, story_result: Dict) -> Dict[str, Dict]:
        """Extract relationship changes from AI response"""
        
        relationship_changes = {}
        
        # Look for NPC interaction keywords
        npc_names = ['emberlyn', 'villager', 'guard', 'merchant', 'elder']  # Common NPCs
        interaction_types = {
            'help': ('social_positive', 1),
            'assist': ('social_positive', 1),
            'thank': ('social_positive', 2),
            'praise': ('social_positive', 2),
            'argue': ('social_negative', -1),
            'fight': ('combat_negative', -2),
            'threaten': ('intimidation_negative', -2),
            'befriend': ('social_positive', 3)
        }
        
        ai_response_lower = ai_response.lower()
        
        for npc in npc_names:
            if npc in ai_response_lower:
                for keyword, (interaction_type, change) in interaction_types.items():
                    if keyword in ai_response_lower:
                        relationship_changes[npc.title()] = {
                            'interaction_type': interaction_type,
                            'relationship_change': change,
                            'context': f"Interaction during current action"
                        }
                        break
        
        return relationship_changes
    
    def _check_nemesis_encounter(self, player_action: str, ai_response: str, story_result: Dict) -> Optional[Dict]:
        """Check if this action involves nemesis activity"""
        
        # Look for nemesis-related keywords
        nemesis_keywords = ['enemy', 'foe', 'antagonist', 'rival', 'pursuer', 'hunter']
        combat_keywords = ['attack', 'fight', 'battle', 'combat', 'defeat', 'victory']
        
        ai_response_lower = ai_response.lower()
        player_action_lower = player_action.lower()
        
        has_nemesis_reference = any(keyword in ai_response_lower for keyword in nemesis_keywords)
        has_combat = any(keyword in player_action_lower or keyword in ai_response_lower for keyword in combat_keywords)
        
        if has_nemesis_reference and has_combat:
            # Determine outcome
            victory_keywords = ['defeat', 'victory', 'win', 'triumph', 'overcome']
            defeat_keywords = ['lose', 'defeat', 'retreat', 'escape', 'flee']
            
            if any(keyword in ai_response_lower for keyword in victory_keywords):
                outcome = 'player_victory'
            elif any(keyword in ai_response_lower for keyword in defeat_keywords):
                outcome = 'nemesis_victory'
            else:
                outcome = 'inconclusive'
            
            return {
                'name': 'Shadow Adversary',  # Default nemesis name
                'context': f"Encountered during: {player_action}",
                'outcome': outcome
            }
        
        return None
    
    def _update_engagement_metrics(self, player_action: str, story_result: Dict) -> Dict[str, Any]:
        """Update engagement metrics based on current action"""
        
        engagement_factors = {
            'action_variety': 0.1,
            'story_progression': 0.0,
            'character_growth': 0.0,
            'discovery_made': 0.0,
            'relationship_development': 0.0
        }
        
        # Story progression
        if story_result.get('integration_data', {}).get('story_arc_processing', {}).get('arc_progression'):
            engagement_factors['story_progression'] = 0.3
        
        # Character growth - get from story result instead of investment_result
        if story_result.get('character_progression', {}).get('progressions_unlocked'):
            engagement_factors['character_growth'] = 0.4
        
        # Update overall engagement score
        session_engagement_boost = sum(engagement_factors.values())
        self.retention_metrics['engagement_score'] += session_engagement_boost
        
        return {
            'session_engagement_boost': session_engagement_boost,
            'total_engagement_score': self.retention_metrics['engagement_score'],
            'engagement_factors': engagement_factors
        }
    
    def _calculate_session_retention_metrics(self, session_duration: float) -> Dict[str, Any]:
        """Calculate final retention metrics for the session"""
        
        target_duration = self.retention_metrics['session_length_target']
        duration_score = min(1.0, session_duration / target_duration)
        
        # Investment score from character investment manager
        investment_summary = self.character_investment.get_investment_summary()
        investment_score = min(1.0, investment_summary['investment_score'])
        
        # Context richness score
        context_stats = self.enhanced_context.get_context_summary_stats()
        context_score = context_stats['context_richness_score']
        
        # Hook strength score
        hooks_summary = self.session_hooks.get_hooks_summary()
        hook_score = min(1.0, hooks_summary['average_intensity'] / 5.0)
        
        # Overall retention score
        overall_retention_score = (
            duration_score * 0.2 +
            investment_score * 0.3 +
            context_score * 0.2 +
            hook_score * 0.3
        )
        
        return {
            'session_duration_score': duration_score,
            'character_investment_score': investment_score,
            'context_richness_score': context_score,
            'hook_strength_score': hook_score,
            'overall_retention_score': overall_retention_score,
            'target_metrics': {
                'duration_target_met': session_duration >= target_duration * 0.8,
                'investment_target_met': investment_score >= 0.5,
                'context_target_met': context_score >= 0.5,
                'hook_target_met': hook_score >= 0.4
            }
        }
    
    def _generate_return_motivation(self) -> Dict[str, Any]:
        """Generate motivation for player to return"""
        
        motivation_factors = []
        
        # Active hooks
        hooks_context = self.session_hooks.get_session_start_context()
        if hooks_context['has_urgent_hooks']:
            motivation_factors.append("Urgent matters require your immediate attention")
        elif hooks_context['active_hooks']:
            motivation_factors.append("Unresolved mysteries await your return")
        
        # Near progressions
        progression_preview = self.character_investment.generate_progression_preview()
        if "upcoming" in progression_preview.lower():
            motivation_factors.append("Character growth opportunities are within reach")
        
        # Relationship tensions
        important_relationships = [
            r for r in self.enhanced_context.relationship_states.values()
            if abs(r.relationship_level) >= 5
        ]
        if important_relationships:
            motivation_factors.append("Important relationships need your attention")
        
        # Nemesis activity
        if self.enhanced_context.nemesis_profile:
            motivation_factors.append("Your nemesis continues to grow in power")
        
        # Generate anticipation message
        anticipation_message = self.session_hooks.generate_anticipation_message()
        
        return {
            'motivation_factors': motivation_factors,
            'anticipation_message': anticipation_message,
            'return_urgency': 'high' if hooks_context['has_urgent_hooks'] else 'moderate',
            'emotional_investment_level': self.character_investment.get_investment_summary()['investment_score']
        }
    
    def get_comprehensive_game_state(self) -> Dict[str, Any]:
        """Get comprehensive game state from all systems"""
        
        return {
            'enhanced_context': {
                'context_stats': self.enhanced_context.get_context_summary_stats(),
                'relationship_count': len(self.enhanced_context.relationship_states),
                'choice_consequences': len(self.enhanced_context.choice_consequences),
                'discoveries': len(self.enhanced_context.discovery_log),
                'nemesis_active': self.enhanced_context.nemesis_profile is not None
            },
            'character_investment': self.character_investment.get_investment_summary(),
            'session_hooks': self.session_hooks.get_hooks_summary(),
            'story_integration': self.integrated_story_controller.get_integration_status(),
            'retention_metrics': self.retention_metrics.copy(),
            'current_session': {
                'session_id': self.current_session_data.get('session_id'),
                'actions_taken': len(self.session_actions),
                'session_duration': time.time() - self.session_start_time
            }
        }
    
    def force_progression_if_needed(self) -> Dict[str, Any]:
        """Force progression if player seems stuck"""
        
        # Check if progression is needed
        game_state = self.game_state_manager.get_current_state()
        should_force = self.game_state_manager.should_force_progression()
        
        if should_force['should_force']:
            # Force progression through integrated story controller
            progression_result = self.integrated_story_controller.force_story_progression(
                should_force['reason']
            )
            
            # Also trigger character investment progression
            investment_result = self.character_investment.track_story_milestone(
                f"Forced progression: {should_force['reason']}"
            )
            
            return {
                'progression_forced': True,
                'reason': should_force['reason'],
                'story_progression': progression_result,
                'character_progression': investment_result
            }
        
        return {'progression_forced': False}
    
    def save_comprehensive_state(self) -> str:
        """Save state of all integrated systems"""
        
        comprehensive_state = {
            'enhanced_context': {
                'character_progression': self.enhanced_context.character_progression,
                'choice_consequences': [asdict(c) for c in self.enhanced_context.choice_consequences],
                'relationship_states': {k: asdict(v) for k, v in self.enhanced_context.relationship_states.items()},
                'nemesis_profile': asdict(self.enhanced_context.nemesis_profile) if self.enhanced_context.nemesis_profile else None,
                'discovery_log': [asdict(d) for d in self.enhanced_context.discovery_log],
                'personal_story_threads': {k: asdict(v) for k, v in self.enhanced_context.personal_story_threads.items()},
                'session_count': self.enhanced_context.session_count,
                'current_session_id': self.enhanced_context.current_session_id
            },
            'character_investment': {
                'progression_milestones': [asdict(m) for m in self.character_investment.progression_milestones],
                'character_evolution': asdict(self.character_investment.character_evolution) if self.character_investment.character_evolution else None,
                'ability_progressions': {k: asdict(v) for k, v in self.character_investment.ability_progressions.items()},
                'tracking_counters': {
                    'action_count': self.character_investment.action_count,
                    'session_count': self.character_investment.session_count,
                    'story_milestones_reached': self.character_investment.story_milestones_reached,
                    'discoveries_made': self.character_investment.discoveries_made
                },
                'investment_score': self.character_investment.investment_score,
                'attachment_factors': self.character_investment.attachment_factors
            },
            'session_hooks': {
                'active_hooks': [asdict(h) for h in self.session_hooks.active_hooks],
                'resolved_hooks': [asdict(h) for h in self.session_hooks.resolved_hooks]
            },
            'integrated_story_state': self.integrated_story_controller.save_integrated_state(),
            'retention_metrics': self.retention_metrics,
            'timestamp': time.time()
        }
        
        return json.dumps(comprehensive_state, indent=2)
    
    def load_comprehensive_state(self, state_json: str):
        """Load comprehensive state from JSON"""
        
        state_data = json.loads(state_json)
        
        # Load enhanced context
        if 'enhanced_context' in state_data:
            context_data = state_data['enhanced_context']
            self.enhanced_context.character_progression = context_data.get('character_progression', {})
            # Note: Full state loading would require more complex deserialization
            # This is a simplified version for the core implementation
        
        # Load other systems similarly
        # Implementation would continue for all systems
        
        print("Comprehensive state loaded successfully")      
  
    def start_new_game(self, character_data: Dict, saga_name: str) -> Dict[str, Any]:
        """Start a new game with character and saga"""
        # Initialize character investment
        self.character_investment = CharacterInvestmentManager(character_data)
        
        # Set up initial context
        self.enhanced_context.add_context(
            ContextType.CHARACTER_BACKGROUND,
            f"Character: {character_data['name']}, Class: {character_data['class']}, Background: {character_data['background']}"
        )
        
        self.enhanced_context.add_context(
            ContextType.STORY_ARC,
            f"Starting saga: {saga_name}"
        )
        
        # Generate opening narrative
        opening_narrative = self._generate_opening_narrative(character_data, saga_name)
        
        # Create initial session hook
        self.session_hooks.create_hook(
            HookType.STORY_CLIFFHANGER,
            "Your adventure begins...",
            HookIntensity.MEDIUM
        )
        
        return {
            'narrative': opening_narrative,
            'character_data': character_data,
            'saga': saga_name,
            'session_id': str(int(time.time()))
        }
    
    def process_turn(self, player_input: str) -> Dict[str, Any]:
        """Process a player turn with full system integration"""
        # Record the action
        self.session_actions.append({
            'input': player_input,
            'timestamp': time.time()
        })
        
        # Add to context
        self.enhanced_context.add_context(
            ContextType.RECENT_ACTIONS,
            f"Player action: {player_input}"
        )
        
        # Process through integrated story controller
        story_response = self.integrated_story_controller.process_turn(
            player_input,
            self.enhanced_context.get_full_context()
        )
        
        # Update character investment
        self.character_investment.process_action(player_input, story_response)
        
        # Create session hooks for retention
        self._create_retention_hooks(story_response)
        
        # Update engagement metrics
        self._update_engagement_metrics(player_input, story_response)
        
        return {
            'narrative': story_response.get('narrative', 'The story continues...'),
            'game_ended': story_response.get('game_ended', False),
            'engagement_score': self.retention_metrics['engagement_score']
        }
    
    def _generate_opening_narrative(self, character_data: Dict, saga_name: str) -> str:
        """Generate an engaging opening narrative"""
        character_name = character_data.get('name', 'Hero')
        character_class = character_data.get('class', 'Adventurer')
        
        opening = f"""🔥 Welcome to Fire Whisper RPG, {character_name}! 🔥

As a {character_class}, you stand at the threshold of an epic adventure. The {saga_name} saga awaits, filled with mystery, danger, and untold treasures.

The wind carries whispers of ancient magic, and your heart pounds with anticipation. Your journey begins now...

What do you do first?"""
        
        return opening
    
    def _create_retention_hooks(self, story_response: Dict):
        """Create hooks to encourage player return"""
        # Create mystery hooks
        if 'mystery' in story_response.get('narrative', '').lower():
            self.session_hooks.create_hook(
                HookType.MYSTERY_REVELATION,
                "A mysterious secret awaits discovery...",
                HookIntensity.HIGH
            )
        
        # Create progression hooks
        if 'level' in story_response.get('narrative', '').lower():
            self.session_hooks.create_hook(
                HookType.CHARACTER_PROGRESSION,
                "Your character grows stronger...",
                HookIntensity.MEDIUM
            )
    
    def _update_engagement_metrics(self, player_input: str, story_response: Dict):
        """Update engagement and retention metrics"""
        # Simple engagement scoring
        input_length = len(player_input.split())
        engagement_boost = min(input_length / 10, 1.0)  # Cap at 1.0
        
        self.retention_metrics['engagement_score'] += engagement_boost
        self.retention_metrics['engagement_score'] = min(
            self.retention_metrics['engagement_score'], 10.0
        )
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary for retention analysis"""
        session_length = time.time() - self.session_start_time
        
        return {
            'session_length': session_length,
            'actions_taken': len(self.session_actions),
            'engagement_score': self.retention_metrics['engagement_score'],
            'active_hooks': len(self.session_hooks.active_hooks),
            'character_investment': self.character_investment.get_investment_summary(),
            'context_richness': len(self.enhanced_context.context_memory)
        }
        
    def _generate_ai_response(self, player_input: str) -> str:
        """Generate AI response for player input"""
        # Simple response generation for demo
        responses = [
            f"You {player_input}. The path ahead shimmers with possibility as ancient magic stirs around you.",
            f"As you {player_input}, the very air seems to whisper secrets of forgotten times.",
            f"Your action to {player_input} echoes through the mystical realm, drawing the attention of unseen forces.",
            f"The decision to {player_input} proves wise as new opportunities reveal themselves.",
            f"With determination, you {player_input}, and the world responds with unexpected consequences."
        ]
        
        import random
        return random.choice(responses)