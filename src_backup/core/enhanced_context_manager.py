"""
Enhanced Context Manager - Core system for managing game context across sessions
Implements the billion-dollar game strategy with persistent context and emotional investment
"""
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class ContextType(Enum):
    CHARACTER_PROGRESSION = "character_progression"
    CHOICE_CONSEQUENCES = "choice_consequences"
    RELATIONSHIP_DYNAMICS = "relationship_dynamics"
    WORLD_STATE = "world_state"
    PERSONAL_STORY = "personal_story"
    NEMESIS_EVOLUTION = "nemesis_evolution"
    DISCOVERY_LOG = "discovery_log"
    EMOTIONAL_STATE = "emotional_state"

@dataclass
class ChoiceConsequence:
    choice_id: str
    choice_text: str
    consequence_type: str  # immediate, delayed, cascading
    impact_level: int  # 1-5 scale
    affected_npcs: List[str]
    world_changes: Dict[str, Any]
    future_options_unlocked: List[str]
    future_options_blocked: List[str]
    timestamp: float
    session_id: str

@dataclass
class RelationshipState:
    npc_name: str
    relationship_level: int  # -10 to +10
    trust_level: int  # 0-10
    shared_experiences: List[str]
    personal_secrets_known: List[str]
    relationship_type: str  # ally, enemy, neutral, romantic, mentor
    last_interaction: str
    evolution_notes: List[str]
    timestamp: float

@dataclass
class NemesisProfile:
    name: str
    nemesis_type: str  # personal, ideological, circumstantial
    power_level: int
    intelligence_level: int
    personal_grudge_reason: str
    learned_tactics: List[str]
    failed_encounters: List[Dict]
    successful_encounters: List[Dict]
    next_appearance_conditions: Dict[str, Any]
    evolution_stage: int
    timestamp: float

@dataclass
class DiscoveryEntry:
    discovery_id: str
    discovery_type: str  # secret_area, hidden_lore, easter_egg, rare_item
    discovery_name: str
    discovery_description: str
    rarity_level: int  # 1-5, 5 being ultra rare
    prerequisites_met: List[str]
    unlocks_content: List[str]
    player_reaction_context: str
    timestamp: float
    session_id: str

@dataclass
class PersonalStoryThread:
    thread_id: str
    thread_name: str
    background_element: str  # family, past, mystery, goal
    current_status: str  # dormant, active, climaxing, resolved
    story_beats: List[Dict]
    emotional_investment_level: int  # 1-10
    resolution_conditions: List[str]
    connected_npcs: List[str]
    timestamp: float

