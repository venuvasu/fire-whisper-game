"""
Dice Rolling System - Pure randomness outside of AI
Handles all dice mechanics and feeds results to AI for narrative response
"""
import random
import time
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

class DifficultyClass(Enum):
    """Standard D&D-style difficulty classes"""
    TRIVIAL = 5
    EASY = 10
    MEDIUM = 15
    HARD = 20
    VERY_HARD = 25
    NEARLY_IMPOSSIBLE = 30

class DiceResult(Enum):
    """Outcome categories for dice rolls"""
    CRITICAL_FAILURE = "critical_failure"
    FAILURE = "failure" 
    SUCCESS = "success"
    CRITICAL_SUCCESS = "critical_success"

@dataclass
class RollResult:
    """Complete dice roll result"""
    dice_rolled: str  # e.g. "1d20+3"
    raw_roll: int     # The actual dice result
    modifier: int     # Applied modifier
    total: int        # Final result
    difficulty: int   # Target number
    result: DiceResult # Success/failure category
    margin: int       # How much over/under target
    description: str  # Human readable description

class DiceSystem:
    """
    Pure randomness system - no AI involved
    Handles all dice mechanics and probability
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
        else:
            # Use current time for true randomness
            random.seed(int(time.time() * 1000000) % 2**32)
    
    def roll_dice(self, sides: int = 20, count: int = 1) -> List[int]:
        """Roll dice and return raw results"""
        return [random.randint(1, sides) for _ in range(count)]
    
    def roll_d20(self, modifier: int = 0, advantage: bool = False, disadvantage: bool = False) -> Tuple[int, List[int]]:
        """
        Roll 1d20 with optional advantage/disadvantage
        Returns (final_result, raw_rolls)
        """
        if advantage and disadvantage:
            # Cancel out
            rolls = self.roll_dice(20, 1)
        elif advantage:
            rolls = self.roll_dice(20, 2)
            rolls = [max(rolls)]  # Take higher
        elif disadvantage:
            rolls = self.roll_dice(20, 2) 
            rolls = [min(rolls)]  # Take lower
        else:
            rolls = self.roll_dice(20, 1)
        
        final_result = rolls[0] + modifier
        return final_result, rolls
    
    def make_ability_check(self, ability_modifier: int, difficulty: DifficultyClass, 
                          advantage: bool = False, disadvantage: bool = False) -> RollResult:
        """Make a standard ability check"""
        dc = difficulty.value
        total, raw_rolls = self.roll_d20(ability_modifier, advantage, disadvantage)
        raw_roll = raw_rolls[0]
        
        # Determine result category
        if raw_roll == 1:
            result = DiceResult.CRITICAL_FAILURE
        elif raw_roll == 20:
            result = DiceResult.CRITICAL_SUCCESS
        elif total >= dc:
            result = DiceResult.SUCCESS
        else:
            result = DiceResult.FAILURE
        
        margin = total - dc
        
        # Generate description
        dice_str = f"1d20+{ability_modifier}" if ability_modifier >= 0 else f"1d20{ability_modifier}"
        if advantage:
            dice_str += " (advantage)"
        elif disadvantage:
            dice_str += " (disadvantage)"
        
        description = f"Rolled {dice_str}: {raw_roll}+{ability_modifier}={total} vs DC {dc}"
        
        return RollResult(
            dice_rolled=dice_str,
            raw_roll=raw_roll,
            modifier=ability_modifier,
            total=total,
            difficulty=dc,
            result=result,
            margin=margin,
            description=description
        )
    
    def make_action_check(self, character_stats: Dict[str, int], action_type: str, 
                         context: Dict[str, Any] = None) -> RollResult:
        """
        Make contextual action check based on action type
        Maps actions to appropriate ability scores and difficulties
        """
        context = context or {}
        
        # Map action types to ability scores and base difficulties
        action_mapping = {
            'examine': ('intelligence', DifficultyClass.EASY),
            'investigate': ('intelligence', DifficultyClass.MEDIUM),
            'move': ('dexterity', DifficultyClass.EASY),
            'sneak': ('dexterity', DifficultyClass.MEDIUM),
            'climb': ('strength', DifficultyClass.MEDIUM),
            'social': ('charisma', DifficultyClass.MEDIUM),
            'persuade': ('charisma', DifficultyClass.HARD),
            'intimidate': ('charisma', DifficultyClass.MEDIUM),
            'magic': ('intelligence', DifficultyClass.MEDIUM),
            'perception': ('wisdom', DifficultyClass.MEDIUM),
            'survival': ('wisdom', DifficultyClass.MEDIUM),
            'athletics': ('strength', DifficultyClass.MEDIUM),
            'acrobatics': ('dexterity', DifficultyClass.MEDIUM),
        }
        
        # Default to intelligence/medium if action not mapped
        ability, base_difficulty = action_mapping.get(action_type.lower(), ('intelligence', DifficultyClass.MEDIUM))
        
        # Get ability modifier (D&D style: (score - 10) // 2)
        ability_score = character_stats.get(ability, 10)
        ability_modifier = (ability_score - 10) // 2
        
        # Adjust difficulty based on context
        difficulty = self._adjust_difficulty(base_difficulty, context)
        
        # Check for advantage/disadvantage
        advantage = context.get('advantage', False)
        disadvantage = context.get('disadvantage', False)
        
        return self.make_ability_check(ability_modifier, difficulty, advantage, disadvantage)
    
    def _adjust_difficulty(self, base_difficulty: DifficultyClass, context: Dict[str, Any]) -> DifficultyClass:
        """Adjust difficulty based on context"""
        difficulty_value = base_difficulty.value
        
        # Environmental factors
        if context.get('favorable_conditions'):
            difficulty_value -= 2
        if context.get('unfavorable_conditions'):
            difficulty_value += 2
        
        # Character state
        if context.get('injured'):
            difficulty_value += 3
        if context.get('well_rested'):
            difficulty_value -= 1
        
        # Equipment/tools
        if context.get('proper_tools'):
            difficulty_value -= 2
        if context.get('improvised_tools'):
            difficulty_value += 2
        
        # Clamp to valid range
        difficulty_value = max(5, min(30, difficulty_value))
        
        # Find closest difficulty class
        for dc in DifficultyClass:
            if dc.value >= difficulty_value:
                return dc
        
        return DifficultyClass.NEARLY_IMPOSSIBLE
    
    def roll_damage(self, damage_dice: str) -> Tuple[int, List[int]]:
        """
        Roll damage dice (e.g., "1d6+2", "2d8", "1d4+1")
        Returns (total_damage, individual_rolls)
        """
        # Parse dice notation
        if '+' in damage_dice:
            dice_part, modifier_str = damage_dice.split('+')
            modifier = int(modifier_str)
        elif '-' in damage_dice:
            dice_part, modifier_str = damage_dice.split('-')
            modifier = -int(modifier_str)
        else:
            dice_part = damage_dice
            modifier = 0
        
        # Parse dice (e.g., "2d6" -> count=2, sides=6)
        if 'd' in dice_part:
            count_str, sides_str = dice_part.split('d')
            count = int(count_str) if count_str else 1
            sides = int(sides_str)
        else:
            # Just a number
            return int(dice_part) + modifier, [int(dice_part)]
        
        # Roll the dice
        rolls = self.roll_dice(sides, count)
        total = sum(rolls) + modifier
        
        return total, rolls

# Global dice system instance
_dice_system = None

def get_dice_system() -> DiceSystem:
    """Get global dice system instance"""
    global _dice_system
    if _dice_system is None:
        _dice_system = DiceSystem()
    return _dice_system