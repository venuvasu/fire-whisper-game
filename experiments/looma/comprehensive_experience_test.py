#!/usr/bin/env python3
"""
Comprehensive Game Experience Test
Runs 8-turn sessions across different architectures and player personalities
to measure real player experience metrics.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from looma.core.comprehensive_game_tester import (
    ComprehensiveGameTester, ArchitectureType, PlayerPersonality, ExperienceMetrics
)
import json
from datetime import datetime
from typing import Dict, List, Any

def run_comprehensive_test():
    """Run comprehensive testing across all architectures and personalities"""
    
    print("🎮 Comprehensive Game Experience Testing")
    print("=" * 60)
    print("Testing 8-turn sessions across different architectures and player types")
    print()
    
    tester = ComprehensiveGameTester()
    
    # Test configurations
    architectures = list(ArchitectureType)
    personalities = list(PlayerPersonality)
    scenarios = ["village_quest", "dungeon_crawl", "social_intrigue"]
    
    results = {}
    session_count = 0
    total_sessions = len(architectures) * len(personalities) * len(scenarios)
    
    print(f"🔬 Running {total_sessions} test sessions...")
    print()
    
    # Run tests for each combination
    for architecture in architectures:
        results[architecture.value] = {}
        
        print(f"🏗️  Testing {architecture.value.upper()} Architecture")
        print("-" * 40)
        
        for personality in personalities:
            results[architecture.value][personality.value] = {}
            
            for scenario in scenarios:
                session_count += 1
                print(f"  📋 Session {session_count}/{total_sessions}: {personality.value} player, {scenario} scenario")
                
                # Run 8-turn session
                turn_results, metrics = tester.run_8_turn_session(
                    architecture, personality, scenario
                )
                
                results[architecture.value][personality.value][scenario] = {
                    'metrics': metrics,
                    'turn_count': len(turn_results),
                    'sample_turns': [
                        {
                            'turn': result.turn_number,
                            'action': result.player_action,
                            'narrative': result.narrative_response[:100] + "...",
                            'choices': len(result.choices_offered),
                            'issues': len(result.world_consistency_issues)
                        }
                        for result in turn_results[:3]  # Show first 3 turns
                    ]
                }
                
                # Show quick metrics
                print(f"    ✅ Fun: {metrics.fun_score:.2f} | 🧠 Logic: {metrics.logical_coherence:.2f} | "
                      f"🎭 NPC: {metrics.npc_relationship_quality:.2f} | 🔄 Comeback: {metrics.comeback_desire:.2f}")
        
        print()
    
    return results

def analyze_results(results: Dict[str, Any]):
    """Analyze and present comprehensive results"""
    
    print("\n📊 COMPREHENSIVE ANALYSIS")
    print("=" * 60)
    
    # Calculate average metrics per architecture
    architecture_averages = {}
    
    for arch_name, arch_data in results.items():
        metrics_sum = {}
        count = 0
        
        for personality_data in arch_data.values():
            for scenario_data in personality_data.values():
                metrics = scenario_data['metrics']
                count += 1
                
                for attr_name in dir(metrics):
                    if not attr_name.startswith('_') and isinstance(getattr(metrics, attr_name), (int, float)):
                        if attr_name not in metrics_sum:
                            metrics_sum[attr_name] = 0
                        metrics_sum[attr_name] += getattr(metrics, attr_name)
        
        # Calculate averages
        architecture_averages[arch_name] = {
            metric: value / count for metric, value in metrics_sum.items()
        }
    
    # Display key metrics comparison
    key_metrics = [
        'fun_score', 'hallucination_score', 'logical_coherence', 'dynamic_nature',
        'npc_relationship_quality', 'story_arc_progression', 'comeback_desire',
        'player_agency', 'world_consistency', 'emotional_investment'
    ]
    
    print("🎯 KEY METRICS COMPARISON")
    print("-" * 40)
    print(f"{'Architecture':<15} | {'Fun':<5} | {'Logic':<5} | {'NPC':<5} | {'Story':<5} | {'Come':<5} | {'Total':<5}")
    print("-" * 70)
    
    architecture_scores = {}
    
    for arch_name, averages in architecture_averages.items():
        # Calculate composite score
        core_metrics = [averages.get(metric, 0) for metric in key_metrics[:7]]  # First 7 are most important
        total_score = sum(core_metrics) / len(core_metrics)
        architecture_scores[arch_name] = total_score
        
        print(f"{arch_name:<15} | {averages.get('fun_score', 0):.2f} | "
              f"{averages.get('logical_coherence', 0):.2f} | "
              f"{averages.get('npc_relationship_quality', 0):.2f} | "
              f"{averages.get('story_arc_progression', 0):.2f} | "
              f"{averages.get('comeback_desire', 0):.2f} | "
              f"{total_score:.2f}")
    
    # Find best architecture
    best_architecture = max(architecture_scores.items(), key=lambda x: x[1])
    
    print(f"\n🏆 OPTIMAL ARCHITECTURE: {best_architecture[0].upper()}")
    print(f"Overall Score: {best_architecture[1]:.3f}")
    
    # Detailed analysis by player personality
    print(f"\n🎭 PLAYER PERSONALITY ANALYSIS")
    print("-" * 40)
    
    personality_preferences = {}
    
    for personality in PlayerPersonality:
        personality_scores = {}
        
        for arch_name, arch_data in results.items():
            if personality.value in arch_data:
                personality_data = arch_data[personality.value]
                
                # Average across scenarios for this personality
                scenario_scores = []
                for scenario_data in personality_data.values():
                    metrics = scenario_data['metrics']
                    core_metrics = [
                        metrics.fun_score, metrics.logical_coherence, 
                        metrics.npc_relationship_quality, metrics.comeback_desire
                    ]
                    scenario_scores.append(sum(core_metrics) / len(core_metrics))
                
                personality_scores[arch_name] = sum(scenario_scores) / len(scenario_scores)
        
        best_for_personality = max(personality_scores.items(), key=lambda x: x[1])
        personality_preferences[personality.value] = best_for_personality
        
        print(f"{personality.value.capitalize():<12} players prefer: {best_for_personality[0]:<12} (score: {best_for_personality[1]:.3f})")
    
    # Problem areas analysis
    print(f"\n⚠️  PROBLEM AREAS ANALYSIS")
    print("-" * 40)
    
    for arch_name, averages in architecture_averages.items():
        problems = []
        
        if averages.get('hallucination_score', 1) < 0.7:
            problems.append(f"High hallucination rate ({1-averages['hallucination_score']:.1%})")
        
        if averages.get('logical_coherence', 1) < 0.7:
            problems.append(f"Logic issues ({1-averages['logical_coherence']:.1%})")
        
        if averages.get('average_response_time', 0) > 2.5:
            problems.append(f"Slow responses ({averages['average_response_time']:.1f}s avg)")
        
        if averages.get('fun_score', 0) < 0.6:
            problems.append(f"Low engagement ({averages['fun_score']:.1%})")
        
        if problems:
            print(f"{arch_name:<15}: {', '.join(problems)}")
        else:
            print(f"{arch_name:<15}: No major issues detected")
    
    # Recommendations
    print(f"\n💡 STRATEGIC RECOMMENDATIONS")
    print("-" * 40)
    
    best_arch_data = architecture_averages[best_architecture[0]]
    
    print(f"1. IMPLEMENT {best_architecture[0].upper()} ARCHITECTURE")
    print(f"   - Provides best overall player experience")
    print(f"   - Balanced across all key metrics")
    
    if best_arch_data.get('hallucination_score', 1) < 0.9:
        print(f"2. ADD CONSISTENCY GUARDRAILS")
        print(f"   - Current hallucination rate: {1-best_arch_data['hallucination_score']:.1%}")
        print(f"   - Implement fact-checking and validation")
    
    if best_arch_data.get('npc_relationship_quality', 0) < 0.8:
        print(f"3. ENHANCE NPC RELATIONSHIP SYSTEM")
        print(f"   - Current NPC quality: {best_arch_data['npc_relationship_quality']:.1%}")
        print(f"   - Add memory and personality consistency")
    
    if best_arch_data.get('story_arc_progression', 0) < 0.7:
        print(f"4. IMPROVE STORY PROGRESSION")
        print(f"   - Current story quality: {best_arch_data['story_arc_progression']:.1%}")
        print(f"   - Add quest tracking and narrative threads")
    
    print(f"5. PERSONALIZATION BY PLAYER TYPE")
    for personality, (best_arch, score) in personality_preferences.items():
        if best_arch != best_architecture[0]:
            print(f"   - Consider {best_arch} variant for {personality} players")
    
    return architecture_scores, personality_preferences

def save_detailed_results(results: Dict[str, Any], architecture_scores: Dict[str, float]):
    """Save detailed results to file"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comprehensive_game_test_results_{timestamp}.json"
    
    # Prepare serializable results
    serializable_results = {}
    
    for arch_name, arch_data in results.items():
        serializable_results[arch_name] = {}
        
        for personality, personality_data in arch_data.items():
            serializable_results[arch_name][personality] = {}
            
            for scenario, scenario_data in personality_data.items():
                metrics = scenario_data['metrics']
                
                # Convert metrics to dict
                metrics_dict = {}
                for attr_name in dir(metrics):
                    if not attr_name.startswith('_') and isinstance(getattr(metrics, attr_name), (int, float)):
                        metrics_dict[attr_name] = getattr(metrics, attr_name)
                
                serializable_results[arch_name][personality][scenario] = {
                    'metrics': metrics_dict,
                    'turn_count': scenario_data['turn_count'],
                    'sample_turns': scenario_data['sample_turns']
                }
    
    # Add summary
    serializable_results['_summary'] = {
        'architecture_scores': architecture_scores,
        'test_timestamp': timestamp,
        'total_sessions': sum(len(personality_data) * len(scenario_data) 
                            for arch_data in results.values() 
                            for personality_data in arch_data.values()
                            for scenario_data in personality_data.values())
    }
    
    with open(filename, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"\n📁 Detailed results saved to: {filename}")

def main():
    """Run comprehensive game experience testing"""
    
    print("Starting comprehensive 8-turn game experience testing...")
    print("This will test all architectures against different player personalities")
    print("and scenarios to measure real player experience metrics.")
    print()
    
    # Run comprehensive tests
    results = run_comprehensive_test()
    
    # Analyze results
    architecture_scores, personality_preferences = analyze_results(results)
    
    # Save detailed results
    save_detailed_results(results, architecture_scores)
    
    print(f"\n✅ COMPREHENSIVE TESTING COMPLETE!")
    print(f"Tested {len(results)} architectures across multiple scenarios and player types")
    print(f"Use these insights to optimize your game architecture for maximum player experience.")

if __name__ == "__main__":
    main()