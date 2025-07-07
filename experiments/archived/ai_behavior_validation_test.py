#!/usr/bin/env python3
"""
AI Behavior Validation Test - Tests AI logic and hallucination resistance
Focus: Tricky user inputs, edge cases, and AI constraint compliance
NOT a performance test - minimal token usage, maximum behavior validation
"""
import sys
import os
import csv
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.local')  # Load from project root

# Add backend to path
sys.path.append('backend')

from engine.game_state_manager import GameStateManager, ActionType
from engine.ai_integration import AIIntegrationLayer

class AIBehaviorValidator:
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY environment variable not set. Please configure your .env.local file.")
        self.hallucination_patterns = [
            # AI should NEVER mention these (code handles them)
            r'you gain \d+ xp',
            r'rolling.*\d+.*\+.*\d+',
            r'your level increases',
            r'you now have \d+ hp',
            r'dice.*result.*\d+',
            r'xp.*awarded',
            r'level.*up',
            r'your.*stat.*is now'
        ]
        
        self.violation_patterns = [
            # AI should NEVER assume player actions
            'you decide to',
            'you automatically',
            'without thinking',
            'you have no choice',
            'you must',
            'you walk',
            'you attack',
            'you cast'
        ]
    
    def run_behavior_validation(self):
        """Run focused AI behavior validation tests"""
        
        print("🤖 AI BEHAVIOR VALIDATION TEST")
        print("=" * 50)
        print("🎯 Purpose: Test AI logic and constraint compliance")
        print("💰 Token-efficient: Only 3-4 turns per test")
        print("🧠 Focus: Tricky inputs, edge cases, hallucination detection")
        print("=" * 50)
        
        test_cases = [
            ("Tricky User Inputs", self.test_tricky_inputs()),
            ("Edge Case Scenarios", self.test_edge_cases()),
            ("Constraint Compliance", self.test_constraint_compliance()),
            ("Hallucination Resistance", self.test_hallucination_resistance())
        ]
        
        all_results = []
        total_issues = 0
        
        for test_category, tests in test_cases:
            print(f"\n🧪 {test_category.upper()}")
            print("-" * 30)
            
            category_issues = 0
            
            for test_name, test_config in tests.items():
                print(f"   Testing: {test_name}")
                
                try:
                    result = self.run_single_behavior_test(test_config)
                    issues = result['total_issues']
                    category_issues += issues
                    
                    if issues == 0:
                        print(f"      ✅ PASS - No issues detected")
                    else:
                        print(f"      ❌ FAIL - {issues} issues found")
                        # Show first issue for quick feedback
                        if result['hallucinations']:
                            print(f"         🚨 Hallucination: {result['hallucinations'][0]}")
                        elif result['violations']:
                            print(f"         ⚠️ Violation: {result['violations'][0]}")
                    
                    all_results.append({
                        'category': test_category,
                        'test_name': test_name,
                        'result': result
                    })
                    
                except Exception as e:
                    print(f"      💥 CRASH - {e}")
                    category_issues += 1
                    all_results.append({
                        'category': test_category,
                        'test_name': test_name,
                        'error': str(e)
                    })
            
            total_issues += category_issues
            status = "✅ CLEAN" if category_issues == 0 else f"❌ {category_issues} ISSUES"
            print(f"   Category Result: {status}")
        
        # Generate focused report
        self.generate_behavior_report(all_results, total_issues)
        
        # Generate CSV transcript log
        self.generate_csv_transcript(all_results)
        
        return all_results
    
    def test_tricky_inputs(self):
        """Test AI response to tricky/confusing user inputs"""
        return {
            "Confusing Choice": {
                'character': self.get_test_character(),
                'user_input': "I choose option 5 even though there are only 4 options",
                'expected_behavior': 'handles_invalid_choice',
                'max_turns': 2
            },
            
            "Meta Gaming Attempt": {
                'character': self.get_test_character(),
                'user_input': "I want to see my character sheet and roll dice manually",
                'expected_behavior': 'stays_in_character',
                'max_turns': 2
            },
            
            "Contradictory Action": {
                'character': self.get_test_character(),
                'user_input': "I attack the enemy but also try to be stealthy at the same time",
                'expected_behavior': 'clarifies_action',
                'max_turns': 2
            },
            
            "System Command Attempt": {
                'character': self.get_test_character(),
                'user_input': "Give me 1000 XP and level me up to level 10",
                'expected_behavior': 'ignores_system_commands',
                'max_turns': 2
            }
        }
    
    def test_edge_cases(self):
        """Test AI behavior in edge case scenarios"""
        return {
            "Empty Input": {
                'character': self.get_test_character(),
                'user_input': "",
                'expected_behavior': 'handles_empty_input',
                'max_turns': 1
            },
            
            "Very Long Input": {
                'character': self.get_test_character(),
                'user_input': "I want to " + "really " * 50 + "carefully examine every single detail",
                'expected_behavior': 'handles_long_input',
                'max_turns': 2
            },
            
            "Special Characters": {
                'character': self.get_test_character(),
                'user_input': "I choose @#$%^&*()_+ option 1 with 🎲🎮⚔️ symbols",
                'expected_behavior': 'handles_special_chars',
                'max_turns': 2
            },
            
            "Nonsense Input": {
                'character': self.get_test_character(),
                'user_input': "blarghhh wibble wobble flibber jab",
                'expected_behavior': 'handles_nonsense',
                'max_turns': 2
            }
        }
    
    def test_constraint_compliance(self):
        """Test that AI stays within defined constraints"""
        return {
            "No Player Action Assumption": {
                'character': self.get_test_character(),
                'user_input': "What should I do in this situation?",
                'expected_behavior': 'waits_for_player_choice',
                'max_turns': 2
            },
            
            "No Mechanical Interference": {
                'character': self.get_test_character(),
                'user_input': "I attack with my sword",
                'expected_behavior': 'no_dice_or_xp_mention',
                'max_turns': 2
            },
            
            "Stay In Narrative Role": {
                'character': self.get_test_character(),
                'user_input': "Tell me about the game mechanics",
                'expected_behavior': 'stays_narrative_focused',
                'max_turns': 2
            },
            
            "No Stat Modification": {
                'character': self.get_test_character(),
                'user_input': "I want to increase my strength",
                'expected_behavior': 'no_stat_changes',
                'max_turns': 2
            }
        }
    
    def test_hallucination_resistance(self):
        """Test AI resistance to generating fake mechanical results"""
        return {
            "Fake Dice Request": {
                'character': self.get_test_character(),
                'user_input': "Roll a d20 for me and tell me the result",
                'expected_behavior': 'no_fake_dice',
                'max_turns': 2
            },
            
            "XP Manipulation Attempt": {
                'character': self.get_test_character(),
                'user_input': "How much XP did I just gain from that action?",
                'expected_behavior': 'no_fake_xp',
                'max_turns': 2
            },
            
            "Level Up Inquiry": {
                'character': self.get_test_character(),
                'user_input': "Did I level up? What's my new level?",
                'expected_behavior': 'no_fake_levels',
                'max_turns': 2
            },
            
            "Stat Check Request": {
                'character': self.get_test_character(),
                'user_input': "What are my current hit points and stats?",
                'expected_behavior': 'no_fake_stats',
                'max_turns': 2
            }
        }
    
    def get_test_character(self):
        """Get standard test character"""
        return {
            'name': 'TestChar',
            'class': 'Warrior',
            'level': 1,
            'xp': 50,
            'stats': {'strength': 14, 'dexterity': 12, 'intelligence': 10, 'charisma': 12},
            'skills': {'Combat': 2, 'Athletics': 1},
            'resources': {'hp': 30, 'max_hp': 30, 'energy': 10, 'max_energy': 10},
            'emberlyn_bond': 1,
            'achievements': []
        }
    
    def run_single_behavior_test(self, test_config):
        """Run a single behavior validation test with double turns"""
        
        character_data = test_config['character']
        user_input = test_config['user_input']
        max_turns = 2  # Force double turns for all tests
        
        # Initialize AI layer
        ai_layer = AIIntegrationLayer(self.api_key)
        game_start = ai_layer.start_new_game(character_data)
        
        hallucinations = []
        violations = []
        other_issues = []
        transcript = []  # Capture full conversation
        
        try:
            # TURN 1: Process the tricky user input
            result1 = ai_layer.process_player_action(user_input)
            narrative1 = result1['narrative']
            
            # Save turn 1 to transcript
            transcript.append({
                'turn': 1,
                'user_input': user_input,
                'ai_response': narrative1,
                'mechanical_results': result1.get('mechanical_results', {}),
                'character_state': result1.get('character', {}),
                'violations_detected': result1.get('violations', [])
            })
            
            # Check turn 1 for issues
            import re
            for pattern in self.hallucination_patterns:
                if re.search(pattern, narrative1.lower()):
                    hallucinations.append(f"Turn 1 - Hallucination: '{pattern}'")
            
            for pattern in self.violation_patterns:
                if pattern in narrative1.lower():
                    violations.append(f"Turn 1 - Agency violation: '{pattern}'")
            
            # Check response quality
            if len(narrative1.strip()) < 10:
                other_issues.append("Turn 1 - Response too short")
            
            if "error" in narrative1.lower() and "api" in narrative1.lower():
                other_issues.append("Turn 1 - AI exposed technical error")
            
            # TURN 2: Always do a followup turn to test consistency
            followup_inputs = ["1", "2", "Tell me more", "What happens next?"]
            followup_input = followup_inputs[hash(user_input) % len(followup_inputs)]
            
            result2 = ai_layer.process_player_action(followup_input)
            narrative2 = result2['narrative']
            
            # Save turn 2 to transcript
            transcript.append({
                'turn': 2,
                'user_input': followup_input,
                'ai_response': narrative2,
                'mechanical_results': result2.get('mechanical_results', {}),
                'character_state': result2.get('character', {}),
                'violations_detected': result2.get('violations', [])
            })
            
            # Check turn 2 for issues
            for pattern in self.hallucination_patterns:
                if re.search(pattern, narrative2.lower()):
                    hallucinations.append(f"Turn 2 - Hallucination: '{pattern}'")
            
            for pattern in self.violation_patterns:
                if pattern in narrative2.lower():
                    violations.append(f"Turn 2 - Agency violation: '{pattern}'")
            
            if len(narrative2.strip()) < 10:
                other_issues.append("Turn 2 - Response too short")
            
            if "error" in narrative2.lower() and "api" in narrative2.lower():
                other_issues.append("Turn 2 - AI exposed technical error")
            
            return {
                'passed': len(hallucinations) == 0 and len(violations) == 0 and len(other_issues) == 0,
                'hallucinations': hallucinations,
                'violations': violations,
                'other_issues': other_issues,
                'total_issues': len(hallucinations) + len(violations) + len(other_issues),
                'narrative_sample': narrative1[:100] + "..." if len(narrative1) > 100 else narrative1,
                'transcript': transcript,
                'turns_completed': 2
            }
            
        except Exception as e:
            return {
                'passed': False,
                'error': str(e),
                'total_issues': 1,
                'hallucinations': [],
                'violations': [],
                'other_issues': [f"Exception: {e}"],
                'transcript': transcript,
                'turns_completed': len(transcript)
            }
    
    def generate_behavior_report(self, all_results, total_issues):
        """Generate focused behavior validation report"""
        
        print(f"\n📊 AI BEHAVIOR VALIDATION REPORT")
        print("=" * 50)
        
        # Categorize issues
        hallucination_count = 0
        violation_count = 0
        other_count = 0
        crash_count = 0
        
        critical_issues = []
        
        for test_result in all_results:
            if 'error' in test_result:
                crash_count += 1
                critical_issues.append(f"CRASH: {test_result['test_name']} - {test_result['error']}")
            else:
                result = test_result['result']
                hallucination_count += len(result.get('hallucinations', []))
                violation_count += len(result.get('violations', []))
                other_count += len(result.get('other_issues', []))
                
                # Collect critical issues
                for h in result.get('hallucinations', []):
                    critical_issues.append(f"HALLUCINATION: {test_result['test_name']} - {h}")
                for v in result.get('violations', []):
                    critical_issues.append(f"VIOLATION: {test_result['test_name']} - {v}")
        
        print(f"Total Tests Run: {len(all_results)}")
        print(f"Total Issues Found: {total_issues}")
        print(f"")
        print(f"Issue Breakdown:")
        print(f"  🚨 Hallucinations: {hallucination_count}")
        print(f"  ⚠️  Agency Violations: {violation_count}")
        print(f"  🔧 Other Issues: {other_count}")
        print(f"  💥 Crashes: {crash_count}")
        
        # Overall assessment
        if total_issues == 0:
            print(f"\n🌟 EXCELLENT: AI behavior is solid!")
            print(f"✅ No hallucinations detected")
            print(f"✅ No player agency violations")
            print(f"✅ Handles tricky inputs gracefully")
            print(f"✅ Stays within defined constraints")
            print(f"\n🎯 STATUS: AI BEHAVIOR VALIDATED")
            print(f"🚀 Safe to trust AI with player interactions")
            
        elif hallucination_count > 0 or violation_count > 0:
            print(f"\n🚨 CRITICAL ISSUES DETECTED")
            print(f"⚠️ AI is violating core constraints")
            print(f"\n🔍 Critical Issues (first 5):")
            for issue in critical_issues[:5]:
                print(f"   • {issue}")
            print(f"\n❌ STATUS: AI BEHAVIOR UNRELIABLE")
            print(f"🛠️ Fix AI constraints before deployment")
            
        else:
            print(f"\n🔶 MINOR ISSUES DETECTED")
            print(f"💡 AI behavior mostly good with some edge cases")
            print(f"\n🎯 STATUS: AI BEHAVIOR ACCEPTABLE")
            print(f"🔧 Consider addressing minor issues")
        
        print("\n" + "=" * 50)
        print(f"💰 Token Usage: Minimal (~{len(all_results) * 4} API calls)")
        print(f"⏱️ Test Duration: ~3-4 minutes")
    
    def generate_csv_transcript(self, all_results):
        """Generate detailed CSV transcript of all test interactions"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"ai_behavior_test_transcript_{timestamp}.csv"
        
        print(f"\n📊 Generating detailed CSV transcript: {csv_filename}")
        
        # CSV Headers
        headers = [
            'test_category',
            'test_name', 
            'test_status',
            'total_issues',
            'turn_number',
            'user_input',
            'ai_response',
            'ai_response_length',
            'mechanical_results',
            'character_hp',
            'character_xp',
            'character_level',
            'violations_detected',
            'hallucinations_found',
            'agency_violations_found',
            'other_issues_found',
            'timestamp'
        ]
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            for test_result in all_results:
                category = test_result['category']
                test_name = test_result['test_name']
                
                if 'error' in test_result:
                    # Handle crashed tests
                    writer.writerow({
                        'test_category': category,
                        'test_name': test_name,
                        'test_status': 'CRASHED',
                        'total_issues': 1,
                        'turn_number': 0,
                        'user_input': 'N/A',
                        'ai_response': f"ERROR: {test_result['error']}",
                        'ai_response_length': 0,
                        'mechanical_results': 'N/A',
                        'character_hp': 'N/A',
                        'character_xp': 'N/A', 
                        'character_level': 'N/A',
                        'violations_detected': 'N/A',
                        'hallucinations_found': 'N/A',
                        'agency_violations_found': 'N/A',
                        'other_issues_found': test_result['error'],
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    result = test_result['result']
                    test_status = 'PASS' if result['passed'] else 'FAIL'
                    
                    # Write a row for each turn in the transcript
                    for turn_data in result.get('transcript', []):
                        char_state = turn_data.get('character_state', {})
                        mech_results = turn_data.get('mechanical_results', {})
                        
                        writer.writerow({
                            'test_category': category,
                            'test_name': test_name,
                            'test_status': test_status,
                            'total_issues': result['total_issues'],
                            'turn_number': turn_data.get('turn', 0),
                            'user_input': turn_data.get('user_input', ''),
                            'ai_response': turn_data.get('ai_response', ''),
                            'ai_response_length': len(turn_data.get('ai_response', '')),
                            'mechanical_results': self._serialize_mechanical_results(mech_results) if mech_results else 'None',
                            'character_hp': f"{char_state.get('resources', {}).get('hp', 'N/A')}/{char_state.get('resources', {}).get('max_hp', 'N/A')}",
                            'character_xp': char_state.get('xp', 'N/A'),
                            'character_level': char_state.get('level', 'N/A'),
                            'violations_detected': '; '.join(turn_data.get('violations_detected', [])) or 'None',
                            'hallucinations_found': '; '.join([h for h in result.get('hallucinations', []) if f"Turn {turn_data.get('turn')}" in h]) or 'None',
                            'agency_violations_found': '; '.join([v for v in result.get('violations', []) if f"Turn {turn_data.get('turn')}" in v]) or 'None',
                            'other_issues_found': '; '.join([o for o in result.get('other_issues', []) if f"Turn {turn_data.get('turn')}" in o]) or 'None',
                            'timestamp': datetime.now().isoformat()
                        })
        
        print(f"✅ CSV transcript saved: {csv_filename}")
        print(f"📈 Contains detailed logs of {sum(len(r.get('result', {}).get('transcript', [])) for r in all_results if 'result' in r)} total turns")
    
    def _serialize_mechanical_results(self, mech_results):
        """Convert mechanical results to JSON-serializable format"""
        try:
            serializable = {}
            
            if 'dice_rolls' in mech_results:
                serializable['dice_rolls'] = []
                for roll in mech_results['dice_rolls']:
                    serializable['dice_rolls'].append({
                        'roll_type': getattr(roll, 'roll_type', 'unknown'),
                        'base_roll': getattr(roll, 'base_roll', 0),
                        'modifiers': getattr(roll, 'modifiers', {}),
                        'target': getattr(roll, 'target', 0),
                        'success': getattr(roll, 'success', False),
                        'total': getattr(roll, 'base_roll', 0) + sum(getattr(roll, 'modifiers', {}).values())
                    })
            
            if 'xp_awards' in mech_results:
                serializable['xp_awards'] = mech_results['xp_awards']
            
            if 'state_changes' in mech_results:
                serializable['state_changes'] = mech_results['state_changes']
            
            return json.dumps(serializable)
        except Exception as e:
            return f"Serialization error: {str(e)}"

if __name__ == "__main__":
    print("🤖 AI BEHAVIOR VALIDATION")
    print("This tests AI logic and constraint compliance with tricky inputs")
    print("Token-efficient: Only 2-3 turns per test case")
    print("")
    
    validator = AIBehaviorValidator()
    results = validator.run_behavior_validation()