"""
AI Providers Module
Handles all AI model integrations for Fire Whisper RPG
"""

from .mistral import take_turn as take_turn_mistral
from .claude_haiku_take_turn import take_turn
from .claude_direct_api import take_turn_direct

__all__ = [
    'take_turn_mistral',
    'take_turn', 
    'take_turn_direct'
]