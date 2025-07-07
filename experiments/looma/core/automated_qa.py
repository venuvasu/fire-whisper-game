"""
Looma Automated Quality Assurance - Self-Healing AI Systems
Pattern discovered from Fire Whisper RPG automated testing
"""
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import time
import json

@dataclass
class QualityIssue:
    """Detected quality issue in AI behavior"""
    issue_type: str
    severity: str  # "critical", "high", "medium", "low"
    description: str
    context: Dict[str, Any]
    evidence: Dict[str, Any]
    suggested_fix: str = ""
    auto_fixable: bool = False
    timestamp: float = field(default_factory=time.time)

@dataclass
class QualitySession:
    """Complete quality assessment session"""
    session_id: str
    interactions: List[Dict[str, Any]]
    issues_detected: List[QualityIssue]
    fixes_applied: List[str]
    quality_score: float
    timestamp: float

class QualityAnalyzer(ABC):
    """Abstract base for quality analyzers"""
    
    @abstractmethod
    def analyze(self, interactions: List[Dict[str, Any]]) -> List[QualityIssue]:
        """Analyze interactions for quality issues"""
        pass
    
    @abstractmethod
    def get_analyzer_name(self) -> str:
        """Get analyzer name for reporting"""
        pass

class ConsistencyAnalyzer(QualityAnalyzer):
    """Analyzes AI responses for consistency issues"""
    
    def analyze(self, interactions: List[Dict[str, Any]]) -> List[QualityIssue]:
        issues = []
        
        # Track context elements across interactions
        context_elements = {}
        
        for i, interaction in enumerate(interactions):
            ai_response = interaction.get('ai_response', '').lower()
            
            # Extract key elements
            current_elements = self._extract_context_elements(ai_response)
            
            if i == 0:
                context_elements = current_elements
            else:
                # Check for inconsistencies
                inconsistencies = self._find_inconsistencies(context_elements, current_elements)
                for inconsistency in inconsistencies:
                    issues.append(QualityIssue(
                        issue_type="consistency_violation",
                        severity="medium",
                        description=inconsistency['description'],
                        context={"interaction_index": i},
                        evidence=inconsistency['evidence'],
                        suggested_fix="Maintain consistent context elements",
                        auto_fixable=True
                    ))
        
        return issues
    
    def _extract_context_elements(self, response: str) -> Dict[str, List[str]]:
        """Extract context elements from AI response"""
        elements = {
            'locations': [],
            'characters': [],
            'tone_indicators': [],
            'objects': []
        }
        
        # Location keywords
        location_words = ['village', 'forest', 'cave', 'shrine', 'path', 'road', 'grove']
        for word in location_words:
            if word in response:
                elements['locations'].append(word)
        
        # Tone indicators
        peaceful_words = ['peaceful', 'calm', 'lovely', 'beautiful', 'gentle']
        dangerous_words = ['danger', 'threat', 'hostile', 'enemy', 'shadow', 'dark']
        
        for word in peaceful_words:
            if word in response:
                elements['tone_indicators'].append('peaceful')
        
        for word in dangerous_words:
            if word in response:
                elements['tone_indicators'].append('dangerous')
        
        return elements
    
    def _find_inconsistencies(self, previous: Dict, current: Dict) -> List[Dict]:
        """Find inconsistencies between context elements"""
        inconsistencies = []
        
        # Check tone consistency
        prev_tones = set(previous.get('tone_indicators', []))
        curr_tones = set(current.get('tone_indicators', []))
        
        if 'peaceful' in prev_tones and 'dangerous' in curr_tones:
            inconsistencies.append({
                'description': 'Tone shifted from peaceful to dangerous without explanation',
                'evidence': {'previous_tones': list(prev_tones), 'current_tones': list(curr_tones)}
            })
        
        return inconsistencies
    
    def get_analyzer_name(self) -> str:
        return "consistency_analyzer"

