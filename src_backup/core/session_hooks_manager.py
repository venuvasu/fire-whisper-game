"""
Session Hooks Manager - Creates compelling reasons to return
Implements cliffhangers, anticipation, and "what happens next" psychology
"""
import json
import time
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class HookType(Enum):
    CLIFFHANGER = "cliffhanger"
    MYSTERY_DEEPENS = "mystery_deepens"
    CONSEQUENCE_PENDING = "consequence_pending"
    RELATIONSHIP_TENSION = "relationship_tension"
    POWER_GROWTH = "power_growth"
    NEMESIS_ACTIVITY = "nemesis_activity"
    DISCOVERY_TEASER = "discovery_teaser"
    WORLD_EVENT = "world_event"

class HookIntensity(Enum):
    SUBTLE = 1
    MODERATE = 2
    STRONG = 3
    URGENT = 4
    CRITICAL = 5

@dataclass
class SessionHook:
    hook_id: str
    hook_type: HookType
    intensity: HookIntensity
    hook_text: str
    setup_context: str
    resolution_conditions: List[str]
    time_pressure: bool
    emotional_stakes: str
    next_session_preview: str
    created_timestamp: float
    expires_after_sessions: int
    resolved: bool = False

@dataclass
class TeaserEvent:
    event_id: str
    event_type: str
    teaser_text: str
    full_event_conditions: List[str]
    emotional_impact_level: int
    connected_npcs: List[str]
    world_implications: Dict[str, Any]
    timestamp: float

