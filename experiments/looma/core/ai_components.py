"""
AI Components for Dynamic System
Real AI implementations using Claude API for the dynamic component swapper.
"""

import os
from anthropic import Anthropic
from typing import Dict, Any, List, Tuple
import random

def get_api_key():
    """Get API key from environment or .env.local"""
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
    
    return api_key

class RealAI_NPCRelationshipManager:
    """Real AI-powered NPC relationship management using Claude"""
    
    def __init__(self):
        self.client = Anthropic(api_key=get_api_key())
        self.npc_personalities = {}
        self.relationship_history = {}
        
    def update_relationship(self, npc_id: str, player_action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """AI analyzes player action and updates relationship dynamically"""
        
        # Initialize NPC if new
        if npc_id not in self.npc_personalities:
            self.npc_personalities[npc_id] = self._generate_ai_personality(npc_id, context)
        
        if npc_id not in self.relationship_history:
            self.relationship_history[npc_id] = {
                "interactions": [],
                "trust": 0.5,
                "affection": 0.5,
                "respect": 0.5,
                "fear": 0.0,
                "shared_experiences": []
            }
        
        # Use AI to analyze the action impact
        personality = self.npc_personalities[npc_id]
        current_relationship = self.relationship_history[npc_id]
        
        # AI prompt for relationship analysis
        prompt = f"""
You are analyzing how a player action affects an NPC relationship.

NPC: {npc_id}
NPC Personality: {personality}
Player Action: {player_action}
Context: {context}
Current Relationship: Trust={current_relationship['trust']:.2f}, Affection={current_relationship['affection']:.2f}, Respect={current_relationship['respect']:.2f}, Fear={current_relationship['fear']:.2f}

Analyze how this action would realistically affect each relationship aspect. Consider:
1. The NPC's personality and values
2. The context of the situation
3. The current relationship state
4. Realistic human psychology

Respond with ONLY a JSON object containing the changes (can be positive or negative):
{{"trust": 0.0, "affection": 0.0, "respect": 0.0, "fear": 0.0}}

Changes should be between -0.3 and +0.3 for realistic relationship progression.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse AI response
            import json
            changes = json.loads(response.content[0].text.strip())
            
            # Apply changes
            for aspect, change in changes.items():
                if aspect in current_relationship:
                    current_relationship[aspect] = max(0.0, min(1.0, current_relationship[aspect] + change))
            
        except Exception as e:
            print(f"AI relationship analysis failed: {e}")
            # Fallback to simple rules
            if player_action in ["help", "assist", "compliment"]:
                current_relationship["trust"] += 0.1
                current_relationship["affection"] += 0.1
            elif player_action in ["attack", "insult", "threaten"]:
                current_relationship["fear"] += 0.2
                current_relationship["trust"] -= 0.2
        
        # Add to interaction history
        current_relationship["interactions"].append({
            "action": player_action,
            "context": context,
            "timestamp": "now"
        })
        
        return current_relationship
    
    def get_npc_response(self, npc_id: str, player_input: str, history: List[Dict]) -> str:
        """Generate contextual, personality-driven NPC response using AI"""
        
        if npc_id not in self.npc_personalities:
            return "The NPC looks at you with uncertainty."
        
        personality = self.npc_personalities[npc_id]
        relationship = self.relationship_history.get(npc_id, {})
        
        # AI prompt for NPC response
        prompt = f"""
You are roleplaying as an NPC in a fantasy RPG game.

NPC: {npc_id}
Personality: {personality}
Relationship with Player: Trust={relationship.get('trust', 0.5):.2f}, Affection={relationship.get('affection', 0.5):.2f}, Respect={relationship.get('respect', 0.5):.2f}, Fear={relationship.get('fear', 0.0):.2f}
Recent Interactions: {relationship.get('interactions', [])[-3:]}

Player says: "{player_input}"

Respond as this NPC would, considering:
1. Their personality and background
2. Their current relationship with the player
3. The context of recent interactions
4. Realistic dialogue for a fantasy setting

Keep the response to 1-2 sentences, natural and in-character.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"AI NPC response failed: {e}")
            # Fallback response
            trust = relationship.get('trust', 0.5)
            if trust > 0.7:
                return f"*{npc_id} smiles warmly* I'm glad to see you again, friend."
            elif trust < 0.3:
                return f"*{npc_id} eyes you warily* What do you want?"
            else:
                return f"*{npc_id} nods politely* How can I help you?"
    
    def calculate_relationship_score(self, npc_id: str) -> float:
        """Calculate overall relationship quality"""
        
        if npc_id not in self.relationship_history:
            return 0.0
        
        rel = self.relationship_history[npc_id]
        
        # AI can create much deeper relationships than code
        base_score = (rel.get("trust", 0) + rel.get("affection", 0) + rel.get("respect", 0)) / 3
        
        # Bonus for interaction depth
        interaction_bonus = min(0.3, len(rel.get("interactions", [])) * 0.05)
        
        # Penalty for fear
        fear_penalty = rel.get("fear", 0) * 0.3
        
        final_score = base_score + interaction_bonus - fear_penalty
        return max(0.0, min(1.0, final_score))
    
    def _generate_ai_personality(self, npc_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate rich NPC personality using AI"""
        
        prompt = f"""
Create a detailed personality profile for an NPC in a fantasy RPG.

NPC ID: {npc_id}
Context: {context}

Generate a realistic personality with:
1. 3-4 key personality traits
2. 2-3 core values they hold dear
3. 2-3 fears or concerns
4. 2-3 desires or goals
5. Speech patterns/mannerisms

Respond with a JSON object:
{{
  "traits": ["trait1", "trait2", "trait3"],
  "values": ["value1", "value2"],
  "fears": ["fear1", "fear2"],
  "desires": ["desire1", "desire2"],
  "speech_patterns": ["pattern1", "pattern2"]
}}
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            import json
            return json.loads(response.content[0].text.strip())
            
        except Exception as e:
            print(f"AI personality generation failed: {e}")
            # Fallback personality
            return {
                "traits": ["friendly", "helpful", "cautious"],
                "values": ["honesty", "community"],
                "fears": ["conflict", "change"],
                "desires": ["peace", "prosperity"],
                "speech_patterns": ["polite", "thoughtful"]
            }

class RealAI_NarrativeGenerator:
    """Real AI-powered narrative generation using Claude"""
    
    def __init__(self):
        self.client = Anthropic(api_key=get_api_key())
        
    def generate_scene_description(self, context: Dict[str, Any]) -> str:
        """AI creates rich, contextual scene descriptions"""
        
        prompt = f"""
Create a vivid scene description for a fantasy RPG game.

Context: {context}

Write a 2-3 sentence description that:
1. Sets the atmosphere and mood
2. Includes sensory details (sight, sound, smell)
3. Reflects the current context and recent events
4. Maintains immersion in a fantasy setting

Be descriptive but concise, focusing on what the player would notice.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"AI scene description failed: {e}")
            location = context.get("location", "unknown place")
            time = context.get("time", "day")
            return f"You find yourself in {location} during {time}. The atmosphere is calm and peaceful."
    
    def generate_dialogue(self, character: str, emotion: str, context: Dict[str, Any]) -> str:
        """AI generates emotionally appropriate dialogue"""
        
        prompt = f"""
Generate dialogue for a character in a fantasy RPG.

Character: {character}
Emotion: {emotion}
Context: {context}

Create 1-2 sentences of dialogue that:
1. Reflects the character's emotional state
2. Fits their personality and background
3. Responds appropriately to the context
4. Uses natural, fantasy-appropriate language

Include brief action/expression in *asterisks* if appropriate.
"""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"AI dialogue generation failed: {e}")
            return f"*{character} looks {emotion}* I have much on my mind right now."
    
    def adapt_narrative_tone(self, player_preferences: Dict[str, Any]) -> None:
        """AI adapts narrative style to player preferences"""
        # This would modify internal parameters based on player feedback
        # For now, just acknowledge the preferences
        pass