class HallucinationAnalyzer(QualityAnalyzer):
    """Analyzes AI responses for hallucinations"""
    
    def __init__(self):
        self.hallucination_patterns = [
            r"you gain \d+ (xp|experience)",
            r"rolling.*\d+.*\+.*\d+",
            r"your level increases",
            r"dice.*result.*\d+",
            r"according to your.*file",
            r"I found.*in your repository"
        ]
    
    def analyze(self, interactions: List[Dict[str, Any]]) -> List[QualityIssue]:
        issues = []
        
        import re
        
        for i, interaction in enumerate(interactions):
            ai_response = interaction.get('ai_response', '').lower()
            
            for pattern in self.hallucination_patterns:
                if re.search(pattern, ai_response):
                    issues.append(QualityIssue(
                        issue_type="hallucination",
                        severity="critical",
                        description=f"AI hallucinated: {pattern}",
                        context={"interaction_index": i},
                        evidence={"pattern_matched": pattern, "response_excerpt": ai_response[:200]},
                        suggested_fix="Remove hallucinated content, focus on verified information",
                        auto_fixable=True
                    ))
        
        return issues
    
    def get_analyzer_name(self) -> str:
        return "hallucination_analyzer"

class ResponseQualityAnalyzer(QualityAnalyzer):
    """Analyzes AI response quality and engagement"""
    
    def analyze(self, interactions: List[Dict[str, Any]]) -> List[QualityIssue]:
        issues = []
        
        for i, interaction in enumerate(interactions):
            ai_response = interaction.get('ai_response', '')
            
            # Check response length
            if len(ai_response) < 50:
                issues.append(QualityIssue(
                    issue_type="response_quality",
                    severity="medium",
                    description=f"Response too short ({len(ai_response)} characters)",
                    context={"interaction_index": i},
                    evidence={"response_length": len(ai_response)},
                    suggested_fix="Generate more detailed responses",
                    auto_fixable=False
                ))
            
            # Check for repetitive patterns
            if i > 0:
                prev_response = interactions[i-1].get('ai_response', '')
                similarity = self._calculate_similarity(ai_response, prev_response)
                
                if similarity > 0.7:  # 70% similar
                    issues.append(QualityIssue(
                        issue_type="response_quality",
                        severity="high",
                        description=f"Response too similar to previous ({similarity:.1%})",
                        context={"interaction_index": i},
                        evidence={"similarity_score": similarity},
                        suggested_fix="Generate more varied responses",
                        auto_fixable=True
                    ))
        
        return issues
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        # Simple word-based similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def get_analyzer_name(self) -> str:
        return "response_quality_analyzer"

class AutoFixSystem:
    """Automatically applies fixes for detected issues"""
    
    def __init__(self):
        self.fix_handlers = {
            "consistency_violation": self._fix_consistency,
            "hallucination": self._fix_hallucination,
            "response_quality": self._fix_response_quality
        }
    
    def apply_fixes(self, issues: List[QualityIssue]) -> List[str]:
        """Apply automatic fixes for issues"""
        fixes_applied = []
        
        for issue in issues:
            if issue.auto_fixable and issue.issue_type in self.fix_handlers:
                fix_result = self.fix_handlers[issue.issue_type](issue)
                if fix_result:
                    fixes_applied.append(fix_result)
        
        return fixes_applied
    
    def _fix_consistency(self, issue: QualityIssue) -> Optional[str]:
        """Fix consistency issues"""
        # In practice, this would update prompts or context management
        return f"Enhanced consistency checking for: {issue.description}"
    
    def _fix_hallucination(self, issue: QualityIssue) -> Optional[str]:
        """Fix hallucination issues"""
        # In practice, this would update guardrail patterns
        pattern = issue.evidence.get('pattern_matched', '')
        return f"Added hallucination detection pattern: {pattern}"
    
    def _fix_response_quality(self, issue: QualityIssue) -> Optional[str]:
        """Fix response quality issues"""
        # In practice, this would update response generation parameters
        return f"Enhanced response quality rules: {issue.description}"

