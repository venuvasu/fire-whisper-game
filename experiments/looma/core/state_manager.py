"""
Looma State Management - Persistent Context Tracking
Abstracted from Fire Whisper RPG story state management
"""
from typing import Dict, List, Any, Optional, TypeVar, Generic
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import time
from enum import Enum

T = TypeVar('T')

class ContextType(Enum):
    """Types of contexts Looma can manage"""
    CODE_REPOSITORY = "code_repo"
    CONVERSATION = "conversation"
    PROJECT_STATE = "project_state"
    USER_SESSION = "user_session"
    GAME_WORLD = "game_world"  # For RPG-style applications

@dataclass
class ContextSnapshot:
    """Immutable snapshot of context at a point in time"""
    timestamp: float
    context_type: ContextType
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "context_type": self.context_type.value,
            "data": self.data,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextSnapshot':
        return cls(
            timestamp=data["timestamp"],
            context_type=ContextType(data["context_type"]),
            data=data["data"],
            metadata=data.get("metadata", {})
        )

class StateManager(ABC, Generic[T]):
    """Abstract base for managing persistent state"""
    
    def __init__(self, context_type: ContextType):
        self.context_type = context_type
        self.current_state: Dict[str, Any] = {}
        self.history: List[ContextSnapshot] = []
        self.event_log: List[str] = []
        
    @abstractmethod
    def initialize_state(self) -> Dict[str, Any]:
        """Initialize the default state"""
        pass
    
    @abstractmethod
    def validate_state_change(self, change: Dict[str, Any]) -> bool:
        """Validate that a state change is allowed"""
        pass
    
    def update_state(self, changes: Dict[str, Any], event_description: str = ""):
        """Update state with validation and history tracking"""
        if not self.validate_state_change(changes):
            raise ValueError(f"Invalid state change: {changes}")
        
        # Create snapshot before change
        snapshot = ContextSnapshot(
            timestamp=time.time(),
            context_type=self.context_type,
            data=self.current_state.copy(),
            metadata={"event": event_description}
        )
        self.history.append(snapshot)
        
        # Apply changes
        self._deep_update(self.current_state, changes)
        
        # Log event
        if event_description:
            self.event_log.append(f"{time.time()}: {event_description}")
            
        # Keep history manageable
        if len(self.history) > 100:
            self.history = self.history[-50:]  # Keep last 50
    
    def _deep_update(self, target: Dict, source: Dict):
        """Deep update dictionary"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current state (read-only copy)"""
        return json.loads(json.dumps(self.current_state))  # Deep copy
    
    def get_state_summary(self) -> str:
        """Get human-readable state summary for AI prompts"""
        return self._format_state_summary(self.current_state)
    
    @abstractmethod
    def _format_state_summary(self, state: Dict[str, Any]) -> str:
        """Format state for AI consumption"""
        pass
    
    def rollback_to_snapshot(self, snapshot_index: int):
        """Rollback to a previous state snapshot"""
        if 0 <= snapshot_index < len(self.history):
            snapshot = self.history[snapshot_index]
            self.current_state = snapshot.data.copy()
            self.event_log.append(f"{time.time()}: Rolled back to snapshot {snapshot_index}")
    
    def export_state(self) -> Dict[str, Any]:
        """Export complete state for persistence"""
        return {
            "context_type": self.context_type.value,
            "current_state": self.current_state,
            "history": [snap.to_dict() for snap in self.history],
            "event_log": self.event_log
        }
    
    def import_state(self, data: Dict[str, Any]):
        """Import state from persistence"""
        self.context_type = ContextType(data["context_type"])
        self.current_state = data["current_state"]
        self.history = [ContextSnapshot.from_dict(snap) for snap in data["history"]]
        self.event_log = data["event_log"]

