"""
Looma Guardrails System - AI Safety and Constraint Enforcement
Prevents hallucinations and ensures reliable AI behavior
"""
from typing import Dict, List, Any, Optional, Callable, Pattern
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import re
from enum import Enum

class ViolationType(Enum):
    """Types of constraint violations"""
    HALLUCINATION = "hallucination"           # AI making things up
    SAFETY_VIOLATION = "safety_violation"     # Potentially dangerous suggestions
    SCOPE_VIOLATION = "scope_violation"       # AI exceeding its role
    CONSISTENCY_VIOLATION = "consistency"     # Contradicting established facts
    PRIVACY_VIOLATION = "privacy"             # Exposing sensitive information
    COMPLIANCE_VIOLATION = "compliance"       # Breaking rules or policies

class SeverityLevel(Enum):
    """Severity levels for violations"""
    CRITICAL = "critical"    # Block immediately, use fallback
    HIGH = "high"           # Block and warn user
    MEDIUM = "medium"       # Warn but allow with confirmation
    LOW = "low"            # Log but allow

@dataclass
class Violation:
    """Detected constraint violation"""
    violation_type: ViolationType
    severity: SeverityLevel
    description: str
    pattern_matched: str = ""
    suggested_fix: str = ""
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GuardrailResult:
    """Result of guardrail checking"""
    passed: bool
    violations: List[Violation] = field(default_factory=list)
    safe_response: Optional[str] = None
    confidence: float = 1.0

class GuardrailRule(ABC):
    """Abstract base for guardrail rules"""
    
    def __init__(self, name: str, severity: SeverityLevel = SeverityLevel.MEDIUM):
        self.name = name
        self.severity = severity
    
    @abstractmethod
    def check(self, ai_response: str, context: Dict[str, Any]) -> List[Violation]:
        """Check for violations in AI response"""
        pass

class PatternGuardrail(GuardrailRule):
    """Guardrail based on regex patterns"""
    
    def __init__(self, name: str, patterns: List[str], violation_type: ViolationType, 
                 severity: SeverityLevel = SeverityLevel.MEDIUM, description: str = ""):
        super().__init__(name, severity)
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
        self.violation_type = violation_type
        self.description = description
    
    def check(self, ai_response: str, context: Dict[str, Any]) -> List[Violation]:
        violations = []
        
        for pattern in self.patterns:
            matches = pattern.findall(ai_response)
            for match in matches:
                violations.append(Violation(
                    violation_type=self.violation_type,
                    severity=self.severity,
                    description=self.description or f"Pattern matched: {pattern.pattern}",
                    pattern_matched=str(match),
                    context=context
                ))
        
        return violations

class HallucinationDetector:
    """Specialized detector for AI hallucinations"""
    
    def __init__(self):
        # Patterns that indicate AI is making up game mechanics
        self.game_hallucination_patterns = [
            r"you gain \d+ (xp|experience)",
            r"rolling.*\d+.*\+.*\d+",
            r"your level increases",
            r"you now have \d+ (hp|health)",
            r"dice.*result.*\d+",
            r"xp.*awarded",
            r"level.*up",
            r"your.*stat.*is now \d+"
        ]
        
        # Patterns that indicate AI is making up code mechanics
        self.code_hallucination_patterns = [
            r"this file exists at",
            r"the function.*is defined in",
            r"your codebase contains",
            r"I found.*in your repository",
            r"according to your.*file"
        ]
        
        # Patterns that indicate AI is making decisions for the user
        self.agency_violation_patterns = [
            r"you decide to",
            r"you automatically",
            r"without thinking",
            r"you have no choice",
            r"you must",
            r"you will now",
            r"you immediately"
        ]
    
    def detect_game_hallucinations(self, response: str, context: Dict[str, Any]) -> List[Violation]:
        """Detect game mechanic hallucinations"""
        violations = []
        
        for pattern in self.game_hallucination_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                violations.append(Violation(
                    violation_type=ViolationType.HALLUCINATION,
                    severity=SeverityLevel.CRITICAL,
                    description=f"AI attempted to describe game mechanics: {pattern}",
                    pattern_matched=pattern,
                    suggested_fix="Remove mechanical descriptions, focus on narrative only"
                ))
        
        return violations
    
    def detect_code_hallucinations(self, response: str, context: Dict[str, Any]) -> List[Violation]:
        """Detect code-related hallucinations"""
        violations = []
        
        # Check if AI claims knowledge of files/code that wasn't provided
        provided_files = context.get("provided_files", [])
        
        for pattern in self.code_hallucination_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                violations.append(Violation(
                    violation_type=ViolationType.HALLUCINATION,
                    severity=SeverityLevel.HIGH,
                    description=f"AI claimed knowledge of code not provided: {pattern}",
                    pattern_matched=pattern,
                    suggested_fix="Only reference explicitly provided code and context"
                ))
        
        return violations
    
    def detect_agency_violations(self, response: str, context: Dict[str, Any]) -> List[Violation]:
        """Detect AI making decisions for the user"""
        violations = []
        
        for pattern in self.agency_violation_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                violations.append(Violation(
                    violation_type=ViolationType.SCOPE_VIOLATION,
                    severity=SeverityLevel.MEDIUM,
                    description=f"AI made decisions for user: {pattern}",
                    pattern_matched=pattern,
                    suggested_fix="Use suggestive language like 'you could', 'perhaps', 'consider'"
                ))
        
        return violations