class AutomatedQASystem:
    """Main automated quality assurance system"""
    
    def __init__(self):
        self.analyzers: List[QualityAnalyzer] = [
            ConsistencyAnalyzer(),
            HallucinationAnalyzer(),
            ResponseQualityAnalyzer()
        ]
        self.auto_fixer = AutoFixSystem()
        self.sessions: List[QualitySession] = []
    
    def add_analyzer(self, analyzer: QualityAnalyzer):
        """Add custom quality analyzer"""
        self.analyzers.append(analyzer)
    
    def assess_quality(self, interactions: List[Dict[str, Any]], 
                      session_id: str = None) -> QualitySession:
        """Assess quality of AI interactions"""
        
        if not session_id:
            session_id = f"qa_{int(time.time())}"
        
        all_issues = []
        
        # Run all analyzers
        for analyzer in self.analyzers:
            try:
                issues = analyzer.analyze(interactions)
                all_issues.extend(issues)
            except Exception as e:
                print(f"Analyzer {analyzer.get_analyzer_name()} failed: {e}")
        
        # Apply auto-fixes
        fixes_applied = self.auto_fixer.apply_fixes(all_issues)
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(all_issues)
        
        # Create session
        session = QualitySession(
            session_id=session_id,
            interactions=interactions,
            issues_detected=all_issues,
            fixes_applied=fixes_applied,
            quality_score=quality_score,
            timestamp=time.time()
        )
        
        self.sessions.append(session)
        return session
    
    def _calculate_quality_score(self, issues: List[QualityIssue]) -> float:
        """Calculate overall quality score"""
        if not issues:
            return 1.0
        
        severity_weights = {
            "critical": 0.4,
            "high": 0.3,
            "medium": 0.2,
            "low": 0.1
        }
        
        total_penalty = sum(severity_weights.get(issue.severity, 0.1) for issue in issues)
        return max(0.0, 1.0 - min(1.0, total_penalty))
    
    def get_quality_report(self, session_id: str = None) -> Dict[str, Any]:
        """Get quality assessment report"""
        
        if session_id:
            sessions = [s for s in self.sessions if s.session_id == session_id]
        else:
            sessions = self.sessions[-5:]  # Last 5 sessions
        
        if not sessions:
            return {"error": "No sessions found"}
        
        # Aggregate statistics
        total_interactions = sum(len(s.interactions) for s in sessions)
        total_issues = sum(len(s.issues_detected) for s in sessions)
        total_fixes = sum(len(s.fixes_applied) for s in sessions)
        avg_quality = sum(s.quality_score for s in sessions) / len(sessions)
        
        # Issue breakdown
        issue_types = {}
        for session in sessions:
            for issue in session.issues_detected:
                if issue.issue_type not in issue_types:
                    issue_types[issue.issue_type] = 0
                issue_types[issue.issue_type] += 1
        
        return {
            "sessions_analyzed": len(sessions),
            "total_interactions": total_interactions,
            "total_issues": total_issues,
            "total_fixes": total_fixes,
            "average_quality_score": avg_quality,
            "issue_breakdown": issue_types,
            "latest_session": sessions[-1].session_id if sessions else None
        }
    
    def export_session(self, session_id: str, filepath: str):
        """Export session data for analysis"""
        session = next((s for s in self.sessions if s.session_id == session_id), None)
        
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        export_data = {
            "session_id": session.session_id,
            "timestamp": session.timestamp,
            "quality_score": session.quality_score,
            "interactions_count": len(session.interactions),
            "issues_detected": [
                {
                    "type": issue.issue_type,
                    "severity": issue.severity,
                    "description": issue.description,
                    "auto_fixable": issue.auto_fixable,
                    "evidence": issue.evidence
                }
                for issue in session.issues_detected
            ],
            "fixes_applied": session.fixes_applied
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

# Integration helpers
def create_game_qa_system() -> AutomatedQASystem:
    """Create QA system optimized for game applications"""
    qa_system = AutomatedQASystem()
    
    # Add game-specific analyzers if needed
    # qa_system.add_analyzer(GameMechanicsAnalyzer())
    
    return qa_system

def create_code_qa_system() -> AutomatedQASystem:
    """Create QA system optimized for code assistance"""
    qa_system = AutomatedQASystem()
    
    # Add code-specific analyzers
    # qa_system.add_analyzer(CodeHallucinationAnalyzer())
    # qa_system.add_analyzer(SecurityAnalyzer())
    
    return qa_system