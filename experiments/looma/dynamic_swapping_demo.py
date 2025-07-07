#!/usr/bin/env python3
"""
Dynamic Component Swapping Demo
Demonstrates real-time AI/Code switching based on performance metrics
optimized for user experience and return engagement.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from looma.core.dynamic_component_swapper import DynamicGameEngine, RealTimeMetrics
import json
import time
from datetime import datetime

def create_test_scenarios():
    """Create test scenarios that will trigger component switches"""
    
    return [
        # Scenario 1: NPC relationship building (AI should excel)
        {
            "turn": 1,
            "description": "Building trust with village elder",
            "npc_interaction": {
                "npc_id": "village_elder",
                "action": "help_with_problem",
                "context": {"public_setting": True, "urgent_need": True}
            },
            "narrative_request": {
                "scene_context": {
                    "location": "village_square",
                    "time": "evening",
                    "mood": "hopeful",
                    "recent_events": ["player_arrived", "offered_help"]
                }
            }
        },
        
        # Scenario 2: Complex emotional interaction (AI should excel)
        {
            "turn": 2,
            "description": "Deep conversation with NPC",
            "npc_interaction": {
                "npc_id": "village_elder",
                "action": "share_personal_story",
                "context": {"private_setting": True, "emotional_vulnerability": True}
            },
            "narrative_request": {
                "character": "village_elder",
                "emotion": "grateful",
                "context": {"relationship_level": 0.8, "personality": {"traits": ["wise", "caring"]}}
            }
        },
        
        # Scenario 3: Repeated interactions (test consistency)
        {
            "turn": 3,
            "description": "Follow-up conversation",
            "npc_interaction": {
                "npc_id": "village_elder",
                "action": "ask_about_quest",
                "context": {"continuation": True}
            },
            "narrative_request": {
                "scene_context": {
                    "location": "village_square",
                    "time": "night",
                    "mood": "mysterious"
                }
            }
        },
        
        # Scenario 4: High-stakes situation (test under pressure)
        {
            "turn": 4,
            "description": "Crisis situation requiring quick response",
            "npc_interaction": {
                "npc_id": "village_elder",
                "action": "urgent_request_for_help",
                "context": {"life_threatening": True, "time_pressure": True}
            },
            "narrative_request": {
                "character": "village_elder",
                "emotion": "fearful",
                "context": {"crisis_situation": True}
            }
        },
        
        # Scenario 5: New NPC introduction (test adaptability)
        {
            "turn": 5,
            "description": "Meeting new character",
            "npc_interaction": {
                "npc_id": "mysterious_stranger",
                "action": "first_meeting",
                "context": {"unknown_intentions": True, "cautious_approach": True}
            },
            "narrative_request": {
                "scene_context": {
                    "location": "tavern",
                    "time": "late_night",
                    "mood": "tense",
                    "recent_events": ["stranger_arrived"]
                }
            }
        },
        
        # Scenario 6: Complex relationship dynamics
        {
            "turn": 6,
            "description": "Navigating complex social situation",
            "npc_interaction": {
                "npc_id": "mysterious_stranger",
                "action": "probe_for_information",
                "context": {"social_tension": True, "multiple_npcs_present": True}
            },
            "narrative_request": {
                "character": "mysterious_stranger",
                "emotion": "suspicious",
                "context": {"relationship_level": 0.2, "personality": {"traits": ["secretive", "intelligent"]}}
            }
        },
        
        # Scenario 7: Relationship recovery after conflict
        {
            "turn": 7,
            "description": "Attempting to repair damaged relationship",
            "npc_interaction": {
                "npc_id": "village_elder",
                "action": "apologize_for_misunderstanding",
                "context": {"relationship_repair": True, "public_apology": True}
            },
            "narrative_request": {
                "character": "village_elder",
                "emotion": "conflicted",
                "context": {"relationship_level": 0.4, "recent_conflict": True}
            }
        },
        
        # Scenario 8: Final relationship test
        {
            "turn": 8,
            "description": "Testing final relationship strength",
            "npc_interaction": {
                "npc_id": "village_elder",
                "action": "request_major_favor",
                "context": {"trust_test": True, "significant_consequences": True}
            },
            "narrative_request": {
                "scene_context": {
                    "location": "village_square",
                    "time": "dawn",
                    "mood": "hopeful",
                    "recent_events": ["relationship_restored", "trust_rebuilt"]
                }
            }
        }
    ]

def run_dynamic_swapping_demo():
    """Run comprehensive demo of dynamic component swapping"""
    
    print("🔄 DYNAMIC COMPONENT SWAPPING DEMO")
    print("=" * 60)
    print("Real-time AI/Code switching optimized for user experience")
    print()
    
    # Initialize game engine
    engine = DynamicGameEngine()
    scenarios = create_test_scenarios()
    
    all_results = []
    
    print("🎮 Starting 8-turn game session with performance monitoring...")
    print()
    
    for scenario in scenarios:
        print(f"🎯 TURN {scenario['turn']}: {scenario['description']}")
        print("-" * 50)
        
        # Process the turn
        turn_result = engine.process_game_turn(scenario)
        all_results.append(turn_result)
        
        # Display results
        print(f"📊 Components Used:")
        for component, impl_type in turn_result.get("components_used", {}).items():
            print(f"  • {component}: {impl_type.upper()}")
        
        # Show performance metrics
        print(f"📈 Performance Metrics:")
        for component, metrics in turn_result.get("performance_metrics", {}).items():
            print(f"  • {component}:")
            print(f"    - User Engagement: {metrics.user_engagement:.2f}")
            print(f"    - Return Likelihood: {metrics.return_likelihood:.2f}")
            print(f"    - Session Quality: {metrics.session_quality:.2f}")
            print(f"    - Response Time: {metrics.response_time:.2f}s")
            print(f"    - Consistency: {metrics.consistency_score:.2f}")
            print(f"    - Creativity: {metrics.creativity_score:.2f}")
            print(f"    - Relationship Depth: {metrics.relationship_depth:.2f}")
            if metrics.hallucination_count > 0:
                print(f"    - ⚠️  Hallucinations: {metrics.hallucination_count}")
        
        # Show any switches made
        if turn_result.get("switches_made"):
            print(f"🔄 Component Switches:")
            for switch in turn_result["switches_made"]:
                print(f"  • {switch['component']}: {switch['from']} → {switch['to']} ({switch['reason']})")
        
        # Show sample outputs
        if "npc_result" in turn_result:
            npc_result = turn_result["npc_result"]
            print(f"🎭 NPC Response ({npc_result.get('implementation', 'Unknown')}):")
            print(f"  \"{npc_result.get('response', 'No response')[:100]}...\"")
            print(f"  Relationship Score: {npc_result.get('relationship_score', 0):.2f}")
        
        if "narrative_result" in turn_result:
            narrative_result = turn_result["narrative_result"]
            print(f"📖 Narrative ({narrative_result.get('implementation', 'Unknown')}):")
            print(f"  \"{narrative_result.get('narrative', 'No narrative')[:100]}...\"")
        
        print()
        
        # Brief pause for readability
        time.sleep(0.5)
    
    # Generate final session report
    print("📋 FINAL SESSION REPORT")
    print("=" * 60)
    
    session_report = engine.get_session_report()
    
    # Session overview
    session_info = session_report.get("session_info", {})
    print(f"🕒 Session Duration: {session_info.get('duration_minutes', 0):.1f} minutes")
    print(f"🎮 Turns Completed: {session_info.get('turns_completed', 0)}")
    print(f"⚡ Turns per Minute: {session_info.get('turns_per_minute', 0):.1f}")
    print()
    
    # Overall metrics
    overall = session_report.get("overall_metrics", {})
    print(f"📊 OVERALL SESSION METRICS:")
    print(f"  🎯 Average User Engagement: {overall.get('average_user_engagement', 0):.2f}")
    print(f"  🔄 Average Return Likelihood: {overall.get('average_return_likelihood', 0):.2f}")
    print(f"  ⭐ Average Session Quality: {overall.get('average_session_quality', 0):.2f}")
    print(f"  ⚡ Average Response Time: {overall.get('average_response_time', 0):.2f}s")
    print(f"  ❌ Total Errors: {overall.get('total_errors', 0)}")
    print(f"  🌀 Total Hallucinations: {overall.get('total_hallucinations', 0)}")
    print()
    
    # Component-specific performance
    print(f"🧩 COMPONENT PERFORMANCE:")
    for component_name, component_data in session_report.get("components", {}).items():
        print(f"  📦 {component_name.upper()}:")
        print(f"    Current Implementation: {component_data.get('current_implementation', 'unknown').upper()}")
        print(f"    Performance Level: {component_data.get('performance_level', 'unknown').upper()}")
        print(f"    Switches Made: {component_data.get('switch_count', 0)}")
        
        recent_avgs = component_data.get("recent_averages", {})
        print(f"    Recent Averages:")
        print(f"      - User Engagement: {recent_avgs.get('user_engagement', 0):.2f}")
        print(f"      - Return Likelihood: {recent_avgs.get('return_likelihood', 0):.2f}")
        print(f"      - Session Quality: {recent_avgs.get('session_quality', 0):.2f}")
        print(f"      - Creativity: {recent_avgs.get('creativity_score', 0):.2f}")
        print(f"      - Consistency: {recent_avgs.get('consistency_score', 0):.2f}")
        print(f"      - Relationship Depth: {recent_avgs.get('relationship_depth', 0):.2f}")
        
        if component_data.get("total_hallucinations", 0) > 0:
            print(f"    ⚠️  Issues: {component_data.get('total_hallucinations', 0)} hallucinations")
        print()
    
    # Recommendations
    recommendations = session_report.get("recommendations", [])
    if recommendations:
        print(f"💡 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        print()
    
    # Performance analysis
    print(f"🔍 PERFORMANCE ANALYSIS:")
    
    # Calculate AI vs Code usage
    ai_usage = sum(1 for result in all_results 
                   for component, impl_type in result.get("components_used", {}).items() 
                   if impl_type == "ai")
    code_usage = sum(1 for result in all_results 
                     for component, impl_type in result.get("components_used", {}).items() 
                     if impl_type == "code")
    
    total_usage = ai_usage + code_usage
    if total_usage > 0:
        print(f"  🤖 AI Usage: {ai_usage}/{total_usage} ({ai_usage/total_usage*100:.1f}%)")
        print(f"  💻 Code Usage: {code_usage}/{total_usage} ({code_usage/total_usage*100:.1f}%)")
    
    # Count switches
    total_switches = sum(len(result.get("switches_made", [])) for result in all_results)
    print(f"  🔄 Total Component Switches: {total_switches}")
    
    # User experience assessment
    avg_engagement = overall.get('average_user_engagement', 0)
    avg_return = overall.get('average_return_likelihood', 0)
    avg_quality = overall.get('average_session_quality', 0)
    
    overall_ux_score = (avg_engagement + avg_return + avg_quality) / 3
    
    print(f"  🎯 Overall UX Score: {overall_ux_score:.2f}/1.0")
    
    if overall_ux_score > 0.8:
        print(f"  ✅ EXCELLENT - Players will love this experience and return!")
    elif overall_ux_score > 0.7:
        print(f"  👍 GOOD - Solid player experience with room for improvement")
    elif overall_ux_score > 0.6:
        print(f"  ⚠️  FAIR - Needs optimization to retain players")
    else:
        print(f"  ❌ POOR - Significant improvements needed")
    
    print()
    print(f"🎮 Dynamic swapping successfully optimized for user experience!")
    print(f"The system automatically switched between AI and Code based on real-time performance.")
    
    return session_report, all_results

def save_detailed_results(session_report, all_results):
    """Save detailed results for analysis"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dynamic_swapping_results_{timestamp}.json"
    
    # Prepare serializable data
    def serialize_metrics(obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)
    
    serializable_data = {
        "session_report": session_report,
        "turn_results": []
    }
    
    for result in all_results:
        serializable_result = {}
        for key, value in result.items():
            if key == "performance_metrics":
                serializable_result[key] = {}
                for component, metrics in value.items():
                    serializable_result[key][component] = serialize_metrics(metrics)
            else:
                serializable_result[key] = value
        serializable_data["turn_results"].append(serializable_result)
    
    with open(filename, 'w') as f:
        json.dump(serializable_data, f, indent=2, default=str)
    
    print(f"📁 Detailed results saved to: {filename}")

def main():
    """Run the dynamic swapping demonstration"""
    
    print("🚀 Starting Dynamic Component Swapping Demo")
    print("This demo shows real-time AI/Code switching optimized for user experience")
    print()
    
    session_report, all_results = run_dynamic_swapping_demo()
    
    # Save results
    save_detailed_results(session_report, all_results)
    
    print("✅ Demo complete! The system demonstrated:")
    print("  • Real-time performance monitoring")
    print("  • Automatic component switching based on user experience metrics")
    print("  • Optimization for user engagement and return likelihood")
    print("  • Granular AI vs Code performance comparison")

if __name__ == "__main__":
    main()