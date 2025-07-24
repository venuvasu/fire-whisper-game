"""
Game State Manager - Deterministic game logic separate from AI
"""
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class ActionType(Enum):
    COMBAT = "combat"
    SKILL_CHECK = "skill_check"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    MAGIC = "magic"

@dataclass
class DiceRoll:
    roll_type: str
    stat_used: str
    skill_used: Optional[str]
    base_roll: int
    modifiers: Dict[str, int]
    target: int
    success: bool
    timestamp: float

@dataclass
class XPAward:
    amount: int
    reason: str
    category: str
    timestamp: float

@dataclass
class GameAction:
    action_type: ActionType
    description: str
    dice_rolls: List[DiceRoll]
    xp_awards: List[XPAward]
    state_changes: Dict[str, Any]
    timestamp: float

class GameStateManager:
    def __init__(self, character_data: Dict = None):
        self.character = character_data or self._create_default_character()
        self.session_data = {
            'turn_count': 0,
            'episode_number': 1,
            'last_context_refresh': 0,
            'session_start': time.time()
        }
        
        # Add progression state tracking
        self.progression_state = {
            'current_location': 'village_outskirts',
            'story_progress': 0,
            'discovered_locations': ['village_outskirts'],
            'completed_events': [],
            'world_state': {
                'shadow_blight_level': 1,
                'ashbrook_alert_level': 0,
                'emberlyn_bond': 1
            },
            'turns_at_current_location': 0
        }
        self.action_history: List[GameAction] = []
        self.pending_rolls: List[DiceRoll] = []
        self.rule_violations: List[str] = []
        
    def _create_default_character(self) -> Dict:
        return {
            'name': 'Adventurer',
            'level': 1,
            'xp': 0,
            'class': 'Warrior',
            'stats': {
                'strength': 14,
                'dexterity': 12,
                'intelligence': 10,
                'charisma': 12
            },
            'resources': {
                'hp': 30,
                'max_hp': 30,
                'energy': 10,
                'max_energy': 10
            },
            'skills': {
                'Combat': 2,
                'Athletics': 1,
                'Intimidation': 1
            },
            'achievements': [],
            'emberlyn_bond': 1
        }
    
    def validate_action(self, action_type: ActionType, parameters: Dict) -> Dict:
        """Validate if an action is legal given current game state"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check resource requirements
        if action_type == ActionType.MAGIC:
            energy_cost = parameters.get('energy_cost', 1)
            if self.character['resources']['energy'] < energy_cost:
                validation_result['valid'] = False
                validation_result['errors'].append(f"Insufficient energy: need {energy_cost}, have {self.character['resources']['energy']}")
        
        # Check class restrictions
        if action_type == ActionType.MAGIC and self.character['class'] not in ['Mage', 'Cleric']:
            validation_result['warnings'].append("This character class has limited magic abilities")
        
        return validation_result
    
    def execute_dice_roll(self, stat: str, skill: str = None, difficulty: str = "normal", 
                         context: str = "") -> DiceRoll:
        """Execute a dice roll with all modifiers calculated deterministically"""
        import random
        
        # Base roll (1-20)
        base_roll = random.randint(1, 20)
        
        # Calculate modifiers
        modifiers = {}
        
        # Stat modifier
        stat_value = self.character['stats'].get(stat.lower(), 10)
        stat_mod = max(0, (stat_value - 10) // 2)
        if stat_mod > 0:
            modifiers[f"{stat.title()}"] = stat_mod
        
        # Skill modifier
        if skill:
            skill_level = self.character['skills'].get(skill, 0)
            if skill_level > 0:
                modifiers[skill] = skill_level
        
        # Class bonuses
        class_bonuses = self._get_class_bonuses(skill)
        if class_bonuses:
            modifiers.update(class_bonuses)
        
        # Calculate target
        difficulty_targets = {
            'trivial': 5,
            'easy': 8,
            'normal': 12,
            'hard': 15,
            'extreme': 18
        }
        target = difficulty_targets.get(difficulty, 12)
        
        # Determine success
        total_modifier = sum(modifiers.values())
        final_result = base_roll + total_modifier
        success = final_result >= target
        
        # Create roll record
        roll = DiceRoll(
            roll_type=context,
            stat_used=stat,
            skill_used=skill,
            base_roll=base_roll,
            modifiers=modifiers,
            target=target,
            success=success,
            timestamp=time.time()
        )
        
        self.pending_rolls.append(roll)
        return roll
    
    def _get_class_bonuses(self, skill: str) -> Dict[str, int]:
        """Get class-specific bonuses for skills"""
        class_bonuses = {
            'Warrior': {
                'Combat': 2,
                'Intimidation': 1,
                'Athletics': 1
            },
            'Mage': {
                'Magic': 3,
                'Knowledge': 2,
                'Investigation': 1
            },
            'Rogue': {
                'Stealth': 2,
                'Lockpicking': 2,
                'Deception': 1
            },
            'Cleric': {
                'Healing': 3,
                'Persuasion': 2,
                'Knowledge': 1
            }
        }
        
        character_class = self.character.get('class', 'Warrior')
        class_skills = class_bonuses.get(character_class, {})
        
        if skill in class_skills:
            return {f"{character_class} Training": class_skills[skill]}
        
        return {}
    
    def award_xp(self, amount: int, reason: str, category: str = "general") -> Dict:
        """Award XP and handle level-ups deterministically"""
        old_level = self.character['level']
        old_xp = self.character['xp']
        
        # Award XP
        self.character['xp'] += amount
        
        # Create XP record
        xp_award = XPAward(
            amount=amount,
            reason=reason,
            category=category,
            timestamp=time.time()
        )
        
        # Check for level up
        level_up_data = self._check_level_up()
        
        result = {
            'xp_awarded': amount,
            'reason': reason,
            'old_xp': old_xp,
            'new_xp': self.character['xp'],
            'old_level': old_level,
            'new_level': self.character['level'],
            'level_up': level_up_data['leveled_up'],
            'new_abilities': level_up_data.get('new_abilities', [])
        }
        
        return result
    
    def _check_level_up(self) -> Dict:
        """Check if character should level up and apply changes"""
        level_thresholds = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500]
        
        old_level = self.character['level']
        current_xp = self.character['xp']
        
        # Find new level
        new_level = 1  # Start at level 1
        for i, threshold in enumerate(level_thresholds[1:], 1):  # Skip level 0, start from level 1
            if current_xp >= threshold:
                new_level = i + 1
        
        # Ensure we don't exceed max level
        new_level = min(new_level, len(level_thresholds))
        
        if new_level > old_level:
            # Level up!
            self.character['level'] = new_level
            
            # Increase HP and Energy
            hp_gain = self._calculate_hp_gain()
            energy_gain = self._calculate_energy_gain()
            
            self.character['resources']['max_hp'] += hp_gain
            self.character['resources']['hp'] = self.character['resources']['max_hp']  # Full heal
            self.character['resources']['max_energy'] += energy_gain
            self.character['resources']['energy'] = self.character['resources']['max_energy']
            
            # Get new abilities
            new_abilities = self._get_level_abilities(new_level)
            
            return {
                'leveled_up': True,
                'levels_gained': new_level - old_level,
                'hp_gained': hp_gain,
                'energy_gained': energy_gain,
                'new_abilities': new_abilities
            }
        
        return {'leveled_up': False}
    
    def _calculate_hp_gain(self) -> int:
        """Calculate HP gain based on class"""
        class_hp_gains = {
            'Warrior': 8,
            'Cleric': 6,
            'Rogue': 5,
            'Mage': 4
        }
        return class_hp_gains.get(self.character['class'], 6)
    
    def _calculate_energy_gain(self) -> int:
        """Calculate energy gain per level"""
        return 2
    
    def _get_level_abilities(self, level: int) -> List[str]:
        """Get new abilities unlocked at this level"""
        class_abilities = {
            'Warrior': {
                2: ["Power Attack: Deal +2 damage but -2 accuracy"],
                3: ["Second Wind: Recover 1d6+2 HP once per combat"],
                4: ["Weapon Mastery: +1 to all weapon attacks"],
                5: ["Intimidating Presence: +3 to Intimidation checks"]
            },
            'Mage': {
                2: ["Magic Missile: Guaranteed hit spell"],
                3: ["Shield: +2 AC for one combat"],
                4: ["Fireball: Area damage spell"],
                5: ["Counterspell: Negate enemy magic"]
            },
            'Rogue': {
                2: ["Sneak Attack: +1d6 damage when hidden"],
                3: ["Evasion: Half damage from area effects"],
                4: ["Uncanny Dodge: Reduce damage by 2"],
                5: ["Expertise: Double skill bonuses"]
            },
            'Cleric': {
                2: ["Healing Word: Restore 1d4+2 HP"],
                3: ["Turn Undead: Frighten undead enemies"],
                4: ["Divine Strike: +1d6 radiant damage"],
                5: ["Greater Heal: Restore 2d6+4 HP"]
            }
        }
        
        character_class = self.character.get('class', 'Warrior')
        return class_abilities.get(character_class, {}).get(level, [])
    
    def get_current_state(self) -> Dict:
        """Get complete current game state"""
        return {
            'character': self.character.copy(),
            'session': self.session_data.copy(),
            'pending_rolls': [asdict(roll) for roll in self.pending_rolls],
            'recent_actions': [asdict(action) for action in self.action_history[-5:]],
            'rule_violations': self.rule_violations.copy(),
            # Add progression state for local runner compatibility
            'current_location': self.progression_state['current_location'],
            'story_progress': self.progression_state['story_progress'],
            'turn_count': self.session_data['turn_count']
        }
    
    def clear_pending_rolls(self):
        """Clear pending rolls after they've been used"""
        self.pending_rolls.clear()
    
    def increment_turn(self):
        """Increment turn counter and check for context refresh"""
        self.session_data['turn_count'] += 1
        
        # Check if context refresh is needed (every 5 turns)
        if self.session_data['turn_count'] % 5 == 0:
            self.session_data['last_context_refresh'] = self.session_data['turn_count']
            return True  # Signal that context should be refreshed
        
        return False
    
    def add_rule_violation(self, violation: str):
        """Track rule violations for debugging"""
        self.rule_violations.append(f"Turn {self.session_data['turn_count']}: {violation}")
    
    def save_state(self) -> str:
        """Serialize game state for persistence"""
        state = self.get_current_state()
        return json.dumps(state, indent=2)
    
    @classmethod
    def load_state(cls, state_json: str) -> 'GameStateManager':
        """Load game state from serialized data"""
        state = json.loads(state_json)
        manager = cls(state['character'])
        manager.session_data = state['session']
        manager.rule_violations = state['rule_violations']
        return manager 
   
    def update_location(self, new_location: str, reason: str = "player_action") -> Dict:
        """Update current location and track progression"""
        old_location = self.progression_state['current_location']
        
        if new_location != old_location:
            self.progression_state['current_location'] = new_location
            self.progression_state['turns_at_current_location'] = 0
            
            if new_location not in self.progression_state['discovered_locations']:
                self.progression_state['discovered_locations'].append(new_location)
                self.progression_state['story_progress'] += 1
            
            return {
                'location_changed': True,
                'old_location': old_location,
                'new_location': new_location,
                'story_progress': self.progression_state['story_progress'],
                'reason': reason
            }
        else:
            self.progression_state['turns_at_current_location'] += 1
            return {'location_changed': False, 'turns_at_location': self.progression_state['turns_at_current_location']}
    
    def should_force_progression(self) -> Dict:
        """Check if we should force story progression to prevent loops"""
        turns_at_location = self.progression_state['turns_at_current_location']
        current_location = self.progression_state['current_location']
        
        # Force progression after 3 turns at same location
        if turns_at_location >= 3:
            return {
                'should_force': True,
                'reason': f'stuck_at_{current_location}_for_{turns_at_location}_turns',
                'suggested_action': 'force_location_change'
            }
        
        # Force progression if story hasn't advanced in many turns
        if self.session_data['turn_count'] > 5 and self.progression_state['story_progress'] == 0:
            return {
                'should_force': True,
                'reason': 'no_story_progress',
                'suggested_action': 'advance_story'
            }
        
        return {'should_force': False}
    
    def get_progression_context(self) -> Dict:
        """Get rich context for AI about current progression state"""
        return {
            'current_location': self.progression_state['current_location'],
            'story_progress': self.progression_state['story_progress'],
            'turns_at_location': self.progression_state['turns_at_current_location'],
            'discovered_locations': self.progression_state['discovered_locations'],
            'world_state': self.progression_state['world_state'],
            'total_turns': self.session_data['turn_count'],
            'should_force_progression': self.should_force_progression()
        }
    
    def parse_location_from_response(self, ai_response: str) -> Optional[str]:
        """Parse location changes from AI response"""
        # Look for location indicators in AI response
        location_keywords = {
            'ashbrook': 'ashbrook_village',
            'village': 'ashbrook_village', 
            'cave': 'crystal_cave',
            'forest': 'dark_forest',
            'outskirts': 'village_outskirts'
        }
        
        response_lower = ai_response.lower()
        for keyword, location in location_keywords.items():
            # Original specific phrases
            if f"arrive at {keyword}" in response_lower or f"reach {keyword}" in response_lower or f"enter {keyword}" in response_lower:
                return location
            # Add more natural language patterns
            if f"approaching {keyword}" in response_lower or f"heading to {keyword}" in response_lower or f"moving toward {keyword}" in response_lower:
                return location
            # Add movement-based triggers
            if f"path to {keyword}" in response_lower or f"road to {keyword}" in response_lower:
                # Only trigger location change if player is actively moving
                if any(move_word in response_lower for move_word in ['moving', 'walking', 'heading', 'traveling', 'going']):
                    return location
        
        return None
    
    def advance_story_progress(self, event_description: str) -> bool:
        """Advance story progress for meaningful events"""
        if event_description not in self.progression_state['completed_events']:
            self.progression_state['completed_events'].append(event_description)
            self.progression_state['story_progress'] += 1
            return True
        return False