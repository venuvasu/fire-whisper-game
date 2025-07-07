"""
Looma Action Processing - Intent Classification and Structured Outcomes
Abstracted from Fire Whisper RPG action result processing
"""
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from enum import Enum
import re

class IntentType(Enum):
    """Types of user intents Looma can handle"""
    # Code-related intents
    CODE_GENERATION = "code_generation"
    CODE_REFACTORING = "code_refactoring"
    BUG_FIXING = "bug_fixing"
    TEST_CREATION = "test_creation"
    DOCUMENTATION = "documentation"
    
    # Analysis intents
    CODE_REVIEW = "code_review"
    SECURITY_AUDIT = "security_audit"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    
    # Information intents
    EXPLANATION = "explanation"
    GUIDANCE = "guidance"
    RESEARCH = "research"
    
    # Game-related intents (for RPG applications)
    GAME_ACTION = "game_action"
    EXPLORATION = "exploration"
    SOCIAL_INTERACTION = "social_interaction"

class ConfidenceLevel(Enum):
    """Confidence levels for intent classification"""
    HIGH = "high"        # 90%+ confidence
    MEDIUM = "medium"    # 70-90% confidence  
    LOW = "low"         # 50-70% confidence
    UNCLEAR = "unclear"  # <50% confidence

@dataclass
class ClassifiedIntent:
    """Result of intent classification"""
    intent_type: IntentType
    confidence: ConfidenceLevel
    parameters: Dict[str, Any] = field(default_factory=dict)
    context_requirements: List[str] = field(default_factory=list)
    safety_flags: List[str] = field(default_factory=list)
    reasoning: str = ""

@dataclass
class ActionResult:
    """Structured result of processing an action"""
    intent: ClassifiedIntent
    success: bool
    outcome_type: str
    data: Dict[str, Any] = field(default_factory=dict)
    side_effects: List[str] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    ai_prompt_template: str = ""
    ai_context_data: Dict[str, Any] = field(default_factory=dict)

class IntentClassifier(ABC):
    """Abstract base for intent classification"""
    
    @abstractmethod
    def classify(self, user_input: str, context: Dict[str, Any]) -> ClassifiedIntent:
        """Classify user intent from input and context"""
        pass
    
    @abstractmethod
    def get_supported_intents(self) -> List[IntentType]:
        """Get list of intents this classifier supports"""
        pass

