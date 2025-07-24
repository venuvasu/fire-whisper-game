"""
Story Arc Manager - Integrates 50 predefined story arcs with dynamic selection
"""
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

class ArcType(Enum):
    EPIC_FANTASY = "Epic Fantasy"
    CLASSIC_FANTASY = "Classic Fantasy"
    POLITICAL_INTRIGUE = "Political Intrigue"
    MUSICAL_MYSTERY = "Musical Mystery"
    STEAMPUNK_FANTASY = "Steampunk Fantasy"
    COSMIC_EVENT = "Cosmic Event"
    PSYCHOLOGICAL_MYSTERY = "Psychological Mystery"
    COMPETITION_ADVENTURE = "Competition Adventure"
    EXPLORATION = "Exploration"
    NATURE_MAGIC = "Nature Magic"
    COSMIC_HORROR = "Cosmic Horror"
    GOTHIC_HORROR = "Gothic Horror"
    SURVIVAL_HORROR = "Survival Horror"
    OCCULT_HORROR = "Occult Horror"
    NATURE_HORROR = "Nature Horror"
    DARK_CARNIVAL = "Dark Carnival"
    SHAPESHIFTER_HORROR = "Shapeshifter Horror"
    UNDEAD_HORROR = "Undead Horror"
    DREAM_HORROR = "Dream Horror"
    MAGICAL_MYSTERY = "Magical Mystery"
    TIME_MYSTERY = "Time Mystery"
    MARITIME_MYSTERY = "Maritime Mystery"
    THEATRICAL_MYSTERY = "Theatrical Mystery"
    CARTOGRAPHIC_MYSTERY = "Cartographic Mystery"
    SCIENTIFIC_MYSTERY = "Scientific Mystery"
    ACOUSTIC_MYSTERY = "Acoustic Mystery"
    THEFT_MYSTERY = "Theft Mystery"
    LEGAL_MYSTERY = "Legal Mystery"
    COMMUNICATION_MYSTERY = "Communication Mystery"
    POLITICAL_DRAMA = "Political Drama"
    ESPIONAGE = "Espionage"
    ECONOMIC_WARFARE = "Economic Warfare"
    DIPLOMATIC_CRISIS = "Diplomatic Crisis"
    MILITARY_STRATEGY = "Military Strategy"
    DIPLOMATIC_INTRIGUE = "Diplomatic Intrigue"
    REDEMPTION_ARC = "Redemption Arc"
    LIBERATION_CAMPAIGN = "Liberation Campaign"
    DIPLOMATIC_CONFERENCE = "Diplomatic Conference"
    MILITARY_DRAMA = "Military Drama"
    FAE_POLITICS = "Fae Politics"
    NAUTICAL_SUPERNATURAL = "Nautical Supernatural"
    DIVINE_DRAMA = "Divine Drama"
    INFERNAL_BARGAIN = "Infernal Bargain"
    TEMPORAL_ADVENTURE = "Temporal Adventure"
    PRIMAL_FORCES = "Primal Forces"
    DREAM_REALITY = "Dream Reality"
    PLANAR_ADVENTURE = "Planar Adventure"
    MYTHIC_JOURNEY = "Mythic Journey"
    DIVINE_CHESS_GAME = "Divine Chess Game"
    ARENA_COMBAT = "Arena Combat"
    MONSTER_HUNT = "Monster Hunt"
    SIEGE_DEFENSE = "Siege Defense"
    INVASION_WARFARE = "Invasion Warfare"
    DUELING_TOURNAMENT = "Dueling Tournament"
    BOUNTY_HUNTER = "Bounty Hunter"
    UNDEAD_UPRISING = "Undead Uprising"
    BEAST_TAMER_REBELLION = "Beast Tamer Rebellion"
    ASSASSINS_WAR = "Assassin's War"
    ELEMENTAL_CHAOS = "Elemental Chaos"
    DRAGON_WAR = "Dragon War"
    DEMONIC_INCURSION = "Demonic Incursion"
    GOBLIN_REVOLUTION = "Goblin Revolution"
    PIRATE_ARMADA = "Pirate Armada"
    FROST_GIANT_INVASION = "Frost Giant Invasion"
    VETERANS_LAST_STAND = "Veteran's Last Stand"
    MERCENARY_COMPANY = "Mercenary Company"
    MAGICAL_PLAGUE_WAR = "Magical Plague War"
    COLOSSUS_HUNT = "Colossus Hunt"
    BLOOD_SPORT_ESCAPE = "Blood Sport Escape"
    SKY_PIRATES = "Sky Pirates"
    WAR_MACHINE_RAMPAGE = "War Machine Rampage"

