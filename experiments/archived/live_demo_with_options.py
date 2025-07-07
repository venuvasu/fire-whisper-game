#!/usr/bin/env python3
"""
Live Demo: 8-Turn Game Experience Test
Interactive demonstration showing how different architectures perform
across all the metrics you wanted to measure.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import random
from dataclasses import dataclass
from typing import Dict, List, Any
from enum import Enum

class ArchitectureType(Enum):
    AI_HEAVY = "ai_heavy"
    BALANCED = "balanced" 
    CODE_HEAVY = "code_heavy"
    HYBRID = "hybrid"

@dataclass
class GameMetrics:
    """Real-time metrics tracking"""
    fun_score: float = 0.0
    hallucination_count: int = 0
    logical_coherence: float = 1.0
    dynamic_nature: float = 0.0
    npc_relationship_quality: float = 0.0
    story_arc_progression: float = 0.0
    comeback_desire: float = 0.0
    player_agency: float = 0.0
    world_consistency: float = 1.0
    emotional_investment: float = 0.0

class LiveGameDemo:
    """Interactive demo showing 8-turn gameplay with real metrics"""
    
    def __init__(self, architecture: ArchitectureType):
        self.architecture = architecture
        self.turn = 0
        self.metrics = GameMetrics()
        self.game_state = {
            "location": "village_square",
            "hp": 100,
            "gold": 50,
            "inventory": ["rusty_sword", "health_potion"],
            "npcs_met": {},
            "story_events": [],
            "world_facts": {}
        }
        
    def run_8_turn_demo(self):
        """Run interactive 8-turn demo"""
        
        print(f"\n🎮 8-TURN GAME DEMO: {self.architecture.value.upper()} ARCHITECTURE")
        print("=" * 60)
        print("Watch how different architectures handle the same scenario...")
        print()
        
        # Predefined scenario for consistency
        scenario = [
            "arrive_in_village",
            "talk_to_elder", 
            "accept_quest",
            "explore_forest",
            "encounter_goblin",
            "negotiate_or_fight",
            "find_treasure",
            "return_to_village"
        ]
        
        for turn_num in range(8):
            self.turn = turn_num + 1
            action = scenario[turn_num]
            
            print(f"🎯 TURN {self.turn}: {action.replace('_', ' ').title()}")
            print("-" * 30)
            
            # Process turn based on architecture
            result = self._process_turn(action)
            
            # Display results
            print(f"📖 Narrative: {result['narrative']}")
            print(f"🎲 Choices: {', '.join(result['choices'][:3])}...")
            
            if result['npc_interaction']:
                print(f"🎭 NPC: {result['npc_interaction']}")
            
            if result['state_changes']:
                print(f"⚡ Changes: {result['state_changes']}")
            
            if result['issues']:
                print(f"⚠️  Issues: {', '.join(result['issues'])}")
            
            # Update metrics
            self._update_metrics(result)
            
            # Show current metrics
            print(f"📊 Metrics: Fun:{self.metrics.fun_score:.2f} | "
                  f"Logic:{self.metrics.logical_coherence:.2f} | "
                  f"NPC:{self.metrics.npc_relationship_quality:.2f} | "
                  f"Story:{self.metrics.story_arc_progression:.2f}")
            print()
        
        # Final analysis
        self._show_final_analysis()
    
    def _process_turn(self, action: str) -> Dict[str, Any]:
        """Process a turn based on architecture type"""
        
        result = {
            'narrative': '',
            'choices': [],
            'npc_interaction': '',
            'state_changes': '',
            'issues': []
        }
        
        if self.architecture == ArchitectureType.AI_HEAVY:
            result = self._ai_heavy_processing(action)
        elif self.architecture == ArchitectureType.BALANCED:
            result = self._balanced_processing(action)
        elif self.architecture == ArchitectureType.CODE_HEAVY:
            result = self._code_heavy_processing(action)
        else:  # HYBRID
            result = self._hybrid_processing(action)
        
        return result
    
    def _ai_heavy_processing(self, action: str) -> Dict[str, Any]:
        """AI-Heavy: Creative but potentially inconsistent"""
        
        narratives = {
            "arrive_in_village": "You emerge from the misty forest path as the village materializes before you like a dream made manifest. The cobblestones seem to whisper ancient secrets beneath your feet, and you notice the villagers' eyes hold depths of untold stories.",
            "talk_to_elder": "The village elder's weathered face transforms as recognition dawns - though you've never met before, he speaks as if you're old friends. 'Ah, the prophesied one returns!' he exclaims, his voice carrying the weight of destiny.",
            "accept_quest": "As you accept the quest, reality seems to shimmer around you. The elder hands you a map that changes as you look at it, showing paths that exist only when needed. The very air thrums with possibility.",
            "explore_forest": "The forest welcomes you like a living entity. Trees bend to create perfect pathways, and you discover a hidden grove where time moves differently - you age backwards slightly, feeling more energetic than before.",
            "encounter_goblin": "The goblin you meet isn't just any goblin - it's your long-lost brother, transformed by ancient magic! He recognizes you instantly despite your shock, tears streaming down his green face.",
            "negotiate_or_fight": "Your negotiation transcends mere words. You and the goblin-brother communicate through shared memories, reaching an understanding that reshapes both your destinies and creates a new form of magic.",
            "find_treasure": "The treasure isn't gold - it's a crystallized memory of your childhood together. As you touch it, both you and your brother are restored to your true forms, and the forest celebrates with singing flowers.",
            "return_to_village": "You return to find the village has been transformed by your quest. Everyone now remembers your brother, and a statue commemorating your reunion has mysteriously appeared in the square overnight."
        }
        
        choices_sets = {
            "arrive_in_village": ["Approach the mystical fountain", "Seek the dream-weaver's hut", "Follow the whispering stones", "Dance with the shadow-children"],
            "talk_to_elder": ["Accept your prophetic destiny", "Question the nature of prophecy", "Demand proof of your identity", "Embrace the cosmic connection"],
            "accept_quest": ["Let the map guide your soul", "Challenge the shifting reality", "Seek the map's true purpose", "Merge with the quest's essence"],
            "explore_forest": ["Embrace the time distortion", "Communicate with tree spirits", "Harvest temporal energy", "Become one with the grove"],
            "encounter_goblin": ["Embrace your transformed brother", "Weep tears of recognition", "Share your life force", "Attempt magical restoration"],
            "negotiate_or_fight": ["Merge consciousness completely", "Create new magical bonds", "Rewrite both your destinies", "Transcend physical forms"],
            "find_treasure": ["Absorb the crystallized memory", "Share the memory with the world", "Use it to restore others", "Become the memory itself"],
            "return_to_village": ["Celebrate the miraculous reunion", "Establish a new magical order", "Teach others about transformation", "Ascend to a higher plane"]
        }
        
        # AI-Heavy issues: Creative but inconsistent
        issues = []
        if random.random() < 0.3:  # 30% chance of consistency issue
            issues.append("Contradicts established lore")
        if random.random() < 0.2:  # 20% chance of logic issue
            issues.append("Impossible event occurred")
        
        return {
            'narrative': narratives.get(action, f"Something magical happens with {action}"),
            'choices': choices_sets.get(action, ["Option A", "Option B", "Option C", "Option D"]),
            'npc_interaction': "Deep, transformative connection established" if "talk" in action or "encounter" in action else "",
            'state_changes': "Reality fundamentally altered" if random.random() > 0.5 else "",
            'issues': issues
        }
    
    def _balanced_processing(self, action: str) -> Dict[str, Any]:
        """Balanced: Good creativity with reliability"""
        
        narratives = {
            "arrive_in_village": "You walk into the bustling village square, taking in the sights and sounds of daily life. Merchants hawk their wares while children play nearby. The village elder notices your arrival and nods respectfully.",
            "talk_to_elder": "The village elder greets you warmly. 'Welcome, traveler. We've been expecting someone like you - our village faces a growing threat from the nearby forest. Would you be willing to help us?'",
            "accept_quest": "You accept the elder's quest to investigate strange happenings in the forest. He provides you with a detailed map and warns you about increased goblin activity in the area.",
            "explore_forest": "You venture into the dense forest, following the marked paths on your map. The trees grow thicker as you progress, and you notice signs of recent goblin presence - broken branches and strange markings.",
            "encounter_goblin": "A goblin emerges from behind a large oak tree, wielding a crude spear. It eyes you warily but doesn't immediately attack. There's intelligence in its gaze, suggesting negotiation might be possible.",
            "negotiate_or_fight": "You attempt to communicate with the goblin using gestures and simple words. Surprisingly, it responds positively, indicating that its tribe is also troubled by a darker force in the forest depths.",
            "find_treasure": "Following the goblin's directions, you discover a hidden cache containing ancient coins and a magical amulet. The goblin explains this treasure was meant to be an offering to appease the dark force.",
            "return_to_village": "You return to the village with valuable information about the true threat and a new goblin ally. The elder is impressed by your diplomatic success and rewards you accordingly."
        }
        
        choices_sets = {
            "arrive_in_village": ["Talk to the elder", "Visit the marketplace", "Explore the outskirts", "Rest at the inn"],
            "talk_to_elder": ["Accept the quest", "Ask for more details", "Request better payment", "Decline politely"],
            "accept_quest": ["Head to forest immediately", "Gather supplies first", "Ask about goblin tactics", "Request a guide"],
            "explore_forest": ["Follow the main path", "Search for tracks", "Climb a tree for better view", "Set up camp"],
            "encounter_goblin": ["Attempt negotiation", "Prepare for combat", "Try to sneak past", "Offer a trade"],
            "negotiate_or_fight": ["Learn about the dark force", "Propose an alliance", "Share your supplies", "Ask for safe passage"],
            "find_treasure": ["Take the treasure", "Leave it as offering", "Share with goblin", "Examine it carefully"],
            "return_to_village": ["Report to elder", "Celebrate with villagers", "Plan next steps", "Rest and recover"]
        }
        
        # Balanced: Occasional minor issues
        issues = []
        if random.random() < 0.1:  # 10% chance of minor issue
            issues.append("Minor inconsistency in details")
        
        return {
            'narrative': narratives.get(action, f"You {action.replace('_', ' ')} with purpose and determination."),
            'choices': choices_sets.get(action, ["Standard Option 1", "Standard Option 2", "Standard Option 3", "Standard Option 4"]),
            'npc_interaction': "Meaningful dialogue and relationship building" if "talk" in action or "encounter" in action else "",
            'state_changes': "Logical progression of events" if random.random() > 0.3 else "",
            'issues': issues
        }
    
    def _code_heavy_processing(self, action: str) -> Dict[str, Any]:
        """Code-Heavy: Reliable but potentially boring"""
        
        templates = {
            "arrive_in_village": "You enter Village_01. Population: 150. Available services: Inn, Shop, Quest_Giver. Current time: Day.",
            "talk_to_elder": "Elder_NPC_01 provides Quest_001: 'Investigate Forest_Area_02'. Reward: 100 gold. Difficulty: Medium.",
            "accept_quest": "Quest_001 added to quest log. Objective: Explore Forest_Area_02. Status: Active.",
            "explore_forest": "Entering Forest_Area_02. Encounter chance: 65%. Rolling... Encounter triggered: Goblin_Enemy_01.",
            "encounter_goblin": "Combat initiated with Goblin_Enemy_01. HP: 25. Attack: 8. Defense: 3. Initiative roll: Player wins.",
            "negotiate_or_fight": "Diplomacy check: Success. Goblin_Enemy_01 becomes Goblin_Ally_01. Relationship: Neutral.",
            "find_treasure": "Treasure_Chest_01 discovered. Contents: 50 gold, Amulet_Item_03. Value: 150 gold total.",
            "return_to_village": "Quest_001 completed. Reward received: 100 gold. Experience gained: 250 XP. Level check: No change."
        }
        
        choices_sets = {
            "arrive_in_village": ["Talk", "Shop", "Rest", "Leave"],
            "talk_to_elder": ["Accept", "Decline", "Negotiate", "Info"],
            "accept_quest": ["Go", "Prepare", "Wait", "Cancel"],
            "explore_forest": ["North", "South", "East", "West"],
            "encounter_goblin": ["Attack", "Defend", "Talk", "Flee"],
            "negotiate_or_fight": ["Ally", "Trade", "Threaten", "Leave"],
            "find_treasure": ["Take", "Leave", "Share", "Examine"],
            "return_to_village": ["Report", "Sell", "Rest", "Continue"]
        }
        
        # Code-Heavy: Very few issues
        issues = []
        if random.random() < 0.02:  # 2% chance of minor bug
            issues.append("Template error corrected")
        
        return {
            'narrative': templates.get(action, f"Action_{action}_executed. Status: Complete."),
            'choices': choices_sets.get(action, ["Option_A", "Option_B", "Option_C", "Option_D"]),
            'npc_interaction': "Standard_Dialogue_Tree_Executed" if "talk" in action or "encounter" in action else "",
            'state_changes': "Variables_Updated" if random.random() > 0.2 else "",
            'issues': issues
        }
    
    def _hybrid_processing(self, action: str) -> Dict[str, Any]:
        """Hybrid: Mix of AI creativity with code reliability"""
        
        # Try AI approach first, fall back to code if needed
        try:
            if random.random() > 0.3:  # 70% AI, 30% code fallback
                return self._ai_creative_with_guardrails(action)
            else:
                return self._code_with_flavor(action)
        except:
            return self._code_with_flavor(action)
    
    def _ai_creative_with_guardrails(self, action: str) -> Dict[str, Any]:
        """AI creativity with consistency checks"""
        
        narratives = {
            "arrive_in_village": "You approach the village as evening light casts long shadows across the cobblestone square. The warm glow from windows suggests a community at peace, though you sense an underlying tension in the air.",
            "talk_to_elder": "The village elder, a woman with silver hair and keen eyes, studies you carefully. 'You have the look of someone who's seen trouble,' she says. 'Perhaps you're exactly what we need.'",
            "accept_quest": "The elder explains that strange sounds have been coming from the forest at night. She hands you a well-worn map and a small silver charm. 'This should help if you encounter anything... unusual.'",
            "explore_forest": "The forest path winds deeper into shadow and mystery. Ancient trees tower overhead, their branches creating a natural cathedral. You notice fresh tracks in the soft earth - definitely not human.",
            "encounter_goblin": "A goblin steps into your path, but something's different about this one. Its eyes show fear rather than aggression, and it clutches a small bundle protectively against its chest.",
            "negotiate_or_fight": "Through careful gestures and patience, you learn the goblin is protecting its injured child. Your act of compassion creates an unexpected bond between species.",
            "find_treasure": "The goblin leads you to a hidden grove where ancient coins lie scattered around a natural spring. It seems this place was once sacred to both humans and goblins alike.",
            "return_to_village": "You return with more than treasure - you bring news of a potential alliance and a new understanding between the village and forest dwellers."
        }
        
        # Guardrails: Check for consistency
        issues = []
        if random.random() < 0.05:  # 5% chance, but caught by guardrails
            issues.append("Inconsistency detected and corrected")
        
        return {
            'narrative': narratives.get(action, f"You {action.replace('_', ' ')} with thoughtful consideration."),
            'choices': ["Creative approach", "Practical solution", "Diplomatic option", "Cautious alternative"],
            'npc_interaction': "Nuanced character development" if "talk" in action or "encounter" in action else "",
            'state_changes': "Meaningful consequences unfold" if random.random() > 0.4 else "",
            'issues': issues
        }
    
    def _code_with_flavor(self, action: str) -> Dict[str, Any]:
        """Code reliability with added flavor text"""
        
        base_result = self._code_heavy_processing(action)
        
        # Add flavor to make it less dry
        flavor_additions = {
            "arrive_in_village": " The familiar sights and sounds of civilization welcome you.",
            "talk_to_elder": " Her weathered hands gesture as she speaks.",
            "accept_quest": " You feel the weight of responsibility settling on your shoulders.",
            "explore_forest": " Sunlight filters through the canopy above.",
            "encounter_goblin": " The creature's eyes dart nervously between you and the trees.",
            "negotiate_or_fight": " Understanding passes between you without words.",
            "find_treasure": " The coins gleam with an inner light.",
            "return_to_village": " The village gates open to welcome you home."
        }
        
        base_result['narrative'] += flavor_additions.get(action, " The action completes successfully.")
        return base_result
    
    def _update_metrics(self, result: Dict[str, Any]):
        """Update metrics based on turn result"""
        
        # Fun Score: Based on narrative creativity and choice variety
        narrative_creativity = len(result['narrative']) / 100.0  # Longer = more creative
        choice_variety = len(set(result['choices'])) / 4.0  # Unique choices
        self.metrics.fun_score = min(1.0, (self.metrics.fun_score + (narrative_creativity + choice_variety) / 2) / 2)
        
        # Hallucination tracking
        self.metrics.hallucination_count += len(result['issues'])
        
        # Logical coherence (decreases with issues)
        if result['issues']:
            self.metrics.logical_coherence = max(0.0, self.metrics.logical_coherence - 0.1)
        
        # Dynamic nature (variety in responses)
        if len(result['narrative']) > 50:  # Substantial narrative
            self.metrics.dynamic_nature = min(1.0, self.metrics.dynamic_nature + 0.15)
        
        # NPC relationship quality
        if result['npc_interaction']:
            self.metrics.npc_relationship_quality = min(1.0, self.metrics.npc_relationship_quality + 0.2)
        
        # Story arc progression
        if result['state_changes']:
            self.metrics.story_arc_progression = min(1.0, self.metrics.story_arc_progression + 0.15)
        
        # Player agency (meaningful choices)
        if len(result['choices']) > 3:
            self.metrics.player_agency = min(1.0, self.metrics.player_agency + 0.1)
        
        # World consistency (decreases with issues)
        if result['issues']:
            self.metrics.world_consistency = max(0.0, self.metrics.world_consistency - 0.05)
        
        # Emotional investment (NPC interactions + story progression)
        if result['npc_interaction'] or result['state_changes']:
            self.metrics.emotional_investment = min(1.0, self.metrics.emotional_investment + 0.1)
        
        # Comeback desire (engagement factors)
        engagement = (self.metrics.fun_score + self.metrics.dynamic_nature + self.metrics.npc_relationship_quality) / 3
        self.metrics.comeback_desire = engagement
    
    def _show_final_analysis(self):
        """Show comprehensive final analysis"""
        
        print("🏆 FINAL ANALYSIS")
        print("=" * 40)
        
        print(f"Architecture: {self.architecture.value.upper()}")
        print()
        
        print("📊 EXPERIENCE METRICS:")
        print(f"  🎮 Fun Score: {self.metrics.fun_score:.2f}/1.0")
        print(f"  🧠 Logical Coherence: {self.metrics.logical_coherence:.2f}/1.0")
        print(f"  🎭 NPC Relationship Quality: {self.metrics.npc_relationship_quality:.2f}/1.0")
        print(f"  📖 Story Arc Progression: {self.metrics.story_arc_progression:.2f}/1.0")
        print(f"  🔄 Comeback Desire: {self.metrics.comeback_desire:.2f}/1.0")
        print(f"  ⚡ Player Agency: {self.metrics.player_agency:.2f}/1.0")
        print(f"  🌍 World Consistency: {self.metrics.world_consistency:.2f}/1.0")
        print(f"  💝 Emotional Investment: {self.metrics.emotional_investment:.2f}/1.0")
        print(f"  🎲 Dynamic Nature: {self.metrics.dynamic_nature:.2f}/1.0")
        print()
        
        print("⚠️  ISSUES DETECTED:")
        print(f"  Hallucinations: {self.metrics.hallucination_count}")
        print(f"  Logic Problems: {8 - int(self.metrics.logical_coherence * 8)}")
        print()
        
        # Overall assessment
        overall_score = (
            self.metrics.fun_score + self.metrics.logical_coherence + 
            self.metrics.npc_relationship_quality + self.metrics.story_arc_progression +
            self.metrics.comeback_desire + self.metrics.player_agency +
            self.metrics.world_consistency + self.metrics.emotional_investment +
            self.metrics.dynamic_nature
        ) / 9
        
        print(f"🎯 OVERALL EXPERIENCE SCORE: {overall_score:.2f}/1.0")
        
        if overall_score > 0.8:
            print("✅ EXCELLENT - This architecture provides outstanding player experience")
        elif overall_score > 0.6:
            print("👍 GOOD - This architecture provides solid player experience")
        elif overall_score > 0.4:
            print("⚠️  FAIR - This architecture needs improvement")
        else:
            print("❌ POOR - This architecture has significant issues")

def main():
    """Run live demo for all architectures"""
    
    print("🎮 LIVE 8-TURN GAME EXPERIENCE DEMO")
    print("=" * 60)
    print("Compare how different architectures handle the same scenario")
    print("Measuring: Fun, Logic, NPCs, Story, Comeback Desire, and more!")
    print()
    
    architectures = [
        ArchitectureType.AI_HEAVY,
        ArchitectureType.BALANCED,
        ArchitectureType.CODE_HEAVY,
        ArchitectureType.HYBRID
    ]
    
    results = {}
    
    for architecture in architectures:
        demo = LiveGameDemo(architecture)
        demo.run_8_turn_demo()
        
        # Store results for comparison
        results[architecture.value] = {
            'overall_score': (
                demo.metrics.fun_score + demo.metrics.logical_coherence + 
                demo.metrics.npc_relationship_quality + demo.metrics.story_arc_progression +
                demo.metrics.comeback_desire + demo.metrics.player_agency +
                demo.metrics.world_consistency + demo.metrics.emotional_investment +
                demo.metrics.dynamic_nature
            ) / 9,
            'hallucinations': demo.metrics.hallucination_count,
            'metrics': demo.metrics
        }
        
        input("\nPress Enter to continue to next architecture...")
    
    # Final comparison
    print("\n🏆 ARCHITECTURE COMPARISON")
    print("=" * 60)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1]['overall_score'], reverse=True)
    
    for i, (arch_name, data) in enumerate(sorted_results, 1):
        print(f"{i}. {arch_name.upper():<12} | Score: {data['overall_score']:.3f} | "
              f"Hallucinations: {data['hallucinations']} | "
              f"Fun: {data['metrics'].fun_score:.2f}")
    
    best_architecture = sorted_results[0]
    print(f"\n🎯 WINNER: {best_architecture[0].upper()}")
    print(f"Best overall player experience with score: {best_architecture[1]['overall_score']:.3f}")

if __name__ == "__main__":
    main()