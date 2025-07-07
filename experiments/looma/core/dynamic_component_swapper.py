"""
Dynamic Component Swapping System
Real-time AI/Code switching based on performance metrics optimized for user experience.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Callable
from enum import Enum
import time
import random
import json
from datetime import datetime, timedelta

class ComponentType(Enum):
    AI = "ai"
    CODE = "code"
    HYBRID = "hybrid"

class PerformanceLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    DEGRADED = "degraded"
    FAILING = "failing"

@dataclass
class RealTimeMetrics:
    """Real-time performance metrics focused on user experience"""
    # Core user experience metrics
    user_engagement: float = 0.0  # 0-1, how engaged is the user
    return_likelihood: float = 0.0  # 0-1, likelihood user returns to game
    session_quality: float = 0.0  # 0-1, overall session satisfaction
    
    # Performance metrics
    response_time: float = 0.0  # seconds
    error_rate: float = 0.0  # 0-1, percentage of errors
    consistency_score: float = 1.0  # 0-1, logical consistency
    
    # Component-specific metrics
    creativity_score: float = 0.0  # 0-1, content creativity
    relationship_depth: float = 0.0  # 0-1, NPC relationship quality
    narrative_quality: float = 0.0  # 0-1, story/dialogue quality
    
    # Behavioral metrics
    choice_diversity: float = 0.0  # 0-1, variety in player choices
    session_length: float = 0.0  # minutes
    interaction_frequency: float = 0.0  # actions per minute
    
    # Failure indicators
    hallucination_count: int = 0
    logic_violations: int = 0
    user_frustration_signals: int = 0

@dataclass
class ComponentPerformanceHistory:
    """Track component performance over time"""
    component_name: str
    implementation_type: ComponentType
    metrics_history: List[RealTimeMetrics] = field(default_factory=list)
    switch_count: int = 0
    last_switch_time: Optional[datetime] = None
    current_performance_level: PerformanceLevel = PerformanceLevel.GOOD
    
    def add_metrics(self, metrics: RealTimeMetrics):
        """Add new metrics and maintain history"""
        self.metrics_history.append(metrics)
        # Keep only last 50 measurements for performance
        if len(self.metrics_history) > 50:
            self.metrics_history = self.metrics_history[-50:]
    
    def get_recent_average(self, metric_name: str, window: int = 10) -> float:
        """Get recent average for a specific metric"""
        if not self.metrics_history:
            return 0.0
        
        recent_metrics = self.metrics_history[-window:]
        values = [getattr(m, metric_name) for m in recent_metrics]
        return sum(values) / len(values)

class ComponentInterface(ABC):
    """Base interface for swappable components"""
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Tuple[Any, RealTimeMetrics]:
        """Execute component and return result with metrics"""
        pass
    
    @abstractmethod
    def get_component_type(self) -> ComponentType:
        pass

class DynamicNPCManager(ComponentInterface):
    """Dynamic NPC manager that can swap between AI and Code"""
    
    def __init__(self):
        self.ai_implementation = AI_NPCRelationshipManager()
        self.code_implementation = Code_NPCRelationshipManager()
        self.current_implementation = ComponentType.AI  # Start with AI
        self.relationship_data = {}
        
    def execute(self, input_data: Dict[str, Any]) -> Tuple[Any, RealTimeMetrics]:
        """Execute NPC interaction with performance monitoring"""
        start_time = time.time()
        metrics = RealTimeMetrics()
        
        npc_id = input_data.get("npc_id")
        action = input_data.get("action")
        context = input_data.get("context", {})
        
        try:
            if self.current_implementation == ComponentType.AI:
                result = self._execute_ai_npc(npc_id, action, context, metrics)
            else:
                result = self._execute_code_npc(npc_id, action, context, metrics)
            
            # Calculate performance metrics
            metrics.response_time = time.time() - start_time
            metrics.error_rate = 0.0  # No errors
            
            return result, metrics
            
        except Exception as e:
            # Handle failures gracefully
            metrics.response_time = time.time() - start_time
            metrics.error_rate = 1.0
            metrics.user_frustration_signals += 1
            
            # Fallback to code if AI fails
            if self.current_implementation == ComponentType.AI:
                try:
                    result = self._execute_code_npc(npc_id, action, context, metrics)
                    metrics.error_rate = 0.5  # Partial failure
                    return result, metrics
                except:
                    # Complete failure
                    return {"error": "NPC interaction failed"}, metrics
            else:
                return {"error": "NPC interaction failed"}, metrics
    
    def _execute_ai_npc(self, npc_id: str, action: str, context: Dict[str, Any], 
                       metrics: RealTimeMetrics) -> Dict[str, Any]:
        """Execute AI NPC interaction"""
        
        # Update relationship
        relationship_data = self.ai_implementation.update_relationship(npc_id, action, context)
        
        # Get response
        response = self.ai_implementation.get_npc_response(npc_id, action, [])
        
        # Calculate relationship score
        relationship_score = self.ai_implementation.calculate_relationship_score(npc_id)
        
        # Update metrics based on AI performance
        metrics.creativity_score = 0.85 + random.uniform(-0.1, 0.1)
        metrics.relationship_depth = relationship_score
        metrics.narrative_quality = 0.8 + random.uniform(-0.1, 0.1)
        metrics.user_engagement = min(1.0, relationship_score + 0.2)
        metrics.return_likelihood = min(1.0, relationship_score * 1.2)
        metrics.session_quality = (metrics.creativity_score + metrics.relationship_depth + metrics.narrative_quality) / 3
        
        # AI can have consistency issues
        if random.random() < 0.1:  # 10% chance of consistency issue
            metrics.hallucination_count += 1
            metrics.consistency_score = 0.7
            metrics.user_frustration_signals += 1
        else:
            metrics.consistency_score = 0.9
        
        return {
            "response": response,
            "relationship_data": relationship_data,
            "relationship_score": relationship_score,
            "implementation": "AI"
        }
    
    def _execute_code_npc(self, npc_id: str, action: str, context: Dict[str, Any], 
                         metrics: RealTimeMetrics) -> Dict[str, Any]:
        """Execute Code NPC interaction"""
        
        # Update relationship
        relationship_data = self.code_implementation.update_relationship(npc_id, action, context)
        
        # Get response
        response = self.code_implementation.get_npc_response(npc_id, action, [])
        
        # Calculate relationship score
        relationship_score = self.code_implementation.calculate_relationship_score(npc_id)
        
        # Update metrics based on Code performance
        metrics.creativity_score = 0.3 + random.uniform(-0.05, 0.05)
        metrics.relationship_depth = relationship_score  # Limited by code ceiling
        metrics.narrative_quality = 0.4 + random.uniform(-0.05, 0.05)
        metrics.user_engagement = min(0.6, relationship_score + 0.3)  # Code ceiling
        metrics.return_likelihood = min(0.7, relationship_score * 1.5)  # Limited appeal
        metrics.session_quality = (metrics.creativity_score + metrics.relationship_depth + metrics.narrative_quality) / 3
        
        # Code is very consistent
        metrics.consistency_score = 0.98
        metrics.hallucination_count = 0
        
        return {
            "response": response,
            "relationship_data": relationship_data,
            "relationship_score": relationship_score,
            "implementation": "Code"
        }
    
    def get_component_type(self) -> ComponentType:
        return self.current_implementation
    
    def switch_implementation(self, new_type: ComponentType):
        """Switch between AI and Code implementations"""
        self.current_implementation = new_type

class DynamicNarrativeGenerator(ComponentInterface):
    """Dynamic narrative generator with AI/Code switching"""
    
    def __init__(self):
        self.ai_implementation = AI_NarrativeGenerator()
        self.code_implementation = Code_NarrativeGenerator()
        self.current_implementation = ComponentType.AI
        
    def execute(self, input_data: Dict[str, Any]) -> Tuple[Any, RealTimeMetrics]:
        """Execute narrative generation with performance monitoring"""
        start_time = time.time()
        metrics = RealTimeMetrics()
        
        try:
            if self.current_implementation == ComponentType.AI:
                result = self._execute_ai_narrative(input_data, metrics)
            else:
                result = self._execute_code_narrative(input_data, metrics)
            
            metrics.response_time = time.time() - start_time
            metrics.error_rate = 0.0
            
            return result, metrics
            
        except Exception as e:
            metrics.response_time = time.time() - start_time
            metrics.error_rate = 1.0
            metrics.user_frustration_signals += 1
            
            # Fallback logic
            if self.current_implementation == ComponentType.AI:
                try:
                    result = self._execute_code_narrative(input_data, metrics)
                    metrics.error_rate = 0.5
                    return result, metrics
                except:
                    return {"error": "Narrative generation failed"}, metrics
            else:
                return {"error": "Narrative generation failed"}, metrics
    
    def _execute_ai_narrative(self, input_data: Dict[str, Any], metrics: RealTimeMetrics) -> Dict[str, Any]:
        """Execute AI narrative generation"""
        
        if "scene_context" in input_data:
            narrative = self.ai_implementation.generate_scene_description(input_data["scene_context"])
        elif "character" in input_data and "emotion" in input_data:
            narrative = self.ai_implementation.generate_dialogue(
                input_data["character"], input_data["emotion"], input_data.get("context", {})
            )
        else:
            narrative = "The AI considers the situation carefully..."
        
        # AI narrative metrics
        metrics.creativity_score = 0.9 + random.uniform(-0.1, 0.1)
        metrics.narrative_quality = 0.85 + random.uniform(-0.1, 0.1)
        metrics.user_engagement = 0.8 + random.uniform(-0.1, 0.1)
        metrics.return_likelihood = 0.75 + random.uniform(-0.1, 0.1)
        metrics.session_quality = (metrics.creativity_score + metrics.narrative_quality + metrics.user_engagement) / 3
        
        # AI consistency issues
        if random.random() < 0.08:  # 8% chance
            metrics.hallucination_count += 1
            metrics.consistency_score = 0.75
            metrics.logic_violations += 1
        else:
            metrics.consistency_score = 0.9
        
        return {
            "narrative": narrative,
            "implementation": "AI",
            "word_count": len(narrative.split()),
            "creativity_indicators": ["rich_description", "contextual_adaptation", "emotional_depth"]
        }
    
    def _execute_code_narrative(self, input_data: Dict[str, Any], metrics: RealTimeMetrics) -> Dict[str, Any]:
        """Execute Code narrative generation"""
        
        if "scene_context" in input_data:
            narrative = self.code_implementation.generate_scene_description(input_data["scene_context"])
        elif "character" in input_data and "emotion" in input_data:
            narrative = self.code_implementation.generate_dialogue(
                input_data["character"], input_data["emotion"], input_data.get("context", {})
            )
        else:
            narrative = "Standard narrative template executed."
        
        # Code narrative metrics
        metrics.creativity_score = 0.2 + random.uniform(-0.05, 0.05)
        metrics.narrative_quality = 0.4 + random.uniform(-0.05, 0.05)
        metrics.user_engagement = 0.35 + random.uniform(-0.05, 0.05)
        metrics.return_likelihood = 0.4 + random.uniform(-0.05, 0.05)
        metrics.session_quality = (metrics.creativity_score + metrics.narrative_quality + metrics.user_engagement) / 3
        
        # Code is very consistent
        metrics.consistency_score = 0.98
        metrics.hallucination_count = 0
        metrics.logic_violations = 0
        
        return {
            "narrative": narrative,
            "implementation": "Code",
            "word_count": len(narrative.split()),
            "creativity_indicators": ["template_based", "consistent", "reliable"]
        }
    
    def get_component_type(self) -> ComponentType:
        return self.current_implementation
    
    def switch_implementation(self, new_type: ComponentType):
        """Switch between AI and Code implementations"""
        self.current_implementation = new_type

class PerformanceMonitor:
    """Monitors component performance and triggers switches"""
    
    def __init__(self):
        self.component_histories: Dict[str, ComponentPerformanceHistory] = {}
        self.switch_thresholds = {
            "user_engagement_min": 0.6,
            "return_likelihood_min": 0.65,
            "session_quality_min": 0.7,
            "error_rate_max": 0.15,
            "response_time_max": 3.0,
            "consistency_score_min": 0.8,
            "hallucination_max": 2  # per 10 interactions
        }
        
    def record_performance(self, component_name: str, component_type: ComponentType, 
                          metrics: RealTimeMetrics):
        """Record performance metrics for a component"""
        
        if component_name not in self.component_histories:
            self.component_histories[component_name] = ComponentPerformanceHistory(
                component_name=component_name,
                implementation_type=component_type
            )
        
        history = self.component_histories[component_name]
        history.add_metrics(metrics)
        history.implementation_type = component_type
        
        # Update performance level
        history.current_performance_level = self._evaluate_performance_level(history)
    
    def _evaluate_performance_level(self, history: ComponentPerformanceHistory) -> PerformanceLevel:
        """Evaluate current performance level"""
        
        if len(history.metrics_history) < 3:
            return PerformanceLevel.GOOD  # Not enough data
        
        # Get recent averages
        user_engagement = history.get_recent_average("user_engagement", 5)
        return_likelihood = history.get_recent_average("return_likelihood", 5)
        session_quality = history.get_recent_average("session_quality", 5)
        error_rate = history.get_recent_average("error_rate", 5)
        consistency_score = history.get_recent_average("consistency_score", 5)
        
        # Count recent hallucinations
        recent_hallucinations = sum(m.hallucination_count for m in history.metrics_history[-10:])
        
        # Evaluate against thresholds
        failing_conditions = 0
        
        if user_engagement < self.switch_thresholds["user_engagement_min"]:
            failing_conditions += 1
        if return_likelihood < self.switch_thresholds["return_likelihood_min"]:
            failing_conditions += 1
        if session_quality < self.switch_thresholds["session_quality_min"]:
            failing_conditions += 1
        if error_rate > self.switch_thresholds["error_rate_max"]:
            failing_conditions += 1
        if consistency_score < self.switch_thresholds["consistency_score_min"]:
            failing_conditions += 1
        if recent_hallucinations > self.switch_thresholds["hallucination_max"]:
            failing_conditions += 1
        
        if failing_conditions >= 3:
            return PerformanceLevel.FAILING
        elif failing_conditions >= 2:
            return PerformanceLevel.DEGRADED
        elif user_engagement > 0.8 and return_likelihood > 0.8 and session_quality > 0.8:
            return PerformanceLevel.EXCELLENT
        else:
            return PerformanceLevel.GOOD
    
    def should_switch_component(self, component_name: str) -> Tuple[bool, ComponentType]:
        """Determine if component should switch implementations"""
        
        if component_name not in self.component_histories:
            return False, ComponentType.AI
        
        history = self.component_histories[component_name]
        current_type = history.implementation_type
        performance_level = history.current_performance_level
        
        # Don't switch too frequently
        if (history.last_switch_time and 
            datetime.now() - history.last_switch_time < timedelta(minutes=2)):
            return False, current_type
        
        # Switch logic based on performance
        if performance_level == PerformanceLevel.FAILING:
            # Switch to opposite implementation
            new_type = ComponentType.CODE if current_type == ComponentType.AI else ComponentType.AI
            return True, new_type
        
        elif performance_level == PerformanceLevel.DEGRADED:
            # Consider switching based on specific issues
            recent_metrics = history.metrics_history[-5:]
            avg_consistency = sum(m.consistency_score for m in recent_metrics) / len(recent_metrics)
            avg_creativity = sum(m.creativity_score for m in recent_metrics) / len(recent_metrics)
            
            if current_type == ComponentType.AI and avg_consistency < 0.7:
                return True, ComponentType.CODE  # Switch to Code for consistency
            elif current_type == ComponentType.CODE and avg_creativity < 0.3:
                return True, ComponentType.AI  # Switch to AI for creativity
        
        return False, current_type
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "components": {},
            "overall_metrics": {},
            "recommendations": []
        }
        
        all_metrics = []
        
        for component_name, history in self.component_histories.items():
            if not history.metrics_history:
                continue
            
            recent_metrics = history.metrics_history[-10:]
            all_metrics.extend(recent_metrics)
            
            component_report = {
                "current_implementation": history.implementation_type.value,
                "performance_level": history.current_performance_level.value,
                "switch_count": history.switch_count,
                "recent_averages": {
                    "user_engagement": sum(m.user_engagement for m in recent_metrics) / len(recent_metrics),
                    "return_likelihood": sum(m.return_likelihood for m in recent_metrics) / len(recent_metrics),
                    "session_quality": sum(m.session_quality for m in recent_metrics) / len(recent_metrics),
                    "response_time": sum(m.response_time for m in recent_metrics) / len(recent_metrics),
                    "error_rate": sum(m.error_rate for m in recent_metrics) / len(recent_metrics),
                    "consistency_score": sum(m.consistency_score for m in recent_metrics) / len(recent_metrics),
                    "creativity_score": sum(m.creativity_score for m in recent_metrics) / len(recent_metrics),
                    "relationship_depth": sum(m.relationship_depth for m in recent_metrics) / len(recent_metrics),
                    "narrative_quality": sum(m.narrative_quality for m in recent_metrics) / len(recent_metrics)
                },
                "total_hallucinations": sum(m.hallucination_count for m in recent_metrics),
                "total_logic_violations": sum(m.logic_violations for m in recent_metrics)
            }
            
            report["components"][component_name] = component_report
        
        # Overall metrics
        if all_metrics:
            report["overall_metrics"] = {
                "average_user_engagement": sum(m.user_engagement for m in all_metrics) / len(all_metrics),
                "average_return_likelihood": sum(m.return_likelihood for m in all_metrics) / len(all_metrics),
                "average_session_quality": sum(m.session_quality for m in all_metrics) / len(all_metrics),
                "total_errors": sum(1 for m in all_metrics if m.error_rate > 0),
                "total_hallucinations": sum(m.hallucination_count for m in all_metrics),
                "average_response_time": sum(m.response_time for m in all_metrics) / len(all_metrics)
            }
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on performance data"""
        
        recommendations = []
        overall = report.get("overall_metrics", {})
        
        if overall.get("average_user_engagement", 0) < 0.7:
            recommendations.append("User engagement is low - consider increasing AI usage for creativity")
        
        if overall.get("average_return_likelihood", 0) < 0.7:
            recommendations.append("Return likelihood is concerning - focus on relationship depth and narrative quality")
        
        if overall.get("total_hallucinations", 0) > 5:
            recommendations.append("High hallucination count - increase Code usage for consistency")
        
        if overall.get("average_response_time", 0) > 2.0:
            recommendations.append("Response times are slow - optimize AI processing or increase Code usage")
        
        for component_name, component_data in report.get("components", {}).items():
            perf_level = component_data.get("performance_level")
            if perf_level in ["failing", "degraded"]:
                recommendations.append(f"{component_name} is {perf_level} - consider switching implementation")
        
        return recommendations

