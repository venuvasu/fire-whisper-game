"""
Experiment Manager - Strangler Fig Pattern Implementation
Gradually replaces legacy components with new implementations based on configuration
"""
import json
import random
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib

class ExperimentManager:
    """
    Manages feature experiments using Strangler Fig pattern
    Allows gradual replacement of legacy code with new implementations
    """
    
    def __init__(self, user_id: str = "local_dev", environment: str = "local_development"):
        self.user_id = user_id
        self.environment = environment
        self.config = self._load_experiment_config()
        self.metrics = []
        
    def _load_experiment_config(self) -> Dict[str, Any]:
        """Load experiment configuration from config file"""
        config_path = Path(__file__).parent.parent.parent / "config" / "experiments.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback configuration
            return {
                "experiments": {},
                "user_segments": {"local_development": {"experiments": [], "override_rollout": 100}},
                "metrics_collection": {"enabled": True, "sample_rate": 1.0}
            }
    
    def is_experiment_enabled(self, experiment_name: str) -> bool:
        """
        Determine if experiment is enabled for this user
        Uses consistent hashing to ensure same user always gets same experience
        """
        experiment = self.config.get("experiments", {}).get(experiment_name)
        if not experiment or not experiment.get("enabled", False):
            return False
        
        # Check user segment override
        user_segment = self.config.get("user_segments", {}).get(self.environment, {})
        if experiment_name in user_segment.get("experiments", []):
            rollout_percentage = user_segment.get("override_rollout", 0)
        else:
            rollout_percentage = experiment.get("rollout_percentage", 0)
        
        # Use consistent hashing for stable assignment
        hash_input = f"{self.user_id}_{experiment_name}".encode()
        hash_value = int(hashlib.md5(hash_input).hexdigest()[:8], 16)
        user_percentage = hash_value % 100
        
        return user_percentage < rollout_percentage
    
    def get_feature_flag(self, experiment_name: str, flag_name: str, default: Any = False) -> Any:
        """Get feature flag value for experiment"""
        if not self.is_experiment_enabled(experiment_name):
            return default
        
        experiment = self.config.get("experiments", {}).get(experiment_name, {})
        return experiment.get("feature_flags", {}).get(flag_name, default)
    
    def get_fallback_strategy(self, experiment_name: str) -> str:
        """Get fallback strategy if experiment fails"""
        experiment = self.config.get("experiments", {}).get(experiment_name, {})
        return experiment.get("fallback_strategy", "legacy")
    
    def record_metric(self, experiment_name: str, metric_name: str, value: Any, metadata: Dict[str, Any] = None):
        """Record experiment metric"""
        if not self.config.get("metrics_collection", {}).get("enabled", False):
            return
        
        metric = {
            "experiment": experiment_name,
            "metric": metric_name,
            "value": value,
            "user_id": self.user_id,
            "environment": self.environment,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.metrics.append(metric)
        
        # In a real system, this would send to analytics backend
        # For local development, we'll log to file
        self._log_metric_to_file(metric)
    
    def _log_metric_to_file(self, metric: Dict[str, Any]):
        """Log metric to local file for development"""
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        log_file = logs_dir / "experiment_metrics.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(metric) + '\n')
    
    def should_use_new_implementation(self, component_name: str) -> bool:
        """
        Strangler Fig Pattern: Determine if we should use new implementation
        This is the key method that gradually replaces legacy code
        """
        # Map component names to experiments
        component_experiment_map = {
            "game_engine": "local_game_engine_v2",
            "narrative_generator": "improved_narrative_coherence",
            "story_progression": "local_game_engine_v2",
            "choice_processor": "local_game_engine_v2"
        }
        
        experiment_name = component_experiment_map.get(component_name)
        if not experiment_name:
            return False
        
        return self.is_experiment_enabled(experiment_name)
    
    def get_component_config(self, component_name: str) -> Dict[str, Any]:
        """Get configuration for a specific component"""
        component_experiment_map = {
            "game_engine": "local_game_engine_v2",
            "narrative_generator": "improved_narrative_coherence",
            "story_progression": "local_game_engine_v2",
            "choice_processor": "local_game_engine_v2"
        }
        
        experiment_name = component_experiment_map.get(component_name)
        if not experiment_name or not self.is_experiment_enabled(experiment_name):
            return {}
        
        experiment = self.config.get("experiments", {}).get(experiment_name, {})
        return experiment.get("feature_flags", {})

# Global experiment manager instance
_experiment_manager = None

def get_experiment_manager(user_id: str = "local_dev", environment: str = "local_development") -> ExperimentManager:
    """Get global experiment manager instance"""
    global _experiment_manager
    if _experiment_manager is None:
        _experiment_manager = ExperimentManager(user_id, environment)
    return _experiment_manager