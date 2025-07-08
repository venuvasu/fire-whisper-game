"""
Character Investment Manager - Makes players emotionally invested in character growth
Implements visible progression, meaningful upgrades, and personal development
"""
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class ProgressionType(Enum):
    STAT_IMPROVEMENT = "stat_improvement"
    SKILL_UNLOCK = "skill_unlock"
    ABILITY_GAINED = "ability_gained"
    EQUIPMENT_UPGRADE = "equipment_upgrade"
    BACKSTORY_REVELATION = "backstory_revelation"
    DIALOGUE_OPTION = "dialogue_option"
    WORLD_INTERACTION = "world_interaction"

class InvestmentTrigger(Enum):
    ACTION_COUNT = "action_count"
    SESSION_COUNT = "session_count"
    STORY_MILESTONE = "story_milestone"
    RELATIONSHIP_LEVEL = "relationship_level"
    DISCOVERY_MADE = "discovery_made"

@dataclass
class ProgressionMilestone:
    milestone_id: str
    progression_type: ProgressionType
    trigger_type: InvestmentTrigger
    trigger_threshold: int
    current_progress: int
    reward_description: str
    visual_change: str
    mechanical_benefit: Dict[str, Any]
    emotional_impact: str
    unlocked: bool = False
    timestamp: Optional[float] = None

@dataclass
class CharacterEvolution:
    evolution_id: str
    evolution_name: str
    base_description: str
    current_description: str
    visual_elements: List[str]
    personality_traits: List[str]
    backstory_elements: List[str]
    reputation_factors: List[str]
    last_updated: float

@dataclass
class AbilityProgression:
    ability_id: str
    ability_name: str
    current_level: int
    max_level: int
    description: str
    usage_count: int
    mastery_requirements: List[str]
    evolution_stages: Dict[int, str]
    unlocked_features: List[str]

