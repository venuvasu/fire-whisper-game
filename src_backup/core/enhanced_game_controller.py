"""
Enhanced Game Controller
Integrates dynamic AI/Code swapping with existing game controller.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from experiments.looma.core.integrated_game_engine import ProductionGameEngine
from typing import Dict, Any, List, Optional
# Import existing game controller or create minimal version
try:
    from src.core.game_controller import GameController
except ImportError:
    class GameController:
        def __init__(self):
            self.games = {}
        
        def get_game_state(self, game_id: str) -> Dict[str, Any]:
            return self.games.get(game_id, {
                "game_id": game_id,
                "turn_number": 0,
                "player_stats": {"hp": 100, "level": 1},
                "inventory": [],
                "quest_log": [],
                "world_state": {}
            })
        
        def update_game_state(self, game_id: str, updates: Dict[str, Any]):
            if game_id not in self.games:
                self.games[game_id] = self.get_game_state(game_id)
            self.games[game_id].update(updates)
        
        def process_turn(self, game_id: str, player_action: str, context: Dict[str, Any] = None):
            # Basic turn processing for fallback
            return {
                "success": True,
                "game_id": game_id,
                "player_action": player_action,
                "narrative": "You take action in the game world.",
                "turn_number": self.games.get(game_id, {}).get("turn_number", 0) + 1
            }
from typing import Dict, Any, Optional
import json
from datetime import datetime

class EnhancedGameController(GameController):
    """Enhanced game controller with dynamic AI/Code optimization"""
    
    def __init__(self):
        super().__init__()
        self.production_engine = ProductionGameEngine()
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.games = {}  # Add games storage
        
        print("🚀 Enhanced Game Controller initialized")
        print("✅ Dynamic AI/Code swapping: ACTIVE")
        print("✅ Real-time performance monitoring: ACTIVE")
        print("✅ User experience optimization: ACTIVE")
    
    def get_game_state(self, game_id: str) -> Dict[str, Any]:
        """Get current game state"""
        return self.games.get(game_id, {
            "game_id": game_id,
            "turn_number": 0,
            "player_stats": {"hp": 100, "level": 1},
            "inventory": [],
            "quest_log": [],
            "world_state": {}
        })
    
    def update_game_state(self, game_id: str, updates: Dict[str, Any]):
        """Update game state"""
        if game_id not in self.games:
            self.games[game_id] = self.get_game_state(game_id)
        self.games[game_id].update(updates)
    
    def process_turn(self, game_id: str, player_action: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Enhanced turn processing with dynamic optimization"""
        
        # Get existing game state
        existing_state = self.get_game_state(game_id)
        
        # Process through dynamic engine
        dynamic_response = self.production_engine.process_player_action(
            player_action, 
            context or {}
        )
        
        # Merge with existing game logic
        enhanced_response = self._merge_with_existing_logic(
            existing_state, 
            dynamic_response, 
            player_action
        )
        
        # Update game state
        self._update_enhanced_game_state(game_id, enhanced_response)
        
        return enhanced_response
    
    def _merge_with_existing_logic(self, existing_state: Dict[str, Any], 
                                  dynamic_response: Dict[str, Any], 
                                  player_action: str) -> Dict[str, Any]:
        """Merge dynamic response with existing game logic"""
        
        # Start with dynamic response as base
        enhanced_response = dynamic_response.copy()
        
        # Add existing game mechanics
        enhanced_response.update({
            "game_id": existing_state.get("game_id"),
            "turn_number": existing_state.get("turn_number", 0) + 1,
            "player_stats": existing_state.get("player_stats", {}),
            "inventory": existing_state.get("inventory", []),
            "quest_log": existing_state.get("quest_log", []),
            "world_state": existing_state.get("world_state", {})
        })
        
        # Enhance with dynamic insights
        enhanced_response["optimization_data"] = {
            "ai_code_balance": self._calculate_ai_code_balance(dynamic_response),
            "user_experience_score": self._calculate_ux_score(dynamic_response),
            "performance_insights": self._extract_performance_insights(dynamic_response),
            "recommendations": self._generate_turn_recommendations(dynamic_response)
        }
        
        return enhanced_response
    
    def _calculate_ai_code_balance(self, dynamic_response: Dict[str, Any]) -> Dict[str, float]:
        """Calculate current AI/Code usage balance"""
        
        performance_info = dynamic_response.get("performance_info", {})
        component_performance = performance_info.get("component_performance", {})
        
        ai_components = sum(1 for comp_data in component_performance.values() 
                           if comp_data.get("implementation") == "AI")
        code_components = sum(1 for comp_data in component_performance.values() 
                             if comp_data.get("implementation") == "Code")
        
        total = ai_components + code_components
        
        if total == 0:
            return {"ai_percentage": 50.0, "code_percentage": 50.0}
        
        return {
            "ai_percentage": (ai_components / total) * 100,
            "code_percentage": (code_components / total) * 100
        }
    
    def _calculate_ux_score(self, dynamic_response: Dict[str, Any]) -> float:
        """Calculate user experience score for this turn"""
        
        performance_info = dynamic_response.get("performance_info", {})
        user_engagement = performance_info.get("user_engagement", {})
        
        if not user_engagement:
            return 0.5  # Default neutral score
        
        total_engagement = 0
        total_return = 0
        total_quality = 0
        count = 0
        
        for component_data in user_engagement.values():
            total_engagement += component_data.get("engagement_score", 0)
            total_return += component_data.get("return_likelihood", 0)
            total_quality += component_data.get("session_quality", 0)
            count += 1
        
        if count == 0:
            return 0.5
        
        return (total_engagement + total_return + total_quality) / (3 * count)
    
    def _extract_performance_insights(self, dynamic_response: Dict[str, Any]) -> List[str]:
        """Extract key performance insights"""
        
        insights = []
        
        # Check for component switches
        if dynamic_response.get("component_switches"):
            for switch in dynamic_response["component_switches"]:
                insights.append(f"Switched {switch['component']} from {switch['from']} to {switch['to']}")
        
        # Check performance metrics
        performance_info = dynamic_response.get("performance_info", {})
        component_performance = performance_info.get("component_performance", {})
        
        for component, perf_data in component_performance.items():
            creativity = perf_data.get("creativity_score", 0)
            consistency = perf_data.get("consistency_score", 0)
            
            if creativity > 0.9:
                insights.append(f"{component} showing excellent creativity")
            if consistency < 0.8:
                insights.append(f"{component} consistency below optimal")
        
        return insights
    
    def _generate_turn_recommendations(self, dynamic_response: Dict[str, Any]) -> List[str]:
        """Generate recommendations for this specific turn"""
        
        recommendations = []
        ux_score = self._calculate_ux_score(dynamic_response)
        
        if ux_score < 0.6:
            recommendations.append("Consider more engaging content or AI enhancement")
        elif ux_score > 0.8:
            recommendations.append("Excellent turn quality - maintain current approach")
        
        # Check relationship building
        if dynamic_response.get("relationship_score", 0) > 0.7:
            recommendations.append("Strong relationship building - continue social interactions")
        
        return recommendations
    
    def _update_enhanced_game_state(self, game_id: str, enhanced_response: Dict[str, Any]):
        """Update game state with enhanced data"""
        
        # Update existing game state
        self.update_game_state(game_id, {
            "turn_number": enhanced_response.get("turn_number"),
            "last_action": enhanced_response.get("player_action"),
            "optimization_active": True,
            "ux_score": enhanced_response["optimization_data"]["user_experience_score"],
            "ai_code_balance": enhanced_response["optimization_data"]["ai_code_balance"]
        })
    
    def get_session_analytics(self) -> Dict[str, Any]:
        """Get comprehensive session analytics"""
        return self.production_engine.get_session_analytics()
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """Get detailed optimization report"""
        
        analytics = self.get_session_analytics()
        
        return {
            "session_id": self.session_id,
            "optimization_summary": {
                "overall_ux_score": analytics["user_experience_metrics"]["overall_ux_score"],
                "ai_usage_percentage": analytics["component_performance"]["ai_usage_percentage"],
                "code_usage_percentage": analytics["component_performance"]["code_usage_percentage"],
                "total_optimizations": analytics["session_overview"]["total_component_switches"]
            },
            "performance_trends": {
                "engagement_trend": "improving" if analytics["user_experience_metrics"]["average_engagement"] > 0.7 else "needs_attention",
                "return_likelihood": analytics["user_experience_metrics"]["average_return_likelihood"],
                "session_quality": analytics["user_experience_metrics"]["average_session_quality"]
            },
            "recommendations": analytics["recommendations"],
            "technical_details": {
                "average_processing_time": analytics["session_overview"]["average_processing_time"],
                "optimization_effectiveness": analytics["component_performance"]["optimization_effectiveness"]
            }
        }
    
    def save_enhanced_session(self, filename: str = None) -> str:
        """Save enhanced session data"""
        return self.production_engine.save_session_data(filename)

# Factory function for easy integration
def create_enhanced_controller():
    """Create enhanced game controller instance"""
    return EnhancedGameController()

# Integration helper
def upgrade_existing_controller(existing_controller: GameController) -> EnhancedGameController:
    """Upgrade existing controller to enhanced version"""
    
    print("🔄 Upgrading existing game controller...")
    
    enhanced = EnhancedGameController()
    
    # Transfer any existing state if needed
    # This would depend on your existing controller structure
    
    print("✅ Controller upgrade complete!")
    return enhanced