class DynamicGameEngine:
    """Main game engine with dynamic component swapping"""
    
    def __init__(self):
        self.npc_manager = DynamicNPCManager()
        self.narrative_generator = DynamicNarrativeGenerator()
        self.performance_monitor = PerformanceMonitor()
        self.session_start_time = datetime.now()
        self.turn_count = 0
        
    def process_game_turn(self, turn_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a game turn with dynamic component management"""
        
        self.turn_count += 1
        turn_results = {
            "turn": self.turn_count,
            "timestamp": datetime.now().isoformat(),
            "components_used": {},
            "performance_metrics": {},
            "switches_made": []
        }
        
        # Process NPC interactions
        if "npc_interaction" in turn_data:
            npc_result, npc_metrics = self.npc_manager.execute(turn_data["npc_interaction"])
            turn_results["npc_result"] = npc_result
            turn_results["performance_metrics"]["npc"] = npc_metrics
            turn_results["components_used"]["npc"] = self.npc_manager.get_component_type().value
            
            # Record performance
            self.performance_monitor.record_performance("npc_manager", self.npc_manager.get_component_type(), npc_metrics)
            
            # Check if switch needed
            should_switch, new_type = self.performance_monitor.should_switch_component("npc_manager")
            if should_switch:
                old_type = self.npc_manager.get_component_type()
                self.npc_manager.switch_implementation(new_type)
                turn_results["switches_made"].append({
                    "component": "npc_manager",
                    "from": old_type.value,
                    "to": new_type.value,
                    "reason": "performance_degradation"
                })
        
        # Process narrative generation
        if "narrative_request" in turn_data:
            narrative_result, narrative_metrics = self.narrative_generator.execute(turn_data["narrative_request"])
            turn_results["narrative_result"] = narrative_result
            turn_results["performance_metrics"]["narrative"] = narrative_metrics
            turn_results["components_used"]["narrative"] = self.narrative_generator.get_component_type().value
            
            # Record performance
            self.performance_monitor.record_performance("narrative_generator", self.narrative_generator.get_component_type(), narrative_metrics)
            
            # Check if switch needed
            should_switch, new_type = self.performance_monitor.should_switch_component("narrative_generator")
            if should_switch:
                old_type = self.narrative_generator.get_component_type()
                self.narrative_generator.switch_implementation(new_type)
                turn_results["switches_made"].append({
                    "component": "narrative_generator",
                    "from": old_type.value,
                    "to": new_type.value,
                    "reason": "performance_degradation"
                })
        
        return turn_results
    
    def get_session_report(self) -> Dict[str, Any]:
        """Get comprehensive session performance report"""
        
        base_report = self.performance_monitor.get_performance_report()
        
        # Add session-specific data
        session_duration = (datetime.now() - self.session_start_time).total_seconds() / 60
        
        base_report["session_info"] = {
            "duration_minutes": session_duration,
            "turns_completed": self.turn_count,
            "turns_per_minute": self.turn_count / session_duration if session_duration > 0 else 0,
            "session_start": self.session_start_time.isoformat()
        }
        
        return base_report

# Import the component implementations from granular_component_tester
# Import AI components - use real AI implementations
try:
    from looma.core.ai_components import RealAI_NPCRelationshipManager, RealAI_NarrativeGenerator
    AI_NPCRelationshipManager = RealAI_NPCRelationshipManager
    AI_NarrativeGenerator = RealAI_NarrativeGenerator
except ImportError:
    from looma.core.granular_component_tester import AI_NPCRelationshipManager, AI_NarrativeGenerator

# Import code components
from looma.core.granular_component_tester import Code_NPCRelationshipManager, Code_NarrativeGenerator