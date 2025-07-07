"""
Architecture Testing Framework
Systematically test different AI/Code responsibility splits to find optimal balance.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Callable
from enum import Enum
import time
import json
from datetime import datetime

class ComponentType(Enum):
    AI = "ai"
    CODE = "code" 
    HYBRID = "hybrid"

@dataclass
class ArchitectureConfig:
    """Defines how responsibilities are split between AI and Code"""
    name: str
    state_management: ComponentType
    narrative_generation: ComponentType
    action_processing: ComponentType
    choice_generation: ComponentType
    consistency_checking: ComponentType

@dataclass
class TestMetrics:
    """Measurable outcomes from architecture testing"""
    reliability_score: float  # 0-1, consistency of outputs
    response_time: float     # Average response time in seconds
    story_coherence: float   # 0-1, narrative consistency
    choice_variety: float    # 0-1, diversity of options
    session_length: float    # Average session duration
    error_rate: float        # Percentage of failed operations

class ArchitectureTester:
    """Test different AI/Code architectures systematically"""
    
    def __init__(self):
        self.test_scenarios = []
        self.results = {}
        
    def define_test_architectures(self) -> Dict[str, ArchitectureConfig]:
        """Define different architecture configurations to test"""
        return {
            "ai_heavy": ArchitectureConfig(
                name="AI Heavy",
                state_management=ComponentType.AI,
                narrative_generation=ComponentType.AI,
                action_processing=ComponentType.AI,
                choice_generation=ComponentType.AI,
                consistency_checking=ComponentType.CODE
            ),
            "balanced": ArchitectureConfig(
                name="Balanced",
                state_management=ComponentType.CODE,
                narrative_generation=ComponentType.AI,
                action_processing=ComponentType.HYBRID,
                choice_generation=ComponentType.AI,
                consistency_checking=ComponentType.CODE
            ),
            "code_heavy": ArchitectureConfig(
                name="Code Heavy", 
                state_management=ComponentType.CODE,
                narrative_generation=ComponentType.HYBRID,
                action_processing=ComponentType.CODE,
                choice_generation=ComponentType.HYBRID,
                consistency_checking=ComponentType.CODE
            ),
            "reliability_focused": ArchitectureConfig(
                name="Reliability Focused",
                state_management=ComponentType.CODE,
                narrative_generation=ComponentType.HYBRID,
                action_processing=ComponentType.CODE,
                choice_generation=ComponentType.CODE,
                consistency_checking=ComponentType.CODE
            )
        }
    
    def create_test_scenarios(self) -> List[Dict[str, Any]]:
        """Create standardized test scenarios"""
        return [
            {
                "name": "combat_encounter",
                "description": "Player fights a goblin",
                "initial_state": {"hp": 100, "location": "forest", "enemy": "goblin"},
                "actions": ["attack", "defend", "flee", "use_item"],
                "expected_outcomes": ["victory", "defeat", "escape"]
            },
            {
                "name": "social_interaction", 
                "description": "Player talks to village elder",
                "initial_state": {"location": "village", "npc": "elder", "reputation": "neutral"},
                "actions": ["ask_quest", "trade", "insult", "compliment"],
                "expected_outcomes": ["quest_received", "trade_completed", "reputation_change"]
            },
            {
                "name": "exploration",
                "description": "Player explores mysterious cave",
                "initial_state": {"location": "cave_entrance", "light": True, "inventory": ["torch"]},
                "actions": ["enter_cave", "examine_walls", "light_torch", "retreat"],
                "expected_outcomes": ["discovery", "trap_triggered", "treasure_found"]
            }
        ]
    
    def run_architecture_test(self, config: ArchitectureConfig, scenario: Dict[str, Any], 
                            iterations: int = 10) -> TestMetrics:
        """Run a specific architecture against a test scenario"""
        
        results = []
        start_time = time.time()
        errors = 0
        
        for i in range(iterations):
            try:
                # Simulate running the game with this architecture
                iteration_result = self._simulate_game_iteration(config, scenario)
                results.append(iteration_result)
            except Exception as e:
                errors += 1
                print(f"Error in iteration {i}: {e}")
        
        total_time = time.time() - start_time
        
        if not results:
            return TestMetrics(0, 0, 0, 0, 0, 1.0)
            
        # Calculate metrics
        reliability = self._calculate_reliability(results)
        response_time = total_time / len(results)
        coherence = self._calculate_coherence(results)
        variety = self._calculate_variety(results)
        session_length = sum(r.get('session_duration', 0) for r in results) / len(results)
        error_rate = errors / iterations
        
        return TestMetrics(
            reliability_score=reliability,
            response_time=response_time,
            story_coherence=coherence,
            choice_variety=variety,
            session_length=session_length,
            error_rate=error_rate
        )
    
    def _simulate_game_iteration(self, config: ArchitectureConfig, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate one game iteration with the given architecture"""
        
        # This would integrate with your actual game components
        # For now, simulate based on architecture choices
        
        result = {
            'scenario': scenario['name'],
            'architecture': config.name,
            'session_duration': 0,
            'choices_generated': [],
            'narrative_quality': 0,
            'consistency_score': 0,
            'errors': []
        }
        
        # Simulate different performance based on component types
        if config.narrative_generation == ComponentType.AI:
            result['narrative_quality'] = 0.8 + (0.2 * (1 - 0.1))  # High quality, some variance
            result['session_duration'] += 2.5  # AI takes longer
        elif config.narrative_generation == ComponentType.HYBRID:
            result['narrative_quality'] = 0.7 + (0.2 * (1 - 0.05))  # Good quality, less variance
            result['session_duration'] += 1.5
        else:  # CODE
            result['narrative_quality'] = 0.6  # Consistent but lower quality
            result['session_duration'] += 0.8
            
        if config.choice_generation == ComponentType.AI:
            result['choices_generated'] = ['creative_option_1', 'creative_option_2', 'unexpected_option']
            result['session_duration'] += 1.0
        elif config.choice_generation == ComponentType.HYBRID:
            result['choices_generated'] = ['standard_option_1', 'standard_option_2', 'contextual_option']
            result['session_duration'] += 0.5
        else:  # CODE
            result['choices_generated'] = ['option_1', 'option_2', 'option_3']
            result['session_duration'] += 0.2
            
        if config.consistency_checking == ComponentType.CODE:
            result['consistency_score'] = 0.95  # Very consistent
        else:
            result['consistency_score'] = 0.75  # Less consistent
            
        return result
    
    def _calculate_reliability(self, results: List[Dict[str, Any]]) -> float:
        """Calculate reliability score based on consistency"""
        if not results:
            return 0.0
            
        consistency_scores = [r.get('consistency_score', 0) for r in results]
        return sum(consistency_scores) / len(consistency_scores)
    
    def _calculate_coherence(self, results: List[Dict[str, Any]]) -> float:
        """Calculate story coherence score"""
        if not results:
            return 0.0
            
        narrative_scores = [r.get('narrative_quality', 0) for r in results]
        return sum(narrative_scores) / len(narrative_scores)
    
    def _calculate_variety(self, results: List[Dict[str, Any]]) -> float:
        """Calculate choice variety score"""
        if not results:
            return 0.0
            
        all_choices = []
        for result in results:
            all_choices.extend(result.get('choices_generated', []))
            
        unique_choices = len(set(all_choices))
        total_choices = len(all_choices)
        
        return unique_choices / total_choices if total_choices > 0 else 0.0
    
    def run_comprehensive_test(self) -> Dict[str, Dict[str, TestMetrics]]:
        """Run all architectures against all scenarios"""
        
        architectures = self.define_test_architectures()
        scenarios = self.create_test_scenarios()
        
        results = {}
        
        print("🔬 Starting Architecture Testing...")
        print(f"Testing {len(architectures)} architectures against {len(scenarios)} scenarios")
        
        for arch_name, arch_config in architectures.items():
            print(f"\n🧪 Testing {arch_config.name} Architecture...")
            results[arch_name] = {}
            
            for scenario in scenarios:
                print(f"  📋 Scenario: {scenario['name']}")
                metrics = self.run_architecture_test(arch_config, scenario)
                results[arch_name][scenario['name']] = metrics
                
                print(f"    ✅ Reliability: {metrics.reliability_score:.2f}")
                print(f"    ⚡ Response Time: {metrics.response_time:.2f}s")
                print(f"    📖 Coherence: {metrics.story_coherence:.2f}")
                print(f"    🎲 Variety: {metrics.choice_variety:.2f}")
        
        return results
    
    def calculate_balance_scores(self, results: Dict[str, Dict[str, TestMetrics]]) -> Dict[str, float]:
        """Calculate the sweet spot balance score for each architecture"""
        
        balance_scores = {}
        
        for arch_name, scenarios in results.items():
            # Average metrics across all scenarios
            avg_reliability = sum(m.reliability_score for m in scenarios.values()) / len(scenarios)
            avg_coherence = sum(m.story_coherence for m in scenarios.values()) / len(scenarios)
            avg_variety = sum(m.choice_variety for m in scenarios.values()) / len(scenarios)
            avg_response_time = sum(m.response_time for m in scenarios.values()) / len(scenarios)
            avg_error_rate = sum(m.error_rate for m in scenarios.values()) / len(scenarios)
            
            # Balance formula: Reliability * Engagement - Performance Penalties
            engagement = (avg_coherence + avg_variety) / 2
            performance_penalty = (avg_response_time / 10) + avg_error_rate  # Normalize response time
            
            balance_score = (avg_reliability * engagement) - performance_penalty
            balance_scores[arch_name] = max(0, balance_score)  # Don't go negative
            
        return balance_scores
    
    def generate_recommendations(self, results: Dict[str, Dict[str, TestMetrics]], 
                               balance_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate actionable recommendations based on test results"""
        
        best_architecture = max(balance_scores.items(), key=lambda x: x[1])
        
        recommendations = {
            'optimal_architecture': best_architecture[0],
            'balance_score': best_architecture[1],
            'key_insights': [],
            'specific_recommendations': []
        }
        
        # Analyze patterns
        for arch_name, scenarios in results.items():
            avg_reliability = sum(m.reliability_score for m in scenarios.values()) / len(scenarios)
            avg_coherence = sum(m.story_coherence for m in scenarios.values()) / len(scenarios)
            
            if avg_reliability > 0.9:
                recommendations['key_insights'].append(f"{arch_name}: Excellent reliability")
            if avg_coherence > 0.8:
                recommendations['key_insights'].append(f"{arch_name}: High narrative quality")
                
        # Generate specific recommendations
        if best_architecture[0] == 'balanced':
            recommendations['specific_recommendations'].append(
                "Balanced architecture performs best - use AI for narrative, Code for state management"
            )
        elif best_architecture[0] == 'code_heavy':
            recommendations['specific_recommendations'].append(
                "Code-heavy approach wins - prioritize reliability over creativity"
            )
        elif best_architecture[0] == 'ai_heavy':
            recommendations['specific_recommendations'].append(
                "AI-heavy approach wins - creativity outweighs consistency concerns"
            )
            
        return recommendations
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"architecture_test_results_{timestamp}.json"
            
        # Convert TestMetrics objects to dictionaries for JSON serialization
        serializable_results = {}
        for arch_name, scenarios in results.items():
            serializable_results[arch_name] = {}
            for scenario_name, metrics in scenarios.items():
                serializable_results[arch_name][scenario_name] = {
                    'reliability_score': metrics.reliability_score,
                    'response_time': metrics.response_time,
                    'story_coherence': metrics.story_coherence,
                    'choice_variety': metrics.choice_variety,
                    'session_length': metrics.session_length,
                    'error_rate': metrics.error_rate
                }
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2)
            
        print(f"📊 Results saved to {filename}")