#!/usr/bin/env python3
"""
Comprehensive Stress Test - Multiple iterations with different scenarios
Tests happy path, edge cases, negative scenarios, and outliers
"""
import sys
import os
import time
import random
from typing import Dict, List

# Add backend to path
sys.path.append('backend')

from engine.game_state_manager import GameStateManager, ActionType
from engine.ai_integration import AIIntegrationLayer

class ComprehensiveStressTester:
    def __init__(self):
        self.api_key = "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"
        self.test_results = []
        self.total_issues = 0
        
    def run_comprehensive_stress_test(self):
        """Run comprehensive stress test with multiple scenarios"""
        
        print("🔥 FIRE WHISPER - COMPREHENSIVE STRESS TEST")
        print("=" * 70)
        print("🎯 Purpose: Stress test AI reliability across multiple scenarios")
        print("🔄 Iterations: 3 full runs per scenario type")
        print("⏱️ Duration: ~15-20 minutes")
        print("🧪 Scenarios: Happy Path, Edge Cases, Negative Tests, Outliers")
        print("=" * 70)
        
        test_scenarios = [
            ("Happy Path", self.happy_path_scenarios()),
            ("Edge Cases", self.edge_case_scenarios()),
            ("Negative Tests", self.negative_test_scenarios()),
            ("Outlier Tests", self.outlier_scenarios())
        ]
        
        overall_results = []
        
        for scenario_type, scenarios in test_scenarios:
            print(f"\n🧪 TESTING: {scenario_type.upper()}")
            print("=" * 50)
            
            scenario_results = []
            
            # Run each scenario 3 times for consistency
            for iteration in range(3):
                print(f"\n🔄 Iteration {iteration + 1}/3 for {scenario_type}")
                print("-" * 30)
                
                iteration_results = []
                
                for scenario_name, scenario_config in scenarios.items():
                    print(f"   Testing: {scenario_name}")
                    
                    try:
                        result = self.run_single_scenario(scenario_config)
                        result['scenario_name'] = scenario_name
                        result['scenario_type'] = scenario_type
                        result['iteration'] = iteration + 1
                        iteration_results.append(result)
                        
                        status = "✅ PASS" if result['passed'] else "❌ FAIL"
                        print(f"      {status} - {result.get('summary', 'Completed')}")
                        
                    except Exception as e:
                        error_result = {
                            'scenario_name': scenario_name,
                            'scenario_type': scenario_type,
                            'iteration': iteration + 1,
                            'passed': False,
                            'error': str(e),
                            'summary': f"Exception: {e}"
                        }
                        iteration_results.append(error_result)
                        print(f"      ❌ CRASH - {e}")
                
                scenario_results.append(iteration_results)
            
            # Analyze consistency across iterations
            consistency_analysis = self.analyze_consistency(scenario_results, scenario_type)
            overall_results.append({
                'scenario_type': scenario_type,
                'results': scenario_results,
                'consistency': consistency_analysis
            })
        
        # Generate comprehensive report
        self.generate_comprehensive_report(overall_results)
        
        return overall_results
    
    def happy_path_scenarios(self) -> Dict:
        """Standard gameplay scenarios that should always work"""
        return {
            "Balanced Warrior": {
                'character': {
                    'name': 'HappyWarrior',
                    'class': 'Warrior',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 16, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
                    'skills': {'Combat': 2, 'Athletics': 1},
                    'resources': {'hp': 35, 'max_hp': 35, 'energy': 10, 'max_energy': 10}
                },
                'actions': ['1', '2', '3', '4', '1', '3', '2', '4'],
                'expected_behavior': 'smooth_progression',
                'turns': 8
            },
            
            "Skilled Mage": {
                'character': {
                    'name': 'HappyMage',
                    'class': 'Mage',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 10, 'dexterity': 12, 'intelligence': 16, 'charisma': 12},
                    'skills': {'Magic': 2, 'Knowledge': 1},
                    'resources': {'hp': 25, 'max_hp': 25, 'energy': 15, 'max_energy': 15}
                },
                'actions': ['2', '1', '4', '3', '2', '4', '1', '3'],
                'expected_behavior': 'magic_focused',
                'turns': 8
            },
            
            "Progression Test": {
                'character': {
                    'name': 'ProgressTest',
                    'class': 'Rogue',
                    'level': 1,
                    'xp': 80,  # Close to level up
                    'stats': {'strength': 12, 'dexterity': 16, 'intelligence': 12, 'charisma': 10},
                    'skills': {'Stealth': 2, 'Lockpicking': 1},
                    'resources': {'hp': 28, 'max_hp': 28, 'energy': 12, 'max_energy': 12}
                },
                'actions': ['3', '1', '3', '2'],  # Should trigger level up
                'expected_behavior': 'level_up_occurs',
                'turns': 4
            }
        }
    
    def edge_case_scenarios(self) -> Dict:
        """Edge cases that might cause issues"""
        return {
            "Low Stats Character": {
                'character': {
                    'name': 'WeakChar',
                    'class': 'Warrior',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 8, 'dexterity': 8, 'intelligence': 8, 'charisma': 8},  # Very low
                    'skills': {'Combat': 1},
                    'resources': {'hp': 20, 'max_hp': 20, 'energy': 8, 'max_energy': 8}
                },
                'actions': ['1', '1', '1', '1', '1'],  # Repetitive combat
                'expected_behavior': 'handles_low_stats',
                'turns': 5
            },
            
            "High Level Character": {
                'character': {
                    'name': 'HighLevel',
                    'class': 'Mage',
                    'level': 5,
                    'xp': 1200,
                    'stats': {'strength': 12, 'dexterity': 14, 'intelligence': 20, 'charisma': 16},
                    'skills': {'Magic': 5, 'Knowledge': 3},
                    'resources': {'hp': 45, 'max_hp': 45, 'energy': 25, 'max_energy': 25}
                },
                'actions': ['2', '2', '2', '2'],  # Magic-heavy
                'expected_behavior': 'handles_high_level',
                'turns': 4
            },
            
            "Exact Threshold XP": {
                'character': {
                    'name': 'ThresholdTest',
                    'class': 'Cleric',
                    'level': 1,
                    'xp': 99,  # 1 XP away from level 2
                    'stats': {'strength': 12, 'dexterity': 10, 'intelligence': 12, 'charisma': 16},
                    'skills': {'Healing': 2, 'Persuasion': 1},
                    'resources': {'hp': 30, 'max_hp': 30, 'energy': 13, 'max_energy': 13}
                },
                'actions': ['4', '1'],  # Should trigger level up on first success
                'expected_behavior': 'precise_level_up',
                'turns': 2
            }
        }
    
    def negative_test_scenarios(self) -> Dict:
        """Scenarios designed to potentially break the system"""
        return {
            "Repetitive Actions": {
                'character': {
                    'name': 'RepeatTest',
                    'class': 'Warrior',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 16, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
                    'skills': {'Combat': 2, 'Athletics': 1},
                    'resources': {'hp': 35, 'max_hp': 35, 'energy': 10, 'max_energy': 10}
                },
                'actions': ['1'] * 10,  # Same action 10 times
                'expected_behavior': 'handles_repetition',
                'turns': 10
            },
            
            "Rapid Switching": {
                'character': {
                    'name': 'SwitchTest',
                    'class': 'Rogue',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 12, 'dexterity': 16, 'intelligence': 12, 'charisma': 10},
                    'skills': {'Stealth': 2, 'Lockpicking': 1},
                    'resources': {'hp': 28, 'max_hp': 28, 'energy': 12, 'max_energy': 12}
                },
                'actions': ['1', '4', '2', '3', '4', '1', '3', '2', '1', '4'],  # Rapid switching
                'expected_behavior': 'handles_switching',
                'turns': 10
            },
            
            "Extreme Stats": {
                'character': {
                    'name': 'ExtremeTest',
                    'class': 'Mage',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 3, 'dexterity': 3, 'intelligence': 20, 'charisma': 3},  # Extreme distribution
                    'skills': {'Magic': 3},
                    'resources': {'hp': 15, 'max_hp': 15, 'energy': 20, 'max_energy': 20}
                },
                'actions': ['2', '1', '3', '4'],  # Test all action types
                'expected_behavior': 'handles_extremes',
                'turns': 4
            }
        }
    
    def outlier_scenarios(self) -> Dict:
        """Unusual scenarios that might expose hidden issues"""
        return {
            "Zero Skill Character": {
                'character': {
                    'name': 'NoSkills',
                    'class': 'Warrior',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 14, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
                    'skills': {},  # No skills at all
                    'resources': {'hp': 30, 'max_hp': 30, 'energy': 10, 'max_energy': 10}
                },
                'actions': ['1', '2', '3', '4'],
                'expected_behavior': 'handles_no_skills',
                'turns': 4
            },
            
            "Long Session": {
                'character': {
                    'name': 'EnduranceTest',
                    'class': 'Cleric',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 12, 'dexterity': 10, 'intelligence': 12, 'charisma': 16},
                    'skills': {'Healing': 2, 'Persuasion': 1},
                    'resources': {'hp': 30, 'max_hp': 30, 'energy': 13, 'max_energy': 13}
                },
                'actions': ['1', '2', '3', '4'] * 6,  # 24 turns
                'expected_behavior': 'maintains_quality',
                'turns': 20  # Limit to 20 for time
            },
            
            "Random Actions": {
                'character': {
                    'name': 'RandomTest',
                    'class': 'Rogue',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 12, 'dexterity': 16, 'intelligence': 12, 'charisma': 10},
                    'skills': {'Stealth': 2, 'Lockpicking': 1},
                    'resources': {'hp': 28, 'max_hp': 28, 'energy': 12, 'max_energy': 12}
                },
                'actions': [str(random.randint(1, 4)) for _ in range(8)],  # Truly random
                'expected_behavior': 'handles_randomness',
                'turns': 8
            }
        }
    
    def run_single_scenario(self, scenario_config: Dict) -> Dict:
        """Run a single test scenario"""
        
        character_data = scenario_config['character'].copy()
        character_data.update({
            'emberlyn_bond': 1,
            'achievements': []
        })
        
        actions = scenario_config['actions']
        max_turns = scenario_config['turns']
        expected_behavior = scenario_config['expected_behavior']
        
        # Initialize AI layer
        ai_layer = AIIntegrationLayer(self.api_key)
        
        issues = []
        mechanical_issues = []
        ai_issues = []
        
        try:
            # Start game
            game_start = ai_layer.start_new_game(character_data)
            
            initial_xp = ai_layer.game_manager.character['xp']
            initial_level = ai_layer.game_manager.character['level']
            
            # Process actions
            for i, action in enumerate(actions[:max_turns]):
                try:
                    result = ai_layer.process_player_action(action)
                    
                    # Check for AI hallucinations
                    narrative = result['narrative'].lower()
                    hallucination_phrases = [
                        'you gain', 'xp awarded', '+xp', 'rolling dice', 
                        'dice roll', 'level up', 'your level', 'you now have'
                    ]
                    
                    for phrase in hallucination_phrases:
                        if phrase in narrative:
                            ai_issues.append(f"Turn {i+1}: AI hallucination - '{phrase}'")
                    
                    # Check mechanical consistency
                    if result['mechanical_results']['dice_rolls']:
                        dice_roll = result['mechanical_results']['dice_rolls'][0]
                        if dice_roll.base_roll < 1 or dice_roll.base_roll > 20:
                            mechanical_issues.append(f"Turn {i+1}: Invalid dice roll {dice_roll.base_roll}")
                    
                    # Check XP consistency
                    if result['mechanical_results']['xp_awards']:
                        xp_award = result['mechanical_results']['xp_awards'][0]
                        if xp_award['xp_awarded'] < 0 or xp_award['xp_awarded'] > 100:
                            mechanical_issues.append(f"Turn {i+1}: Suspicious XP award {xp_award['xp_awarded']}")
                    
                    # Check narrative quality
                    if len(narrative) < 20:
                        ai_issues.append(f"Turn {i+1}: Very short response")
                    
                except Exception as e:
                    issues.append(f"Turn {i+1}: Exception - {e}")
            
            final_xp = ai_layer.game_manager.character['xp']
            final_level = ai_layer.game_manager.character['level']
            
            # Validate expected behavior
            behavior_check = self.validate_expected_behavior(
                expected_behavior, initial_xp, final_xp, initial_level, final_level, len(actions)
            )
            
            if not behavior_check['passed']:
                issues.extend(behavior_check['issues'])
            
            total_issues = len(issues) + len(mechanical_issues) + len(ai_issues)
            
            return {
                'passed': total_issues == 0,
                'total_issues': total_issues,
                'general_issues': issues,
                'mechanical_issues': mechanical_issues,
                'ai_issues': ai_issues,
                'behavior_check': behavior_check,
                'turns_completed': min(len(actions), max_turns),
                'xp_progression': f"{initial_xp} → {final_xp}",
                'level_progression': f"{initial_level} → {final_level}",
                'summary': f"{total_issues} issues found" if total_issues > 0 else "All checks passed"
            }
            
        except Exception as e:
            return {
                'passed': False,
                'error': str(e),
                'summary': f"Scenario crashed: {e}"
            }
    
    def validate_expected_behavior(self, expected: str, initial_xp: int, final_xp: int, 
                                 initial_level: int, final_level: int, turns: int) -> Dict:
        """Validate that the scenario behaved as expected"""
        
        issues = []
        
        if expected == 'smooth_progression':
            if final_xp <= initial_xp:
                issues.append("No XP progression detected")
        
        elif expected == 'level_up_occurs':
            if final_level <= initial_level:
                issues.append("Expected level up did not occur")
        
        elif expected == 'precise_level_up':
            if initial_xp == 99 and final_level <= initial_level:
                issues.append("Level up should have occurred at XP threshold")
        
        elif expected == 'handles_repetition':
            # For repetitive actions, we just check it didn't crash
            pass
        
        elif expected == 'maintains_quality':
            if turns > 15:  # Long sessions should maintain progression
                if final_xp <= initial_xp + (turns * 5):  # Minimum expected XP
                    issues.append("Long session showed poor XP progression")
        
        return {
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def analyze_consistency(self, scenario_results: List, scenario_type: str) -> Dict:
        """Analyze consistency across multiple iterations"""
        
        # Flatten results
        all_results = []
        for iteration in scenario_results:
            all_results.extend(iteration)
        
        # Group by scenario name
        by_scenario = {}
        for result in all_results:
            name = result['scenario_name']
            if name not in by_scenario:
                by_scenario[name] = []
            by_scenario[name].append(result)
        
        consistency_report = {}
        
        for scenario_name, results in by_scenario.items():
            pass_count = sum(1 for r in results if r['passed'])
            total_count = len(results)
            
            # Check for consistency issues
            issues_per_iteration = [r.get('total_issues', 0) for r in results]
            consistency_issues = []
            
            if pass_count < total_count:
                consistency_issues.append(f"Inconsistent results: {pass_count}/{total_count} passed")
            
            if len(set(issues_per_iteration)) > 1:
                consistency_issues.append(f"Variable issue counts: {issues_per_iteration}")
            
            consistency_report[scenario_name] = {
                'pass_rate': f"{pass_count}/{total_count}",
                'consistent': len(consistency_issues) == 0,
                'issues': consistency_issues
            }
        
        return consistency_report
    
    def generate_comprehensive_report(self, overall_results: List):
        """Generate comprehensive test report"""
        
        print("\n" + "=" * 70)
        print("📊 COMPREHENSIVE STRESS TEST RESULTS")
        print("=" * 70)
        
        total_scenarios = 0
        total_passed = 0
        critical_issues = []
        
        for scenario_group in overall_results:
            scenario_type = scenario_group['scenario_type']
            consistency = scenario_group['consistency']
            
            print(f"\n🧪 {scenario_type.upper()} RESULTS:")
            print("-" * 40)
            
            for scenario_name, consistency_data in consistency.items():
                total_scenarios += 1
                
                if consistency_data['consistent'] and "3/3" in consistency_data['pass_rate']:
                    total_passed += 1
                    print(f"   ✅ {scenario_name}: {consistency_data['pass_rate']} - CONSISTENT")
                else:
                    print(f"   ❌ {scenario_name}: {consistency_data['pass_rate']} - INCONSISTENT")
                    critical_issues.extend(consistency_data['issues'])
        
        # Overall assessment
        print(f"\n📈 OVERALL ASSESSMENT:")
        print("=" * 40)
        print(f"Total Scenarios: {total_scenarios}")
        print(f"Consistently Passing: {total_passed}")
        print(f"Success Rate: {total_passed}/{total_scenarios} ({total_passed/total_scenarios*100:.1f}%)")
        
        if len(critical_issues) == 0:
            print(f"\n🌟 EXCELLENT: All scenarios passed consistently across 3 iterations")
            print(f"✅ AI behavior is reliable and predictable")
            print(f"✅ No drift or inconsistency detected")
            print(f"✅ System handles edge cases and outliers")
            print(f"\n🎯 STATUS: PRODUCTION READY")
            print(f"🚀 Safe to deploy with confidence")
        else:
            print(f"\n⚠️ ISSUES DETECTED: {len(critical_issues)} consistency problems")
            print(f"🔍 Critical Issues:")
            for issue in critical_issues[:10]:  # Show first 10
                print(f"   • {issue}")
            
            if total_passed / total_scenarios >= 0.8:
                print(f"\n🔶 STATUS: MOSTLY STABLE")
                print(f"💡 Consider addressing consistency issues before production")
            else:
                print(f"\n🚨 STATUS: UNSTABLE")
                print(f"⚠️ Fix critical issues before deployment")
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    print("⚠️  WARNING: This is a comprehensive stress test that will take 15-20 minutes")
    print("🔄 It will run 3 iterations of 4 different scenario types")
    print("🧪 This tests AI consistency under various conditions")
    
    confirm = input("\nProceed with comprehensive stress test? (y/n): ").lower()
    if confirm == 'y':
        tester = ComprehensiveStressTester()
        results = tester.run_comprehensive_stress_test()
    else:
        print("Test cancelled.")