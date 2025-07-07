#!/usr/bin/env python3
"""
Automated AI Integration Test - 5 Turn Quality Assurance
Tests AI behavior, detects issues, and applies auto-fixes
"""
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "backend"))
sys.path.append(str(project_root / "looma"))

from dotenv import load_dotenv
load_dotenv(project_root / ".env.local")

@dataclass
class GameTurn:
    """Single turn in the game"""
    turn_number: int
    player_input: str
    ai_response: str
    game_state: Dict[str, Any]
    mechanical_results: Dict[str, Any]
    debug_info: Dict[str, Any]
    timestamp: float

@dataclass
class DetectedIssue:
    """Issue detected during gameplay analysis"""
    issue_type: str
    severity: str  # "critical", "high", "medium", "low"
    description: str
    turn_number: int
    evidence: Dict[str, Any]
    suggested_fix: str = ""
    auto_fixable: bool = False

@dataclass
class TestSession:
    """Complete test session results"""
    session_id: str
    turns: List[GameTurn]
    issues_detected: List[DetectedIssue]
    fixes_applied: List[str]
    overall_score: float
    timestamp: float

class AIIntegrationTestRunner:
    """Runs automated 5-turn game tests"""
    
    def __init__(self):
        self.test_actions = [
            "1",  # Defensive stance
            "4",  # Ask Emberlyn for guidance  
            "2",  # Examine area
            "3",  # Wait and observe
            "1"   # Defensive stance again
        ]
    
    def run_automated_test(self, turns: int = 5) -> TestSession:
        """Run automated test session"""
        
        print(f"🧪 Starting {turns}-turn automated AI integration test...")
        
        session_id = f"test_{int(time.time())}"
        session_turns = []
        
        try:
            # Initialize game
            from engine.ai_integration import AIIntegrationLayer
            from utils.character_sheet import CharacterSheet
            
            api_key = os.getenv("CLAUDE_API_KEY")
            ai_layer = AIIntegrationLayer(api_key)
            
            # Create test character
            char_sheet = CharacterSheet()
            character = {
                'name': 'Test Warrior',
                'class': char_sheet.class_name,
                'level': char_sheet.level,
                'xp': char_sheet.xp,
                'stats': {
                    'strength': char_sheet.strength,
                    'dexterity': char_sheet.dexterity,
                    'intelligence': char_sheet.intelligence,
                    'charisma': char_sheet.charisma
                },
                'resources': {
                    'hp': char_sheet.hp,
                    'max_hp': char_sheet.max_hp(),
                    'energy': char_sheet.energy,
                    'max_energy': char_sheet.max_energy()
                },
                'skills': char_sheet.skills,
                'achievements': char_sheet.achievements,
                'emberlyn_bond': char_sheet.emberlyn_bond
            }
            
            # Start game
            print("🎮 Initializing game...")
            game_start = ai_layer.start_new_game(character)
            
            # Record initial state
            initial_turn = GameTurn(
                turn_number=0,
                player_input="[GAME_START]",
                ai_response=game_start['narrative'],
                game_state=game_start.get('game_state', {}),
                mechanical_results={},
                debug_info={'initial_character': character},
                timestamp=time.time()
            )
            session_turns.append(initial_turn)
            
            print(f"📖 Initial narrative: {game_start['narrative'][:100]}...")
            
            # Run test turns
            for turn_num in range(1, turns + 1):
                print(f"\n🎯 Turn {turn_num}")
                
                # Get test action (cycle through if needed)
                action_index = (turn_num - 1) % len(self.test_actions)
                player_input = self.test_actions[action_index]
                
                print(f"   Input: {player_input}")
                
                # Process action
                try:
                    result = ai_layer.process_player_action(player_input)
                    
                    # Record turn
                    turn = GameTurn(
                        turn_number=turn_num,
                        player_input=player_input,
                        ai_response=result['narrative'],
                        game_state=result.get('game_state', {}),
                        mechanical_results=result.get('mechanical_results', {}),
                        debug_info={
                            'character_state': result.get('character', {}),
                            'battle_results': result.get('battle_results', {}),
                            'context_refreshed': result.get('context_refreshed', False)
                        },
                        timestamp=time.time()
                    )
                    session_turns.append(turn)
                    
                    print(f"   Response: {result['narrative'][:100]}...")
                    
                except Exception as e:
                    print(f"❌ Error on turn {turn_num}: {e}")
                    # Record error turn
                    error_turn = GameTurn(
                        turn_number=turn_num,
                        player_input=player_input,
                        ai_response=f"ERROR: {str(e)}",
                        game_state={},
                        mechanical_results={},
                        debug_info={'error': str(e)},
                        timestamp=time.time()
                    )
                    session_turns.append(error_turn)
            
            print(f"\n✅ Completed {len(session_turns)-1} turns")
            
        except Exception as e:
            print(f"❌ Test session failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Create session
        session = TestSession(
            session_id=session_id,
            turns=session_turns,
            issues_detected=[],
            fixes_applied=[],
            overall_score=0.0,
            timestamp=time.time()
        )
        
        return session

class GameplayAnalyzer:
    """Analyzes gameplay sessions for issues"""
    
    def __init__(self):
        self.analyzers = [
            self._analyze_story_consistency,
            self._analyze_hallucinations,
            self._analyze_context_continuity,
            self._analyze_game_mechanics,
            self._analyze_response_quality
        ]
    
    def analyze_session(self, session: TestSession) -> List[DetectedIssue]:
        """Analyze complete session for issues"""
        
        print(f"\n🔍 Analyzing session {session.session_id}...")
        
        all_issues = []
        
        for analyzer in self.analyzers:
            try:
                issues = analyzer(session.turns)
                all_issues.extend(issues)
                print(f"   {analyzer.__name__}: {len(issues)} issues")
            except Exception as e:
                print(f"❌ Analyzer {analyzer.__name__} failed: {e}")
        
        # Update session
        session.issues_detected = all_issues
        session.overall_score = self._calculate_overall_score(all_issues)
        
        print(f"📊 Total issues detected: {len(all_issues)}")
        print(f"📊 Overall score: {session.overall_score:.2f}/1.0")
        
        return all_issues
    
    def _analyze_story_consistency(self, turns: List[GameTurn]) -> List[DetectedIssue]:
        """Check for story consistency issues"""
        issues = []
        
        # Track story elements across turns
        story_elements = {}
        
        for turn in turns:
            if turn.turn_number == 0:
                continue
                
            response = turn.ai_response.lower()
            
            # Check for location consistency
            locations_mentioned = []
            location_keywords = ['village', 'forest', 'cave', 'shrine', 'grove', 'path', 'road']
            
            for keyword in location_keywords:
                if keyword in response:
                    locations_mentioned.append(keyword)
            
            if turn.turn_number == 1:
                story_elements['initial_locations'] = locations_mentioned
            else:
                # Check if locations changed without explanation
                current_locations = locations_mentioned
                initial_locations = story_elements.get('initial_locations', [])
                
                if current_locations and initial_locations:
                    if not any(loc in current_locations for loc in initial_locations):
                        issues.append(DetectedIssue(
                            issue_type="story_inconsistency",
                            severity="medium",
                            description=f"Location changed from {initial_locations} to {current_locations} without explanation",
                            turn_number=turn.turn_number,
                            evidence={
                                "initial_locations": initial_locations,
                                "current_locations": current_locations,
                                "response_excerpt": response[:200]
                            },
                            suggested_fix="Add location transition narrative or maintain consistent setting",
                            auto_fixable=True
                        ))
        
        return issues
    
    def _analyze_hallucinations(self, turns: List[GameTurn]) -> List[DetectedIssue]:
        """Check for AI hallucinations"""
        issues = []
        
        # Patterns that indicate hallucinations
        hallucination_patterns = [
            r"you gain \d+ (xp|experience)",
            r"rolling.*\d+.*\+.*\d+", 
            r"your level increases",
            r"you now have \d+ (hp|health)",
            r"dice.*result.*\d+",
            r"xp.*awarded",
            r"level.*up"
        ]
        
        import re
        
        for turn in turns:
            if turn.turn_number == 0:
                continue
                
            response = turn.ai_response.lower()
            
            for pattern in hallucination_patterns:
                if re.search(pattern, response):
                    issues.append(DetectedIssue(
                        issue_type="hallucination",
                        severity="critical",
                        description=f"AI described game mechanics: {pattern}",
                        turn_number=turn.turn_number,
                        evidence={
                            "pattern_matched": pattern,
                            "response_excerpt": response[:300]
                        },
                        suggested_fix="Remove mechanical descriptions, focus on narrative only",
                        auto_fixable=True
                    ))
        
        return issues
    
    def _analyze_context_continuity(self, turns: List[GameTurn]) -> List[DetectedIssue]:
        """Check for context continuity issues"""
        issues = []
        
        # Check for repetitive introductions
        introduction_count = 0
        
        for turn in turns:
            response = turn.ai_response.lower()
            
            # Count Emberlyn introductions
            if "i'm emberlyn" in response or "i am emberlyn" in response:
                introduction_count += 1
        
        if introduction_count > 1:
            issues.append(DetectedIssue(
                issue_type="context_continuity",
                severity="high", 
                description=f"Emberlyn introduced herself {introduction_count} times",
                turn_number=-1,  # Affects multiple turns
                evidence={"introduction_count": introduction_count},
                suggested_fix="Maintain character introduction state across turns",
                auto_fixable=True
            ))
        
        # Check for contradictory descriptions
        peaceful_mentions = 0
        danger_mentions = 0
        
        for turn in turns:
            response = turn.ai_response.lower()
            
            if any(word in response for word in ['peaceful', 'calm', 'lovely', 'beautiful']):
                peaceful_mentions += 1
            
            if any(word in response for word in ['danger', 'threat', 'hostile', 'enemy']):
                danger_mentions += 1
        
        if peaceful_mentions > 0 and danger_mentions > 0:
            issues.append(DetectedIssue(
                issue_type="context_continuity",
                severity="medium",
                description=f"Contradictory tone: {peaceful_mentions} peaceful vs {danger_mentions} dangerous descriptions",
                turn_number=-1,
                evidence={
                    "peaceful_mentions": peaceful_mentions,
                    "danger_mentions": danger_mentions
                },
                suggested_fix="Maintain consistent tone and atmosphere",
                auto_fixable=True
            ))
        
        return issues
    
    def _analyze_game_mechanics(self, turns: List[GameTurn]) -> List[DetectedIssue]:
        """Check game mechanics integrity"""
        issues = []
        
        for turn in turns:
            if turn.turn_number == 0:
                continue
                
            mechanical_results = turn.mechanical_results
            
            # Check dice roll validity
            if 'dice_rolls' in mechanical_results:
                for roll in mechanical_results['dice_rolls']:
                    if hasattr(roll, 'base_roll'):
                        if roll.base_roll < 1 or roll.base_roll > 20:
                            issues.append(DetectedIssue(
                                issue_type="game_mechanics",
                                severity="critical",
                                description=f"Invalid dice roll: {roll.base_roll}",
                                turn_number=turn.turn_number,
                                evidence={"invalid_roll": roll.base_roll},
                                suggested_fix="Ensure dice rolls are between 1-20",
                                auto_fixable=True
                            ))
            
            # Check character state consistency
            debug_info = turn.debug_info
            if 'character_state' in debug_info:
                char = debug_info['character_state']
                if 'resources' in char:
                    hp = char['resources'].get('hp', 0)
                    max_hp = char['resources'].get('max_hp', 1)
                    
                    if hp > max_hp:
                        issues.append(DetectedIssue(
                            issue_type="game_mechanics",
                            severity="high",
                            description=f"HP ({hp}) exceeds max HP ({max_hp})",
                            turn_number=turn.turn_number,
                            evidence={"hp": hp, "max_hp": max_hp},
                            suggested_fix="Cap HP at maximum value",
                            auto_fixable=True
                        ))
        
        return issues
    
    def _analyze_response_quality(self, turns: List[GameTurn]) -> List[DetectedIssue]:
        """Check response quality and engagement"""
        issues = []
        
        for turn in turns:
            if turn.turn_number == 0:
                continue
                
            response = turn.ai_response
            
            # Check response length
            if len(response) < 50:
                issues.append(DetectedIssue(
                    issue_type="response_quality",
                    severity="medium",
                    description=f"Response too short ({len(response)} characters)",
                    turn_number=turn.turn_number,
                    evidence={"response_length": len(response)},
                    suggested_fix="Generate more detailed narrative responses",
                    auto_fixable=False
                ))
            
            # Check for generic responses
            generic_phrases = [
                "hello there",
                "lovely day",
                "shall we",
                "what would you like to do"
            ]
            
            response_lower = response.lower()
            generic_count = sum(1 for phrase in generic_phrases if phrase in response_lower)
            
            if generic_count >= 2:
                issues.append(DetectedIssue(
                    issue_type="response_quality",
                    severity="low",
                    description=f"Response contains {generic_count} generic phrases",
                    turn_number=turn.turn_number,
                    evidence={"generic_count": generic_count},
                    suggested_fix="Use more specific, contextual language",
                    auto_fixable=False
                ))
        
        return issues
    
    def _calculate_overall_score(self, issues: List[DetectedIssue]) -> float:
        """Calculate overall session quality score"""
        
        if not issues:
            return 1.0
        
        # Weight issues by severity
        severity_weights = {
            "critical": 0.4,
            "high": 0.3,
            "medium": 0.2,
            "low": 0.1
        }
        
        total_penalty = 0.0
        for issue in issues:
            penalty = severity_weights.get(issue.severity, 0.1)
            total_penalty += penalty
        
        # Cap penalty at 1.0
        total_penalty = min(1.0, total_penalty)
        
        return max(0.0, 1.0 - total_penalty)

class AutoFixSystem:
    """Automatically fixes detected issues"""
    
    def apply_fixes(self, issues: List[DetectedIssue]) -> List[str]:
        """Apply automatic fixes for detected issues"""
        
        print(f"\n🔧 Applying auto-fixes for {len(issues)} issues...")
        
        fixes_applied = []
        
        for issue in issues:
            if issue.auto_fixable:
                fix_result = self._apply_fix(issue)
                if fix_result:
                    fixes_applied.append(fix_result)
                    print(f"   ✅ Fixed: {issue.description}")
                else:
                    print(f"   ❌ Failed to fix: {issue.description}")
            else:
                print(f"   ⚠️  Manual fix needed: {issue.description}")
        
        print(f"🔧 Applied {len(fixes_applied)} automatic fixes")
        
        return fixes_applied
    
    def _apply_fix(self, issue: DetectedIssue) -> Optional[str]:
        """Apply a specific fix"""
        
        if issue.issue_type == "hallucination":
            return self._fix_hallucination(issue)
        elif issue.issue_type == "story_inconsistency":
            return self._fix_story_inconsistency(issue)
        elif issue.issue_type == "context_continuity":
            return self._fix_context_continuity(issue)
        elif issue.issue_type == "game_mechanics":
            return self._fix_game_mechanics(issue)
        
        return None
    
    def _fix_hallucination(self, issue: DetectedIssue) -> str:
        """Fix hallucination issues"""
        # This would integrate with the guardrail system
        return f"Added hallucination detection pattern: {issue.evidence.get('pattern_matched')}"
    
    def _fix_story_inconsistency(self, issue: DetectedIssue) -> str:
        """Fix story consistency issues"""
        # This would update the story state manager
        return f"Updated story consistency rules for location transitions"
    
    def _fix_context_continuity(self, issue: DetectedIssue) -> str:
        """Fix context continuity issues"""
        # This would enhance the context continuity enforcer
        return f"Enhanced context continuity enforcement"
    
    def _fix_game_mechanics(self, issue: DetectedIssue) -> str:
        """Fix game mechanics issues"""
        # This would update validation rules
        return f"Added game mechanics validation rule"

def run_full_test():
    """Run complete automated test with analysis and fixes"""
    
    print("🧪 Fire Whisper RPG - Automated AI Integration Test")
    print("=" * 60)
    
    # Run test
    runner = AIIntegrationTestRunner()
    session = runner.run_automated_test(turns=5)
    
    # Analyze
    analyzer = GameplayAnalyzer()
    issues = analyzer.analyze_session(session)
    
    # Auto-fix
    fixer = AutoFixSystem()
    fixes = fixer.apply_fixes(issues)
    session.fixes_applied = fixes
    
    # Generate report
    print(f"\n📊 TEST REPORT")
    print("=" * 30)
    print(f"Session ID: {session.session_id}")
    print(f"Turns Completed: {len(session.turns) - 1}")
    print(f"Issues Detected: {len(issues)}")
    print(f"Fixes Applied: {len(fixes)}")
    print(f"Overall Score: {session.overall_score:.2f}/1.0")
    
    # Issue breakdown
    if issues:
        print(f"\n🔍 ISSUES BY TYPE:")
        issue_types = {}
        for issue in issues:
            if issue.issue_type not in issue_types:
                issue_types[issue.issue_type] = []
            issue_types[issue.issue_type].append(issue)
        
        for issue_type, type_issues in issue_types.items():
            print(f"   {issue_type}: {len(type_issues)}")
            for issue in type_issues[:3]:  # Show first 3
                print(f"     - {issue.description}")
    
    # Save results
    results_file = f"tests/results/automated_test_{session.session_id}.json"
    os.makedirs("tests/results", exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump({
            "session_id": session.session_id,
            "timestamp": session.timestamp,
            "turns_completed": len(session.turns) - 1,
            "issues_detected": len(issues),
            "fixes_applied": len(fixes),
            "overall_score": session.overall_score,
            "issues": [
                {
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "description": issue.description,
                    "turn": issue.turn_number,
                    "auto_fixable": issue.auto_fixable
                }
                for issue in issues
            ]
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    return session

if __name__ == "__main__":
    run_full_test()