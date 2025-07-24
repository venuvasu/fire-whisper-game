"""
Visible Dice System - Make players feel their choices and stats matter
"""
import random

class DiceRoll:
    def __init__(self, character_sheet, action_type, difficulty="normal"):
        self.character = character_sheet
        self.action_type = action_type
        self.difficulty = difficulty
        self.modifiers = []
        self.total_modifier = 0
        self.roll_result = 0
        self.success = False
        
    def add_modifier(self, name, value, reason=""):
        """Add a modifier to the roll"""
        self.modifiers.append({
            'name': name,
            'value': value,
            'reason': reason
        })
        self.total_modifier += value
    
    def calculate_modifiers(self, stat_name, skill_name=None):
        """Calculate all modifiers for this roll"""
        # Base difficulty
        difficulty_values = {
            'trivial': 5,
            'easy': 8,
            'normal': 12,
            'hard': 15,
            'extreme': 18
        }
        target = difficulty_values.get(self.difficulty, 12)
        
        # Stat modifier
        stat_mod = self.character.get_stat_modifier(stat_name)
        if stat_mod > 0:
            self.add_modifier(f"{stat_name.title()}", stat_mod, f"Your {stat_name} of {getattr(self.character, stat_name.lower())}")
        
        # Skill modifier
        if skill_name:
            skill_mod = self.character.get_skill_bonus(skill_name)
            if skill_mod > 0:
                self.add_modifier(f"{skill_name}", skill_mod, f"Your {skill_name} training")
        
        # Class bonus
        class_bonuses = {
            'Warrior': {'Combat': 2, 'Intimidation': 1},
            'Mage': {'Magic': 3, 'Knowledge': 2},
            'Rogue': {'Stealth': 2, 'Lockpicking': 2, 'Deception': 1},
            'Cleric': {'Healing': 3, 'Persuasion': 1}
        }
        
        if self.character.class_name in class_bonuses:
            for bonus_skill, bonus_value in class_bonuses[self.character.class_name].items():
                if skill_name == bonus_skill:
                    self.add_modifier("Class Specialty", bonus_value, f"Your {self.character.class_name} training")
        
        return target
    
    def roll(self, stat_name, skill_name=None, dice_pool=None):
        """Perform the actual roll"""
        target = self.calculate_modifiers(stat_name, skill_name)
        
        # Use provided dice or roll new one
        if dice_pool and len(dice_pool) > 0:
            self.roll_result = dice_pool[0]  # Use first available dice
        else:
            self.roll_result = random.randint(1, 20)
        
        # Calculate success
        final_result = self.roll_result + self.total_modifier
        self.success = final_result >= target
        
        return {
            'roll': self.roll_result,
            'modifiers': self.modifiers,
            'total_modifier': self.total_modifier,
            'final_result': final_result,
            'target': target,
            'success': self.success,
            'description': self.get_roll_description()
        }
    
    def get_roll_description(self):
        """Get formatted description of the roll"""
        modifier_text = ""
        if self.modifiers:
            mod_descriptions = []
            for mod in self.modifiers:
                sign = "+" if mod['value'] >= 0 else ""
                mod_descriptions.append(f"{mod['name']} {sign}{mod['value']}")
            modifier_text = f" ({' + '.join(mod_descriptions)})"
        
        result_text = "SUCCESS" if self.success else "FAILURE"
        final_result = self.roll_result + self.total_modifier
        
        return f"""
🎲 **Rolling for {self.action_type}...**
**{self.roll_result}** + {self.total_modifier}{modifier_text} = **{final_result}**
Target: {self.calculate_modifiers('strength')} | Result: **{result_text}**
"""

def create_roll_choice_prompt(character, situation, options):
    """Create a prompt that shows player agency in approach"""
    prompt = f"\n{situation}\n\n"
    
    for i, option in enumerate(options, 1):
        stat = option['stat']
        skill = option.get('skill', '')
        description = option['description']
        
        stat_bonus = character.get_stat_modifier(stat)
        skill_bonus = character.get_skill_bonus(skill) if skill else 0
        total_bonus = stat_bonus + skill_bonus
        
        bonus_text = f" (+{total_bonus})" if total_bonus > 0 else ""
        prompt += f"[{i}] {description} ({stat.title()}{f'/{skill}' if skill else ''}{bonus_text})\n"
    
    prompt += "\nWhat do you do?"
    return prompt

# Example usage for Fire Whisper
def create_fire_whisper_roll_options(situation_type):
    """Create contextual roll options for different situations"""
    
    if situation_type == "locked_door":
        return [
            {
                'stat': 'strength',
                'skill': 'Combat',
                'description': 'Break down the door with brute force',
                'consequence_success': 'The door splinters loudly - you\'re through but everyone heard it',
                'consequence_failure': 'You hurt your shoulder and the door holds firm'
            },
            {
                'stat': 'dexterity', 
                'skill': 'Lockpicking',
                'description': 'Pick the lock carefully',
                'consequence_success': 'The lock clicks open silently',
                'consequence_failure': 'Your picks break and the lock jams'
            },
            {
                'stat': 'intelligence',
                'skill': 'Knowledge',
                'description': 'Look for hidden mechanisms or clues',
                'consequence_success': 'You notice a hidden switch that opens the door',
                'consequence_failure': 'You waste time searching but find nothing useful'
            }
        ]
    
    elif situation_type == "hostile_guard":
        return [
            {
                'stat': 'charisma',
                'skill': 'Persuasion', 
                'description': 'Try to talk your way past',
                'consequence_success': 'The guard believes your story and lets you pass',
                'consequence_failure': 'The guard becomes suspicious and calls for backup'
            },
            {
                'stat': 'charisma',
                'skill': 'Deception',
                'description': 'Lie convincingly about your purpose',
                'consequence_success': 'Your false credentials fool the guard completely',
                'consequence_failure': 'The guard sees through your lie and raises the alarm'
            },
            {
                'stat': 'dexterity',
                'skill': 'Stealth',
                'description': 'Sneak past while distracted',
                'consequence_success': 'You slip by unnoticed in the shadows',
                'consequence_failure': 'You knock over something and alert the guard'
            }
        ]
    
    return []