class EnhancedContextManager:
    """Core context management system for persistent game experience"""
    
    def __init__(self):
        # Core context storage
        self.character_progression = {}
        self.choice_consequences: List[ChoiceConsequence] = []
        self.relationship_states: Dict[str, RelationshipState] = {}
        self.world_state_changes = {}
        self.personal_story_threads: Dict[str, PersonalStoryThread] = {}
        self.nemesis_profile: Optional[NemesisProfile] = None
        self.discovery_log: List[DiscoveryEntry] = []
        self.emotional_state = {}
        
        # Session management
        self.session_count = 0
        self.current_session_id = self._generate_session_id()
        self.total_playtime = 0
        self.last_session_end_hook = ""
        
        # Context weighting for AI
        self.context_weights = {
            ContextType.CHARACTER_PROGRESSION: 0.9,
            ContextType.CHOICE_CONSEQUENCES: 0.8,
            ContextType.RELATIONSHIP_DYNAMICS: 0.7,
            ContextType.WORLD_STATE: 0.6,
            ContextType.PERSONAL_STORY: 0.9,
            ContextType.NEMESIS_EVOLUTION: 0.8,
            ContextType.DISCOVERY_LOG: 0.5,
            ContextType.EMOTIONAL_STATE: 0.7
        }
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{int(time.time())}_{self.session_count}"
    
    def start_new_session(self) -> Dict[str, Any]:
        """Start a new game session with context continuity"""
        self.session_count += 1
        self.current_session_id = self._generate_session_id()
        
        session_start_context = {
            'session_id': self.current_session_id,
            'session_number': self.session_count,
            'returning_player': self.session_count > 1,
            'last_session_hook': self.last_session_end_hook,
            'context_summary': self._generate_session_start_summary()
        }
        
        return session_start_context
    
    def _generate_session_start_summary(self) -> str:
        """Generate context summary for session start"""
        if self.session_count == 1:
            return "Beginning your adventure in the world of Fire Whisper..."
        
        summary_parts = []
        
        # Recent choice consequences
        recent_choices = [c for c in self.choice_consequences[-3:] if c.impact_level >= 3]
        if recent_choices:
            summary_parts.append("Recent significant choices are still affecting your world...")
        
        # Relationship changes
        important_relationships = [r for r in self.relationship_states.values() 
                                if abs(r.relationship_level) >= 5]
        if important_relationships:
            names = [r.npc_name for r in important_relationships[:2]]
            summary_parts.append(f"Your relationships with {', '.join(names)} continue to evolve...")
        
        # Nemesis status
        if self.nemesis_profile and self.nemesis_profile.evolution_stage > 0:
            summary_parts.append(f"{self.nemesis_profile.name} has not forgotten your past encounters...")
        
        # Personal story threads
        active_threads = [t for t in self.personal_story_threads.values() 
                         if t.current_status == 'active']
        if active_threads:
            summary_parts.append("Personal mysteries from your past continue to unfold...")
        
        return " ".join(summary_parts) if summary_parts else "Your adventure continues..."
    
    def record_choice_consequence(self, choice_text: str, immediate_consequence: str,
                                future_implications: Dict[str, Any]) -> str:
        """Record a choice and its consequences for future reference"""
        choice_id = f"choice_{len(self.choice_consequences)}_{int(time.time())}"
        
        consequence = ChoiceConsequence(
            choice_id=choice_id,
            choice_text=choice_text,
            consequence_type=future_implications.get('type', 'immediate'),
            impact_level=future_implications.get('impact_level', 1),
            affected_npcs=future_implications.get('affected_npcs', []),
            world_changes=future_implications.get('world_changes', {}),
            future_options_unlocked=future_implications.get('unlocked_options', []),
            future_options_blocked=future_implications.get('blocked_options', []),
            timestamp=time.time(),
            session_id=self.current_session_id
        )
        
        self.choice_consequences.append(consequence)
        return choice_id
    
    def update_relationship(self, npc_name: str, interaction_type: str, 
                          relationship_change: int, context: str) -> RelationshipState:
        """Update NPC relationship with detailed tracking"""
        if npc_name not in self.relationship_states:
            self.relationship_states[npc_name] = RelationshipState(
                npc_name=npc_name,
                relationship_level=0,
                trust_level=5,
                shared_experiences=[],
                personal_secrets_known=[],
                relationship_type="neutral",
                last_interaction="",
                evolution_notes=[],
                timestamp=time.time()
            )
        
        relationship = self.relationship_states[npc_name]
        relationship.relationship_level = max(-10, min(10, 
            relationship.relationship_level + relationship_change))
        relationship.last_interaction = context
        relationship.shared_experiences.append(f"{interaction_type}: {context}")
        relationship.evolution_notes.append(
            f"Session {self.session_count}: {interaction_type} (change: {relationship_change:+d})"
        )
        relationship.timestamp = time.time()
        
        # Update relationship type based on level
        if relationship.relationship_level >= 7:
            relationship.relationship_type = "ally"
        elif relationship.relationship_level <= -7:
            relationship.relationship_type = "enemy"
        elif relationship.relationship_level >= 3:
            relationship.relationship_type = "friendly"
        elif relationship.relationship_level <= -3:
            relationship.relationship_type = "hostile"
        else:
            relationship.relationship_type = "neutral"
        
        return relationship
    
    def create_or_update_nemesis(self, name: str, encounter_context: str, 
                               player_actions: List[str], outcome: str) -> NemesisProfile:
        """Create or update nemesis profile with learning capabilities"""
        if not self.nemesis_profile:
            self.nemesis_profile = NemesisProfile(
                name=name,
                nemesis_type="personal",
                power_level=1,
                intelligence_level=1,
                personal_grudge_reason=encounter_context,
                learned_tactics=[],
                failed_encounters=[],
                successful_encounters=[],
                next_appearance_conditions={},
                evolution_stage=1,
                timestamp=time.time()
            )
        
        nemesis = self.nemesis_profile
        
        # Record encounter
        encounter_data = {
            'context': encounter_context,
            'player_actions': player_actions,
            'outcome': outcome,
            'session_id': self.current_session_id,
            'timestamp': time.time()
        }
        
        if outcome in ['player_victory', 'nemesis_defeated']:
            nemesis.failed_encounters.append(encounter_data)
            # Nemesis learns from failure
            for action in player_actions:
                if action not in nemesis.learned_tactics:
                    nemesis.learned_tactics.append(f"counter_{action}")
        else:
            nemesis.successful_encounters.append(encounter_data)
        
        # Evolve nemesis
        nemesis.evolution_stage += 1
        nemesis.power_level = min(10, nemesis.power_level + 1)
        if len(nemesis.learned_tactics) > nemesis.intelligence_level * 2:
            nemesis.intelligence_level = min(10, nemesis.intelligence_level + 1)
        
        nemesis.timestamp = time.time()
        return nemesis
    
    def record_discovery(self, discovery_name: str, discovery_type: str,
                        description: str, rarity: int, context: str) -> DiscoveryEntry:
        """Record a discovery for dopamine hit tracking"""
        discovery_id = f"discovery_{len(self.discovery_log)}_{int(time.time())}"
        
        discovery = DiscoveryEntry(
            discovery_id=discovery_id,
            discovery_type=discovery_type,
            discovery_name=discovery_name,
            discovery_description=description,
            rarity_level=rarity,
            prerequisites_met=[],  # Could be filled based on context
            unlocks_content=[],
            player_reaction_context=context,
            timestamp=time.time(),
            session_id=self.current_session_id
        )
        
        self.discovery_log.append(discovery)
        return discovery
    
    def create_personal_story_thread(self, thread_name: str, background_element: str,
                                   initial_context: str) -> PersonalStoryThread:
        """Create a personal story thread for emotional investment"""
        thread_id = f"thread_{len(self.personal_story_threads)}_{int(time.time())}"
        
        thread = PersonalStoryThread(
            thread_id=thread_id,
            thread_name=thread_name,
            background_element=background_element,
            current_status="active",
            story_beats=[{
                'beat_type': 'introduction',
                'description': initial_context,
                'timestamp': time.time(),
                'session_id': self.current_session_id
            }],
            emotional_investment_level=1,
            resolution_conditions=[],
            connected_npcs=[],
            timestamp=time.time()
        )
        
        self.personal_story_threads[thread_id] = thread
        return thread
    
    def advance_personal_story(self, thread_id: str, story_beat: Dict[str, Any]) -> bool:
        """Advance a personal story thread"""
        if thread_id not in self.personal_story_threads:
            return False
        
        thread = self.personal_story_threads[thread_id]
        story_beat.update({
            'timestamp': time.time(),
            'session_id': self.current_session_id
        })
        thread.story_beats.append(story_beat)
        
        # Increase emotional investment
        if story_beat.get('emotional_impact', 0) > 0:
            thread.emotional_investment_level = min(10, 
                thread.emotional_investment_level + story_beat['emotional_impact'])
        
        return True
    
    def generate_weighted_context_for_ai(self, context_types: List[ContextType] = None,
                                       max_tokens: int = 2000) -> str:
        """Generate weighted context for AI with token management"""
        if not context_types:
            context_types = list(ContextType)
        
        context_sections = []
        
        for context_type in sorted(context_types, 
                                 key=lambda x: self.context_weights[x], reverse=True):
            section = self._generate_context_section(context_type)
            if section:
                context_sections.append(section)
        
        # Combine and truncate if needed
        full_context = "\n\n".join(context_sections)
        
        # Simple token estimation (rough)
        if len(full_context) > max_tokens * 4:  # ~4 chars per token
            # Prioritize highest weighted contexts
            truncated_sections = []
            current_length = 0
            
            for section in context_sections:
                if current_length + len(section) < max_tokens * 4:
                    truncated_sections.append(section)
                    current_length += len(section)
                else:
                    break
            
            full_context = "\n\n".join(truncated_sections)
            full_context += "\n\n[Context truncated - additional history available]"
        
        return full_context
    
    def _generate_context_section(self, context_type: ContextType) -> str:
        """Generate specific context section"""
        if context_type == ContextType.CHARACTER_PROGRESSION:
            return self._generate_character_progression_context()
        elif context_type == ContextType.CHOICE_CONSEQUENCES:
            return self._generate_choice_consequences_context()
        elif context_type == ContextType.RELATIONSHIP_DYNAMICS:
            return self._generate_relationship_context()
        elif context_type == ContextType.NEMESIS_EVOLUTION:
            return self._generate_nemesis_context()
        elif context_type == ContextType.PERSONAL_STORY:
            return self._generate_personal_story_context()
        elif context_type == ContextType.DISCOVERY_LOG:
            return self._generate_discovery_context()
        # Add other context types as needed
        return ""
    
    def _generate_character_progression_context(self) -> str:
        """Generate character progression context"""
        if not self.character_progression:
            return ""
        
        context = "=== CHARACTER PROGRESSION CONTEXT ===\n"
        # This would be populated by the game state manager
        # For now, return placeholder
        return context + "Character progression tracking active..."
    
    def _generate_choice_consequences_context(self) -> str:
        """Generate choice consequences context"""
        if not self.choice_consequences:
            return ""
        
        context = "=== CHOICE CONSEQUENCES ===\n"
        
        # Recent high-impact choices
        recent_important = [c for c in self.choice_consequences[-5:] if c.impact_level >= 3]
        
        for choice in recent_important:
            context += f"• {choice.choice_text}\n"
            if choice.affected_npcs:
                context += f"  Affected: {', '.join(choice.affected_npcs)}\n"
            if choice.world_changes:
                context += f"  World Impact: {choice.consequence_type}\n"
        
        return context
    
    def _generate_relationship_context(self) -> str:
        """Generate relationship dynamics context"""
        if not self.relationship_states:
            return ""
        
        context = "=== RELATIONSHIP DYNAMICS ===\n"
        
        # Sort by relationship strength (absolute value)
        sorted_relationships = sorted(self.relationship_states.values(),
                                    key=lambda r: abs(r.relationship_level), reverse=True)
        
        for rel in sorted_relationships[:5]:  # Top 5 relationships
            status = "ally" if rel.relationship_level > 5 else "enemy" if rel.relationship_level < -5 else "neutral"
            context += f"• {rel.npc_name}: {status} (level {rel.relationship_level})\n"
            if rel.shared_experiences:
                context += f"  Last interaction: {rel.shared_experiences[-1]}\n"
        
        return context
    
    def _generate_nemesis_context(self) -> str:
        """Generate nemesis evolution context"""
        if not self.nemesis_profile:
            return ""
        
        nemesis = self.nemesis_profile
        context = "=== NEMESIS PROFILE ===\n"
        context += f"• {nemesis.name} (Power: {nemesis.power_level}, Intelligence: {nemesis.intelligence_level})\n"
        context += f"• Grudge: {nemesis.personal_grudge_reason}\n"
        context += f"• Evolution Stage: {nemesis.evolution_stage}\n"
        
        if nemesis.learned_tactics:
            context += f"• Known Tactics: {', '.join(nemesis.learned_tactics[-3:])}\n"
        
        return context
    
    def _generate_personal_story_context(self) -> str:
        """Generate personal story threads context"""
        if not self.personal_story_threads:
            return ""
        
        context = "=== PERSONAL STORY THREADS ===\n"
        
        active_threads = [t for t in self.personal_story_threads.values() 
                         if t.current_status == 'active']
        
        for thread in active_threads[:3]:  # Top 3 active threads
            context += f"• {thread.thread_name} ({thread.background_element})\n"
            context += f"  Investment Level: {thread.emotional_investment_level}/10\n"
            if thread.story_beats:
                latest_beat = thread.story_beats[-1]
                context += f"  Latest: {latest_beat.get('description', 'Unknown')}\n"
        
        return context
    
    def _generate_discovery_context(self) -> str:
        """Generate discovery log context"""
        if not self.discovery_log:
            return ""
        
        context = "=== RECENT DISCOVERIES ===\n"
        
        recent_discoveries = self.discovery_log[-3:]  # Last 3 discoveries
        for discovery in recent_discoveries:
            rarity_text = "★" * discovery.rarity_level
            context += f"• {discovery.discovery_name} {rarity_text}\n"
            context += f"  {discovery.discovery_description}\n"
        
        return context
    
    def get_context_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics of context data"""
        return {
            'total_sessions': self.session_count,
            'choice_consequences': len(self.choice_consequences),
            'relationships_tracked': len(self.relationship_states),
            'discoveries_made': len(self.discovery_log),
            'personal_story_threads': len(self.personal_story_threads),
            'nemesis_active': self.nemesis_profile is not None,
            'context_richness_score': self._calculate_context_richness()
        }
    
    def _calculate_context_richness(self) -> float:
        """Calculate how rich the context is (0-1 scale)"""
        factors = [
            min(1.0, len(self.choice_consequences) / 10),  # Up to 10 choices
            min(1.0, len(self.relationship_states) / 5),   # Up to 5 relationships
            min(1.0, len(self.discovery_log) / 8),         # Up to 8 discoveries
            min(1.0, len(self.personal_story_threads) / 3), # Up to 3 threads
            1.0 if self.nemesis_profile else 0.0,         # Nemesis presence
            min(1.0, self.session_count / 5)              # Up to 5 sessions
        ]
        
        return sum(factors) / len(factors)