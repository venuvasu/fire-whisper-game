#!/usr/bin/env python3
"""
Show implementation status - Quick way to view current implementation status
"""
import yaml
import os
import sys
from datetime import datetime

def load_status():
    """Load the implementation status from YAML file"""
    try:
        with open("implementation_status.yaml", "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Error loading implementation status: {e}")
        return None

def display_status(status):
    """Display the implementation status in a readable format"""
    if not status:
        return
    
    print("\n" + "="*60)
    print(f"🔥 FIRE WHISPER RPG - IMPLEMENTATION STATUS")
    print("="*60)
    
    # Basic info
    print(f"Version: {status.get('version', 'Unknown')}")
    print(f"Last Updated: {status.get('last_updated', 'Unknown')}")
    print(f"Overall Progress: {status.get('overall_progress', 0)}%")
    print(f"Current Task: {status.get('current_task', 'None specified')}")
    
    # Features
    print("\n" + "-"*60)
    print("FEATURES")
    print("-"*60)
    
    # Completed features
    if status.get('completed_features'):
        print("\n✅ COMPLETED FEATURES:")
        for feature in status['completed_features']:
            print(f"  • {feature['name']} - {feature.get('notes', '')}")
    
    # In progress features
    if status.get('in_progress_features'):
        print("\n🔄 IN PROGRESS FEATURES:")
        for feature in status['in_progress_features']:
            print(f"  • {feature['name']} ({feature.get('progress', 0)}%) - {feature.get('notes', '')}")
            if feature.get('next_steps'):
                for step in feature['next_steps']:
                    print(f"    ◦ {step}")
    
    # Pending features
    if status.get('pending_features'):
        print("\n⏳ PENDING FEATURES:")
        for feature in status['pending_features']:
            print(f"  • {feature['name']} - {feature.get('notes', '')}")
    
    # Modified files
    if status.get('modified_files'):
        print("\n" + "-"*60)
        print("MODIFIED FILES")
        print("-"*60)
        for file in status['modified_files']:
            print(f"  • {file['path']} - {file['status']}")
            if file.get('changes'):
                print(f"    {file['changes']}")
    
    # Next session tasks
    if status.get('next_session_tasks'):
        print("\n" + "-"*60)
        print("NEXT SESSION TASKS")
        print("-"*60)
        for i, task in enumerate(status['next_session_tasks'], 1):
            print(f"  {i}. {task}")
    
    # Context notes
    if status.get('context_notes'):
        print("\n" + "-"*60)
        print("CONTEXT NOTES")
        print("-"*60)
        for note in status['context_notes']:
            print(f"  • {note}")
    
    print("\n" + "="*60)

def main():
    """Main function"""
    status = load_status()
    if status:
        display_status(status)
    else:
        print("❌ Could not load implementation status")
        sys.exit(1)

if __name__ == "__main__":
    main()