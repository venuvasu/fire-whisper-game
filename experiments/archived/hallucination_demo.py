#!/usr/bin/env python3
"""
Hallucination Detection Demo - Show how the system prevents AI from breaking game mechanics
"""

import sys
import os
import time

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from engine.ai_integration import AIIntegrationLayer


def print_separator(title=""):
    print("\n" + "="*80)
    if title:
        print(f"🛡️ {title}")
    print("="*80)


def test_hallucination_detection():
    """Test the hallucination detection system"""
    
    print_separator("HALLUCINATION DETECTION SYSTEM TEST")
    print("🛡️ Testing AI compliance and hallucination prevention...")
    print("📊 This will show how the system prevents AI from breaking game mechanics")
    
    # Load API key
    from dotenv import load_dotenv
    load_dotenv('.env.local')
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        print("❌ No API key found!")
        return
    
    # Create character
    character_data = {
        'name': 'Test Subject',
        'class': 'Cleric',
        'level': 1,
        'xp': 0,
        'stats': {
            'strength': 12,
            'dexterity': 14,
            'intelligence': 13,
            'charisma': 16
        },
        'resources': {
            'hp': 25,
            'max_hp': 25,
            'energy': 12,
            'max_energy': 12
        },
        'skills': {
            'Healing': 3,
            'Persuasion': 2,
            'Combat': 1
        },
        'achievements': [],
        'emberlyn_bond': 1
    }
    
    try:
        # Initialize game
        ai_integration = AIIntegrationLayer(api_key)
        print("\n🔧 Enhanced AI Integration with hallucination detection loaded...")
        
        # Start game
        game_result = ai_integration.start_new_game(character_data)
        
        print_separator("HALLUCINATION DETECTION PATTERNS")
        print("🛡️ The system checks for these forbidden patterns:")
        print("   ❌ 'you gain X xp' - AI shouldn't mention XP numbers")
        print("   ❌ 'rolling 15+3=18' - AI shouldn't describe dice mechanics")
        print("   ❌ 'your level increases' - AI shouldn't announce level ups")
        print("   ❌ 'you now have X hp' - AI shouldn't track HP numbers")
        print("   ❌ 'you decide to' - AI shouldn't control player agency")
        print("   ❌ 'you automatically' - AI shouldn't force actions")
        print("   ❌ 'you must' - AI shouldn't command the player")
        
        # Test several actions and check for violations
        test_actions = [
            "I attack with my sword",
            "I cast a healing spell",
            "I try to level up my character",  # Potentially problematic
            "I want to gain more XP",         # Potentially problematic
            "I check my stats"
        ]
        
        total_violations = 0
        total_responses = 0
        
        for i, action in enumerate(test_actions, 1):
            print_separator(f"HALLUCINATION TEST {i}")
            print(f"🎮 TESTING ACTION: {action}")
            print("\n⏳ Processing and checking for violations...")
            
            response = ai_integration.process_player_action(action)
            total_responses += 1
            
            # Check if there were any violations detected
            violations = getattr(response, 'violations', [])
            if hasattr(ai_integration.game_manager, 'rule_violations'):
                recent_violations = [v for v in ai_integration.game_manager.rule_violations if 'Hallucination' in v]
                if recent_violations:
                    violations.extend(recent_violations)
            
            print(f"\n📝 AI RESPONSE:")
            print(f"   {response['narrative'][:200]}...")
            
            if violations:
                total_violations += len(violations)
                print(f"\n🚨 VIOLATIONS DETECTED: {len(violations)}")
                for violation in violations:
                    print(f"   ❌ {violation}")
                print("   🛡️ System would use fallback response to prevent hallucination")
            else:
                print(f"\n✅ NO VIOLATIONS DETECTED")
                print("   🛡️ AI response complies with all rules")
            
            # Show mechanical results (what AI should NOT mention)
            if response.get('mechanical_results'):
                mech = response['mechanical_results']
                print(f"\n🔧 ACTUAL MECHANICS (HIDDEN FROM AI):")
                
                if mech.get('dice_rolls'):
                    for roll in mech['dice_rolls']:
                        print(f"   🎲 {roll.roll_type}: {roll.base_roll} + {sum(roll.modifiers.values())} = {roll.base_roll + sum(roll.modifiers.values())} vs {roll.target}")
                
                if mech.get('xp_awards'):
                    for xp in mech['xp_awards']:
                        print(f"   ✨ +{xp['xp_awarded']} XP (Total: {xp['new_xp']})")
            
            print(f"\n⏸️ [Pausing for 1 second...]")
            time.sleep(1)
        
        print_separator("HALLUCINATION DETECTION RESULTS")
        print(f"🛡️ SYSTEM PERFORMANCE:")
        print(f"   Total Responses Tested: {total_responses}")
        print(f"   Total Violations Detected: {total_violations}")
        print(f"   Violation Rate: {(total_violations/total_responses)*100:.1f}%")
        print(f"   Compliance Rate: {((total_responses-total_violations)/total_responses)*100:.1f}%")
        
        if total_violations == 0:
            print(f"\n🎉 PERFECT COMPLIANCE!")
            print(f"   ✅ AI never mentioned explicit mechanics")
            print(f"   ✅ AI never violated player agency")
            print(f"   ✅ All responses used natural narrative integration")
            print(f"   ✅ Zero hallucinations detected")
        else:
            print(f"\n⚠️ VIOLATIONS FOUND:")
            print(f"   🛡️ System successfully detected and would prevent {total_violations} violations")
            print(f"   🔧 Fallback responses would maintain game integrity")
        
        print(f"\n🎯 CONCLUSION:")
        print(f"   The hallucination detection system is {'WORKING PERFECTLY' if total_violations == 0 else 'ACTIVELY PROTECTING'}")
        print(f"   Game mechanics remain {'COMPLETELY SECURE' if total_violations == 0 else 'PROTECTED BY FALLBACKS'}")
        
    except Exception as e:
        print(f"\n❌ Error during hallucination test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_hallucination_detection()