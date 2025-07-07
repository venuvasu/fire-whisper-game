"""
Looma Core Framework
AI Guardrails and Integration Patterns
"""

from .state_manager import StateManager, ContextManager
from .action_processor import ActionProcessor, IntentClassifier
from .guardrails import GuardrailSystem, HallucinationDetector
from .context_continuity import ContextContinuityEnforcer, ContextAnchor
from .automated_qa import AutomatedQASystem, QualityAnalyzer, QualityIssue

__version__ = "0.1.0"
__all__ = [
    "StateManager",
    "ContextManager", 
    "ActionProcessor",
    "IntentClassifier",
    "GuardrailSystem",
    "HallucinationDetector",
    "ContextContinuityEnforcer",
    "ContextAnchor",
    "AutomatedQASystem",
    "QualityAnalyzer",
    "QualityIssue"
]