class ContextManager:
    """Manages multiple state managers and provides unified interface"""
    
    def __init__(self):
        self.managers: Dict[str, StateManager] = {}
        self.active_context: Optional[str] = None
    
    def register_manager(self, name: str, manager: StateManager):
        """Register a state manager"""
        self.managers[name] = manager
        if self.active_context is None:
            self.active_context = name
    
    def switch_context(self, context_name: str):
        """Switch to a different context"""
        if context_name in self.managers:
            self.active_context = context_name
        else:
            raise ValueError(f"Unknown context: {context_name}")
    
    def get_active_manager(self) -> Optional[StateManager]:
        """Get the currently active state manager"""
        if self.active_context:
            return self.managers.get(self.active_context)
        return None
    
    def get_unified_context(self) -> Dict[str, Any]:
        """Get context from all managers for comprehensive AI prompts"""
        unified = {}
        for name, manager in self.managers.items():
            unified[name] = {
                "state": manager.get_current_state(),
                "summary": manager.get_state_summary(),
                "recent_events": manager.event_log[-5:] if manager.event_log else []
            }
        return unified
    
    def update_active_context(self, changes: Dict[str, Any], event: str = ""):
        """Update the active context"""
        manager = self.get_active_manager()
        if manager:
            manager.update_state(changes, event)
    
    def export_all_contexts(self) -> Dict[str, Any]:
        """Export all contexts for persistence"""
        return {
            name: manager.export_state() 
            for name, manager in self.managers.items()
        }
    
    def import_all_contexts(self, data: Dict[str, Any]):
        """Import all contexts from persistence"""
        for name, context_data in data.items():
            if name in self.managers:
                self.managers[name].import_state(context_data)

# Example implementation for code repositories
class CodeRepositoryStateManager(StateManager):
    """State manager for code repository context"""
    
    def __init__(self):
        super().__init__(ContextType.CODE_REPOSITORY)
        self.current_state = self.initialize_state()
    
    def initialize_state(self) -> Dict[str, Any]:
        return {
            "current_branch": "main",
            "modified_files": [],
            "recent_commits": [],
            "active_features": [],
            "test_status": "unknown",
            "dependencies": {},
            "security_alerts": [],
            "code_patterns": {},
            "team_preferences": {}
        }
    
    def validate_state_change(self, change: Dict[str, Any]) -> bool:
        # Validate that changes make sense for a code repo
        allowed_keys = set(self.current_state.keys())
        return all(key in allowed_keys for key in change.keys())
    
    def _format_state_summary(self, state: Dict[str, Any]) -> str:
        summary_parts = [
            f"Branch: {state['current_branch']}",
            f"Modified files: {len(state['modified_files'])}",
            f"Recent commits: {len(state['recent_commits'])}",
            f"Active features: {len(state['active_features'])}",
            f"Test status: {state['test_status']}"
        ]
        
        if state['security_alerts']:
            summary_parts.append(f"Security alerts: {len(state['security_alerts'])}")
        
        return " | ".join(summary_parts)

# Example implementation for game worlds (from Fire Whisper)
class GameWorldStateManager(StateManager):
    """State manager for game world context (Fire Whisper RPG)"""
    
    def __init__(self):
        super().__init__(ContextType.GAME_WORLD)
        self.current_state = self.initialize_state()
    
    def initialize_state(self) -> Dict[str, Any]:
        return {
            "current_location": "starting_area",
            "visited_locations": [],
            "npcs_met": [],
            "quests_active": [],
            "quests_completed": [],
            "inventory": [],
            "story_flags": {},
            "environmental_conditions": {
                "weather": "clear",
                "time_of_day": "afternoon"
            }
        }
    
    def validate_state_change(self, change: Dict[str, Any]) -> bool:
        # Game-specific validation
        if "current_location" in change:
            # Could validate location exists, is reachable, etc.
            pass
        return True
    
    def _format_state_summary(self, state: Dict[str, Any]) -> str:
        return f"Location: {state['current_location']} | Quests: {len(state['quests_active'])} active | Weather: {state['environmental_conditions']['weather']}"