class CharacterInvestmentManager:
    """Manages progressive character investment and emotional attachment"""
    
    def __init__(self, character_data: Dict = None):
        self.character_data = character_data or {}
        self.progression_milestones: List[ProgressionMilestone] = []
        self.character_evolution: Optional[CharacterEvolution] = None
        self.ability_progressions: Dict[str, AbilityProgression] = {}
        
        # Tracking counters
        self.action_count = 0
        self.session_count = 0
        self.story_milestones_reached = 0
        self.discoveries_made = 0
        
        # Investment metrics
        self.investment_score = 0.0
        self.attachment_factors = {
            'visual_changes': 0,
            'ability_unlocks': 0,
            'backstory_reveals': 0,
            'world_recognition': 0,
            'personal_growth': 0
        }
        
        self._initialize_progression_system()
    
    def _initialize_progression_system(self):
        """Initialize the progression milestone system"""
        
        # Define progression milestones
        milestones = [
            # Early game - frequent rewards
            {
                'id': 'first_stat_boost',
                'type': ProgressionType.STAT_IMPROVEMENT,
                'trigger': InvestmentTrigger.ACTION_COUNT,
                'threshold': 3,
                'reward': 'Your strength increases from training',
                'visual': 'Your muscles look more defined',
                'benefit': {'stat': 'strength', 'increase': 1},
                'emotion': 'You feel yourself growing stronger'
            },
            {
                'id': 'combat_technique',
                'type': ProgressionType.ABILITY_GAINED,
                'trigger': InvestmentTrigger.ACTION_COUNT,
                'threshold': 5,
                'reward': 'You learn a new combat technique',
                'visual': 'Your stance becomes more confident',
                'benefit': {'ability': 'power_strike', 'damage_bonus': 2},
                'emotion': 'Combat feels more natural to you'
            },
            {
                'id': 'first_backstory',
                'type': ProgressionType.BACKSTORY_REVELATION,
                'trigger': InvestmentTrigger.SESSION_COUNT,
                'threshold': 2,
                'reward': 'A memory from your past surfaces',
                'visual': 'Your eyes show a hint of recognition',
                'benefit': {'dialogue_options': ['mention_past'], 'lore_unlock': 'personal_history'},
                'emotion': 'The past feels closer than before'
            },
            
            # Mid game - meaningful upgrades
            {
                'id': 'signature_equipment',
                'type': ProgressionType.EQUIPMENT_UPGRADE,
                'trigger': InvestmentTrigger.STORY_MILESTONE,
                'threshold': 3,
                'reward': 'You acquire equipment that defines you',
                'visual': 'Your appearance becomes more distinctive',
                'benefit': {'equipment_slot': 'signature', 'stat_bonus': 3},
                'emotion': 'This feels like it was meant for you'
            },
            {
                'id': 'social_recognition',
                'type': ProgressionType.WORLD_INTERACTION,
                'trigger': InvestmentTrigger.RELATIONSHIP_LEVEL,
                'threshold': 15,  # Sum of all relationship levels
                'reward': 'People begin to recognize your reputation',
                'visual': 'NPCs react differently to your presence',
                'benefit': {'social_bonus': 2, 'reputation_unlocks': ['local_hero']},
                'emotion': 'You feel your place in the world solidifying'
            },
            
            # Late game - transformative changes
            {
                'id': 'mastery_unlock',
                'type': ProgressionType.SKILL_UNLOCK,
                'trigger': InvestmentTrigger.ACTION_COUNT,
                'threshold': 25,
                'reward': 'You achieve mastery in your chosen path',
                'visual': 'Your very presence radiates competence',
                'benefit': {'mastery_bonus': 5, 'unique_actions': ['master_technique']},
                'emotion': 'You have become who you were meant to be'
            }
        ]
        
        for milestone_data in milestones:
            milestone = ProgressionMilestone(
                milestone_id=milestone_data['id'],
                progression_type=milestone_data['type'],
                trigger_type=milestone_data['trigger'],
                trigger_threshold=milestone_data['threshold'],
                current_progress=0,
                reward_description=milestone_data['reward'],
                visual_change=milestone_data['visual'],
                mechanical_benefit=milestone_data['benefit'],
                emotional_impact=milestone_data['emotion']
            )
            self.progression_milestones.append(milestone)
        
        # Initialize character evolution
        self._initialize_character_evolution()
    
    def _initialize_character_evolution(self):
        """Initialize character evolution tracking"""
        character_name = self.character_data.get('name', 'Adventurer')
        character_class = self.character_data.get('class', 'Warrior')
        
        self.character_evolution = CharacterEvolution(
            evolution_id=f"evolution_{character_name.lower()}",
            evolution_name=f"{character_name}'s Journey",
            base_description=f"A {character_class.lower()} beginning their adventure",
            current_description=f"A {character_class.lower()} beginning their adventure",
            visual_elements=["basic adventuring gear", "determined expression"],
            personality_traits=["curious", "brave"],
            backstory_elements=["mysterious past"],
            reputation_factors=["unknown newcomer"],
            last_updated=time.time()
        )
    
    def track_action(self, action_description: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Track an action and check for progression triggers"""
        self.action_count += 1
        
        result = {
            'action_tracked': True,
            'total_actions': self.action_count,
            'progressions_unlocked': []
        }
        
        # Check for action-based progressions
        unlocked = self._check_progression_triggers(InvestmentTrigger.ACTION_COUNT, self.action_count)
        if unlocked:
            result['progressions_unlocked'].extend(unlocked)
            result['investment_increased'] = True
        
        # Update ability usage if relevant
        if context and 'ability_used' in context:
            ability_result = self._track_ability_usage(context['ability_used'])
            if ability_result.get('progression'):
                result['ability_progression'] = ability_result
        
        return result
    
    def track_session_start(self) -> Dict[str, Any]:
        """Track session start and check for session-based progressions"""
        self.session_count += 1
        
        result = {
            'session_tracked': True,
            'total_sessions': self.session_count,
            'progressions_unlocked': []
        }
        
        # Check for session-based progressions
        unlocked = self._check_progression_triggers(InvestmentTrigger.SESSION_COUNT, self.session_count)
        if unlocked:
            result['progressions_unlocked'].extend(unlocked)
            result['investment_increased'] = True
        
        return result
    
    def track_story_milestone(self, milestone_description: str) -> Dict[str, Any]:
        """Track story milestone achievement"""
        self.story_milestones_reached += 1
        
        result = {
            'milestone_tracked': True,
            'milestone_description': milestone_description,
            'total_milestones': self.story_milestones_reached,
            'progressions_unlocked': []
        }
        
        # Check for milestone-based progressions
        unlocked = self._check_progression_triggers(InvestmentTrigger.STORY_MILESTONE, self.story_milestones_reached)
        if unlocked:
            result['progressions_unlocked'].extend(unlocked)
            result['investment_increased'] = True
        
        return result
    
    def track_discovery(self, discovery_description: str, rarity: int = 1) -> Dict[str, Any]:
        """Track discovery made by player"""
        self.discoveries_made += 1
        
        result = {
            'discovery_tracked': True,
            'discovery_description': discovery_description,
            'rarity': rarity,
            'total_discoveries': self.discoveries_made,
            'progressions_unlocked': []
        }
        
        # Check for discovery-based progressions
        unlocked = self._check_progression_triggers(InvestmentTrigger.DISCOVERY_MADE, self.discoveries_made)
        if unlocked:
            result['progressions_unlocked'].extend(unlocked)
            result['investment_increased'] = True
        
        # High rarity discoveries might trigger special progressions
        if rarity >= 4:
            special_progression = self._trigger_special_discovery_progression(discovery_description, rarity)
            if special_progression:
                result['special_progression'] = special_progression
        
        return result
    
    def track_relationship_change(self, total_relationship_score: int) -> Dict[str, Any]:
        """Track relationship changes for social progression"""
        result = {
            'relationship_tracked': True,
            'total_relationship_score': total_relationship_score,
            'progressions_unlocked': []
        }
        
        # Check for relationship-based progressions
        unlocked = self._check_progression_triggers(InvestmentTrigger.RELATIONSHIP_LEVEL, total_relationship_score)
        if unlocked:
            result['progressions_unlocked'].extend(unlocked)
            result['investment_increased'] = True
        
        return result
    
    def _check_progression_triggers(self, trigger_type: InvestmentTrigger, 
                                  current_value: int) -> List[Dict[str, Any]]:
        """Check if any progressions should be unlocked"""
        unlocked_progressions = []
        
        for milestone in self.progression_milestones:
            if (milestone.trigger_type == trigger_type and 
                not milestone.unlocked and 
                current_value >= milestone.trigger_threshold):
                
                # Unlock the progression
                milestone.unlocked = True
                milestone.timestamp = time.time()
                milestone.current_progress = current_value
                
                # Apply the progression
                progression_result = self._apply_progression(milestone)
                unlocked_progressions.append(progression_result)
                
                # Update investment score
                self._update_investment_score(milestone)
        
        return unlocked_progressions
    
    def _apply_progression(self, milestone: ProgressionMilestone) -> Dict[str, Any]:
        """Apply a progression milestone"""
        result = {
            'milestone_id': milestone.milestone_id,
            'progression_type': milestone.progression_type.value,
            'reward_description': milestone.reward_description,
            'visual_change': milestone.visual_change,
            'emotional_impact': milestone.emotional_impact,
            'mechanical_benefits': milestone.mechanical_benefit
        }
        
        # Apply specific progression effects
        if milestone.progression_type == ProgressionType.STAT_IMPROVEMENT:
            self._apply_stat_improvement(milestone.mechanical_benefit)
            
        elif milestone.progression_type == ProgressionType.ABILITY_GAINED:
            self._apply_ability_gain(milestone.mechanical_benefit)
            
        elif milestone.progression_type == ProgressionType.BACKSTORY_REVELATION:
            self._apply_backstory_revelation(milestone.mechanical_benefit)
            
        elif milestone.progression_type == ProgressionType.EQUIPMENT_UPGRADE:
            self._apply_equipment_upgrade(milestone.mechanical_benefit)
            
        elif milestone.progression_type == ProgressionType.WORLD_INTERACTION:
            self._apply_world_interaction_change(milestone.mechanical_benefit)
        
        # Update character evolution
        self._update_character_evolution(milestone)
        
        return result
    
    def _apply_stat_improvement(self, benefit: Dict[str, Any]):
        """Apply stat improvement to character"""
        if 'stat' in benefit and 'increase' in benefit:
            stat_name = benefit['stat']
            increase = benefit['increase']
            
            if stat_name in self.character_data.get('stats', {}):
                self.character_data['stats'][stat_name] += increase
                self.attachment_factors['personal_growth'] += 1
    
    def _apply_ability_gain(self, benefit: Dict[str, Any]):
        """Apply new ability gain"""
        if 'ability' in benefit:
            ability_name = benefit['ability']
            
            # Add to character abilities
            if 'abilities' not in self.character_data:
                self.character_data['abilities'] = []
            
            self.character_data['abilities'].append(ability_name)
            self.attachment_factors['ability_unlocks'] += 1
            
            # Create ability progression tracking
            self._create_ability_progression(ability_name, benefit)
    
    def _apply_backstory_revelation(self, benefit: Dict[str, Any]):
        """Apply backstory revelation"""
        if 'lore_unlock' in benefit:
            lore_type = benefit['lore_unlock']
            
            if 'backstory' not in self.character_data:
                self.character_data['backstory'] = {}
            
            self.character_data['backstory'][lore_type] = True
            self.attachment_factors['backstory_reveals'] += 1
    
    def _apply_equipment_upgrade(self, benefit: Dict[str, Any]):
        """Apply equipment upgrade"""
        if 'equipment_slot' in benefit:
            slot = benefit['equipment_slot']
            
            if 'equipment' not in self.character_data:
                self.character_data['equipment'] = {}
            
            self.character_data['equipment'][slot] = benefit
            self.attachment_factors['visual_changes'] += 1
    
    def _apply_world_interaction_change(self, benefit: Dict[str, Any]):
        """Apply world interaction changes"""
        if 'reputation_unlocks' in benefit:
            reputation_types = benefit['reputation_unlocks']
            
            if 'reputation' not in self.character_data:
                self.character_data['reputation'] = []
            
            self.character_data['reputation'].extend(reputation_types)
            self.attachment_factors['world_recognition'] += 1
    
    def _update_character_evolution(self, milestone: ProgressionMilestone):
        """Update character evolution based on milestone"""
        if not self.character_evolution:
            return
        
        evolution = self.character_evolution
        
        # Update visual elements
        if milestone.visual_change not in evolution.visual_elements:
            evolution.visual_elements.append(milestone.visual_change)
        
        # Update description based on progressions
        evolution.current_description = self._generate_evolved_description()
        
        # Add personality development
        if milestone.progression_type == ProgressionType.BACKSTORY_REVELATION:
            evolution.personality_traits.append("introspective")
        elif milestone.progression_type == ProgressionType.ABILITY_GAINED:
            evolution.personality_traits.append("capable")
        elif milestone.progression_type == ProgressionType.WORLD_INTERACTION:
            evolution.personality_traits.append("influential")
        
        evolution.last_updated = time.time()
    
    def _generate_evolved_description(self) -> str:
        """Generate evolved character description"""
        if not self.character_evolution:
            return "An adventurer on their journey"
        
        evolution = self.character_evolution
        character_class = self.character_data.get('class', 'Adventurer')
        character_name = self.character_data.get('name', 'Adventurer')
        
        # Base description
        description_parts = [f"{character_name}, a {character_class.lower()}"]
        
        # Add progression-based descriptors
        if self.attachment_factors['ability_unlocks'] >= 2:
            description_parts.append("skilled in combat")
        
        if self.attachment_factors['backstory_reveals'] >= 1:
            description_parts.append("with a mysterious past")
        
        if self.attachment_factors['world_recognition'] >= 1:
            description_parts.append("known throughout the land")
        
        if self.attachment_factors['visual_changes'] >= 2:
            description_parts.append("bearing distinctive equipment")
        
        # Combine into flowing description
        if len(description_parts) == 1:
            return description_parts[0]
        elif len(description_parts) == 2:
            return f"{description_parts[0]} {description_parts[1]}"
        else:
            return f"{description_parts[0]}, {', '.join(description_parts[1:-1])}, and {description_parts[-1]}"
    
    def _create_ability_progression(self, ability_name: str, benefit: Dict[str, Any]):
        """Create progression tracking for new ability"""
        ability_progression = AbilityProgression(
            ability_id=f"ability_{ability_name}",
            ability_name=ability_name,
            current_level=1,
            max_level=5,
            description=benefit.get('description', f"A {ability_name} ability"),
            usage_count=0,
            mastery_requirements=[f"use_{ability_name}_10_times", f"critical_success_with_{ability_name}"],
            evolution_stages={
                1: "Basic proficiency",
                2: "Improved technique", 
                3: "Advanced mastery",
                4: "Expert level",
                5: "Perfect mastery"
            },
            unlocked_features=[]
        )
        
        self.ability_progressions[ability_name] = ability_progression
    
    def _track_ability_usage(self, ability_name: str) -> Dict[str, Any]:
        """Track ability usage for progression"""
        if ability_name not in self.ability_progressions:
            return {'progression': False}
        
        ability = self.ability_progressions[ability_name]
        ability.usage_count += 1
        
        result = {'progression': False, 'ability_name': ability_name, 'usage_count': ability.usage_count}
        
        # Check for ability level progression
        if ability.usage_count % 5 == 0 and ability.current_level < ability.max_level:
            ability.current_level += 1
            ability.unlocked_features.append(f"level_{ability.current_level}_mastery")
            
            result.update({
                'progression': True,
                'new_level': ability.current_level,
                'evolution_description': ability.evolution_stages[ability.current_level],
                'unlocked_features': ability.unlocked_features[-1:]
            })
        
        return result
    
    def _trigger_special_discovery_progression(self, discovery: str, rarity: int) -> Dict[str, Any]:
        """Trigger special progression for rare discoveries"""
        special_progression = {
            'type': 'rare_discovery_bonus',
            'discovery': discovery,
            'rarity': rarity,
            'bonus_applied': True
        }
        
        # Apply rarity-based bonuses
        if rarity == 4:
            # Rare discovery - minor stat boost
            stat_to_boost = 'intelligence'  # Discovery-related stat
            if stat_to_boost in self.character_data.get('stats', {}):
                self.character_data['stats'][stat_to_boost] += 1
                special_progression['stat_bonus'] = {stat_to_boost: 1}
        
        elif rarity == 5:
            # Ultra rare discovery - unique ability
            unique_ability = f"discovery_insight_{len(self.ability_progressions)}"
            self.character_data.setdefault('abilities', []).append(unique_ability)
            special_progression['unique_ability'] = unique_ability
        
        return special_progression
    
    def _update_investment_score(self, milestone: ProgressionMilestone):
        """Update overall investment score"""
        progression_values = {
            ProgressionType.STAT_IMPROVEMENT: 0.1,
            ProgressionType.SKILL_UNLOCK: 0.2,
            ProgressionType.ABILITY_GAINED: 0.3,
            ProgressionType.EQUIPMENT_UPGRADE: 0.2,
            ProgressionType.BACKSTORY_REVELATION: 0.4,
            ProgressionType.DIALOGUE_OPTION: 0.1,
            ProgressionType.WORLD_INTERACTION: 0.3
        }
        
        self.investment_score += progression_values.get(milestone.progression_type, 0.1)
    
    def get_character_progression_context(self) -> str:
        """Generate context about character progression for AI"""
        if not self.character_evolution:
            return ""
        
        context_parts = ["=== CHARACTER PROGRESSION ==="]
        
        # Current character state
        context_parts.append(f"Current Description: {self.character_evolution.current_description}")
        
        # Recent progressions
        recent_milestones = [m for m in self.progression_milestones if m.unlocked][-3:]
        if recent_milestones:
            context_parts.append("Recent Growth:")
            for milestone in recent_milestones:
                context_parts.append(f"• {milestone.reward_description}")
                context_parts.append(f"  {milestone.emotional_impact}")
        
        # Available progressions (close to unlocking)
        close_milestones = []
        for milestone in self.progression_milestones:
            if not milestone.unlocked:
                progress_ratio = self._get_progress_ratio(milestone)
                if progress_ratio >= 0.7:  # 70% or more progress
                    close_milestones.append((milestone, progress_ratio))
        
        if close_milestones:
            context_parts.append("Approaching Milestones:")
            for milestone, ratio in close_milestones:
                context_parts.append(f"• {milestone.reward_description} ({ratio:.0%} progress)")
        
        # Ability progressions
        if self.ability_progressions:
            context_parts.append("Ability Development:")
            for ability in self.ability_progressions.values():
                if ability.current_level > 1:
                    context_parts.append(f"• {ability.ability_name}: {ability.evolution_stages[ability.current_level]}")
        
        return "\n".join(context_parts)
    
    def _get_progress_ratio(self, milestone: ProgressionMilestone) -> float:
        """Get progress ratio for a milestone"""
        current_value = 0
        
        if milestone.trigger_type == InvestmentTrigger.ACTION_COUNT:
            current_value = self.action_count
        elif milestone.trigger_type == InvestmentTrigger.SESSION_COUNT:
            current_value = self.session_count
        elif milestone.trigger_type == InvestmentTrigger.STORY_MILESTONE:
            current_value = self.story_milestones_reached
        elif milestone.trigger_type == InvestmentTrigger.DISCOVERY_MADE:
            current_value = self.discoveries_made
        
        return min(1.0, current_value / milestone.trigger_threshold)
    
    def get_investment_summary(self) -> Dict[str, Any]:
        """Get summary of player investment metrics"""
        return {
            'investment_score': self.investment_score,
            'attachment_factors': self.attachment_factors.copy(),
            'progression_stats': {
                'total_actions': self.action_count,
                'total_sessions': self.session_count,
                'story_milestones': self.story_milestones_reached,
                'discoveries_made': self.discoveries_made
            },
            'milestones_unlocked': len([m for m in self.progression_milestones if m.unlocked]),
            'abilities_gained': len(self.ability_progressions),
            'character_evolution_stage': len(self.character_evolution.visual_elements) if self.character_evolution else 0
        }
    
    def generate_progression_preview(self) -> str:
        """Generate preview of upcoming progressions for motivation"""
        upcoming = []
        
        for milestone in self.progression_milestones:
            if not milestone.unlocked:
                progress_ratio = self._get_progress_ratio(milestone)
                if progress_ratio > 0.3:  # Show if 30%+ progress
                    remaining = milestone.trigger_threshold - self._get_current_trigger_value(milestone.trigger_type)
                    upcoming.append(f"• {milestone.reward_description} (in {remaining} more {milestone.trigger_type.value.replace('_', ' ')})")
        
        if upcoming:
            return "Upcoming Growth:\n" + "\n".join(upcoming[:3])  # Show top 3
        else:
            return "Continue your adventure to unlock new abilities and growth!"
    
    def _get_current_trigger_value(self, trigger_type: InvestmentTrigger) -> int:
        """Get current value for trigger type"""
        if trigger_type == InvestmentTrigger.ACTION_COUNT:
            return self.action_count
        elif trigger_type == InvestmentTrigger.SESSION_COUNT:
            return self.session_count
        elif trigger_type == InvestmentTrigger.STORY_MILESTONE:
            return self.story_milestones_reached
        elif trigger_type == InvestmentTrigger.DISCOVERY_MADE:
            return self.discoveries_made
        return 0