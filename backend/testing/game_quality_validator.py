"""
Game Quality Validator - Ensures Fire Whisper maintains RPG essence and mechanical integrity
"""
import json
import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class ValidationSeverity(Enum):
    CRITICAL = "CRITICAL"  # Game-breaking issues
    HIGH = "HIGH"         # Major quality problems
    MEDIUM = "MEDIUM"     # Minor issues
    LOW = "LOW"          # Suggestions

@dataclass
class ValidationResult:
    category: str
    severity: ValidationSeverity
    issue: str
    details: str
    suggestion: str
    turn_number: int = 0

class GameQualityValidator:
    def __init__(self):
        self.validation_results = []
        self.game_session_data = []
        
    def validate_game_session(self, session_data: List[Dict]) -> Dict:
        """Validate an entire game session for quality and mechanical integrity"""
        self.game_session_data = session_data
        self.validation_results = []
        
        # Run all validation checks
        self._validate_mechanical_integrity()
        self._validate_story_quality()
        self._validate_player_agency()
        self._validate_progression_systems()
        self._validate_ai_hallucination()
        self._validate_rpg_essence()
        
        return self._generate_report()
    
    def _validate_mechanical_integrity(self):
        """Ensure dice, XP, and character mechanics are working correctly"""
        
        for i, turn in enumerate(self.game_session_data):
            turn_num = i + 1
            
            # Check XP consistency
            if 'xp_awarded' in turn and 'total_xp' in turn:
                expected_total = sum(t.get('xp_awarded', 0) for t in self.game_session_data[:i+1])
                if turn['total_xp'] != expected_total:
                    self.validation_results.append(ValidationResult(
                        category="Mechanical Integrity",
                        severity=ValidationSeverity.CRITICAL,
                        issue="XP Tracking Error",
                        details=f"Expected {expected_total} XP, got {turn['total_xp']} XP",
                        suggestion="Fix XP calculation logic in game state manager",
                        turn_number=turn_num
                    ))
            
            # Check dice roll validity
            if 'dice_roll' in turn:
                dice_data = turn['dice_roll']
                if 'base_roll' in dice_data and 'modifiers' in dice_data:
                    base = dice_data['base_roll']
                    modifiers = sum(dice_data['modifiers'].values())
                    total = dice_data.get('total', 0)
                    
                    if base + modifiers != total:
                        self.validation_results.append(ValidationResult(
                            category="Mechanical Integrity",
                            severity=ValidationSeverity.CRITICAL,
                            issue="Dice Calculation Error",
                            details=f"Base {base} + Modifiers {modifiers} ≠ Total {total}",
                            suggestion="Verify dice calculation in game engine",
                            turn_number=turn_num
                        ))
                    
                    # Check for impossible dice rolls
                    if base < 1 or base > 20:
                        self.validation_results.append(ValidationResult(
                            category="Mechanical Integrity",
                            severity=ValidationSeverity.CRITICAL,
                            issue="Invalid Dice Roll",
                            details=f"Dice roll {base} outside valid range (1-20)",
                            suggestion="Ensure dice rolls use proper random generation",
                            turn_number=turn_num
                        ))
            
            # Check character stat consistency
            if 'character_stats' in turn:
                stats = turn['character_stats']
                for stat_name, value in stats.items():
                    if isinstance(value, int) and (value < 1 or value > 30):
                        self.validation_results.append(ValidationResult(
                            category="Mechanical Integrity",
                            severity=ValidationSeverity.HIGH,
                            issue="Unrealistic Character Stat",
                            details=f"{stat_name}: {value} outside reasonable range (1-30)",
                            suggestion="Implement stat bounds checking",
                            turn_number=turn_num
                        ))
    
    def _validate_story_quality(self):
        """Ensure story maintains quality and doesn't become repetitive"""
        
        story_texts = [turn.get('ai_response', '') for turn in self.game_session_data]
        
        # Check for repetitive content
        for i in range(len(story_texts) - 1):
            current_story = story_texts[i].lower()
            next_story = story_texts[i + 1].lower()
            
            # Simple similarity check (can be enhanced)
            common_phrases = self._find_common_phrases(current_story, next_story)
            if len(common_phrases) > 3:  # Too many repeated phrases
                self.validation_results.append(ValidationResult(
                    category="Story Quality",
                    severity=ValidationSeverity.MEDIUM,
                    issue="Repetitive Content",
                    details=f"Turns {i+1} and {i+2} share {len(common_phrases)} common phrases",
                    suggestion="Enhance AI prompt diversity or add anti-repetition constraints",
                    turn_number=i+2
                ))
        
        # Check story progression
        if len(story_texts) > 5:
            early_stories = ' '.join(story_texts[:3])
            later_stories = ' '.join(story_texts[-3:])
            
            # Check if story is progressing (simple keyword analysis)
            early_keywords = set(re.findall(r'\b\w+\b', early_stories.lower()))
            later_keywords = set(re.findall(r'\b\w+\b', later_stories.lower()))
            
            overlap_ratio = len(early_keywords & later_keywords) / len(early_keywords | later_keywords)
            if overlap_ratio > 0.8:  # Too much overlap suggests lack of progression
                self.validation_results.append(ValidationResult(
                    category="Story Quality",
                    severity=ValidationSeverity.HIGH,
                    issue="Lack of Story Progression",
                    details=f"Story content {overlap_ratio:.1%} similar between early and later turns",
                    suggestion="Ensure AI maintains story progression and introduces new elements",
                    turn_number=len(story_texts)
                ))
    
    def _validate_player_agency(self):
        """Ensure player choices matter and have consequences"""
        
        for i, turn in enumerate(self.game_session_data):
            turn_num = i + 1
            ai_response = turn.get('ai_response', '')
            
            # Check for player agency violations
            agency_violations = [
                "you decide to",
                "you automatically",
                "without thinking",
                "you have no choice",
                "you must"
            ]
            
            for violation in agency_violations:
                if violation in ai_response.lower():
                    self.validation_results.append(ValidationResult(
                        category="Player Agency",
                        severity=ValidationSeverity.HIGH,
                        issue="Player Agency Violation",
                        details=f"AI assumed player action: '{violation}'",
                        suggestion="Ensure AI waits for player input and doesn't assume actions",
                        turn_number=turn_num
                    ))
            
            # Check for meaningful choices
            if 'choices_presented' in turn:
                choices = turn['choices_presented']
                if len(choices) < 3:
                    self.validation_results.append(ValidationResult(
                        category="Player Agency",
                        severity=ValidationSeverity.MEDIUM,
                        issue="Limited Player Choices",
                        details=f"Only {len(choices)} choices presented",
                        suggestion="Provide 3-4 meaningful choices per turn",
                        turn_number=turn_num
                    ))
    
    def _validate_progression_systems(self):
        """Ensure character progression feels rewarding and balanced"""
        
        xp_gains = [turn.get('xp_awarded', 0) for turn in self.game_session_data]
        
        if xp_gains:
            avg_xp = sum(xp_gains) / len(xp_gains)
            
            # Check for XP pacing issues
            if avg_xp < 5:
                self.validation_results.append(ValidationResult(
                    category="Progression Systems",
                    severity=ValidationSeverity.MEDIUM,
                    issue="Slow XP Progression",
                    details=f"Average XP gain: {avg_xp:.1f} per turn",
                    suggestion="Consider increasing XP rewards for player engagement",
                    turn_number=0
                ))
            elif avg_xp > 50:
                self.validation_results.append(ValidationResult(
                    category="Progression Systems",
                    severity=ValidationSeverity.MEDIUM,
                    issue="Rapid XP Progression",
                    details=f"Average XP gain: {avg_xp:.1f} per turn",
                    suggestion="Consider reducing XP rewards to maintain challenge",
                    turn_number=0
                ))
            
            # Check for level-up frequency
            level_ups = sum(1 for turn in self.game_session_data if turn.get('level_up', False))
            if len(self.game_session_data) > 10 and level_ups == 0:
                self.validation_results.append(ValidationResult(
                    category="Progression Systems",
                    severity=ValidationSeverity.HIGH,
                    issue="No Character Progression",
                    details=f"No level-ups in {len(self.game_session_data)} turns",
                    suggestion="Review XP thresholds and ensure progression occurs",
                    turn_number=0
                ))
    
    def _validate_ai_hallucination(self):
        """Detect AI hallucinations and rule violations"""
        
        for i, turn in enumerate(self.game_session_data):
            turn_num = i + 1
            ai_response = turn.get('ai_response', '')
            
            # Check for common hallucination patterns
            hallucination_indicators = [
                r"you gain \d+ xp",  # AI shouldn't announce XP (code does this)
                r"rolling.*\d+.*\+.*\d+",  # AI shouldn't describe dice rolls
                r"your level increases",  # AI shouldn't announce level-ups
                r"you now have \d+ hp",  # AI shouldn't modify stats
                r"your.*stat.*is now",  # AI shouldn't change character stats
            ]
            
            for pattern in hallucination_indicators:
                if re.search(pattern, ai_response.lower()):
                    self.validation_results.append(ValidationResult(
                        category="AI Hallucination",
                        severity=ValidationSeverity.CRITICAL,
                        issue="AI Mechanical Hallucination",
                        details=f"AI attempted to handle mechanics: '{pattern}'",
                        suggestion="Strengthen AI constraints to prevent mechanical interference",
                        turn_number=turn_num
                    ))
            
            # Check for impossible scenarios
            impossible_scenarios = [
                "you teleport",
                "you fly without magic",
                "you become invisible",
                "you read minds",
                "time stops"
            ]
            
            for scenario in impossible_scenarios:
                if scenario in ai_response.lower():
                    self.validation_results.append(ValidationResult(
                        category="AI Hallucination",
                        severity=ValidationSeverity.HIGH,
                        issue="Impossible Scenario",
                        details=f"AI created unrealistic scenario: '{scenario}'",
                        suggestion="Add reality constraints to AI prompts",
                        turn_number=turn_num
                    ))
    
    def _validate_rpg_essence(self):
        """Ensure the game maintains core RPG elements that keep players engaged"""
        
        # Check for essential RPG elements
        rpg_elements = {
            'combat': 0,
            'exploration': 0,
            'social': 0,
            'puzzle': 0,
            'character_development': 0
        }
        
        for turn in self.game_session_data:
            ai_response = turn.get('ai_response', '').lower()
            
            # Simple keyword detection (can be enhanced)
            if any(word in ai_response for word in ['fight', 'attack', 'battle', 'combat']):
                rpg_elements['combat'] += 1
            if any(word in ai_response for word in ['explore', 'search', 'discover', 'find']):
                rpg_elements['exploration'] += 1
            if any(word in ai_response for word in ['talk', 'convince', 'persuade', 'negotiate']):
                rpg_elements['social'] += 1
            if any(word in ai_response for word in ['puzzle', 'riddle', 'mystery', 'solve']):
                rpg_elements['puzzle'] += 1
            if turn.get('level_up', False) or turn.get('xp_awarded', 0) > 0:
                rpg_elements['character_development'] += 1
        
        total_turns = len(self.game_session_data)
        if total_turns > 5:
            # Check for variety in RPG elements
            active_elements = sum(1 for count in rpg_elements.values() if count > 0)
            if active_elements < 3:
                self.validation_results.append(ValidationResult(
                    category="RPG Essence",
                    severity=ValidationSeverity.HIGH,
                    issue="Limited RPG Variety",
                    details=f"Only {active_elements}/5 RPG elements present",
                    suggestion="Ensure game includes combat, exploration, social, puzzle, and progression elements",
                    turn_number=0
                ))
            
            # Check for character development
            if rpg_elements['character_development'] == 0:
                self.validation_results.append(ValidationResult(
                    category="RPG Essence",
                    severity=ValidationSeverity.CRITICAL,
                    issue="No Character Development",
                    details="No XP gains or level-ups detected",
                    suggestion="Ensure progression systems are active and rewarding",
                    turn_number=0
                ))
    
    def _find_common_phrases(self, text1: str, text2: str) -> List[str]:
        """Find common phrases between two texts"""
        words1 = text1.split()
        words2 = text2.split()
        
        common_phrases = []
        for i in range(len(words1) - 2):
            phrase = ' '.join(words1[i:i+3])
            if phrase in text2:
                common_phrases.append(phrase)
        
        return common_phrases
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive validation report"""
        
        # Categorize results by severity
        critical = [r for r in self.validation_results if r.severity == ValidationSeverity.CRITICAL]
        high = [r for r in self.validation_results if r.severity == ValidationSeverity.HIGH]
        medium = [r for r in self.validation_results if r.severity == ValidationSeverity.MEDIUM]
        low = [r for r in self.validation_results if r.severity == ValidationSeverity.LOW]
        
        # Calculate overall game health score
        total_issues = len(self.validation_results)
        critical_weight = len(critical) * 10
        high_weight = len(high) * 5
        medium_weight = len(medium) * 2
        low_weight = len(low) * 1
        
        total_weight = critical_weight + high_weight + medium_weight + low_weight
        max_possible_weight = len(self.game_session_data) * 2  # Baseline expectation
        
        health_score = max(0, 100 - (total_weight / max(1, max_possible_weight)) * 100)
        
        # Determine overall status
        if len(critical) > 0:
            status = "CRITICAL - Game Breaking Issues"
        elif len(high) > 3:
            status = "POOR - Major Quality Issues"
        elif len(high) > 0 or len(medium) > 5:
            status = "FAIR - Some Issues Need Attention"
        elif len(medium) > 0:
            status = "GOOD - Minor Issues"
        else:
            status = "EXCELLENT - High Quality"
        
        return {
            'overall_status': status,
            'health_score': round(health_score, 1),
            'total_turns_analyzed': len(self.game_session_data),
            'issues_by_severity': {
                'critical': len(critical),
                'high': len(high),
                'medium': len(medium),
                'low': len(low)
            },
            'detailed_results': {
                'critical': [self._result_to_dict(r) for r in critical],
                'high': [self._result_to_dict(r) for r in high],
                'medium': [self._result_to_dict(r) for r in medium],
                'low': [self._result_to_dict(r) for r in low]
            },
            'recommendations': self._generate_recommendations(critical, high, medium)
        }
    
    def _result_to_dict(self, result: ValidationResult) -> Dict:
        """Convert validation result to dictionary"""
        return {
            'category': result.category,
            'severity': result.severity.value,
            'issue': result.issue,
            'details': result.details,
            'suggestion': result.suggestion,
            'turn_number': result.turn_number
        }
    
    def _generate_recommendations(self, critical, high, medium) -> List[str]:
        """Generate actionable recommendations based on issues found"""
        recommendations = []
        
        if critical:
            recommendations.append("🚨 IMMEDIATE ACTION REQUIRED: Fix critical mechanical issues before continuing development")
        
        if len(high) > 2:
            recommendations.append("⚠️ Address high-priority issues to maintain game quality")
        
        if any(r.category == "AI Hallucination" for r in critical + high):
            recommendations.append("🤖 Strengthen AI constraints and validation to prevent hallucinations")
        
        if any(r.category == "RPG Essence" for r in critical + high):
            recommendations.append("🎮 Review game design to ensure core RPG elements are present")
        
        if any(r.category == "Player Agency" for r in high):
            recommendations.append("👤 Ensure player choices remain meaningful and impactful")
        
        if len(medium) > 5:
            recommendations.append("🔧 Consider addressing medium-priority issues for better player experience")
        
        return recommendations