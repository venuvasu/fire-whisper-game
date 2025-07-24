"""
Character Sheet System - Make players feel ownership and progression
"""

class CharacterSheet:
    def __init__(self, character_data=None):
        if character_data is None:
            character_data = self.create_default_character()
        
        self.name = character_data.get('name', 'Adventurer')
        self.level = character_data.get('level', 1)
        self.xp = character_data.get('xp', 0)
        self.class_name = character_data.get('class', 'Warrior')
        
        # Core stats (8-18 range, 10 = average)
        self.strength = character_data.get('strength', 12)
        self.dexterity = character_data.get('dexterity', 12)
        self.intelligence = character_data.get('intelligence', 12)
        self.charisma = character_data.get('charisma', 12)
        
        # Resources
        self.hp = character_data.get('hp', self.max_hp())
        self.energy = character_data.get('energy', self.max_energy())
        
        # Progression
        self.skills = character_data.get('skills', {})
        self.achievements = character_data.get('achievements', [])
        
        # Emberlyn relationship
        self.emberlyn_bond = character_data.get('emberlyn_bond', 1)
    
    def create_default_character(self):
        return {
            'name': 'Adventurer',
            'level': 1,
            'xp': 0,
            'class': 'Warrior',
            'strength': 14,
            'dexterity': 12,
            'intelligence': 10,
            'charisma': 12,
            'hp': 25,
            'energy': 10,
            'skills': {'Combat': 1, 'Survival': 1},
            'achievements': [],
            'emberlyn_bond': 1
        }
    
    def max_hp(self):
        """Calculate max HP based on level and class"""
        base_hp = 20
        level_bonus = (self.level - 1) * 5
        class_bonus = {'Warrior': 10, 'Mage': 5, 'Rogue': 7, 'Cleric': 8}.get(self.class_name, 7)
        return base_hp + level_bonus + class_bonus
    
    def max_energy(self):
        """Calculate max energy for special abilities"""
        return 10 + (self.level - 1) * 2
    
    def get_stat_modifier(self, stat_name):
        """Get modifier for stat (used in dice rolls)"""
        stat_value = getattr(self, stat_name.lower(), 10)
        return max(0, (stat_value - 10) // 2)
    
    def xp_to_next_level(self):
        """XP needed for next level"""
        thresholds = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500, 5500]
        if self.level >= len(thresholds):
            return 1000 * self.level  # High level scaling
        return thresholds[self.level] if self.level < len(thresholds) else thresholds[-1]
    
    def add_xp(self, amount, reason=""):
        """Add XP and check for level up"""
        old_level = self.level
        self.xp += amount
        
        # Check for level up
        while self.xp >= self.xp_to_next_level() and self.level < 20:
            self.level += 1
            self.hp = self.max_hp()  # Full heal on level up
            self.energy = self.max_energy()
        
        level_up = self.level > old_level
        return {
            'xp_gained': amount,
            'reason': reason,
            'total_xp': self.xp,
            'level_up': level_up,
            'new_level': self.level if level_up else None
        }
    
    def get_display_sheet(self):
        """Get formatted character sheet for display"""
        next_level_xp = self.xp_to_next_level()
        xp_progress = f"{self.xp}/{next_level_xp}"
        
        return f"""
📊 **{self.name}** - Level {self.level} {self.class_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💪 STR: {self.strength} (+{self.get_stat_modifier('strength')}) | 🏃 DEX: {self.dexterity} (+{self.get_stat_modifier('dexterity')})
🧠 INT: {self.intelligence} (+{self.get_stat_modifier('intelligence')}) | 💬 CHA: {self.charisma} (+{self.get_stat_modifier('charisma')})

❤️ HP: {self.hp}/{self.max_hp()} | ⚡ Energy: {self.energy}/{self.max_energy()}
✨ XP: {xp_progress} | 🧚‍♀️ Emberlyn Bond: Level {self.emberlyn_bond}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    def get_skill_bonus(self, skill_name):
        """Get bonus for specific skill"""
        return self.skills.get(skill_name, 0)
    
    def improve_skill(self, skill_name, amount=1):
        """Improve a skill"""
        if skill_name not in self.skills:
            self.skills[skill_name] = 0
        self.skills[skill_name] += amount
        return self.skills[skill_name]
    
    def add_achievement(self, achievement):
        """Add achievement if not already earned"""
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            return True
        return False
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'name': self.name,
            'level': self.level,
            'xp': self.xp,
            'class': self.class_name,
            'strength': self.strength,
            'dexterity': self.dexterity,
            'intelligence': self.intelligence,
            'charisma': self.charisma,
            'hp': self.hp,
            'energy': self.energy,
            'skills': self.skills,
            'achievements': self.achievements,
            'emberlyn_bond': self.emberlyn_bond
        }