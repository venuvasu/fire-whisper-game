"""
Narrative Template Engine - Provides structured prompts for AI
Replaces generic AI prompts with specific, context-aware templates
"""
from typing import Dict, List, Any
from .action_result_processor import ActionResult, ActionResultType

class NarrativeTemplateEngine:
    """Generates structured prompts for AI based on action results"""
    
    def __init__(self):
        self.templates = {
            # Defensive Stance Templates
            "defensive_stance_vs_enemies": {
                "scenario": "Player takes defensive stance against enemies",
                "emberlyn_role": "tactical_advisor",
                "focus_elements": [
                    "Observe enemy behavior and weaknesses",
                    "Comment on player's tactical wisdom", 
                    "Point out environmental advantages",
                    "Build tension while being encouraging"
                ],
                "tone": "alert_but_supportive",
                "avoid": ["rushing into action", "making decisions for player"]
            },
            
            "defensive_stance_safe": {
                "scenario": "Player takes defensive stance in safe area",
                "emberlyn_role": "gentle_guide",
                "focus_elements": [
                    "Acknowledge player's caution",
                    "Describe peaceful surroundings",
                    "Offer observations about the area",
                    "Suggest this might be a good time to plan"
                ],
                "tone": "calm_and_reassuring",
                "avoid": ["creating false tension", "implying danger where none exists"]
            },
            
            # Examination Templates
            "examination_reveals_secrets": {
                "scenario": "Player examines area and finds hidden details",
                "emberlyn_role": "magical_interpreter",
                "focus_elements": [
                    "Reveal the hidden details discovered",
                    "Explain magical or historical significance",
                    "Show excitement about the discovery",
                    "Connect findings to current quest or situation"
                ],
                "tone": "excited_and_knowledgeable",
                "avoid": ["revealing too much at once", "making discoveries seem trivial"]
            },
            
            "examination_basic_info": {
                "scenario": "Player examines area with obvious features",
                "emberlyn_role": "observant_companion",
                "focus_elements": [
                    "Describe obvious features in engaging detail",
                    "Add fairy perspective on mundane things",
                    "Point out practical considerations",
                    "Maintain interest in simple observations"
                ],
                "tone": "friendly_and_descriptive",
                "avoid": ["making obvious things seem mysterious", "being dismissive"]
            },
            
            # Emberlyn Guidance Templates
            "emberlyn_quest_guidance": {
                "scenario": "Player asks Emberlyn for quest-related advice",
                "emberlyn_role": "wise_mentor",
                "focus_elements": [
                    "Provide helpful quest hints without spoiling",
                    "Share relevant fairy wisdom or legends",
                    "Encourage player's progress",
                    "Offer magical insights about the situation"
                ],
                "tone": "wise_and_encouraging",
                "avoid": ["giving direct solutions", "being cryptic without purpose"]
            },
            
            "emberlyn_general_advice": {
                "scenario": "Player asks Emberlyn for general guidance",
                "emberlyn_role": "supportive_friend",
                "focus_elements": [
                    "Offer perspective on current situation",
                    "Share general knowledge about the area",
                    "Provide emotional support and encouragement",
                    "Suggest practical next steps"
                ],
                "tone": "warm_and_helpful",
                "avoid": ["being overly directive", "repeating information already known"]
            },
            
            # Observation Templates
            "patient_observation_danger": {
                "scenario": "Player waits and observes in dangerous area",
                "emberlyn_role": "alert_scout",
                "focus_elements": [
                    "Reveal enemy patterns or behaviors",
                    "Point out tactical opportunities",
                    "Build suspense through careful observation",
                    "Reward patience with useful information"
                ],
                "tone": "tense_but_informative",
                "avoid": ["making waiting seem pointless", "rushing the moment"]
            },
            
            "patient_observation_safe": {
                "scenario": "Player waits and observes in safe area",
                "emberlyn_role": "peaceful_companion",
                "focus_elements": [
                    "Describe subtle environmental details",
                    "Share quiet moments of beauty or peace",
                    "Reflect on the journey so far",
                    "Create atmosphere without forcing action"
                ],
                "tone": "serene_and_reflective",
                "avoid": ["creating artificial urgency", "making peace seem boring"]
            },
            
            # Stealth Templates
            "stealth_vs_targets": {
                "scenario": "Player uses stealth approach against enemies/targets",
                "emberlyn_role": "stealth_coordinator",
                "focus_elements": [
                    "Describe stealthy movement techniques",
                    "Comment on target awareness levels",
                    "Build tension through near-discovery moments",
                    "Highlight advantages gained through stealth"
                ],
                "tone": "whispered_and_tense",
                "avoid": ["being too loud in description", "making stealth seem easy"]
            },
            
            "stealth_exploration": {
                "scenario": "Player uses stealth to explore area",
                "emberlyn_role": "quiet_guide",
                "focus_elements": [
                    "Describe careful, quiet movement",
                    "Reveal details only visible through careful approach",
                    "Create atmosphere of discovery",
                    "Show benefits of taking time to be careful"
                ],
                "tone": "hushed_and_curious",
                "avoid": ["making noise in descriptions", "rushing the exploration"]
            },
            
            # Combat Preparation
            "combat_preparation": {
                "scenario": "Player prepares for potential combat",
                "emberlyn_role": "battle_advisor",
                "focus_elements": [
                    "Assess combat readiness",
                    "Point out tactical considerations",
                    "Offer magical support or insights",
                    "Build appropriate tension for coming conflict"
                ],
                "tone": "focused_and_supportive",
                "avoid": ["starting combat prematurely", "being overly dramatic"]
            },
            
            # General fallback
            "general_action_response": {
                "scenario": "Player takes an unusual or unrecognized action",
                "emberlyn_role": "adaptive_companion",
                "focus_elements": [
                    "Acknowledge player's creative approach",
                    "Describe how the action affects the situation",
                    "Maintain story continuity",
                    "Offer gentle guidance if needed"
                ],
                "tone": "flexible_and_encouraging",
                "avoid": ["dismissing creative actions", "breaking character"]
            }
        }
    
    def generate_ai_prompt(self, action_result: ActionResult, prompt_data: Dict[str, Any]) -> str:
        """Generate a structured AI prompt based on action result"""
        
        template_key = action_result.description_template
        template = self.templates.get(template_key, self.templates["general_action_response"])
        
        # Build the structured prompt
        prompt = f"""You are Emberlyn, the fairy companion in Fire Whisper RPG.

NARRATIVE TASK: {template['scenario']}
YOUR ROLE: {template['emberlyn_role']}

CURRENT CONTEXT:
Location: {prompt_data['location_context']['name']} ({prompt_data['location_context']['type']})
Setting: {prompt_data['location_context']['description']}
Environmental Features: {', '.join(prompt_data['location_context']['features'])}

SITUATION:
Enemies Present: {', '.join(prompt_data['situation_context']['enemies']) if prompt_data['situation_context']['enemies'] else 'None'}
NPCs Present: {', '.join(prompt_data['situation_context']['npcs']) if prompt_data['situation_context']['npcs'] else 'None'}
Items Available: {', '.join(prompt_data['situation_context']['items']) if prompt_data['situation_context']['items'] else 'None'}
Safe Zone: {prompt_data['situation_context']['safe_zone']}

ACTION RESULT:
Type: {action_result.result_type.value}
Success: {action_result.success}
Mechanical Effects: {action_result.mechanical_effects}

RECENT CONTEXT:
Recent Events: {', '.join(prompt_data['story_context']['recent_events'][-3:]) if prompt_data['story_context']['recent_events'] else 'None'}
Active Quests: {', '.join(prompt_data['story_context']['active_quests']) if prompt_data['story_context']['active_quests'] else 'None'}
Time: {prompt_data['story_context']['time']} | Weather: {prompt_data['story_context']['weather']}

NARRATIVE FOCUS POINTS:
{chr(10).join(f"- {point}" for point in template['focus_elements'])}

TONE: {template['tone']}

AVOID:
{chr(10).join(f"- {avoid_point}" for avoid_point in template['avoid'])}

CRITICAL CONSTRAINTS:
- NEVER describe dice rolls, XP calculations, or mechanical processes
- NEVER use commanding phrases like 'you must', 'you decide to', 'you automatically'
- NEVER mention game mechanics directly
- WAIT for player input - do not assume their next actions
- Use phrases like 'Emberlyn suggests', 'you could', 'perhaps', 'you might consider'
- Focus ONLY on story, dialogue, and atmosphere
- DO NOT include action choices or options in your response
- End your response with narrative only, no player choices
- MAINTAIN STORY CONTINUITY - build on the current situation
- RESPOND SPECIFICALLY to the action taken, don't give generic responses

Generate Emberlyn's response now:"""
        
        return prompt
    
    def get_template_info(self, template_key: str) -> Dict[str, Any]:
        """Get information about a specific template"""
        return self.templates.get(template_key, {})
    
    def list_available_templates(self) -> List[str]:
        """List all available narrative templates"""
        return list(self.templates.keys())
    
    def add_custom_template(self, key: str, template: Dict[str, Any]):
        """Add a custom narrative template"""
        required_fields = ["scenario", "emberlyn_role", "focus_elements", "tone", "avoid"]
        
        if all(field in template for field in required_fields):
            self.templates[key] = template
        else:
            raise ValueError(f"Template must include: {required_fields}")
    
    def get_contextual_suggestions(self, action_result: ActionResult, context: Dict) -> List[str]:
        """Get suggestions for what the narrative should emphasize"""
        
        suggestions = []
        
        # Based on action result type
        if action_result.result_type == ActionResultType.TACTICAL_ADVANTAGE:
            suggestions.append("Emphasize strategic benefits gained")
            suggestions.append("Describe enemy reactions or weaknesses revealed")
        
        elif action_result.result_type == ActionResultType.INVESTIGATION:
            suggestions.append("Focus on details discovered")
            suggestions.append("Connect findings to larger story elements")
        
        elif action_result.result_type == ActionResultType.QUEST_PROGRESSION:
            suggestions.append("Advance quest narrative meaningfully")
            suggestions.append("Provide helpful guidance without spoiling")
        
        # Based on context
        if context.get("enemies_present"):
            suggestions.append("Maintain appropriate tension level")
            suggestions.append("Include enemy behavioral details")
        
        if context.get("safe_zone"):
            suggestions.append("Create peaceful, restorative atmosphere")
            suggestions.append("Allow for planning and reflection")
        
        return suggestions