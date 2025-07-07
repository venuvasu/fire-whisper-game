"""
Dynamic Option Generator - Creates contextual, intelligent player choices
Generates 4-5 options based on character abilities, environment, and story stakes
"""

import random
from typing import Dict, List, Any, Tuple
from enum import Enum


class OptionCategory(Enum):
    COMBAT = "combat_action"
    STEALTH = "stealth_action"
    SOCIAL = "social_action"
    MAGIC = "magic_action"
    INVESTIGATION = "investigation"
    MOVEMENT = "movement"
    CREATIVE = "creative_solution"
    DEFENSIVE = "defensive_action"
    RESOURCE_USE = "resource_use"


class StakesLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EnvironmentType(Enum):
    SHRINE = "shrine"
    FOREST = "forest"
    VILLAGE = "village"
    DUNGEON = "dungeon"
    RUINS = "ruins"
    CAVE = "cave"
    TOWER = "tower"
    WATER = "water"
    MOUNTAIN = "mountain"


class OptionGenerator:
    """Generates contextually appropriate player options"""
    
    def __init__(self):
        self.class_abilities = {
            'Cleric': {
                'primary': ['divine_power', 'healing', 'blessing', 'turn_undead'],
                'secondary': ['wisdom', 'faith', 'protection', 'purification'],
                'stats': ['charisma', 'wisdom']
            },
            'Warrior': {
                'primary': ['combat', 'strength', 'charge', 'intimidate'],
                'secondary': ['tactics', 'endurance', 'leadership', 'weapon_mastery'],
                'stats': ['strength', 'constitution']
            },
            'Rogue': {
                'primary': ['stealth', 'sneak_attack', 'lockpicking', 'deception'],
                'secondary': ['agility', 'cunning', 'traps', 'sleight_of_hand'],
                'stats': ['dexterity', 'intelligence']
            },
            'Mage': {
                'primary': ['spellcasting', 'arcane_knowledge', 'elemental_magic', 'enchantment'],
                'secondary': ['study', 'ritual', 'magical_theory', 'divination'],
                'stats': ['intelligence', 'wisdom']
            }
        }
        
        self.environment_options = {
            EnvironmentType.SHRINE: {
                'elements': ['altar', 'holy_symbols', 'sacred_water', 'prayer_candles', 'ancient_texts'],
                'actions': ['pray', 'consecrate', 'purify', 'commune', 'bless']
            },
            EnvironmentType.FOREST: {
                'elements': ['trees', 'undergrowth', 'wildlife', 'streams', 'hidden_paths'],
                'actions': ['climb', 'hide', 'track', 'forage', 'navigate']
            },
            EnvironmentType.VILLAGE: {
                'elements': ['buildings', 'villagers', 'market', 'inn', 'well'],
                'actions': ['gather_info', 'trade', 'recruit_help', 'blend_in', 'investigate']
            },
            EnvironmentType.RUINS: {
                'elements': ['crumbling_walls', 'ancient_stones', 'mysterious_runes', 'hidden_chambers', 'artifacts'],
                'actions': ['explore', 'decipher', 'excavate', 'climb_ruins', 'search_debris']
            }
        }
        
        self.option_templates = {
            OptionCategory.COMBAT: {
                'Cleric': [
                    "Strike with your blessed {weapon} while chanting a protection prayer",
                    "Channel divine wrath to smite your enemies with holy light",
                    "Call upon your deity's power to enhance your combat abilities",
                    "Use your sacred symbol to turn undead or weaken dark creatures"
                ],
                'Warrior': [
                    "Charge forward with a battle cry, weapon raised high",
                    "Execute a tactical strike targeting your enemy's weak point",
                    "Use your superior strength to overpower the opposition",
                    "Employ defensive combat techniques while seeking an opening"
                ]
            },
            OptionCategory.MAGIC: {
                'Cleric': [
                    "Channel divine energy to {effect} (will drain spiritual reserves)",
                    "Perform a sacred ritual to invoke your deity's intervention",
                    "Use your healing magic to {healing_effect}",
                    "Create a protective ward using holy power"
                ],
                'Mage': [
                    "Cast {spell_type} magic to manipulate the situation",
                    "Use arcane knowledge to understand and counter magical effects",
                    "Weave a complex spell requiring precise concentration",
                    "Draw upon elemental forces to reshape the environment"
                ]
            },
            OptionCategory.SOCIAL: {
                'Cleric': [
                    "Use your divine authority to inspire faith and cooperation",
                    "Offer spiritual guidance and comfort to gain trust",
                    "Appeal to shared moral values and righteousness",
                    "Demonstrate your holy calling through compassionate action"
                ],
                'Rogue': [
                    "Use charm and wit to manipulate the situation to your advantage",
                    "Employ deception and misdirection to achieve your goals",
                    "Gather information through casual conversation and observation",
                    "Create a distraction while pursuing your true objective"
                ]
            }
        }
    
    def generate_scene_options(self, current_situation: str, character: Dict, 
                             story_context: Dict, environment: EnvironmentType = None) -> List[Dict]:
        """Generate 4-5 contextually appropriate options"""
        
        character_class = character.get('class', 'Cleric')
        character_level = character.get('level', 1)
        stakes_level = self._determine_stakes_level(story_context)
        
        # Determine environment if not provided
        if not environment:
            environment = self._detect_environment(current_situation)
        
        # Generate base options
        options = []
        
        # 1. Class-specific primary option (always include)
        primary_option = self._generate_class_primary_option(
            character_class, current_situation, environment, stakes_level
        )
        options.append(primary_option)
        
        # 2. Environmental interaction option
        env_option = self._generate_environmental_option(
            environment, current_situation, character, stakes_level
        )
        options.append(env_option)
        
        # 3. Social/diplomatic option (if appropriate)
        if self._should_include_social_option(current_situation):
            social_option = self._generate_social_option(
                character_class, current_situation, stakes_level
            )
            options.append(social_option)
        
        # 4. Creative/alternative solution
        creative_option = self._generate_creative_option(
            current_situation, character, environment, stakes_level
        )
        options.append(creative_option)
        
        # 5. Always include Emberlyn advice option
        emberlyn_option = {
            'text': "Ask Emberlyn for her guidance and insight",
            'category': 'advice',
            'risk_level': 'safe',
            'consequence_hint': "Emberlyn's fairy wisdom might reveal hidden opportunities"
        }
        options.append(emberlyn_option)
        
        return options
    
    def _generate_class_primary_option(self, character_class: str, situation: str, 
                                     environment: EnvironmentType, stakes: StakesLevel) -> Dict:
        """Generate the primary option based on character class"""
        
        abilities = self.class_abilities.get(character_class, self.class_abilities['Cleric'])
        
        if character_class == 'Cleric':
            if 'corruption' in situation.lower() or 'dark' in situation.lower():
                return {
                    'text': "Channel divine power to purify the corruption with holy light",
                    'category': 'magic',
                    'risk_level': 'medium',
                    'consequence_hint': "Will drain spiritual energy but could cleanse the area"
                }
            elif 'injured' in situation.lower() or 'wounded' in situation.lower():
                return {
                    'text': "Use your healing magic to tend to the wounded",
                    'category': 'magic',
                    'risk_level': 'low',
                    'consequence_hint': "Healing magic will restore health but uses divine energy"
                }
            else:
                return {
                    'text': "Call upon your deity's blessing to guide your actions",
                    'category': 'magic',
                    'risk_level': 'low',
                    'consequence_hint': "Divine guidance may reveal the best path forward"
                }
        
        elif character_class == 'Warrior':
            if stakes == StakesLevel.HIGH or stakes == StakesLevel.CRITICAL:
                return {
                    'text': "Charge into battle with a fierce war cry, weapon ready",
                    'category': 'combat',
                    'risk_level': 'high',
                    'consequence_hint': "Bold action could end the threat quickly or put you in danger"
                }
            else:
                return {
                    'text': "Take a defensive stance and assess the tactical situation",
                    'category': 'combat',
                    'risk_level': 'medium',
                    'consequence_hint': "Careful approach may reveal enemy weaknesses"
                }
        
        # Default fallback
        return {
            'text': f"Use your {character_class.lower()} training to handle this situation",
            'category': 'class_ability',
            'risk_level': 'medium',
            'consequence_hint': "Your specialized skills should prove useful here"
        }
    
    def _generate_environmental_option(self, environment: EnvironmentType, situation: str,
                                     character: Dict, stakes: StakesLevel) -> Dict:
        """Generate option based on environmental context"""
        
        env_data = self.environment_options.get(environment, self.environment_options[EnvironmentType.SHRINE])
        
        if environment == EnvironmentType.SHRINE:
            return {
                'text': "Examine the ancient runes and sacred symbols for hidden meaning",
                'category': 'investigation',
                'risk_level': 'low',
                'consequence_hint': "Ancient knowledge might reveal important clues"
            }
        elif environment == EnvironmentType.FOREST:
            return {
                'text': "Use the forest cover to approach stealthily through the undergrowth",
                'category': 'stealth',
                'risk_level': 'medium',
                'consequence_hint': "Stealth could provide advantage but risks getting lost"
            }
        elif environment == EnvironmentType.VILLAGE:
            return {
                'text': "Speak with the local villagers to gather information and support",
                'category': 'social',
                'risk_level': 'low',
                'consequence_hint': "Villagers might provide useful knowledge or assistance"
            }
        else:
            return {
                'text': "Carefully explore the immediate area for useful resources",
                'category': 'investigation',
                'risk_level': 'medium',
                'consequence_hint': "Thorough searching might uncover helpful items or clues"
            }
    
    def _generate_social_option(self, character_class: str, situation: str, 
                              stakes: StakesLevel) -> Dict:
        """Generate social/diplomatic option"""
        
        if 'enemy' in situation.lower() or 'hostile' in situation.lower():
            risk = 'high' if stakes in [StakesLevel.HIGH, StakesLevel.CRITICAL] else 'medium'
            return {
                'text': "Attempt to negotiate or find a peaceful resolution",
                'category': 'social',
                'risk_level': risk,
                'consequence_hint': "Diplomacy might avoid conflict but could be seen as weakness"
            }
        else:
            return {
                'text': "Use your charisma to inspire and rally others to your cause",
                'category': 'social',
                'risk_level': 'low',
                'consequence_hint': "Leadership could unite allies but draws attention"
            }
    
    def _generate_creative_option(self, situation: str, character: Dict, 
                                environment: EnvironmentType, stakes: StakesLevel) -> Dict:
        """Generate creative/alternative solution option"""
        
        creative_options = [
            {
                'text': "Look for an unconventional solution using your surroundings",
                'category': 'creative',
                'risk_level': 'medium',
                'consequence_hint': "Creative thinking might reveal unexpected opportunities"
            },
            {
                'text': "Combine your abilities in an innovative way to address the challenge",
                'category': 'creative',
                'risk_level': 'medium',
                'consequence_hint': "Unusual approaches could surprise enemies or solve problems uniquely"
            },
            {
                'text': "Wait and observe carefully before taking any action",
                'category': 'defensive',
                'risk_level': 'low',
                'consequence_hint': "Patience might reveal better opportunities but could waste time"
            }
        ]
        
        return random.choice(creative_options)
    
    def _determine_stakes_level(self, story_context: Dict) -> StakesLevel:
        """Determine current stakes level from story context"""
        
        turn_number = story_context.get('turn_number', 1)
        corruption_level = story_context.get('corruption_level', 'low')
        character_health = story_context.get('character_health_ratio', 1.0)
        
        # High stakes conditions
        if turn_number >= 12 or corruption_level == 'critical' or character_health < 0.3:
            return StakesLevel.CRITICAL
        elif turn_number >= 8 or corruption_level == 'high' or character_health < 0.6:
            return StakesLevel.HIGH
        elif turn_number >= 4 or corruption_level == 'medium':
            return StakesLevel.MEDIUM
        else:
            return StakesLevel.LOW
    
    def _detect_environment(self, situation: str) -> EnvironmentType:
        """Detect environment type from situation description"""
        
        situation_lower = situation.lower()
        
        if any(word in situation_lower for word in ['shrine', 'altar', 'temple', 'sacred']):
            return EnvironmentType.SHRINE
        elif any(word in situation_lower for word in ['forest', 'trees', 'woods', 'grove']):
            return EnvironmentType.FOREST
        elif any(word in situation_lower for word in ['village', 'town', 'villagers', 'houses']):
            return EnvironmentType.VILLAGE
        elif any(word in situation_lower for word in ['ruins', 'ancient', 'crumbling', 'stones']):
            return EnvironmentType.RUINS
        elif any(word in situation_lower for word in ['cave', 'cavern', 'underground', 'tunnel']):
            return EnvironmentType.CAVE
        else:
            return EnvironmentType.SHRINE  # Default
    
    def _should_include_social_option(self, situation: str) -> bool:
        """Determine if social option is appropriate for the situation"""
        
        social_keywords = ['villagers', 'people', 'enemy', 'hostile', 'negotiate', 'talk', 'speak']
        return any(keyword in situation.lower() for keyword in social_keywords)
    
    def format_options_for_ai(self, options: List[Dict]) -> str:
        """Format options for inclusion in AI prompt"""
        
        formatted_options = []
        for i, option in enumerate(options, 1):
            risk_emoji = {
                'low': '🟢',
                'medium': '🟡', 
                'high': '🔴',
                'critical': '⚫'
            }.get(option['risk_level'], '🟡')
            
            formatted_text = f"{i}. {option['text']} {risk_emoji}"
            if option.get('consequence_hint'):
                formatted_text += f" ({option['consequence_hint']})"
            
            formatted_options.append(formatted_text)
        
        return "\n".join(formatted_options)


def generate_contextual_options(situation: str, character: Dict, story_context: Dict) -> str:
    """Main function to generate contextual options for AI prompts"""
    
    generator = OptionGenerator()
    options = generator.generate_scene_options(situation, character, story_context)
    return generator.format_options_for_ai(options)