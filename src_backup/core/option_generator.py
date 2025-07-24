"""
Dynamic Option Generator - Creates contextual, intelligent player choices
Generates 4-5 options based on character abilities, environment, and story stakes
"""

import random
from typing import Dict, List, Any, Tuple, Optional
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


class DynamicOptionGenerator(OptionGenerator):
    """Enhanced option generator with dynamic contextual awareness"""
    
    def __init__(self):
        super().__init__()
        self.story_state_cache = {}
        self.recent_actions = []
        self.character_preferences = {}
    
    def generate_dynamic_options(self, situation: str, character: Dict, 
                               story_context: Dict, location_context: Dict = None) -> List[Dict]:
        """Generate truly dynamic options based on full game state"""
        
        # Analyze current situation complexity
        situation_analysis = self._analyze_situation_complexity(situation, story_context)
        
        # Get character-specific options
        character_options = self._generate_character_specific_options(
            character, situation, situation_analysis
        )
        
        # Get location-specific options
        location_options = self._generate_location_specific_options(
            location_context, situation, character
        )
        
        # Get story-progression options
        story_options = self._generate_story_progression_options(
            story_context, situation, character
        )
        
        # Get adaptive options based on recent actions
        adaptive_options = self._generate_adaptive_options(
            self.recent_actions, situation, character
        )
        
        # Combine and prioritize options
        all_options = character_options + location_options + story_options + adaptive_options
        
        # Select best 4-5 options
        selected_options = self._select_best_options(all_options, situation_analysis)
        
        # Always include Emberlyn option
        emberlyn_option = self._generate_emberlyn_option(situation, story_context)
        selected_options.append(emberlyn_option)
        
        return selected_options
    
    def _analyze_situation_complexity(self, situation: str, story_context: Dict) -> Dict[str, Any]:
        """Analyze the complexity and nature of current situation"""
        
        analysis = {
            'complexity_level': 'medium',
            'primary_challenge': 'unknown',
            'emotional_stakes': 'medium',
            'time_pressure': False,
            'multiple_npcs': False,
            'combat_likely': False,
            'puzzle_elements': False,
            'moral_choice': False
        }
        
        situation_lower = situation.lower()
        
        # Detect complexity indicators
        complexity_indicators = {
            'high': ['multiple', 'complex', 'difficult', 'challenging', 'critical'],
            'low': ['simple', 'easy', 'straightforward', 'basic']
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in situation_lower for indicator in indicators):
                analysis['complexity_level'] = level
                break
        
        # Detect challenge types
        if any(word in situation_lower for word in ['fight', 'battle', 'attack', 'enemy', 'hostile']):
            analysis['primary_challenge'] = 'combat'
            analysis['combat_likely'] = True
        elif any(word in situation_lower for word in ['puzzle', 'riddle', 'mystery', 'solve']):
            analysis['primary_challenge'] = 'puzzle'
            analysis['puzzle_elements'] = True
        elif any(word in situation_lower for word in ['choose', 'decision', 'moral', 'right', 'wrong']):
            analysis['primary_challenge'] = 'moral_choice'
            analysis['moral_choice'] = True
        elif any(word in situation_lower for word in ['negotiate', 'persuade', 'convince', 'talk']):
            analysis['primary_challenge'] = 'social'
        
        # Detect time pressure
        if any(word in situation_lower for word in ['quickly', 'urgent', 'hurry', 'time', 'before']):
            analysis['time_pressure'] = True
        
        # Detect multiple NPCs
        npc_indicators = ['villagers', 'people', 'crowd', 'group', 'everyone']
        if any(indicator in situation_lower for indicator in npc_indicators):
            analysis['multiple_npcs'] = True
        
        # Assess emotional stakes
        high_stakes_words = ['life', 'death', 'destroy', 'save', 'rescue', 'doom']
        if any(word in situation_lower for word in high_stakes_words):
            analysis['emotional_stakes'] = 'high'
        
        return analysis
    
    def _generate_character_specific_options(self, character: Dict, situation: str, 
                                           analysis: Dict) -> List[Dict]:
        """Generate options tailored to character build and preferences"""
        
        character_class = character.get('class', 'Cleric')
        character_level = character.get('level', 1)
        character_stats = character.get('stats', {})
        
        options = []
        
        # High-stat options
        highest_stat = max(character_stats.items(), key=lambda x: x[1]) if character_stats else ('strength', 14)
        stat_name, stat_value = highest_stat
        
        if stat_value >= 16:  # High stat
            stat_option = self._generate_high_stat_option(stat_name, situation, analysis)
            if stat_option:
                options.append(stat_option)
        
        # Class mastery options (higher level characters get more sophisticated options)
        if character_level >= 3:
            mastery_option = self._generate_mastery_option(character_class, situation, analysis)
            if mastery_option:
                options.append(mastery_option)
        
        # Skill-based options
        character_skills = character.get('skills', {})
        if isinstance(character_skills, dict):
            for skill, level in character_skills.items():
                if isinstance(level, (int, float)) and level >= 2:  # Skilled in this area
                    skill_option = self._generate_skill_option(skill, situation, analysis)
                    if skill_option:
                        options.append(skill_option)
                        break  # Only add one skill option
        
        return options
    
    def _generate_high_stat_option(self, stat_name: str, situation: str, analysis: Dict) -> Optional[Dict]:
        """Generate option that leverages character's highest stat"""
        
        stat_options = {
            'strength': {
                'text': "Use your exceptional strength to overcome physical obstacles",
                'category': 'physical',
                'risk_level': 'medium',
                'consequence_hint': "Brute force approach - effective but might cause collateral effects"
            },
            'dexterity': {
                'text': "Rely on your agility and quick reflexes to navigate the challenge",
                'category': 'agility',
                'risk_level': 'low',
                'consequence_hint': "Graceful approach - lower risk but may take more time"
            },
            'intelligence': {
                'text': "Apply your keen intellect to analyze and solve the problem systematically",
                'category': 'analytical',
                'risk_level': 'low',
                'consequence_hint': "Thoughtful approach - likely to reveal hidden aspects"
            },
            'charisma': {
                'text': "Use your natural charisma to influence and inspire others",
                'category': 'social',
                'risk_level': 'medium',
                'consequence_hint': "Persuasive approach - could rally support or create expectations"
            }
        }
        
        return stat_options.get(stat_name)
    
    def _generate_mastery_option(self, character_class: str, situation: str, analysis: Dict) -> Optional[Dict]:
        """Generate advanced class-specific option for experienced characters"""
        
        mastery_options = {
            'Cleric': {
                'text': "Channel your deep connection to the divine for a powerful intervention",
                'category': 'divine_mastery',
                'risk_level': 'high',
                'consequence_hint': "Powerful divine magic - great effect but will drain you significantly"
            },
            'Warrior': {
                'text': "Execute a masterful combat technique honed through experience",
                'category': 'combat_mastery',
                'risk_level': 'medium',
                'consequence_hint': "Expert technique - precise and effective with calculated risk"
            },
            'Mage': {
                'text': "Weave a complex spell combining multiple schools of magic",
                'category': 'arcane_mastery',
                'risk_level': 'high',
                'consequence_hint': "Advanced magic - unpredictable but potentially game-changing"
            },
            'Rogue': {
                'text': "Employ a sophisticated strategy using misdirection and timing",
                'category': 'tactical_mastery',
                'risk_level': 'medium',
                'consequence_hint': "Cunning plan - complex but could achieve multiple objectives"
            }
        }
        
        return mastery_options.get(character_class)
    
    def _generate_skill_option(self, skill: str, situation: str, analysis: Dict) -> Optional[Dict]:
        """Generate option based on character's high skill level"""
        
        skill_options = {
            'Combat': {
                'text': f"Apply your combat expertise to handle this situation with precision",
                'category': 'skill_combat',
                'risk_level': 'medium',
                'consequence_hint': "Skilled approach - efficient and controlled"
            },
            'Stealth': {
                'text': f"Use your stealth mastery to approach the problem unseen",
                'category': 'skill_stealth',
                'risk_level': 'low',
                'consequence_hint': "Covert approach - avoid direct confrontation"
            },
            'Persuasion': {
                'text': f"Leverage your persuasive abilities to find a diplomatic solution",
                'category': 'skill_social',
                'risk_level': 'low',
                'consequence_hint': "Diplomatic approach - could create lasting alliances"
            },
            'Investigation': {
                'text': f"Use your investigative skills to uncover hidden information",
                'category': 'skill_investigation',
                'risk_level': 'low',
                'consequence_hint': "Thorough approach - reveals important details"
            }
        }
        
        return skill_options.get(skill)
    
    def _generate_location_specific_options(self, location_context: Dict, 
                                          situation: str, character: Dict) -> List[Dict]:
        """Generate options specific to current location"""
        
        if not location_context:
            return []
        
        location_id = location_context.get('id', '')
        environmental_features = location_context.get('environmental_features', [])
        
        options = []
        
        # Location-specific environmental options
        location_options = {
            'crystal_cave': {
                'text': "Use the cave's crystal formations to amplify magical energy",
                'category': 'environmental',
                'risk_level': 'medium',
                'consequence_hint': "Crystal magic could be powerful but unpredictable"
            },
            'sacred_grove': {
                'text': "Draw upon the grove's ancient spiritual energy for guidance",
                'category': 'spiritual',
                'risk_level': 'low',
                'consequence_hint': "Sacred power provides wisdom and protection"
            },
            'ashbrook_village': {
                'text': "Rally the villagers to help with their local knowledge and resources",
                'category': 'community',
                'risk_level': 'low',
                'consequence_hint': "Community support - strength in numbers but slower decisions"
            },
            'ember_woods': {
                'text': "Use the forest's natural cover and resources to your advantage",
                'category': 'wilderness',
                'risk_level': 'medium',
                'consequence_hint': "Nature's aid - effective but requires wilderness skills"
            }
        }
        
        if location_id in location_options:
            options.append(location_options[location_id])
        
        # Environmental feature options
        if 'magical_atmosphere' in environmental_features:
            options.append({
                'text': "Tap into the ambient magical energy surrounding this place",
                'category': 'magical_environment',
                'risk_level': 'medium',
                'consequence_hint': "Ambient magic - unpredictable but potentially powerful"
            })
        
        return options
    
    def _generate_story_progression_options(self, story_context: Dict, 
                                          situation: str, character: Dict) -> List[Dict]:
        """Generate options that advance story progression"""
        
        options = []
        
        # Check for active quests
        active_quests = story_context.get('active_quests', [])
        if active_quests:
            quest = active_quests[0]  # Focus on first active quest
            options.append({
                'text': f"Focus on advancing your quest: {quest.get('name', 'current objective')}",
                'category': 'quest_progression',
                'risk_level': 'medium',
                'consequence_hint': "Direct progress toward your goal but may ignore other opportunities"
            })
        
        # Story flag progression
        story_flags = story_context.get('story_flags', {})
        if not story_flags.get('sacred_flame_restored', False):
            options.append({
                'text': "Seek information or resources related to restoring the Sacred Flame",
                'category': 'main_story',
                'risk_level': 'low',
                'consequence_hint': "Advances main storyline - reveals important plot elements"
            })
        
        return options
    
    def _generate_adaptive_options(self, recent_actions: List[str], 
                                 situation: str, character: Dict) -> List[Dict]:
        """Generate options that adapt to player's recent choices"""
        
        options = []
        
        if not recent_actions:
            return options
        
        # Analyze recent action patterns
        action_patterns = self._analyze_action_patterns(recent_actions)
        
        # If player has been very aggressive, offer diplomatic option
        if action_patterns.get('aggression_level', 0) > 0.7:
            options.append({
                'text': "Try a more diplomatic and peaceful approach this time",
                'category': 'adaptive_diplomatic',
                'risk_level': 'low',
                'consequence_hint': "Change of pace - might surprise others and open new possibilities"
            })
        
        # If player has been very cautious, offer bold option
        elif action_patterns.get('caution_level', 0) > 0.7:
            options.append({
                'text': "Take a bold, decisive action to break the current pattern",
                'category': 'adaptive_bold',
                'risk_level': 'high',
                'consequence_hint': "Dramatic action - could change everything but carries significant risk"
            })
        
        return options
    
    def _analyze_action_patterns(self, recent_actions: List[str]) -> Dict[str, float]:
        """Analyze patterns in recent player actions"""
        
        if not recent_actions:
            return {}
        
        aggressive_keywords = ['attack', 'fight', 'charge', 'strike', 'battle']
        cautious_keywords = ['wait', 'observe', 'careful', 'slowly', 'consider']
        social_keywords = ['talk', 'persuade', 'negotiate', 'ask', 'discuss']
        
        aggression_count = sum(1 for action in recent_actions 
                              if any(keyword in action.lower() for keyword in aggressive_keywords))
        caution_count = sum(1 for action in recent_actions 
                           if any(keyword in action.lower() for keyword in cautious_keywords))
        social_count = sum(1 for action in recent_actions 
                          if any(keyword in action.lower() for keyword in social_keywords))
        
        total_actions = len(recent_actions)
        
        return {
            'aggression_level': aggression_count / total_actions,
            'caution_level': caution_count / total_actions,
            'social_level': social_count / total_actions
        }
    
    def _generate_emberlyn_option(self, situation: str, story_context: Dict) -> Dict:
        """Generate contextual Emberlyn advice option"""
        
        # Make Emberlyn's advice more specific to situation
        situation_lower = situation.lower()
        
        if 'danger' in situation_lower or 'threat' in situation_lower:
            return {
                'text': "Ask Emberlyn about potential dangers and how to avoid them",
                'category': 'emberlyn_safety',
                'risk_level': 'safe',
                'consequence_hint': "Emberlyn's protective instincts could reveal hidden threats"
            }
        elif 'magic' in situation_lower or 'spell' in situation_lower:
            return {
                'text': "Consult Emberlyn about the magical aspects of this situation",
                'category': 'emberlyn_magic',
                'risk_level': 'safe',
                'consequence_hint': "Fairy magic knowledge might provide unique insights"
            }
        else:
            return {
                'text': "Ask Emberlyn for her fairy wisdom and unique perspective",
                'category': 'emberlyn_wisdom',
                'risk_level': 'safe',
                'consequence_hint': "Emberlyn's otherworldly view might reveal unexpected opportunities"
            }
    
    def _select_best_options(self, all_options: List[Dict], analysis: Dict) -> List[Dict]:
        """Select the best 4 options from all generated options"""
        
        if len(all_options) <= 4:
            return all_options
        
        # Score options based on situation analysis
        scored_options = []
        
        for option in all_options:
            score = 1.0
            
            # Prefer options that match situation complexity
            if analysis['complexity_level'] == 'high' and option['risk_level'] == 'high':
                score += 1.0
            elif analysis['complexity_level'] == 'low' and option['risk_level'] == 'low':
                score += 0.5
            
            # Prefer options that match primary challenge
            primary_challenge = analysis['primary_challenge']
            if primary_challenge == 'combat' and 'combat' in option['category']:
                score += 1.5
            elif primary_challenge == 'social' and 'social' in option['category']:
                score += 1.5
            elif primary_challenge == 'puzzle' and 'investigation' in option['category']:
                score += 1.5
            
            # Prefer variety in risk levels
            risk_bonus = {'low': 0.2, 'medium': 0.5, 'high': 0.3}
            score += risk_bonus.get(option['risk_level'], 0)
            
            scored_options.append((option, score))
        
        # Sort by score and take top 4
        scored_options.sort(key=lambda x: x[1], reverse=True)
        return [option for option, score in scored_options[:4]]
    
    def update_recent_actions(self, action: str):
        """Update recent actions for adaptive option generation"""
        self.recent_actions.append(action)
        if len(self.recent_actions) > 5:  # Keep only last 5 actions
            self.recent_actions.pop(0)


def generate_contextual_options(situation: str, character: Dict, story_context: Dict, 
                              location_context: Dict = None) -> str:
    """Main function to generate contextual options for AI prompts"""
    
    generator = DynamicOptionGenerator()
    options = generator.generate_dynamic_options(situation, character, story_context, location_context)
    return generator.format_options_for_ai(options)