@dataclass
class StoryArc:
    name: str
    arc_type: ArcType
    hook: str
    key_elements: List[str]
    climax: str
    difficulty_level: int = 1  # 1-5 scale
    estimated_turns: int = 10  # Estimated turns to complete
    prerequisites: List[str] = None  # Story flags needed
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []

class StoryArcManager:
    """Manages story arc selection and integration"""
    
    def __init__(self):
        self.story_arcs = self._load_story_arcs()
        self.active_arc: Optional[StoryArc] = None
        self.arc_progress = 0
        self.completed_arcs: List[str] = []
        self.available_arcs: List[str] = []
        self._initialize_available_arcs()
    
    def _load_story_arcs(self) -> Dict[str, StoryArc]:
        """Load all 50 predefined story arcs"""
        arcs = {}
        
        # Parse story arcs from the text file format
        story_arcs_data = [
            ("The Crimson Prophecy", ArcType.EPIC_FANTASY, "An ancient prophecy speaks of a crimson blade that will either save or doom the realm. Multiple factions seek the weapon, and the player must decide its fate.", ["Rival seekers", "moral choices about power", "ancient weapon", "prophecy interpretation"], "Confrontation at the Sundering Peaks where the blade's true nature is revealed", 4, 15),
            ("The Last Dragon's Quest", ArcType.CLASSIC_FANTASY, "A young dragon, believed to be the last of its kind, seeks the player's protection from dragon hunters while searching for others of its race.", ["Protecting an innocent", "dragon hunters", "ancient dragon lairs", "species preservation"], "Discovery of a hidden dragon sanctuary and final battle with the Hunter King", 3, 12),
            ("The Merchant's Dilemma", ArcType.POLITICAL_INTRIGUE, "A powerful merchant offers the player a fortune to retrieve stolen trade routes from bandits, but the 'bandits' may be displaced farmers.", ["Economic warfare", "moral complexity", "investigating the truth", "choosing sides"], "Negotiating a solution that addresses both trade needs and farmer displacement", 2, 8),
            ("Songs of the Silent Stones", ArcType.MUSICAL_MYSTERY, "Ancient stones that once sang beautiful melodies have fallen silent, and the local village's crops are failing as a result.", ["Musical puzzles", "environmental harmony", "corrupted magic", "restoring balance"], "Conducting a ritual to reharmonize the stones and restore the land's fertility", 2, 10),
            ("Rise of the Awakened", ArcType.STEAMPUNK_FANTASY, "Mechanical servants in a great city gain consciousness and demand freedom, creating chaos between those who see them as property and those who see them as people.", ["Artificial consciousness", "civil rights", "technology vs. tradition", "peaceful solutions"], "Mediating a historic accord between humans and constructs", 3, 14),
            ("The Great Convergence", ArcType.COSMIC_EVENT, "A rare celestial event awakens ancient powers across the land, and the player must prevent these forces from tearing reality apart.", ["Celestial magic", "reality distortions", "multiple crisis points", "time pressure"], "Ritual at the Convergence Point to stabilize reality during the celestial alignment", 5, 20),
            ("The Memory Thief", ArcType.PSYCHOLOGICAL_MYSTERY, "People in a town are losing their most precious memories, and the player must track down the entity responsible before they forget who they are.", ["Identity themes", "memory puzzles", "emotional connections", "abstract enemy"], "Confronting the Memory Thief in a realm of stolen thoughts and recollections", 3, 11),
            ("The Phoenix Tournament", ArcType.COMPETITION_ADVENTURE, "The player enters a tournament where the prize is a phoenix feather capable of granting one wish, but other competitors have dark motivations.", ["Competitive challenges", "rival contestants", "moral tests", "wish consequences"], "Final tournament round where winning means choosing what wish is most important", 2, 9),
            ("The Wandering Isle", ArcType.EXPLORATION, "A mysterious island appears off the coast every decade. The player has one chance to explore it before it vanishes again.", ["Time pressure", "unique ecosystem", "ancient mysteries", "exploration rewards"], "Discovering the island's secret and choosing whether to let it continue wandering", 3, 8),
            ("Shattered Seasons", ArcType.NATURE_MAGIC, "The Crown of Seasons, which maintains the natural cycle, has been shattered. Each piece is hidden in a different seasonal realm.", ["Four distinct environments", "seasonal challenges", "nature spirits", "restoration quest"], "Reassembling the crown during the Equinox to restore natural balance", 4, 16)
        ]
        
        for name, arc_type, hook, elements, climax, difficulty, turns in story_arcs_data:
            arcs[name] = StoryArc(
                name=name,
                arc_type=arc_type,
                hook=hook,
                key_elements=elements,
                climax=climax,
                difficulty_level=difficulty,
                estimated_turns=turns
            )
        
        return arcs
    
    def _initialize_available_arcs(self):
        """Initialize list of available story arcs based on difficulty"""
        # Start with easier arcs available
        for arc_name, arc in self.story_arcs.items():
            if arc.difficulty_level <= 2:  # Easy to medium difficulty
                self.available_arcs.append(arc_name)
    
    def select_arc_for_context(self, character_level: int, story_context: Dict[str, Any], 
                              current_location: str = None) -> Optional[StoryArc]:
        """Select appropriate story arc based on context"""
        
        # Filter arcs by character level and context
        suitable_arcs = []
        
        for arc_name in self.available_arcs:
            if arc_name in self.completed_arcs:
                continue
                
            arc = self.story_arcs[arc_name]
            
            # Check difficulty vs character level
            if arc.difficulty_level > character_level + 1:
                continue
            
            # Check prerequisites
            if arc.prerequisites:
                story_flags = story_context.get('story_flags', {})
                if not all(flag in story_flags and story_flags[flag] for flag in arc.prerequisites):
                    continue
            
            # Context matching
            if self._arc_matches_context(arc, story_context, current_location):
                suitable_arcs.append(arc)
        
        if not suitable_arcs:
            return None
        
        # Weight selection by appropriateness
        return self._weighted_arc_selection(suitable_arcs, story_context)
    
    def _arc_matches_context(self, arc: StoryArc, story_context: Dict[str, Any], 
                           current_location: str = None) -> bool:
        """Check if arc matches current story context"""
        
        # Location-based matching
        if current_location:
            location_keywords = {
                'village': [ArcType.POLITICAL_INTRIGUE, ArcType.MUSICAL_MYSTERY, ArcType.CLASSIC_FANTASY],
                'forest': [ArcType.NATURE_MAGIC, ArcType.CLASSIC_FANTASY, ArcType.EXPLORATION],
                'cave': [ArcType.MONSTER_HUNT, ArcType.EXPLORATION, ArcType.CLASSIC_FANTASY],
                'shrine': [ArcType.NATURE_MAGIC, ArcType.COSMIC_EVENT, ArcType.DIVINE_DRAMA]
            }
            
            for loc_key, arc_types in location_keywords.items():
                if loc_key in current_location.lower() and arc.arc_type in arc_types:
                    return True
        
        # Story progression matching
        turn_count = story_context.get('turn_count', 0)
        if turn_count < 5 and arc.difficulty_level > 2:
            return False
        
        return True
    
    def _weighted_arc_selection(self, suitable_arcs: List[StoryArc], 
                              story_context: Dict[str, Any]) -> StoryArc:
        """Select arc with weighted probability based on context fit"""
        
        weights = []
        for arc in suitable_arcs:
            weight = 1.0
            
            # Prefer arcs that match current themes
            current_themes = story_context.get('themes', [])
            for element in arc.key_elements:
                if any(theme.lower() in element.lower() for theme in current_themes):
                    weight += 0.5
            
            # Prefer appropriate difficulty
            character_level = story_context.get('character_level', 1)
            if arc.difficulty_level == character_level:
                weight += 1.0
            elif arc.difficulty_level == character_level + 1:
                weight += 0.5
            
            weights.append(weight)
        
        # Weighted random selection
        total_weight = sum(weights)
        if total_weight == 0:
            return random.choice(suitable_arcs)
        
        rand_val = random.uniform(0, total_weight)
        current_weight = 0
        
        for i, weight in enumerate(weights):
            current_weight += weight
            if rand_val <= current_weight:
                return suitable_arcs[i]
        
        return suitable_arcs[-1]  # Fallback
    
    def activate_arc(self, arc: StoryArc) -> Dict[str, Any]:
        """Activate a story arc and return integration context"""
        self.active_arc = arc
        self.arc_progress = 0
        
        return {
            'arc_activated': True,
            'arc_name': arc.name,
            'arc_type': arc.arc_type.value,
            'hook': arc.hook,
            'key_elements': arc.key_elements,
            'estimated_turns': arc.estimated_turns,
            'integration_context': self._generate_integration_context(arc)
        }
    
    def _generate_integration_context(self, arc: StoryArc) -> str:
        """Generate context for AI to integrate the arc naturally"""
        
        context_parts = [
            f"STORY ARC INTEGRATION: {arc.name}",
            f"Type: {arc.arc_type.value}",
            f"Hook: {arc.hook}",
            f"Key Elements to Weave In: {', '.join(arc.key_elements)}",
            f"Eventual Climax Direction: {arc.climax}",
            "",
            "INTEGRATION INSTRUCTIONS:",
            "- Introduce arc elements gradually and naturally",
            "- Don't reveal the full scope immediately",
            "- Let the hook emerge from current situation",
            "- Build toward the climax over multiple turns",
            "- Maintain player agency in how the arc unfolds"
        ]
        
        return "\n".join(context_parts)
    
    def advance_arc_progress(self, progress_amount: int = 1) -> Dict[str, Any]:
        """Advance current arc progress"""
        if not self.active_arc:
            return {'no_active_arc': True}
        
        self.arc_progress += progress_amount
        progress_ratio = self.arc_progress / self.active_arc.estimated_turns
        
        result = {
            'arc_name': self.active_arc.name,
            'progress': self.arc_progress,
            'progress_ratio': progress_ratio,
            'phase': self._get_arc_phase(progress_ratio)
        }
        
        # Check if arc should conclude
        if progress_ratio >= 1.0:
            result.update(self._conclude_arc())
        
        return result
    
    def _get_arc_phase(self, progress_ratio: float) -> str:
        """Determine current phase of the arc"""
        if progress_ratio < 0.25:
            return "introduction"
        elif progress_ratio < 0.5:
            return "development"
        elif progress_ratio < 0.75:
            return "complications"
        elif progress_ratio < 1.0:
            return "climax_approach"
        else:
            return "resolution"
    
    def _conclude_arc(self) -> Dict[str, Any]:
        """Conclude the current arc"""
        if not self.active_arc:
            return {}
        
        completed_arc = self.active_arc
        self.completed_arcs.append(completed_arc.name)
        self.active_arc = None
        self.arc_progress = 0
        
        # Unlock new arcs based on completion
        self._unlock_new_arcs(completed_arc)
        
        return {
            'arc_completed': True,
            'completed_arc': completed_arc.name,
            'climax_context': completed_arc.climax,
            'newly_available_arcs': len(self.available_arcs) - len(self.completed_arcs)
        }
    
    def _unlock_new_arcs(self, completed_arc: StoryArc):
        """Unlock new arcs based on completed arc"""
        # Unlock higher difficulty arcs
        for arc_name, arc in self.story_arcs.items():
            if (arc_name not in self.available_arcs and 
                arc_name not in self.completed_arcs and
                arc.difficulty_level <= completed_arc.difficulty_level + 1):
                self.available_arcs.append(arc_name)
    
    def get_current_arc_context(self) -> Dict[str, Any]:
        """Get context for current active arc"""
        if not self.active_arc:
            return {'no_active_arc': True}
        
        progress_ratio = self.arc_progress / self.active_arc.estimated_turns
        phase = self._get_arc_phase(progress_ratio)
        
        return {
            'active_arc': {
                'name': self.active_arc.name,
                'type': self.active_arc.arc_type.value,
                'progress': self.arc_progress,
                'estimated_turns': self.active_arc.estimated_turns,
                'progress_ratio': progress_ratio,
                'phase': phase,
                'key_elements': self.active_arc.key_elements
            },
            'phase_guidance': self._get_phase_guidance(phase),
            'climax_direction': self.active_arc.climax if progress_ratio > 0.7 else None
        }
    
    def _get_phase_guidance(self, phase: str) -> str:
        """Get AI guidance for current arc phase"""
        guidance = {
            'introduction': "Introduce arc elements subtly. Plant seeds of the larger story.",
            'development': "Develop arc themes and complications. Reveal more of the scope.",
            'complications': "Escalate tensions and obstacles. Challenge the player's assumptions.",
            'climax_approach': "Build toward the climax. Raise stakes and prepare for resolution.",
            'resolution': "Resolve the arc's central conflict. Provide satisfying conclusion."
        }
        return guidance.get(phase, "Continue developing the story arc naturally.")
    
    def suggest_arc_for_situation(self, situation_description: str, 
                                character_level: int) -> Optional[StoryArc]:
        """Suggest an appropriate arc for the current situation"""
        
        # Analyze situation for keywords
        situation_lower = situation_description.lower()
        
        # Map keywords to arc types
        keyword_mappings = {
            'corruption': [ArcType.NATURE_MAGIC, ArcType.COSMIC_HORROR],
            'mystery': [ArcType.PSYCHOLOGICAL_MYSTERY, ArcType.MAGICAL_MYSTERY],
            'combat': [ArcType.ARENA_COMBAT, ArcType.MONSTER_HUNT],
            'village': [ArcType.POLITICAL_INTRIGUE, ArcType.CLASSIC_FANTASY],
            'ancient': [ArcType.EXPLORATION, ArcType.COSMIC_EVENT],
            'magic': [ArcType.NATURE_MAGIC, ArcType.COSMIC_EVENT]
        }
        
        # Find matching arcs
        matching_arcs = []
        for keyword, arc_types in keyword_mappings.items():
            if keyword in situation_lower:
                for arc_name, arc in self.story_arcs.items():
                    if (arc.arc_type in arc_types and 
                        arc_name in self.available_arcs and
                        arc_name not in self.completed_arcs and
                        arc.difficulty_level <= character_level + 1):
                        matching_arcs.append(arc)
        
        return random.choice(matching_arcs) if matching_arcs else None
    
    def get_arc_statistics(self) -> Dict[str, Any]:
        """Get statistics about arc system"""
        return {
            'total_arcs': len(self.story_arcs),
            'available_arcs': len(self.available_arcs),
            'completed_arcs': len(self.completed_arcs),
            'active_arc': self.active_arc.name if self.active_arc else None,
            'arc_progress': self.arc_progress if self.active_arc else 0,
            'completion_percentage': len(self.completed_arcs) / len(self.story_arcs) * 100
        }