class ActionProcessor(ABC):
    """Abstract base for processing actions based on classified intent"""
    
    def __init__(self, intent_classifier: IntentClassifier):
        self.classifier = intent_classifier
        self.action_handlers: Dict[IntentType, Callable] = {}
        self.validation_rules: Dict[IntentType, List[Callable]] = {}
    
    def register_handler(self, intent_type: IntentType, handler: Callable):
        """Register a handler for a specific intent type"""
        self.action_handlers[intent_type] = handler
    
    def register_validation_rule(self, intent_type: IntentType, rule: Callable):
        """Register a validation rule for an intent type"""
        if intent_type not in self.validation_rules:
            self.validation_rules[intent_type] = []
        self.validation_rules[intent_type].append(rule)
    
    def process_action(self, user_input: str, context: Dict[str, Any]) -> ActionResult:
        """Process a user action through the full pipeline"""
        
        # Step 1: Classify intent
        intent = self.classifier.classify(user_input, context)
        
        # Step 2: Validate intent
        validation_result = self._validate_intent(intent, context)
        if not validation_result["valid"]:
            return ActionResult(
                intent=intent,
                success=False,
                outcome_type="validation_failed",
                data={"error": validation_result["reason"]},
                ai_prompt_template="validation_error",
                ai_context_data={"error_details": validation_result}
            )
        
        # Step 3: Process action
        if intent.intent_type in self.action_handlers:
            try:
                result = self.action_handlers[intent.intent_type](intent, context)
                result.intent = intent
                return result
            except Exception as e:
                return ActionResult(
                    intent=intent,
                    success=False,
                    outcome_type="processing_error",
                    data={"error": str(e)},
                    ai_prompt_template="processing_error",
                    ai_context_data={"exception": str(e)}
                )
        else:
            return ActionResult(
                intent=intent,
                success=False,
                outcome_type="unsupported_intent",
                data={"error": f"No handler for {intent.intent_type}"},
                ai_prompt_template="unsupported_intent",
                ai_context_data={"intent_type": intent.intent_type.value}
            )
    
    def _validate_intent(self, intent: ClassifiedIntent, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an intent against registered rules"""
        
        # Check confidence threshold
        if intent.confidence == ConfidenceLevel.UNCLEAR:
            return {
                "valid": False,
                "reason": "Intent unclear - please provide more specific information"
            }
        
        # Check safety flags
        if intent.safety_flags:
            return {
                "valid": False,
                "reason": f"Safety concerns: {', '.join(intent.safety_flags)}"
            }
        
        # Run custom validation rules
        if intent.intent_type in self.validation_rules:
            for rule in self.validation_rules[intent.intent_type]:
                result = rule(intent, context)
                if not result.get("valid", True):
                    return result
        
        return {"valid": True}

# Concrete implementation for code-related intents
class CodeIntentClassifier(IntentClassifier):
    """Intent classifier for code-related requests"""
    
    def __init__(self):
        self.patterns = {
            IntentType.CODE_GENERATION: [
                r"(create|generate|write|build|make)\s+(a\s+)?(function|class|method|component)",
                r"add\s+(jwt|auth|login|api|endpoint)",
                r"implement\s+",
                r"build\s+.*\s+(feature|system|module)"
            ],
            IntentType.BUG_FIXING: [
                r"(fix|debug|solve|repair)\s+",
                r"(error|bug|issue|problem)\s+",
                r"not\s+working",
                r"broken\s+"
            ],
            IntentType.CODE_REFACTORING: [
                r"(refactor|improve|optimize|clean\s+up)",
                r"make\s+.*\s+(better|cleaner|faster)",
                r"restructure\s+"
            ],
            IntentType.TEST_CREATION: [
                r"(test|spec|unit\s+test|integration\s+test)",
                r"write\s+tests\s+for",
                r"add\s+test\s+coverage"
            ],
            IntentType.EXPLANATION: [
                r"(what|how|why|explain)",
                r"what\s+does\s+.*\s+do",
                r"how\s+does\s+.*\s+work"
            ]
        }
    
    def classify(self, user_input: str, context: Dict[str, Any]) -> ClassifiedIntent:
        """Classify code-related intent"""
        
        input_lower = user_input.lower()
        best_match = None
        best_confidence = ConfidenceLevel.UNCLEAR
        
        # Pattern matching
        for intent_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, input_lower):
                    confidence = self._calculate_confidence(pattern, input_lower, context)
                    if confidence.value > best_confidence.value:
                        best_match = intent_type
                        best_confidence = confidence
        
        if best_match is None:
            best_match = IntentType.EXPLANATION  # Default fallback
        
        # Extract parameters
        parameters = self._extract_parameters(user_input, best_match)
        
        # Check for safety flags
        safety_flags = self._check_safety_flags(user_input, context)
        
        return ClassifiedIntent(
            intent_type=best_match,
            confidence=best_confidence,
            parameters=parameters,
            context_requirements=self._get_context_requirements(best_match),
            safety_flags=safety_flags,
            reasoning=f"Matched pattern for {best_match.value} with {best_confidence.value} confidence"
        )
    
    def _calculate_confidence(self, pattern: str, input_text: str, context: Dict[str, Any]) -> ConfidenceLevel:
        """Calculate confidence based on pattern match and context"""
        
        # Simple confidence calculation - could be much more sophisticated
        match_strength = len(re.findall(pattern, input_text))
        
        if match_strength >= 2:
            return ConfidenceLevel.HIGH
        elif match_strength == 1:
            # Check context for additional confidence
            if context.get("code_files_present", False):
                return ConfidenceLevel.HIGH
            else:
                return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
    
    def _extract_parameters(self, user_input: str, intent_type: IntentType) -> Dict[str, Any]:
        """Extract parameters specific to the intent type"""
        
        parameters = {}
        
        if intent_type == IntentType.CODE_GENERATION:
            # Extract what to generate
            if "function" in user_input.lower():
                parameters["target_type"] = "function"
            elif "class" in user_input.lower():
                parameters["target_type"] = "class"
            elif "component" in user_input.lower():
                parameters["target_type"] = "component"
            
            # Extract technology mentions
            tech_keywords = ["jwt", "auth", "api", "react", "python", "javascript"]
            for tech in tech_keywords:
                if tech in user_input.lower():
                    parameters.setdefault("technologies", []).append(tech)
        
        elif intent_type == IntentType.BUG_FIXING:
            # Extract error types
            if "test" in user_input.lower():
                parameters["error_context"] = "testing"
            elif "runtime" in user_input.lower():
                parameters["error_context"] = "runtime"
        
        return parameters
    
    def _get_context_requirements(self, intent_type: IntentType) -> List[str]:
        """Get required context for processing this intent"""
        
        requirements = {
            IntentType.CODE_GENERATION: ["current_files", "project_structure", "dependencies"],
            IntentType.BUG_FIXING: ["error_logs", "recent_changes", "test_results"],
            IntentType.CODE_REFACTORING: ["current_code", "test_coverage", "performance_metrics"],
            IntentType.TEST_CREATION: ["target_code", "existing_tests", "test_framework"],
            IntentType.EXPLANATION: ["relevant_code", "documentation"]
        }
        
        return requirements.get(intent_type, [])
    
    def _check_safety_flags(self, user_input: str, context: Dict[str, Any]) -> List[str]:
        """Check for potential safety issues"""
        
        flags = []
        
        # Check for dangerous operations
        dangerous_keywords = ["delete", "drop", "remove", "destroy", "format"]
        for keyword in dangerous_keywords:
            if keyword in user_input.lower():
                flags.append(f"potentially_destructive_{keyword}")
        
        # Check for security concerns
        if any(word in user_input.lower() for word in ["password", "secret", "key", "token"]):
            flags.append("handles_sensitive_data")
        
        return flags
    
    def get_supported_intents(self) -> List[IntentType]:
        """Get supported intent types"""
        return list(self.patterns.keys())

# Concrete implementation for game actions (from Fire Whisper)
class GameActionProcessor(ActionProcessor):
    """Action processor for game-related actions"""
    
    def __init__(self, intent_classifier: IntentClassifier):
        super().__init__(intent_classifier)
        self._register_game_handlers()
    
    def _register_game_handlers(self):
        """Register handlers for game-specific actions"""
        
        self.register_handler(IntentType.GAME_ACTION, self._handle_game_action)
        self.register_handler(IntentType.EXPLORATION, self._handle_exploration)
        self.register_handler(IntentType.SOCIAL_INTERACTION, self._handle_social_interaction)
    
    def _handle_game_action(self, intent: ClassifiedIntent, context: Dict[str, Any]) -> ActionResult:
        """Handle general game actions"""
        
        # Determine action type from parameters
        action_type = intent.parameters.get("action_type", "general")
        
        if action_type == "defensive_stance":
            return self._handle_defensive_stance(intent, context)
        elif action_type == "attack":
            return self._handle_attack(intent, context)
        else:
            return ActionResult(
                intent=intent,
                success=True,
                outcome_type="general_action",
                data={"action_acknowledged": True},
                ai_prompt_template="general_game_action",
                ai_context_data=context
            )
    
    def _handle_defensive_stance(self, intent: ClassifiedIntent, context: Dict[str, Any]) -> ActionResult:
        """Handle defensive stance action"""
        
        enemies_present = context.get("enemies_present", [])
        
        if enemies_present:
            return ActionResult(
                intent=intent,
                success=True,
                outcome_type="tactical_advantage",
                data={
                    "defensive_bonus": 2,
                    "observation_bonus": 1,
                    "enemies_observed": enemies_present
                },
                side_effects=["gained_tactical_awareness"],
                next_steps=["choose_combat_action", "continue_observation"],
                ai_prompt_template="defensive_stance_with_enemies",
                ai_context_data={
                    "enemies": enemies_present,
                    "tactical_advantage": True,
                    "location": context.get("current_location", "unknown")
                }
            )
        else:
            return ActionResult(
                intent=intent,
                success=True,
                outcome_type="cautious_preparation",
                data={"alertness_bonus": 1},
                side_effects=["increased_awareness"],
                next_steps=["explore_area", "move_forward"],
                ai_prompt_template="defensive_stance_safe_area",
                ai_context_data={
                    "safe_area": True,
                    "location": context.get("current_location", "unknown")
                }
            )
    
    def _handle_exploration(self, intent: ClassifiedIntent, context: Dict[str, Any]) -> ActionResult:
        """Handle exploration actions"""
        
        return ActionResult(
            intent=intent,
            success=True,
            outcome_type="discovery",
            data={"exploration_bonus": 1},
            ai_prompt_template="exploration_action",
            ai_context_data=context
        )
    
    def _handle_social_interaction(self, intent: ClassifiedIntent, context: Dict[str, Any]) -> ActionResult:
        """Handle social interaction actions"""
        
        npcs_present = context.get("npcs_present", [])
        
        return ActionResult(
            intent=intent,
            success=True,
            outcome_type="social_engagement",
            data={"npcs_available": npcs_present},
            ai_prompt_template="social_interaction",
            ai_context_data={
                "npcs": npcs_present,
                "social_context": context.get("social_context", "neutral")
            }
        )