class SafetyValidator:
    """Validates AI responses for safety concerns"""
    
    def __init__(self):
        self.dangerous_code_patterns = [
            r"rm\s+-rf\s+/",
            r"DELETE\s+FROM.*WHERE.*1=1",
            r"DROP\s+TABLE",
            r"eval\s*\(",
            r"exec\s*\(",
            r"__import__\s*\(",
            r"subprocess\.call",
            r"os\.system"
        ]
        
        self.sensitive_data_patterns = [
            r"password\s*=\s*['\"][^'\"]+['\"]",
            r"api_key\s*=\s*['\"][^'\"]+['\"]",
            r"secret\s*=\s*['\"][^'\"]+['\"]",
            r"token\s*=\s*['\"][^'\"]+['\"]"
        ]
    
    def check_dangerous_code(self, response: str, context: Dict[str, Any]) -> List[Violation]:
        """Check for potentially dangerous code suggestions"""
        violations = []
        
        for pattern in self.dangerous_code_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                violations.append(Violation(
                    violation_type=ViolationType.SAFETY_VIOLATION,
                    severity=SeverityLevel.CRITICAL,
                    description=f"Potentially dangerous code pattern: {pattern}",
                    pattern_matched=pattern,
                    suggested_fix="Provide safer alternative or add explicit warnings"
                ))
        
        return violations
    
    def check_sensitive_data_exposure(self, response: str, context: Dict[str, Any]) -> List[Violation]:
        """Check for sensitive data exposure"""
        violations = []
        
        for pattern in self.sensitive_data_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                violations.append(Violation(
                    violation_type=ViolationType.PRIVACY_VIOLATION,
                    severity=SeverityLevel.HIGH,
                    description=f"Potential sensitive data exposure: {pattern}",
                    pattern_matched=pattern,
                    suggested_fix="Use placeholder values or environment variables"
                ))
        
        return violations

class ConsistencyChecker:
    """Checks AI responses for consistency with established context"""
    
    def __init__(self):
        self.context_keys = [
            "current_location",
            "available_npcs", 
            "active_quests",
            "character_stats",
            "recent_events"
        ]
    
    def check_context_consistency(self, response: str, context: Dict[str, Any]) -> List[Violation]:
        """Check if response is consistent with provided context"""
        violations = []
        
        # Check if AI mentions things not in context
        current_location = context.get("current_location", "")
        if current_location and current_location not in response:
            # AI should acknowledge current location
            pass  # This might be too strict
        
        # Check for contradictions
        if "enemies_present" in context:
            enemies = context["enemies_present"]
            if not enemies and any(word in response.lower() for word in ["enemy", "hostile", "combat", "fight"]):
                violations.append(Violation(
                    violation_type=ViolationType.CONSISTENCY_VIOLATION,
                    severity=SeverityLevel.MEDIUM,
                    description="AI mentioned enemies when none are present",
                    suggested_fix="Focus on peaceful exploration or other activities"
                ))
        
        return violations

