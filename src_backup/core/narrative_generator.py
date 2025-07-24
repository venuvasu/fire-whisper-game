"""
Narrative Generator - AI handles ONLY creative writing
Code provides all context, AI just writes the story
"""
from typing import Dict, List, Any
from anthropic import Anthropic
import os

class NarrativeGenerator:
    """Pure AI narrative generation - no game logic"""
    
    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv('CLAUDE_API_KEY')
            if not api_key:
                # Load from .env.local for local testing
                try:
                    with open('.env.local', 'r') as f:
                        for line in f:
                            if line.startswith('CLAUDE_API_KEY='):
                                api_key = line.split('=', 1)[1].strip()
                                break
                except FileNotFoundError:
                    pass
                
                if not api_key:
                    raise ValueError("CLAUDE_API_KEY not found in environment or .env.local")
        
        self.client = Anthropic(api_key=api_key)
    
    def generate_narrative(self, action_result, game_context: Dict[str, Any]) -> str:
        """Generate narrative response based on code-determined results"""
        
        # Build structured prompt with all context provided by code
        prompt = self._build_narrative_prompt(action_result, game_context)
        
        # Get AI response
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"*Emberlyn flutters uncertainly* Something seems amiss with the magical energies... ({str(e)})"
    
    def _build_narrative_prompt(self, action_result, game_context: Dict[str, Any]) -> str:
        """Build structured prompt for AI - all context provided by code"""
        
        location = game_context["location"]
        situation = game_context["situation"]
        immediate = game_context["immediate_context"]
        
        prompt = f"""You are Emberlyn, the fairy companion in Fire Whisper RPG.

CRITICAL: You are ONLY responsible for creative writing. All game logic, state, and mechanics are handled by code.

CURRENT SITUATION (determined by code):
Location: {location['name']} - {location['description']}
Current Situation: {situation['current_situation']}
Mood/Atmosphere: {situation['mood']}
Turn: {game_context['game_state']['turn']}

ACTION RESULT (determined by code):
Action Type: {action_result.action_type.value}
Success: {action_result.success}
Description: {action_result.description}
Discoveries: {', '.join(action_result.discoveries) if action_result.discoveries else 'None'}

IMMEDIATE CONTEXT (determined by code):
Enemies Present: {', '.join(immediate['enemies_present']) if immediate['enemies_present'] else 'None'}
NPCs Present: {', '.join(immediate['npcs_present']) if immediate['npcs_present'] else 'None'}
Items Available: {', '.join(immediate['items_available']) if immediate['items_available'] else 'None'}
Special Features: {', '.join(immediate['special_features']) if immediate['special_features'] else 'None'}

NARRATIVE FOCUS (determined by code):
Focus on: {', '.join(action_result.narrative_focus)}

YOUR ROLE:
- Write Emberlyn's response to the action result
- Focus on the specified narrative elements
- Bring the scene to life with creative descriptions
- Show Emberlyn's personality and fairy perspective
- DO NOT make up game mechanics, stats, or dice rolls
- DO NOT decide what happens next - just describe what happened
- DO NOT create new story elements not provided in context

CONSTRAINTS:
- Write 2-4 paragraphs maximum
- Stay in character as Emberlyn
- Use the discoveries and context provided
- Focus on atmosphere and character interaction
- End with Emberlyn's reaction/commentary, not player choices

Generate Emberlyn's narrative response now:"""
        
        return prompt
    
    def generate_game_start_narrative(self, game_context: Dict[str, Any]) -> str:
        """Generate opening narrative for new game"""
        
        location = game_context["location"]
        
        prompt = f"""You are Emberlyn, the fairy companion in Fire Whisper RPG.

GAME START SCENARIO:
You are meeting the player character (a warrior) for the first time at {location['name']}.
Location: {location['description']}

YOUR ROLE:
- Introduce yourself as Emberlyn, a fire fairy companion
- Establish the initial setting and atmosphere
- Hint at the adventure ahead (finding Fire Essence crystal to restore Sacred Flame)
- Show your fairy personality - helpful, magical, slightly mischievous
- Create intrigue about the current location

CONSTRAINTS:
- Write 3-4 paragraphs
- Focus on character introduction and world-building
- DO NOT provide player choices (code handles that)
- DO NOT mention game mechanics
- End with setting up the current situation

Generate the opening narrative:"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"*A small fairy appears before you* Hello, brave warrior! I'm Emberlyn, and I'll be your guide. ({str(e)})"