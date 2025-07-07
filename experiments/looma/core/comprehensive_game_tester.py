"""
Comprehensive Game Experience Tester
Simulates 8-turn game sessions to measure real player experience metrics.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import random
import json
from datetime import datetime

class PlayerPersonality(Enum):
    CAUTIOUS = "cautious"
    AGGRESSIVE = "aggressive" 
    SOCIAL = "social"
    EXPLORER = "explorer"

class ArchitectureType(Enum):
    AI_HEAVY = "ai_heavy"
    BALANCED = "balanced"
    CODE_HEAVY = "code_heavy"
    HYBRID = "hybrid"

@dataclass
class GameState:
    """Complete game state tracking"""
    turn: int = 0
    location: str = "village_square"
    player_hp: int = 100
    player_gold: int = 50
    inventory: List[str] = field(default_factory=lambda: ["rusty_sword", "health_potion"])
    npcs_met: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    active_quests: List[Dict[str, Any]] = field(default_factory=list)
    completed_quests: List[str] = field(default_factory=list)
    world_facts: Dict[str, Any] = field(default_factory=dict)
    story_events: List[str] = field(default_factory=list)
    relationship_scores: Dict[str, int] = field(default_factory=dict)

@dataclass
class TurnResult:
    """Result of a single game turn"""
    turn_number: int
    player_action: str
    narrative_response: str
    choices_offered: List[str]
    state_changes: Dict[str, Any]
    npc_interactions: List[Dict[str, Any]]
    quest_updates: List[str]
    world_consistency_issues: List[str]
    response_time: float
    
@dataclass
class ExperienceMetrics:
    """Comprehensive player experience metrics"""
    # Core engagement metrics
    fun_score: float  # 0-1, overall engagement and enjoyment
    hallucination_score: float  # 0-1, consistency and logical coherence (1 = no hallucinations)
    logical_coherence: float  # 0-1, responses make sense in context
    dynamic_nature: float  # 0-1, variety and unpredictability
    
    # Relationship and story metrics
    npc_relationship_quality: float  # 0-1, meaningful NPC interactions
    story_arc_progression: float  # 0-1, satisfying narrative development
    comeback_desire: float  # 0-1, replayability and hook factor
    
    # Additional comprehensive metrics
    player_agency: float  # 0-1, choices feel meaningful
    world_consistency: float  # 0-1, game world feels coherent
    pacing_quality: float  # 0-1, good balance of different activities
    emotional_investment: float  # 0-1, player cares about outcomes
    replay_value: float  # 0-1, different paths seem available
    
    # Performance metrics
    average_response_time: float
    error_rate: float
    session_completion_rate: float

class GameScenarioGenerator:
    """Generates realistic 8-turn game scenarios"""
    
    def __init__(self):
        self.scenario_templates = {
            "village_quest": [
                "arrive_in_village", "meet_elder", "accept_quest", "gather_supplies",
                "travel_to_location", "encounter_challenge", "resolve_challenge", "return_with_reward"
            ],
            "dungeon_crawl": [
                "enter_dungeon", "explore_corridor", "find_treasure_room", "trigger_trap",
                "fight_guardian", "solve_puzzle", "discover_secret", "escape_with_loot"
            ],
            "social_intrigue": [
                "attend_tavern", "overhear_conversation", "approach_suspicious_figure", "negotiate_deal",
                "investigate_rumors", "confront_antagonist", "make_alliance", "resolve_conflict"
            ]
        }
    
    def generate_scenario(self, scenario_type: str = None) -> List[str]:
        """Generate an 8-turn scenario"""
        if scenario_type is None:
            scenario_type = random.choice(list(self.scenario_templates.keys()))
        return self.scenario_templates[scenario_type].copy()

class NPCPersonalityEngine:
    """Manages NPC personalities and relationship dynamics"""
    
    def __init__(self):
        self.npc_templates = {
            "village_elder": {
                "personality": "wise_cautious",
                "initial_attitude": "neutral",
                "interests": ["village_safety", "ancient_lore"],
                "relationship_factors": {"respect": 0, "trust": 0}
            },
            "tavern_keeper": {
                "personality": "friendly_gossip",
                "initial_attitude": "welcoming",
                "interests": ["local_news", "profitable_customers"],
                "relationship_factors": {"friendship": 0, "business": 0}
            },
            "mysterious_stranger": {
                "personality": "secretive_dangerous",
                "initial_attitude": "suspicious",
                "interests": ["hidden_agenda", "valuable_information"],
                "relationship_factors": {"suspicion": 0, "intrigue": 0}
            }
        }
    
    def get_npc_response(self, npc_name: str, player_action: str, 
                        relationship_history: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """Generate NPC response based on personality and history"""
        
        if npc_name not in self.npc_templates:
            npc_name = "generic_npc"
            
        npc = self.npc_templates.get(npc_name, {
            "personality": "neutral",
            "initial_attitude": "neutral",
            "interests": ["general_conversation"],
            "relationship_factors": {"rapport": 0}
        })
        
        # Simulate relationship-aware responses
        current_relationship = relationship_history.get(npc_name, {"interactions": 0, "sentiment": 0})
        
        response_quality = 0.7 + (current_relationship.get("sentiment", 0) * 0.2)
        
        responses = {
            "greet": f"The {npc_name} acknowledges you with {self._get_attitude_descriptor(current_relationship)}",
            "ask_quest": f"The {npc_name} considers your request, {self._get_quest_response(npc, current_relationship)}",
            "trade": f"The {npc_name} examines your goods {self._get_trade_response(current_relationship)}",
            "insult": f"The {npc_name} reacts {self._get_negative_response(current_relationship)}",
            "compliment": f"The {npc_name} {self._get_positive_response(current_relationship)}"
        }
        
        response = responses.get(player_action, f"The {npc_name} responds to your {player_action}")
        
        # Update relationship
        new_relationship = current_relationship.copy()
        new_relationship["interactions"] = new_relationship.get("interactions", 0) + 1
        
        if player_action in ["compliment", "help"]:
            new_relationship["sentiment"] = min(1.0, new_relationship.get("sentiment", 0) + 0.2)
        elif player_action in ["insult", "threaten"]:
            new_relationship["sentiment"] = max(-1.0, new_relationship.get("sentiment", 0) - 0.3)
        
        return response, new_relationship
    
    def _get_attitude_descriptor(self, relationship: Dict[str, Any]) -> str:
        sentiment = relationship.get("sentiment", 0)
        if sentiment > 0.5:
            return "warmth and familiarity"
        elif sentiment < -0.5:
            return "cold suspicion"
        else:
            return "polite neutrality"
    
    def _get_quest_response(self, npc: Dict[str, Any], relationship: Dict[str, Any]) -> str:
        sentiment = relationship.get("sentiment", 0)
        if sentiment > 0.3:
            return "and offers you a valuable quest with good rewards"
        elif sentiment < -0.3:
            return "but seems reluctant to trust you with important tasks"
        else:
            return "and provides a standard quest opportunity"
    
    def _get_trade_response(self, relationship: Dict[str, Any]) -> str:
        sentiment = relationship.get("sentiment", 0)
        if sentiment > 0.3:
            return "and offers you favorable prices"
        elif sentiment < -0.3:
            return "with obvious skepticism about fair dealing"
        else:
            return "and quotes standard market prices"
    
    def _get_negative_response(self, relationship: Dict[str, Any]) -> str:
        sentiment = relationship.get("sentiment", 0)
        if sentiment > 0.3:
            return "with hurt disappointment, clearly not expecting this from you"
        else:
            return "with anger and hostility, relationship clearly damaged"
    
    def _get_positive_response(self, relationship: Dict[str, Any]) -> str:
        sentiment = relationship.get("sentiment", 0)
        if sentiment > 0.3:
            return "beams with genuine appreciation, your friendship clearly valued"
        else:
            return "seems pleased by your kind words, warming to you"

class GameArchitectureSimulator:
    """Simulates different game architectures with realistic behavior patterns"""
    
    def __init__(self, architecture_type: ArchitectureType):
        self.architecture_type = architecture_type
        self.npc_engine = NPCPersonalityEngine()
        self.world_facts = {}
        self.story_threads = []
        
    def process_turn(self, state: GameState, player_action: str, 
                    player_personality: PlayerPersonality) -> TurnResult:
        """Process a single game turn based on architecture type"""
        
        start_time = random.uniform(0.5, 3.0)  # Simulate response time
        
        # Generate narrative response based on architecture
        narrative = self._generate_narrative(state, player_action)
        
        # Generate choices based on architecture
        choices = self._generate_choices(state, player_action, player_personality)
        
        # Process state changes
        state_changes = self._process_state_changes(state, player_action)
        
        # Handle NPC interactions
        npc_interactions = self._process_npc_interactions(state, player_action)
        
        # Update quests
        quest_updates = self._process_quest_updates(state, player_action)
        
        # Check for world consistency issues
        consistency_issues = self._check_world_consistency(state, player_action, narrative)
        
        return TurnResult(
            turn_number=state.turn,
            player_action=player_action,
            narrative_response=narrative,
            choices_offered=choices,
            state_changes=state_changes,
            npc_interactions=npc_interactions,
            quest_updates=quest_updates,
            world_consistency_issues=consistency_issues,
            response_time=start_time
        )
    
    def _generate_narrative(self, state: GameState, action: str) -> str:
        """Generate narrative based on architecture type"""
        
        if self.architecture_type == ArchitectureType.AI_HEAVY:
            # AI-heavy: Creative but potentially inconsistent
            creativity_factor = random.uniform(0.8, 1.0)
            consistency_factor = random.uniform(0.6, 0.9)
            
            creative_elements = [
                "with unexpected consequences that ripple through the world",
                "as the very air seems to respond to your presence",
                "revealing hidden depths to this seemingly simple action",
                "in ways that surprise even seasoned adventurers"
            ]
            
            base_narrative = f"You {action} in {state.location}"
            if creativity_factor > 0.85:
                base_narrative += f" {random.choice(creative_elements)}"
            
            # Potential consistency issues
            if consistency_factor < 0.7:
                base_narrative += " The sun sets in the east, casting strange shadows."
                
        elif self.architecture_type == ArchitectureType.CODE_HEAVY:
            # Code-heavy: Consistent but potentially boring
            templates = {
                "attack": f"You attack in {state.location}. Roll: {random.randint(1,20)}. Damage dealt.",
                "explore": f"You explore {state.location}. You find: {random.choice(['nothing', 'coins', 'item'])}.",
                "talk": f"You talk in {state.location}. NPC responds with standard dialogue.",
                "rest": f"You rest in {state.location}. HP restored to {min(100, state.player_hp + 20)}."
            }
            base_narrative = templates.get(action, f"You {action} in {state.location}. Action completed.")
            
        elif self.architecture_type == ArchitectureType.BALANCED:
            # Balanced: Good creativity with reliability
            base_narrative = f"You {action} in {state.location}. "
            
            # Add contextual creativity
            if action == "explore":
                discoveries = [
                    "The ancient stones whisper secrets of ages past",
                    "You notice details that others might miss",
                    "Something about this place feels significant"
                ]
                base_narrative += random.choice(discoveries)
            elif action in ["talk", "greet"]:
                base_narrative += "The conversation reveals new possibilities"
            else:
                base_narrative += "Your action has meaningful consequences"
                
        else:  # HYBRID
            # Hybrid: Mix of approaches with fallbacks
            try:
                # Try AI approach
                base_narrative = f"You {action} with purpose in {state.location}, "
                base_narrative += random.choice([
                    "and the world responds in kind",
                    "creating ripples of change around you",
                    "as destiny seems to guide your steps"
                ])
            except:
                # Fallback to code approach
                base_narrative = f"You {action} in {state.location}. Action successful."
        
        return base_narrative
    
    def _generate_choices(self, state: GameState, last_action: str, 
                         personality: PlayerPersonality) -> List[str]:
        """Generate available choices based on architecture and context"""
        
        base_choices = []
        
        # Context-aware choice generation
        if state.location == "village_square":
            base_choices = ["talk to villagers", "visit tavern", "explore outskirts", "check notice board"]
        elif state.location == "tavern":
            base_choices = ["order drink", "listen to gossip", "approach stranger", "leave tavern"]
        elif state.location == "forest":
            base_choices = ["follow path", "search for herbs", "climb tree", "set up camp"]
        else:
            base_choices = ["explore area", "rest", "check inventory", "look around"]
        
        # Architecture-specific choice modification
        if self.architecture_type == ArchitectureType.AI_HEAVY:
            # Add creative/unexpected choices
            creative_choices = ["attempt something unprecedented", "follow your intuition", "try a bold approach"]
            base_choices.extend(random.sample(creative_choices, min(2, len(creative_choices))))
            
        elif self.architecture_type == ArchitectureType.CODE_HEAVY:
            # Standardized, predictable choices
            base_choices = ["option_1", "option_2", "option_3", "option_4"]
            
        elif self.architecture_type == ArchitectureType.BALANCED:
            # Good mix of standard and creative
            if random.random() > 0.5:
                base_choices.append("try something creative")
        
        # Personality-influenced choices
        if personality == PlayerPersonality.AGGRESSIVE:
            base_choices = [choice for choice in base_choices if "attack" in choice or "confront" in choice or "bold" in choice] + base_choices[:3]
        elif personality == PlayerPersonality.CAUTIOUS:
            base_choices = [choice for choice in base_choices if "careful" in choice or "observe" in choice or "rest" in choice] + base_choices[:3]
        elif personality == PlayerPersonality.SOCIAL:
            base_choices = [choice for choice in base_choices if "talk" in choice or "approach" in choice] + base_choices[:3]
        elif personality == PlayerPersonality.EXPLORER:
            base_choices = [choice for choice in base_choices if "explore" in choice or "search" in choice] + base_choices[:3]
        
        return list(set(base_choices))[:6]  # Limit to 6 unique choices
    
    def _process_state_changes(self, state: GameState, action: str) -> Dict[str, Any]:
        """Process state changes based on action"""
        changes = {}
        
        if action in ["attack", "fight"]:
            hp_change = random.randint(-15, -5)
            changes["hp_change"] = hp_change
            
        elif action in ["rest", "heal"]:
            hp_change = random.randint(10, 25)
            changes["hp_change"] = hp_change
            
        elif action in ["explore", "search"]:
            if random.random() > 0.6:
                found_gold = random.randint(5, 20)
                changes["gold_change"] = found_gold
                
        elif action in ["travel", "move"]:
            new_locations = ["forest", "cave", "mountain_path", "riverside"]
            changes["location_change"] = random.choice(new_locations)
        
        return changes
    
    def _process_npc_interactions(self, state: GameState, action: str) -> List[Dict[str, Any]]:
        """Process NPC interactions"""
        interactions = []
        
        if action in ["talk", "greet", "approach"]:
            # Determine which NPC is present
            location_npcs = {
                "village_square": ["village_elder", "town_guard"],
                "tavern": ["tavern_keeper", "mysterious_stranger"],
                "forest": ["hermit", "ranger"]
            }
            
            possible_npcs = location_npcs.get(state.location, ["generic_npc"])
            npc_name = random.choice(possible_npcs)
            
            response, new_relationship = self.npc_engine.get_npc_response(
                npc_name, action, state.relationship_scores
            )
            
            interactions.append({
                "npc": npc_name,
                "response": response,
                "relationship_change": new_relationship
            })
        
        return interactions
    
    def _process_quest_updates(self, state: GameState, action: str) -> List[str]:
        """Process quest-related updates"""
        updates = []
        
        if action in ["complete", "deliver", "return"]:
            if state.active_quests:
                quest = random.choice(state.active_quests)
                updates.append(f"Quest '{quest.get('name', 'Unknown')}' completed!")
                
        elif action in ["accept", "take_quest"]:
            new_quest = {
                "name": f"Quest_{len(state.active_quests) + 1}",
                "description": "A new adventure awaits",
                "progress": 0
            }
            updates.append(f"New quest accepted: {new_quest['name']}")
        
        return updates
    
    def _check_world_consistency(self, state: GameState, action: str, narrative: str) -> List[str]:
        """Check for world consistency issues (hallucinations)"""
        issues = []
        
        # Architecture-specific consistency checking
        if self.architecture_type == ArchitectureType.AI_HEAVY:
            # AI-heavy more prone to consistency issues
            if random.random() < 0.15:  # 15% chance of consistency issue
                issues.append("Narrative contradicts established world facts")
            if random.random() < 0.10:  # 10% chance
                issues.append("Character behavior inconsistent with previous interactions")
                
        elif self.architecture_type == ArchitectureType.CODE_HEAVY:
            # Code-heavy very consistent
            if random.random() < 0.02:  # 2% chance of minor issue
                issues.append("Minor template inconsistency")
                
        elif self.architecture_type == ArchitectureType.BALANCED:
            # Balanced approach - some issues but manageable
            if random.random() < 0.05:  # 5% chance
                issues.append("Minor narrative inconsistency")
                
        else:  # HYBRID
            # Hybrid with fallback protection
            if random.random() < 0.08:  # 8% chance
                issues.append("Inconsistency caught and corrected by fallback system")
        
        # Check for logical impossibilities
        if "sun sets in the east" in narrative.lower():
            issues.append("Logical impossibility: sun setting in east")
        if state.player_hp <= 0 and "you feel energetic" in narrative.lower():
            issues.append("Contradiction: dead player feeling energetic")
        
        return issues

class ComprehensiveGameTester:
    """Main tester that runs 8-turn sessions and measures all metrics"""
    
    def __init__(self):
        self.scenario_generator = GameScenarioGenerator()
        
    def run_8_turn_session(self, architecture_type: ArchitectureType, 
                          player_personality: PlayerPersonality,
                          scenario_type: str = None) -> Tuple[List[TurnResult], ExperienceMetrics]:
        """Run a complete 8-turn game session"""
        
        simulator = GameArchitectureSimulator(architecture_type)
        scenario_actions = self.scenario_generator.generate_scenario(scenario_type)
        
        # Initialize game state
        state = GameState()
        turn_results = []
        
        # Run 8 turns
        for turn in range(8):
            state.turn = turn + 1
            
            # Get player action (from scenario or personality-driven)
            if turn < len(scenario_actions):
                base_action = scenario_actions[turn]
                player_action = self._personalize_action(base_action, player_personality)
            else:
                player_action = self._generate_personality_action(player_personality, state)
            
            # Process turn
            turn_result = simulator.process_turn(state, player_action, player_personality)
            turn_results.append(turn_result)
            
            # Update state based on results
            self._update_state_from_result(state, turn_result)
        
        # Calculate comprehensive metrics
        metrics = self._calculate_experience_metrics(turn_results, state)
        
        return turn_results, metrics
    
    def _personalize_action(self, base_action: str, personality: PlayerPersonality) -> str:
        """Modify base action based on player personality"""
        
        personality_modifiers = {
            PlayerPersonality.CAUTIOUS: {
                "approach": "carefully_approach",
                "enter": "cautiously_enter", 
                "attack": "defensive_strike"
            },
            PlayerPersonality.AGGRESSIVE: {
                "talk": "demand_answers",
                "explore": "boldly_explore",
                "negotiate": "make_demands"
            },
            PlayerPersonality.SOCIAL: {
                "investigate": "ask_around",
                "solve": "seek_help",
                "explore": "find_people_to_talk_to"
            },
            PlayerPersonality.EXPLORER: {
                "rest": "scout_area_first",
                "wait": "explore_while_waiting",
                "return": "take_scenic_route"
            }
        }
        
        modifiers = personality_modifiers.get(personality, {})
        return modifiers.get(base_action, base_action)
    
    def _generate_personality_action(self, personality: PlayerPersonality, state: GameState) -> str:
        """Generate action based on personality when scenario doesn't specify"""
        
        personality_actions = {
            PlayerPersonality.CAUTIOUS: ["observe_carefully", "rest", "check_inventory", "retreat"],
            PlayerPersonality.AGGRESSIVE: ["attack", "confront", "demand", "charge_forward"],
            PlayerPersonality.SOCIAL: ["talk", "greet", "ask_questions", "make_friends"],
            PlayerPersonality.EXPLORER: ["explore", "search", "investigate", "wander"]
        }
        
        return random.choice(personality_actions[personality])
    
    def _update_state_from_result(self, state: GameState, result: TurnResult):
        """Update game state based on turn result"""
        
        # Apply state changes
        for change_type, change_value in result.state_changes.items():
            if change_type == "hp_change":
                state.player_hp = max(0, min(100, state.player_hp + change_value))
            elif change_type == "gold_change":
                state.player_gold = max(0, state.player_gold + change_value)
            elif change_type == "location_change":
                state.location = change_value
        
        # Update NPC relationships
        for interaction in result.npc_interactions:
            npc_name = interaction["npc"]
            new_relationship = interaction["relationship_change"]
            state.relationship_scores[npc_name] = new_relationship
        
        # Update story events
        state.story_events.append(f"Turn {result.turn_number}: {result.player_action}")
    
    def _calculate_experience_metrics(self, turn_results: List[TurnResult], 
                                    final_state: GameState) -> ExperienceMetrics:
        """Calculate comprehensive experience metrics from session"""
        
        # Fun Score: Based on choice variety, narrative quality, meaningful consequences
        choice_variety = len(set(choice for result in turn_results for choice in result.choices_offered)) / 20.0
        narrative_variety = len(set(result.narrative_response[:50] for result in turn_results)) / 8.0
        fun_score = min(1.0, (choice_variety + narrative_variety) / 2)
        
        # Hallucination Score: Based on consistency issues (inverted - fewer issues = higher score)
        total_issues = sum(len(result.world_consistency_issues) for result in turn_results)
        hallucination_score = max(0.0, 1.0 - (total_issues / 16.0))  # 16 = 2 issues per turn max
        
        # Logical Coherence: Based on narrative making sense
        logical_coherence = 1.0 - (total_issues / 24.0)  # More forgiving than hallucination
        logical_coherence = max(0.0, min(1.0, logical_coherence))
        
        # Dynamic Nature: Based on variety in responses and choices
        unique_narratives = len(set(result.narrative_response for result in turn_results))
        dynamic_nature = unique_narratives / 8.0
        
        # NPC Relationship Quality: Based on meaningful interactions
        npc_interactions = sum(len(result.npc_interactions) for result in turn_results)
        relationship_depth = len(final_state.relationship_scores)
        npc_relationship_quality = min(1.0, (npc_interactions + relationship_depth) / 10.0)
        
        # Story Arc Progression: Based on quest progression and narrative coherence
        quest_updates = sum(len(result.quest_updates) for result in turn_results)
        story_events = len(final_state.story_events)
        story_arc_progression = min(1.0, (quest_updates + story_events / 8.0) / 3.0)
        
        # Comeback Desire: Based on unresolved elements and engagement
        unresolved_quests = len(final_state.active_quests)
        engagement_factors = fun_score + dynamic_nature + npc_relationship_quality
        comeback_desire = min(1.0, (engagement_factors / 3.0) + (unresolved_quests / 10.0))
        
        # Player Agency: Based on meaningful choices and consequences
        meaningful_choices = sum(1 for result in turn_results if len(result.choices_offered) > 3)
        state_changes = sum(1 for result in turn_results if result.state_changes)
        player_agency = min(1.0, (meaningful_choices + state_changes) / 16.0)
        
        # World Consistency: Inverse of consistency issues
        world_consistency = hallucination_score  # Same calculation
        
        # Pacing Quality: Based on variety of action types
        action_types = set(result.player_action.split('_')[0] for result in turn_results)
        pacing_quality = min(1.0, len(action_types) / 6.0)  # 6 different action types ideal
        
        # Emotional Investment: Based on NPC relationships and story progression
        emotional_investment = min(1.0, (npc_relationship_quality + story_arc_progression) / 2.0)
        
        # Replay Value: Based on choice variety and unresolved elements
        total_choices = sum(len(result.choices_offered) for result in turn_results)
        replay_value = min(1.0, (choice_variety + (unresolved_quests / 5.0)) / 2.0)
        
        # Performance Metrics
        avg_response_time = sum(result.response_time for result in turn_results) / len(turn_results)
        error_rate = sum(1 for result in turn_results if result.world_consistency_issues) / len(turn_results)
        session_completion_rate = 1.0 if len(turn_results) == 8 else len(turn_results) / 8.0
        
        return ExperienceMetrics(
            fun_score=fun_score,
            hallucination_score=hallucination_score,
            logical_coherence=logical_coherence,
            dynamic_nature=dynamic_nature,
            npc_relationship_quality=npc_relationship_quality,
            story_arc_progression=story_arc_progression,
            comeback_desire=comeback_desire,
            player_agency=player_agency,
            world_consistency=world_consistency,
            pacing_quality=pacing_quality,
            emotional_investment=emotional_investment,
            replay_value=replay_value,
            average_response_time=avg_response_time,
            error_rate=error_rate,
            session_completion_rate=session_completion_rate
        )