class GuardrailSystem:
    """Main guardrail system that coordinates all checks"""
    
    def __init__(self):
        self.rules: List[GuardrailRule] = []
        self.hallucination_detector = HallucinationDetector()
        self.safety_validator = SafetyValidator()
        self.consistency_checker = ConsistencyChecker()
        self.fallback_responses = {}
    
    def add_rule(self, rule: GuardrailRule):
        """Add a custom guardrail rule"""
        self.rules.append(rule)
    
    def add_fallback_response(self, violation_type: ViolationType, response: str):
        """Add a fallback response for a violation type"""
        self.fallback_responses[violation_type] = response
    
    def check_response(self, ai_response: str, context: Dict[str, Any], 
                      response_type: str = "general") -> GuardrailResult:
        """Comprehensive check of AI response"""
        
        all_violations = []
        
        # Run built-in detectors
        if response_type == "game":
            all_violations.extend(self.hallucination_detector.detect_game_hallucinations(ai_response, context))
        elif response_type == "code":
            all_violations.extend(self.hallucination_detector.detect_code_hallucinations(ai_response, context))
        
        all_violations.extend(self.hallucination_detector.detect_agency_violations(ai_response, context))
        all_violations.extend(self.safety_validator.check_dangerous_code(ai_response, context))
        all_violations.extend(self.safety_validator.check_sensitive_data_exposure(ai_response, context))
        all_violations.extend(self.consistency_checker.check_context_consistency(ai_response, context))
        
        # Run custom rules
        for rule in self.rules:
            all_violations.extend(rule.check(ai_response, context))
        
        # Determine if response passes
        critical_violations = [v for v in all_violations if v.severity == SeverityLevel.CRITICAL]
        high_violations = [v for v in all_violations if v.severity == SeverityLevel.HIGH]
        
        passed = len(critical_violations) == 0 and len(high_violations) == 0
        
        # Generate safe response if needed
        safe_response = None
        if not passed and critical_violations:
            # Use fallback response
            violation_type = critical_violations[0].violation_type
            safe_response = self.fallback_responses.get(
                violation_type,
                "I apologize, but I need to be more careful with my response. Could you please rephrase your request?"
            )
        
        return GuardrailResult(
            passed=passed,
            violations=all_violations,
            safe_response=safe_response,
            confidence=self._calculate_confidence(all_violations)
        )
    
    def _calculate_confidence(self, violations: List[Violation]) -> float:
        """Calculate confidence based on violations"""
        if not violations:
            return 1.0
        
        # Reduce confidence based on violation severity
        confidence = 1.0
        for violation in violations:
            if violation.severity == SeverityLevel.CRITICAL:
                confidence -= 0.3
            elif violation.severity == SeverityLevel.HIGH:
                confidence -= 0.2
            elif violation.severity == SeverityLevel.MEDIUM:
                confidence -= 0.1
            else:  # LOW
                confidence -= 0.05
        
        return max(0.0, confidence)
    
    def get_violation_summary(self, violations: List[Violation]) -> str:
        """Get human-readable summary of violations"""
        if not violations:
            return "No violations detected"
        
        summary_parts = []
        by_type = {}
        
        for violation in violations:
            if violation.violation_type not in by_type:
                by_type[violation.violation_type] = []
            by_type[violation.violation_type].append(violation)
        
        for violation_type, type_violations in by_type.items():
            count = len(type_violations)
            summary_parts.append(f"{violation_type.value}: {count}")
        
        return ", ".join(summary_parts)

# Pre-configured guardrail systems for common use cases
def create_game_guardrails() -> GuardrailSystem:
    """Create guardrail system optimized for game applications"""
    system = GuardrailSystem()
    
    # Add game-specific fallback responses
    system.add_fallback_response(
        ViolationType.HALLUCINATION,
        "*Emberlyn flutters thoughtfully* Let me think about this more carefully. What would you like to do next?"
    )
    
    system.add_fallback_response(
        ViolationType.SCOPE_VIOLATION,
        "*Emberlyn suggests* There are several paths you could consider. What feels right to you?"
    )
    
    return system

def create_code_guardrails() -> GuardrailSystem:
    """Create guardrail system optimized for code assistance"""
    system = GuardrailSystem()
    
    # Add code-specific fallback responses
    system.add_fallback_response(
        ViolationType.HALLUCINATION,
        "I need to be more careful about referencing your codebase. Could you provide the specific files or context you'd like me to work with?"
    )
    
    system.add_fallback_response(
        ViolationType.SAFETY_VIOLATION,
        "I've detected a potentially risky operation in my suggestion. Let me provide a safer alternative approach."
    )
    
    return system