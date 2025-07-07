"""
Amplitude Analytics Handler for Fire Whisper RPG
Handles sending events to Amplitude for game analytics
"""
import os
import json
from datetime import datetime

def send_bedrock_amplitude_event(user_id, event_name, model_name, response, additional_data=None):
    """
    Send analytics event to Amplitude
    
    Args:
        user_id: User identifier
        event_name: Name of the event (e.g., "create_character", "create_saga")
        model_name: AI model used (e.g., "claude_haiku_35")
        response: AI response data
        additional_data: Additional event properties
    """
    try:
        # For console/local development, just log the event
        if os.getenv("DEPLOYMENT_MODE", "local") == "local":
            print(f"📊 Analytics Event: {event_name}")
            print(f"   User: {user_id}")
            print(f"   Model: {model_name}")
            if additional_data:
                print(f"   Data: {additional_data}")
            return
        
        # In production, you would send to actual Amplitude API
        # For now, we'll just log it
        event_data = {
            "user_id": user_id,
            "event_type": event_name,
            "event_properties": {
                "model_name": model_name,
                "timestamp": datetime.now().isoformat(),
                **(additional_data or {})
            }
        }
        
        # TODO: Implement actual Amplitude API call for production
        print(f"📊 Would send to Amplitude: {json.dumps(event_data, indent=2)}")
        
    except Exception as e:
        # Don't let analytics failures break the game
        print(f"⚠️  Analytics error (non-critical): {e}")
        pass