class SessionHooksManager:
    """Manages session-ending hooks and return motivation"""
    
    def __init__(self, enhanced_context_manager=None):
        self.enhanced_context = enhanced_context_manager
        self.active_hooks: List[SessionHook] = []
        self.resolved_hooks: List[SessionHook] = []
        self.teaser_events: List[TeaserEvent] = []
        
        # Hook generation templates
        self.hook_templates = {
            HookType.CLIFFHANGER: [
                "As you {action}, you suddenly hear {sound} from {direction}...",
                "Just as {event} happens, everything goes {state}...",
                "The {object} begins to {action}, and you realize {revelation}...",
                "A voice calls out '{message}' but when you turn, {mystery}..."
            ],
            HookType.MYSTERY_DEEPENS: [
                "You notice {clue} that doesn't make sense with what you know...",
                "The {person} gives you a look that suggests {implication}...",
                "Something about {situation} reminds you of {memory}, but why?",
                "You find {evidence} that contradicts {previous_belief}..."
            ],
            HookType.CONSEQUENCE_PENDING: [
                "Your choice to {past_action} has set something in motion...",
                "Word of your {deed} is spreading, and reactions are coming...",
                "The {affected_party} hasn't forgotten what you did...",
                "Your actions have consequences that are about to unfold..."
            ],
            HookType.RELATIONSHIP_TENSION: [
                "{npc_name} looks at you with {emotion} in their eyes...",
                "The tension between you and {npc_name} is reaching a breaking point...",
                "{npc_name} seems to be hiding something important from you...",
                "Your relationship with {npc_name} is about to change forever..."
            ],
            HookType.POWER_GROWTH: [
                "You feel a new power awakening within you...",
                "The {ability} you've been developing is almost ready...",
                "Something has changed in your connection to {power_source}...",
                "You're on the verge of a breakthrough in {skill_area}..."
            ],
            HookType.NEMESIS_ACTIVITY: [
                "Signs suggest {nemesis_name} is planning something...",
                "You hear rumors that {nemesis_name} has been asking about you...",
                "The {evidence} suggests {nemesis_name} was here recently...",
                "{nemesis_name}'s influence is growing stronger in this area..."
            ],
            HookType.DISCOVERY_TEASER: [
                "You glimpse something {adjective} just beyond your reach...",
                "There's definitely more to {location} than meets the eye...",
                "The {object} seems to be pointing toward {direction}...",
                "You have the feeling you're close to discovering something important..."
            ],
            HookType.WORLD_EVENT: [
                "Strange events are occurring across the land...",
                "The {phenomenon} is affecting more than just this area...",
                "People are talking about {event} happening elsewhere...",
                "The world itself seems to be changing in response to {catalyst}..."
            ]
        }
        
        # Preview templates for next session
        self.preview_templates = [
            "When you return, {preview_event}...",
            "Next time: {preview_event}",
            "Your next adventure: {preview_event}",
            "Coming up: {preview_event}",
            "The story continues with {preview_event}..."
        ]
        
    def generate_session_end_hook(self, session_context: Dict[str, Any], 
                                 player_actions: List[str],
                                 current_story_state: Dict[str, Any]) -> SessionHook:
        """Generate a compelling session-ending hook"""
        
        # Analyze session for hook opportunities
        hook_opportunities = self._analyze_hook_opportunities(
            session_context, player_actions, current_story_state
        )
        
        # Select best hook type based on context
        selected_hook_type = self._select_optimal_hook_type(hook_opportunities)
        
        # Generate the hook
        hook = self._create_hook(selected_hook_type, session_context, 
                               hook_opportunities, current_story_state)
        
        self.active_hooks.append(hook)
        return hook
    
    def _analyze_hook_opportunities(self, session_context: Dict[str, Any],
                                  player_actions: List[str],
                                  story_state: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the session for hook opportunities"""
        opportunities = {
            'unresolved_tensions': [],
            'pending_consequences': [],
            'relationship_changes': [],
            'mystery_elements': [],
            'power_developments': [],
            'nemesis_potential': [],
            'discovery_hints': [],
            'world_changes': []
        }
        
        # Analyze player actions for consequences
        action_keywords = {
            'conflict': ['attack', 'fight', 'confront', 'challenge'],
            'social': ['persuade', 'deceive', 'befriend', 'threaten'],
            'exploration': ['search', 'investigate', 'explore', 'discover'],
            'magic': ['cast', 'enchant', 'ritual', 'spell']
        }
        
        for action in player_actions:
            action_lower = action.lower()
            for category, keywords in action_keywords.items():
                if any(keyword in action_lower for keyword in keywords):
                    opportunities['pending_consequences'].append({
                        'action': action,
                        'category': category,
                        'potential_impact': 'moderate'
                    })
        
        # Check for relationship tensions
        if self.enhanced_context and self.enhanced_context.relationship_states:
            for npc_name, relationship in self.enhanced_context.relationship_states.items():
                if abs(relationship.relationship_level) >= 3:  # Significant relationship
                    opportunities['relationship_changes'].append({
                        'npc': npc_name,
                        'level': relationship.relationship_level,
                        'type': relationship.relationship_type
                    })
        
        # Check for nemesis activity
        if (self.enhanced_context and self.enhanced_context.nemesis_profile and 
            self.enhanced_context.nemesis_profile.evolution_stage > 1):
            opportunities['nemesis_potential'].append({
                'name': self.enhanced_context.nemesis_profile.name,
                'power_level': self.enhanced_context.nemesis_profile.power_level,
                'last_encounter': len(self.enhanced_context.nemesis_profile.failed_encounters) + 
                                len(self.enhanced_context.nemesis_profile.successful_encounters)
            })
        
        # Check for mystery elements
        if story_state.get('unresolved_mysteries'):
            opportunities['mystery_elements'] = story_state['unresolved_mysteries']
        
        return opportunities
    
    def _select_optimal_hook_type(self, opportunities: Dict[str, Any]) -> HookType:
        """Select the best hook type based on available opportunities"""
        
        # Weight different hook types based on available content
        hook_weights = {}
        
        if opportunities['pending_consequences']:
            hook_weights[HookType.CONSEQUENCE_PENDING] = len(opportunities['pending_consequences']) * 2
        
        if opportunities['relationship_changes']:
            hook_weights[HookType.RELATIONSHIP_TENSION] = len(opportunities['relationship_changes']) * 1.5
        
        if opportunities['nemesis_potential']:
            hook_weights[HookType.NEMESIS_ACTIVITY] = 3  # High priority
        
        if opportunities['mystery_elements']:
            hook_weights[HookType.MYSTERY_DEEPENS] = len(opportunities['mystery_elements']) * 1.5
        
        if opportunities['discovery_hints']:
            hook_weights[HookType.DISCOVERY_TEASER] = len(opportunities['discovery_hints'])
        
        # Always possible hooks
        hook_weights[HookType.CLIFFHANGER] = 1
        hook_weights[HookType.WORLD_EVENT] = 1
        
        # Select weighted random hook type
        if hook_weights:
            total_weight = sum(hook_weights.values())
            random_value = random.uniform(0, total_weight)
            
            current_weight = 0
            for hook_type, weight in hook_weights.items():
                current_weight += weight
                if random_value <= current_weight:
                    return hook_type
        
        # Fallback
        return HookType.CLIFFHANGER
    
    def _create_hook(self, hook_type: HookType, session_context: Dict[str, Any],
                    opportunities: Dict[str, Any], story_state: Dict[str, Any]) -> SessionHook:
        """Create a specific hook based on type and context"""
        
        hook_id = f"hook_{int(time.time())}_{len(self.active_hooks)}"
        
        # Generate hook text based on type
        hook_text = self._generate_hook_text(hook_type, opportunities, story_state)
        
        # Determine intensity
        intensity = self._calculate_hook_intensity(hook_type, opportunities)
        
        # Generate next session preview
        preview = self._generate_session_preview(hook_type, opportunities)
        
        # Set resolution conditions
        resolution_conditions = self._generate_resolution_conditions(hook_type, opportunities)
        
        hook = SessionHook(
            hook_id=hook_id,
            hook_type=hook_type,
            intensity=intensity,
            hook_text=hook_text,
            setup_context=json.dumps(session_context),
            resolution_conditions=resolution_conditions,
            time_pressure=hook_type in [HookType.CONSEQUENCE_PENDING, HookType.NEMESIS_ACTIVITY],
            emotional_stakes=self._generate_emotional_stakes(hook_type, opportunities),
            next_session_preview=preview,
            created_timestamp=time.time(),
            expires_after_sessions=3 if intensity.value <= 2 else 5
        )
        
        return hook
    
    def _generate_hook_text(self, hook_type: HookType, opportunities: Dict[str, Any],
                           story_state: Dict[str, Any]) -> str:
        """Generate the actual hook text"""
        
        templates = self.hook_templates.get(hook_type, ["Something interesting is about to happen..."])
        base_template = random.choice(templates)
        
        # Fill in template based on hook type and context
        if hook_type == HookType.CONSEQUENCE_PENDING and opportunities['pending_consequences']:
            consequence = random.choice(opportunities['pending_consequences'])
            return base_template.format(
                past_action=consequence['action'],
                deed=consequence['action'],
                affected_party="those affected"
            )
        
        elif hook_type == HookType.RELATIONSHIP_TENSION and opportunities['relationship_changes']:
            relationship = random.choice(opportunities['relationship_changes'])
            emotion = "suspicion" if relationship['level'] < 0 else "expectation"
            return base_template.format(
                npc_name=relationship['npc'],
                emotion=emotion
            )
        
        elif hook_type == HookType.NEMESIS_ACTIVITY and opportunities['nemesis_potential']:
            nemesis = opportunities['nemesis_potential'][0]
            return base_template.format(
                nemesis_name=nemesis['name'],
                evidence="strange signs"
            )
        
        elif hook_type == HookType.MYSTERY_DEEPENS:
            return base_template.format(
                clue="something unusual",
                person="someone nearby",
                implication="they know more than they're saying",
                situation="this place",
                memory="something from your past",
                evidence="a detail",
                previous_belief="what you thought you knew"
            )
        
        elif hook_type == HookType.CLIFFHANGER:
            return base_template.format(
                action="take a step forward",
                sound="a strange noise",
                direction="behind you",
                event="you think you understand",
                state="silent",
                object="air around you",
                revelation="this is just the beginning",
                message="Wait!",
                mystery="no one is there"
            )
        
        # Generic fallback
        return "Something significant is about to unfold..."
    
    def _calculate_hook_intensity(self, hook_type: HookType, 
                                opportunities: Dict[str, Any]) -> HookIntensity:
        """Calculate the intensity of the hook"""
        
        base_intensity = {
            HookType.CLIFFHANGER: HookIntensity.MODERATE,
            HookType.MYSTERY_DEEPENS: HookIntensity.SUBTLE,
            HookType.CONSEQUENCE_PENDING: HookIntensity.STRONG,
            HookType.RELATIONSHIP_TENSION: HookIntensity.MODERATE,
            HookType.POWER_GROWTH: HookIntensity.MODERATE,
            HookType.NEMESIS_ACTIVITY: HookIntensity.STRONG,
            HookType.DISCOVERY_TEASER: HookIntensity.SUBTLE,
            HookType.WORLD_EVENT: HookIntensity.MODERATE
        }
        
        intensity = base_intensity.get(hook_type, HookIntensity.MODERATE)
        
        # Modify based on context
        if hook_type == HookType.NEMESIS_ACTIVITY and opportunities['nemesis_potential']:
            nemesis = opportunities['nemesis_potential'][0]
            if nemesis['power_level'] >= 5:
                intensity = HookIntensity.CRITICAL
        
        if hook_type == HookType.CONSEQUENCE_PENDING:
            high_impact_consequences = [c for c in opportunities['pending_consequences'] 
                                      if c.get('potential_impact') == 'high']
            if high_impact_consequences:
                intensity = HookIntensity.URGENT
        
        return intensity
    
    def _generate_session_preview(self, hook_type: HookType, 
                                opportunities: Dict[str, Any]) -> str:
        """Generate a preview of what's coming next session"""
        
        preview_events = {
            HookType.CLIFFHANGER: "the mystery will be revealed",
            HookType.MYSTERY_DEEPENS: "you'll uncover more clues",
            HookType.CONSEQUENCE_PENDING: "the consequences of your actions unfold",
            HookType.RELATIONSHIP_TENSION: "a crucial conversation awaits",
            HookType.POWER_GROWTH: "your abilities will be tested",
            HookType.NEMESIS_ACTIVITY: "a confrontation looms",
            HookType.DISCOVERY_TEASER: "a significant discovery awaits",
            HookType.WORLD_EVENT: "larger forces come into play"
        }
        
        base_preview = preview_events.get(hook_type, "your adventure continues")
        template = random.choice(self.preview_templates)
        
        return template.format(preview_event=base_preview)
    
    def _generate_resolution_conditions(self, hook_type: HookType,
                                      opportunities: Dict[str, Any]) -> List[str]:
        """Generate conditions for resolving the hook"""
        
        base_conditions = {
            HookType.CLIFFHANGER: ["investigate_source", "take_action"],
            HookType.MYSTERY_DEEPENS: ["gather_more_clues", "confront_source"],
            HookType.CONSEQUENCE_PENDING: ["face_consequences", "take_preventive_action"],
            HookType.RELATIONSHIP_TENSION: ["have_conversation", "resolve_conflict"],
            HookType.POWER_GROWTH: ["practice_ability", "seek_training"],
            HookType.NEMESIS_ACTIVITY: ["prepare_for_encounter", "investigate_activity"],
            HookType.DISCOVERY_TEASER: ["explore_further", "solve_puzzle"],
            HookType.WORLD_EVENT: ["investigate_event", "choose_involvement_level"]
        }
        
        return base_conditions.get(hook_type, ["continue_adventure"])
    
    def _generate_emotional_stakes(self, hook_type: HookType,
                                 opportunities: Dict[str, Any]) -> str:
        """Generate emotional stakes for the hook"""
        
        stakes = {
            HookType.CLIFFHANGER: "Your safety and understanding hang in the balance",
            HookType.MYSTERY_DEEPENS: "The truth you seek may change everything",
            HookType.CONSEQUENCE_PENDING: "Your past choices will define your future",
            HookType.RELATIONSHIP_TENSION: "Important relationships are at stake",
            HookType.POWER_GROWTH: "Your potential for greatness awaits",
            HookType.NEMESIS_ACTIVITY: "Your greatest challenge approaches",
            HookType.DISCOVERY_TEASER: "Knowledge that could change your world awaits",
            HookType.WORLD_EVENT: "The fate of many may depend on your actions"
        }
        
        return stakes.get(hook_type, "Something important is at stake")
    
    def get_session_start_context(self) -> Dict[str, Any]:
        """Get context for starting a new session, including active hooks"""
        
        active_hooks_data = []
        for hook in self.active_hooks:
            if not hook.resolved:
                active_hooks_data.append({
                    'hook_text': hook.hook_text,
                    'intensity': hook.intensity.name,
                    'emotional_stakes': hook.emotional_stakes,
                    'time_pressure': hook.time_pressure
                })
        
        return {
            'active_hooks': active_hooks_data,
            'hook_count': len(active_hooks_data),
            'highest_intensity': max([h.intensity.value for h in self.active_hooks if not h.resolved], default=1),
            'has_urgent_hooks': any(h.intensity.value >= 4 for h in self.active_hooks if not h.resolved)
        }
    
    def resolve_hook(self, hook_id: str, resolution_context: str) -> bool:
        """Mark a hook as resolved"""
        for hook in self.active_hooks:
            if hook.hook_id == hook_id:
                hook.resolved = True
                self.resolved_hooks.append(hook)
                return True
        return False
    
    def cleanup_expired_hooks(self, current_session: int) -> List[SessionHook]:
        """Clean up hooks that have expired"""
        expired_hooks = []
        
        for hook in self.active_hooks[:]:  # Copy list to modify during iteration
            sessions_since_creation = current_session - hook.created_timestamp
            if sessions_since_creation > hook.expires_after_sessions:
                expired_hooks.append(hook)
                self.active_hooks.remove(hook)
        
        return expired_hooks
    
    def generate_anticipation_message(self) -> str:
        """Generate a message to build anticipation for return"""
        
        if not self.active_hooks:
            return "Your adventure awaits your return..."
        
        # Get the most intense active hook
        most_intense_hook = max(self.active_hooks, 
                              key=lambda h: h.intensity.value if not h.resolved else 0)
        
        if most_intense_hook.intensity.value >= 4:
            return f"URGENT: {most_intense_hook.hook_text}"
        elif most_intense_hook.intensity.value >= 3:
            return f"Important developments await: {most_intense_hook.hook_text}"
        else:
            return f"Your story continues: {most_intense_hook.hook_text}"
    
    def get_hooks_summary(self) -> Dict[str, Any]:
        """Get summary of all hooks for debugging/analysis"""
        return {
            'active_hooks': len([h for h in self.active_hooks if not h.resolved]),
            'resolved_hooks': len(self.resolved_hooks),
            'hook_types_active': list(set(h.hook_type.name for h in self.active_hooks if not h.resolved)),
            'average_intensity': sum(h.intensity.value for h in self.active_hooks if not h.resolved) / 
                               max(1, len([h for h in self.active_hooks if not h.resolved])),
            'has_time_pressure': any(h.time_pressure for h in self.active_hooks if not h.resolved)
        }