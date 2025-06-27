"""
Automated Game Tester - Runs simulated game sessions to validate quality and mechanics
"""
import json
import random
import time
from typing import List, Dict, Any
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

try:
    from engine.ai_integration import AIIntegrationLayer
    from testing.game_quality_validator import GameQualityValidator
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run from the project root directory")
    sys.exit(1)

class AutomatedGameTester:
    def __init__(self, api_key: str):
        self.ai_layer = AIIntegrationLayer(api_key)
        self.validator = GameQualityValidator()
        self.test_scenarios = self._create_test_scenarios()
        
    def run_comprehensive_test_suite(self) -> Dict:
        """Run comprehensive automated tests across multiple scenarios"""
        
        print("🧪 Starting Comprehensive Game Testing Suite")
        print("=" * 60)
        
        all_results = []
        
        for scenario_name, scenario_config in self.test_scenarios.items():
            print(f"\n🎯 Testing Scenario: {scenario_name}")
            print("-" * 40)
            
            try:
                session_result = self.run_test_session(scenario_config)
                validation_result = self.validator.validate_game_session(session_result['session_data'])
                
                combined_result = {
                    'scenario_name': scenario_name,
                    'scenario_config': scenario_config,
                    'session_result': session_result,
                    'validation_result': validation_result,
                    'timestamp': time.time()
                }
                
                all_results.append(combined_result)
                
                # Print immediate feedback
                status = validation_result['overall_status']
                score = validation_result['health_score']
                print(f"✅ Scenario Complete: {status} (Score: {score}/100)")
                
            except Exception as e:
                print(f"❌ Scenario Failed: {e}")
                all_results.append({
                    'scenario_name': scenario_name,
                    'error': str(e),
                    'timestamp': time.time()
                })
        
        # Generate comprehensive report
        final_report = self._generate_comprehensive_report(all_results)
        
        print(f"\n🎯 COMPREHENSIVE TEST RESULTS")
        print("=" * 60)
        print(f"Overall System Health: {final_report['overall_health_score']}/100")
        print(f"Scenarios Passed: {final_report['scenarios_passed']}/{final_report['total_scenarios']}")
        print(f"Critical Issues: {final_report['total_critical_issues']}")
        print(f"High Priority Issues: {final_report['total_high_issues']}")
        
        return final_report
    
    def run_test_session(self, scenario_config: Dict) -> Dict:
        """Run a single automated test session"""
        
        character_data = scenario_config['character']
        test_actions = scenario_config['test_actions']
        max_turns = scenario_config.get('max_turns', 10)
        
        # Initialize game
        game_start = self.ai_layer.start_new_game(character_data)
        
        session_data = []
        current_turn = 0
        
        for action in test_actions[:max_turns]:
            current_turn += 1
            
            try:
                # Process player action
                result = self.ai_layer.process_player_action(action)
                
                # Extract data for validation
                turn_data = {
                    'turn_number': current_turn,
                    'player_action': action,
                    'ai_response': result['narrative'],
                    'mechanical_results': result['mechanical_results'],
                    'character_stats': result['character'],
                    'game_state': result['game_state']
                }
                
                # Add specific validation data
                if result['mechanical_results']['dice_rolls']:
                    dice_roll = result['mechanical_results']['dice_rolls'][0]
                    turn_data['dice_roll'] = {
                        'base_roll': dice_roll.base_roll,
                        'modifiers': dice_roll.modifiers,
                        'total': dice_roll.base_roll + sum(dice_roll.modifiers.values()),
                        'target': dice_roll.target,
                        'success': dice_roll.success
                    }
                
                if result['mechanical_results']['xp_awards']:
                    xp_award = result['mechanical_results']['xp_awards'][0]
                    turn_data['xp_awarded'] = xp_award['xp_awarded']
                    turn_data['total_xp'] = xp_award['new_xp']
                    turn_data['level_up'] = xp_award['level_up']
                
                session_data.append(turn_data)
                
                # Brief pause to simulate realistic gameplay
                time.sleep(0.1)
                
            except Exception as e:
                session_data.append({
                    'turn_number': current_turn,
                    'player_action': action,
                    'error': str(e)
                })
                break
        
        return {
            'scenario_config': scenario_config,
            'session_data': session_data,
            'total_turns': len(session_data),
            'completed_successfully': current_turn >= len(test_actions)
        }
    
    def _create_test_scenarios(self) -> Dict[str, Dict]:
        """Create comprehensive test scenarios covering different gameplay aspects"""
        
        return {
            'warrior_combat_focused': {
                'description': 'Test combat mechanics with warrior character',
                'character': {
                    'name': 'TestWarrior',
                    'class': 'Warrior',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 16, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
                    'skills': {'Combat': 2, 'Athletics': 1},
                    'resources': {'hp': 35, 'max_hp': 35, 'energy': 10, 'max_energy': 10}
                },
                'test_actions': ['1', '1', '3', '1', '2', '1', '4', '1', '3', '1'],  # Combat-heavy
                'max_turns': 10,
                'expected_elements': ['combat', 'progression']
            },
            
            'mage_balanced_gameplay': {
                'description': 'Test balanced gameplay with mage character',
                'character': {
                    'name': 'TestMage',
                    'class': 'Mage',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 10, 'dexterity': 12, 'intelligence': 16, 'charisma': 12},
                    'skills': {'Magic': 2, 'Knowledge': 1},
                    'resources': {'hp': 25, 'max_hp': 25, 'energy': 15, 'max_energy': 15}
                },
                'test_actions': ['2', '1', '3', '4', '2', '1', '4', '3', '2', '1'],  # Varied choices
                'max_turns': 10,
                'expected_elements': ['magic', 'exploration', 'social']
            },
            
            'rogue_stealth_focused': {
                'description': 'Test stealth and skill mechanics with rogue',
                'character': {
                    'name': 'TestRogue',
                    'class': 'Rogue',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 12, 'dexterity': 16, 'intelligence': 12, 'charisma': 10},
                    'skills': {'Stealth': 2, 'Lockpicking': 1},
                    'resources': {'hp': 28, 'max_hp': 28, 'energy': 12, 'max_energy': 12}
                },
                'test_actions': ['3', '3', '2', '3', '4', '3', '1', '3', '2', '3'],  # Stealth-heavy
                'max_turns': 10,
                'expected_elements': ['stealth', 'skills', 'exploration']
            },
            
            'long_session_endurance': {
                'description': 'Test long session stability and AI drift resistance',
                'character': {
                    'name': 'EnduranceTest',
                    'class': 'Cleric',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 12, 'dexterity': 10, 'intelligence': 12, 'charisma': 16},
                    'skills': {'Healing': 2, 'Persuasion': 1},
                    'resources': {'hp': 30, 'max_hp': 30, 'energy': 13, 'max_energy': 13}
                },
                'test_actions': ['1', '2', '3', '4'] * 8,  # 32 turns - test endurance
                'max_turns': 25,
                'expected_elements': ['consistency', 'progression', 'variety']
            },
            
            'edge_case_testing': {
                'description': 'Test edge cases and potential failure modes',
                'character': {
                    'name': 'EdgeCase',
                    'class': 'Warrior',
                    'level': 1,
                    'xp': 0,
                    'stats': {'strength': 16, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
                    'skills': {'Combat': 2, 'Athletics': 1},
                    'resources': {'hp': 35, 'max_hp': 35, 'energy': 10, 'max_energy': 10}
                },
                'test_actions': ['1', '1', '1', '1', '1', '2', '2', '2', '3', '4'],  # Repetitive then varied
                'max_turns': 10,
                'expected_elements': ['consistency', 'variety_recovery']
            }
        }
    
    def _generate_comprehensive_report(self, all_results: List[Dict]) -> Dict:
        """Generate comprehensive report across all test scenarios"""
        
        total_scenarios = len(all_results)
        successful_scenarios = [r for r in all_results if 'validation_result' in r]
        failed_scenarios = [r for r in all_results if 'error' in r]
        
        # Aggregate validation results
        total_critical = sum(r['validation_result']['issues_by_severity']['critical'] 
                           for r in successful_scenarios)
        total_high = sum(r['validation_result']['issues_by_severity']['high'] 
                        for r in successful_scenarios)
        total_medium = sum(r['validation_result']['issues_by_severity']['medium'] 
                          for r in successful_scenarios)
        
        # Calculate overall health score
        if successful_scenarios:
            avg_health_score = sum(r['validation_result']['health_score'] 
                                 for r in successful_scenarios) / len(successful_scenarios)
        else:
            avg_health_score = 0
        
        # Identify common issues
        common_issues = {}
        for result in successful_scenarios:
            for severity in ['critical', 'high', 'medium']:
                for issue in result['validation_result']['detailed_results'][severity]:
                    issue_key = f"{issue['category']}: {issue['issue']}"
                    common_issues[issue_key] = common_issues.get(issue_key, 0) + 1
        
        # Generate recommendations
        recommendations = []
        
        if total_critical > 0:
            recommendations.append("🚨 CRITICAL: Fix mechanical integrity issues immediately")
        
        if total_high > 5:
            recommendations.append("⚠️ HIGH PRIORITY: Address quality issues affecting player experience")
        
        if len(failed_scenarios) > 0:
            recommendations.append("💥 SYSTEM STABILITY: Fix scenarios causing crashes or errors")
        
        # Most common issues
        if common_issues:
            most_common = max(common_issues.items(), key=lambda x: x[1])
            recommendations.append(f"🔄 RECURRING ISSUE: '{most_common[0]}' appears in {most_common[1]} scenarios")
        
        return {
            'timestamp': time.time(),
            'overall_health_score': round(avg_health_score, 1),
            'total_scenarios': total_scenarios,
            'scenarios_passed': len(successful_scenarios),
            'scenarios_failed': len(failed_scenarios),
            'total_critical_issues': total_critical,
            'total_high_issues': total_high,
            'total_medium_issues': total_medium,
            'common_issues': dict(sorted(common_issues.items(), key=lambda x: x[1], reverse=True)[:5]),
            'recommendations': recommendations,
            'detailed_scenario_results': all_results,
            'system_status': self._determine_system_status(avg_health_score, total_critical, total_high, len(failed_scenarios))
        }
    
    def _determine_system_status(self, health_score: float, critical: int, high: int, failed: int) -> str:
        """Determine overall system status"""
        
        if failed > 0 or critical > 0:
            return "🚨 CRITICAL - System has breaking issues"
        elif health_score < 60 or high > 10:
            return "⚠️ POOR - Major quality issues need attention"
        elif health_score < 80 or high > 5:
            return "🔶 FAIR - Some issues should be addressed"
        elif health_score < 90:
            return "✅ GOOD - Minor issues, generally stable"
        else:
            return "🌟 EXCELLENT - High quality, production ready"
    
    def run_quick_smoke_test(self) -> Dict:
        """Run a quick smoke test to verify basic functionality"""
        
        print("💨 Running Quick Smoke Test...")
        
        # Use the balanced mage scenario for quick testing
        scenario = self.test_scenarios['mage_balanced_gameplay']
        scenario['max_turns'] = 5  # Limit to 5 turns for speed
        scenario['test_actions'] = ['1', '2', '3', '4', '1']
        
        try:
            session_result = self.run_test_session(scenario)
            validation_result = self.validator.validate_game_session(session_result['session_data'])
            
            status = validation_result['overall_status']
            score = validation_result['health_score']
            critical = validation_result['issues_by_severity']['critical']
            
            print(f"💨 Smoke Test Result: {status} (Score: {score}/100)")
            
            if critical > 0:
                print("🚨 SMOKE TEST FAILED - Critical issues detected")
                return {'passed': False, 'critical_issues': critical, 'details': validation_result}
            else:
                print("✅ SMOKE TEST PASSED - Basic functionality working")
                return {'passed': True, 'score': score, 'details': validation_result}
                
        except Exception as e:
            print(f"💥 SMOKE TEST CRASHED: {e}")
            return {'passed': False, 'error': str(e)}
    
    def continuous_monitoring_test(self, duration_minutes: int = 10) -> Dict:
        """Run continuous monitoring test to detect issues over time"""
        
        print(f"⏰ Starting {duration_minutes}-minute continuous monitoring test...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        test_results = []
        test_count = 0
        
        while time.time() < end_time:
            test_count += 1
            print(f"🔄 Running test iteration {test_count}...")
            
            # Rotate through different scenarios
            scenario_names = list(self.test_scenarios.keys())
            scenario_name = scenario_names[test_count % len(scenario_names)]
            scenario = self.test_scenarios[scenario_name].copy()
            scenario['max_turns'] = 3  # Keep tests short for continuous monitoring
            
            try:
                session_result = self.run_test_session(scenario)
                validation_result = self.validator.validate_game_session(session_result['session_data'])
                
                test_results.append({
                    'iteration': test_count,
                    'scenario': scenario_name,
                    'timestamp': time.time(),
                    'health_score': validation_result['health_score'],
                    'critical_issues': validation_result['issues_by_severity']['critical'],
                    'high_issues': validation_result['issues_by_severity']['high']
                })
                
                # Brief pause between tests
                time.sleep(5)
                
            except Exception as e:
                test_results.append({
                    'iteration': test_count,
                    'scenario': scenario_name,
                    'timestamp': time.time(),
                    'error': str(e)
                })
        
        # Analyze continuous test results
        successful_tests = [r for r in test_results if 'health_score' in r]
        failed_tests = [r for r in test_results if 'error' in r]
        
        if successful_tests:
            avg_health = sum(r['health_score'] for r in successful_tests) / len(successful_tests)
            total_critical = sum(r['critical_issues'] for r in successful_tests)
            total_high = sum(r['high_issues'] for r in successful_tests)
        else:
            avg_health = 0
            total_critical = 0
            total_high = 0
        
        print(f"⏰ Continuous monitoring complete: {len(successful_tests)}/{len(test_results)} tests passed")
        
        return {
            'duration_minutes': duration_minutes,
            'total_iterations': len(test_results),
            'successful_iterations': len(successful_tests),
            'failed_iterations': len(failed_tests),
            'average_health_score': round(avg_health, 1),
            'total_critical_issues': total_critical,
            'total_high_issues': total_high,
            'stability_rating': len(successful_tests) / len(test_results) * 100,
            'detailed_results': test_results
        }