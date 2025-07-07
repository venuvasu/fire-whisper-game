"""
Battle System - Manages combat encounters with enemies
"""
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class EnemyType(Enum):
    IMP = "imp"
    BANDIT = "bandit"
    GOBLIN = "goblin"
    WOLF = "wolf"
    SKELETON = "skeleton"
    ORC = "orc"
    TROLL = "troll"

@dataclass
class Enemy:
    name: str
    enemy_type: EnemyType
    max_hp: int
    current_hp: int
    attack_bonus: int
    defense: int
    damage_dice: str  # e.g., "1d6+2"
    special_abilities: List[str]
    loot_table: List[Dict]
    
    @property
    def is_alive(self) -> bool:
        return self.current_hp > 0
    
    @property
    def health_percentage(self) -> float:
        return self.current_hp / self.max_hp if self.max_hp > 0 else 0

class BattleState(Enum):
    NO_BATTLE = "no_battle"
    BATTLE_START = "battle_start"
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    BATTLE_END = "battle_end"

class BattleSystem:
    def __init__(self):
        self.current_enemies: List[Enemy] = []
        self.battle_state = BattleState.NO_BATTLE
        self.battle_round = 0
        self.battle_log: List[str] = []
        
        # Enemy templates
        self.enemy_templates = {
            EnemyType.IMP: {
                'name': 'Forest Imp',
                'max_hp': 8,
                'attack_bonus': 3,
                'defense': 12,
                'damage_dice': '1d4+1',
                'special_abilities': ['fire_dart', 'teleport'],
                'loot_table': [
                    {'item': 'Fire Crystal Shard', 'chance': 0.3},
                    {'item': 'Silver Coins', 'chance': 0.6, 'amount': '1d6'}
                ]
            },
            EnemyType.BANDIT: {
                'name': 'Highway Bandit',
                'max_hp': 15,
                'attack_bonus': 4,
                'defense': 13,
                'damage_dice': '1d6+2',
                'special_abilities': ['dirty_fighting'],
                'loot_table': [
                    {'item': 'Leather Armor', 'chance': 0.2},
                    {'item': 'Silver Coins', 'chance': 0.8, 'amount': '2d6'}
                ]
            },
            EnemyType.GOBLIN: {
                'name': 'Cave Goblin',
                'max_hp': 12,
                'attack_bonus': 3,
                'defense': 11,
                'damage_dice': '1d6+1',
                'special_abilities': ['pack_tactics'],
                'loot_table': [
                    {'item': 'Rusty Dagger', 'chance': 0.3},
                    {'item': 'Healing Potion', 'chance': 0.2}
                ]
            }
        }
    
    def should_trigger_battle(self, situation_text: str, player_action: str) -> bool:
        """Determine if a battle should be triggered based on context"""
        
        # Battle triggers
        combat_keywords = ['attack', 'fight', 'charge', 'strike', 'battle', 'combat']
        enemy_keywords = ['imp', 'bandit', 'goblin', 'monster', 'creature', 'enemy']
        
        # Check if player is taking combat action
        player_wants_combat = any(word in player_action.lower() for word in combat_keywords)
        
        # Check if enemies are present in situation
        enemies_present = any(word in situation_text.lower() for word in enemy_keywords)
        
        # Check if already in battle
        already_in_battle = self.battle_state != BattleState.NO_BATTLE
        
        return (player_wants_combat and enemies_present) or already_in_battle
    
    def start_battle(self, situation_text: str) -> Dict:
        """Initialize a battle based on the current situation"""
        
        # Determine enemy types from situation
        enemies_to_spawn = self._determine_enemies_from_situation(situation_text)
        
        # Spawn enemies
        self.current_enemies = []
        for enemy_type, count in enemies_to_spawn.items():
            for i in range(count):
                enemy = self._create_enemy(enemy_type, i + 1)
                self.current_enemies.append(enemy)
        
        self.battle_state = BattleState.BATTLE_START
        self.battle_round = 1
        self.battle_log = []
        
        return {
            'battle_started': True,
            'enemies': [self._enemy_to_dict(e) for e in self.current_enemies],
            'battle_status': self._get_battle_status()
        }
    
    def process_combat_action(self, player_action: str, player_stats: Dict) -> Dict:
        """Process a combat action and return results"""
        
        if self.battle_state == BattleState.NO_BATTLE:
            return {'error': 'No battle in progress'}
        
        results = {
            'player_damage_dealt': 0,
            'enemy_damage_taken': 0,
            'enemies_defeated': [],
            'battle_log': [],
            'battle_continues': True,
            'loot_gained': []
        }
        
        # Player attacks
        if any(word in player_action.lower() for word in ['attack', 'strike', 'fight', 'charge']):
            attack_result = self._player_attack(player_stats)
            results.update(attack_result)
        
        # Check if all enemies defeated
        if not any(e.is_alive for e in self.current_enemies):
            results['battle_continues'] = False
            results['victory'] = True
            results['loot_gained'] = self._generate_loot()
            self.battle_state = BattleState.NO_BATTLE
            return results
        
        # Enemy turn
        if results['battle_continues']:
            enemy_result = self._enemies_attack()
            results['enemy_damage_taken'] = enemy_result['damage_to_player']
            results['battle_log'].extend(enemy_result['battle_log'])
        
        # Update battle status
        results['battle_status'] = self._get_battle_status()
        
        return results
    
    def _determine_enemies_from_situation(self, situation: str) -> Dict[EnemyType, int]:
        """Determine what enemies to spawn based on situation text"""
        
        situation_lower = situation.lower()
        enemies = {}
        
        if 'imp' in situation_lower:
            # Count mentions to determine number
            imp_count = situation_lower.count('imp')
            enemies[EnemyType.IMP] = max(1, min(imp_count, 3))  # 1-3 imps
        
        if 'bandit' in situation_lower:
            enemies[EnemyType.BANDIT] = 1
        
        if 'goblin' in situation_lower:
            goblin_count = situation_lower.count('goblin')
            enemies[EnemyType.GOBLIN] = max(1, min(goblin_count, 2))
        
        # Default to single imp if no specific enemies mentioned
        if not enemies:
            enemies[EnemyType.IMP] = 1
        
        return enemies
    
    def _create_enemy(self, enemy_type: EnemyType, number: int = 1) -> Enemy:
        """Create an enemy instance from template"""
        
        template = self.enemy_templates[enemy_type]
        name = f"{template['name']}"
        if number > 1:
            name += f" #{number}"
        
        return Enemy(
            name=name,
            enemy_type=enemy_type,
            max_hp=template['max_hp'],
            current_hp=template['max_hp'],
            attack_bonus=template['attack_bonus'],
            defense=template['defense'],
            damage_dice=template['damage_dice'],
            special_abilities=template['special_abilities'],
            loot_table=template['loot_table']
        )
    
    def _player_attack(self, player_stats: Dict) -> Dict:
        """Process player attack against enemies"""
        
        # Choose target (first living enemy)
        target = next((e for e in self.current_enemies if e.is_alive), None)
        if not target:
            return {'error': 'No valid targets'}
        
        # Calculate attack roll
        attack_roll = random.randint(1, 20)
        strength_mod = max(0, (player_stats.get('strength', 10) - 10) // 2)
        combat_skill = player_stats.get('skills', {}).get('Combat', 0)
        
        total_attack = attack_roll + strength_mod + combat_skill
        
        results = {
            'attack_roll': attack_roll,
            'attack_total': total_attack,
            'target_defense': target.defense,
            'hit': total_attack >= target.defense,
            'battle_log': []
        }
        
        if results['hit']:
            # Calculate damage
            damage = self._roll_damage('1d8', strength_mod)  # Player weapon damage
            target.current_hp = max(0, target.current_hp - damage)
            
            results['damage_dealt'] = damage
            results['target_hp_remaining'] = target.current_hp
            results['battle_log'].append(f"You strike {target.name} for {damage} damage!")
            
            if target.current_hp <= 0:
                results['battle_log'].append(f"{target.name} is defeated!")
                results['enemies_defeated'].append(target.name)
        else:
            results['battle_log'].append(f"Your attack misses {target.name}!")
        
        return results
    
    def _enemies_attack(self) -> Dict:
        """Process enemy attacks against player"""
        
        total_damage = 0
        battle_log = []
        
        for enemy in self.current_enemies:
            if not enemy.is_alive:
                continue
            
            # Enemy attack roll
            attack_roll = random.randint(1, 20)
            total_attack = attack_roll + enemy.attack_bonus
            
            # Assume player AC of 12 + DEX mod (simplified)
            player_ac = 12  # Could be calculated from player stats
            
            if total_attack >= player_ac:
                damage = self._roll_damage(enemy.damage_dice)
                total_damage += damage
                battle_log.append(f"{enemy.name} hits you for {damage} damage!")
            else:
                battle_log.append(f"{enemy.name} misses!")
        
        return {
            'damage_to_player': total_damage,
            'battle_log': battle_log
        }
    
    def _roll_damage(self, damage_dice: str, bonus: int = 0) -> int:
        """Roll damage dice (e.g., '1d6+2')"""
        
        # Simple parser for XdY+Z format
        if '+' in damage_dice:
            dice_part, bonus_part = damage_dice.split('+')
            bonus += int(bonus_part)
        elif '-' in damage_dice:
            dice_part, bonus_part = damage_dice.split('-')
            bonus -= int(bonus_part)
        else:
            dice_part = damage_dice
        
        if 'd' in dice_part:
            num_dice, die_size = map(int, dice_part.split('d'))
            total = sum(random.randint(1, die_size) for _ in range(num_dice))
        else:
            total = int(dice_part)
        
        return max(1, total + bonus)  # Minimum 1 damage
    
    def _generate_loot(self) -> List[Dict]:
        """Generate loot from defeated enemies"""
        
        loot = []
        for enemy in self.current_enemies:
            if enemy.current_hp <= 0:  # Defeated
                for loot_item in enemy.loot_table:
                    if random.random() < loot_item['chance']:
                        item = {'name': loot_item['item']}
                        if 'amount' in loot_item:
                            # Roll for amount
                            amount = self._roll_damage(loot_item['amount'])
                            item['amount'] = amount
                        loot.append(item)
        
        return loot
    
    def _get_battle_status(self) -> Dict:
        """Get current battle status for display"""
        
        return {
            'in_battle': self.battle_state != BattleState.NO_BATTLE,
            'round': self.battle_round,
            'enemies': [
                {
                    'name': e.name,
                    'hp': e.current_hp,
                    'max_hp': e.max_hp,
                    'health_percent': int(e.health_percentage * 100),
                    'alive': e.is_alive
                }
                for e in self.current_enemies
            ]
        }
    
    def _enemy_to_dict(self, enemy: Enemy) -> Dict:
        """Convert enemy to dictionary for serialization"""
        return {
            'name': enemy.name,
            'type': enemy.enemy_type.value,
            'hp': enemy.current_hp,
            'max_hp': enemy.max_hp,
            'alive': enemy.is_alive
        }
    
    def get_battle_summary(self) -> str:
        """Get formatted battle status for display"""
        
        if self.battle_state == BattleState.NO_BATTLE:
            return ""
        
        status_lines = [f"\n⚔️ **BATTLE STATUS - Round {self.battle_round}**"]
        
        for enemy in self.current_enemies:
            if enemy.is_alive:
                health_bar = "█" * int(enemy.health_percentage * 10)
                health_bar += "░" * (10 - len(health_bar))
                status_lines.append(
                    f"🔴 {enemy.name}: {enemy.current_hp}/{enemy.max_hp} HP [{health_bar}]"
                )
            else:
                status_lines.append(f"💀 {enemy.name}: DEFEATED")
        
        return "\n".join(status_lines) + "\n"