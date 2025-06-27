#!/usr/bin/env python3
"""
Version Management System for AI-Integrated Projects
Handles MAJOR.MINOR.PROMPT.UI versioning scheme
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class VersionManager:
    def __init__(self, version_file: str = "version.json"):
        self.version_file = version_file
        self.version_data = self._load_version()
    
    def _load_version(self) -> Dict:
        """Load version data from JSON file"""
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r') as f:
                return json.load(f)
        else:
            return self._create_initial_version()
    
    def _create_initial_version(self) -> Dict:
        """Create initial version structure"""
        return {
            "version": "1.0.0.0",
            "major": 1,
            "minor": 0,
            "prompt": 0,
            "ui": 0,
            "last_updated": datetime.now().isoformat(),
            "changelog": {}
        }
    
    def _save_version(self):
        """Save version data to JSON file"""
        with open(self.version_file, 'w') as f:
            json.dump(self.version_data, f, indent=2)
    
    def get_current_version(self) -> str:
        """Get current version string"""
        return self.version_data["version"]
    
    def get_version_components(self) -> Dict[str, int]:
        """Get version components as dict"""
        return {
            "major": self.version_data["major"],
            "minor": self.version_data["minor"], 
            "prompt": self.version_data["prompt"],
            "ui": self.version_data["ui"]
        }
    
    def bump_major(self, changes: List[str], breaking_changes: List[str] = None):
        """Bump major version (breaking architectural changes)"""
        self.version_data["major"] += 1
        self.version_data["minor"] = 0
        self.version_data["prompt"] = 0
        self.version_data["ui"] = 0
        self._update_version_string()
        self._add_changelog_entry(changes, breaking_changes or [], [], [])
    
    def bump_minor(self, changes: List[str], prompt_changes: List[str] = None):
        """Bump minor version (new features, backward compatible)"""
        self.version_data["minor"] += 1
        self.version_data["prompt"] = 0
        self.version_data["ui"] = 0
        self._update_version_string()
        self._add_changelog_entry(changes, [], prompt_changes or [], [])
    
    def bump_prompt(self, changes: List[str], prompt_changes: List[str]):
        """Bump prompt version (AI behavior changes)"""
        self.version_data["prompt"] += 1
        self._update_version_string()
        self._add_changelog_entry(changes, [], prompt_changes, [])
    
    def bump_ui(self, changes: List[str], ui_changes: List[str]):
        """Bump UI version (frontend/UX changes only)"""
        self.version_data["ui"] += 1
        self._update_version_string()
        self._add_changelog_entry(changes, [], [], ui_changes)
    
    def _update_version_string(self):
        """Update the version string from components"""
        self.version_data["version"] = f"{self.version_data['major']}.{self.version_data['minor']}.{self.version_data['prompt']}.{self.version_data['ui']}"
        self.version_data["last_updated"] = datetime.now().isoformat()
    
    def _add_changelog_entry(self, changes: List[str], breaking_changes: List[str], 
                           prompt_changes: List[str], ui_changes: List[str]):
        """Add entry to changelog"""
        version = self.version_data["version"]
        self.version_data["changelog"][version] = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "changes": changes,
            "breaking_changes": breaking_changes,
            "prompt_changes": prompt_changes,
            "ui_changes": ui_changes
        }
        self._save_version()
    
    def get_changelog(self, limit: Optional[int] = None) -> Dict:
        """Get changelog entries"""
        changelog = self.version_data["changelog"]
        if limit:
            # Get last N entries
            items = list(changelog.items())[-limit:]
            return dict(items)
        return changelog
    
    def print_version_info(self):
        """Print current version information"""
        print(f"🏷️  Current Version: {self.get_current_version()}")
        print(f"📅 Last Updated: {self.version_data['last_updated']}")
        
        components = self.get_version_components()
        print(f"📊 Components: Major={components['major']}, Minor={components['minor']}, Prompt={components['prompt']}, UI={components['ui']}")

if __name__ == "__main__":
    import sys
    
    vm = VersionManager()
    
    if len(sys.argv) < 2:
        vm.print_version_info()
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "info":
        vm.print_version_info()
    elif command == "bump-major":
        changes = sys.argv[2:] if len(sys.argv) > 2 else ["Major version bump"]
        vm.bump_major(changes)
        print(f"✅ Bumped to version {vm.get_current_version()}")
    elif command == "bump-minor":
        changes = sys.argv[2:] if len(sys.argv) > 2 else ["Minor version bump"]
        vm.bump_minor(changes)
        print(f"✅ Bumped to version {vm.get_current_version()}")
    elif command == "bump-prompt":
        changes = sys.argv[2:] if len(sys.argv) > 2 else ["Prompt changes"]
        vm.bump_prompt(changes, changes)
        print(f"✅ Bumped to version {vm.get_current_version()}")
    elif command == "bump-ui":
        changes = sys.argv[2:] if len(sys.argv) > 2 else ["UI changes"]
        vm.bump_ui(changes, changes)
        print(f"✅ Bumped to version {vm.get_current_version()}")
    else:
        print("Usage: python version_manager.py [info|bump-major|bump-minor|bump-prompt|bump-ui] [change description]")