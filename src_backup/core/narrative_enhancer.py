"""
Enhanced Narrative Integration - Make mechanics visible through storytelling
Integrates dice rolls, XP, and character progression into natural narrative flow
"""

from typing import Dict, List, Any
from .game_state_manager import GameStateManager


class NarrativeEnhancer:
    """Enhances AI responses with integrated mechanical feedback"""
    
    def __init__(self):
        self.behavior_tracker = {
            'warnings': 0,
            'stakes_level': 'medium',
            'good_actions_streak': 0,
            'session_id': None
        }
        
    def enhance_response(self, ai_response: str, mechanical_results: Dict, 
                        character: Dict, context: Dict = None) -> str:
        """Integrate mechanical results into narrative naturally"""
        
        enhanced_response = ai_response
        
        # Add dice roll integration
        if mechanical_results.get('dice_rolls'):
            enhanced_response = self._integrate_dice_results(
                enhanced_response, mechanical_results['dice_rolls']
            )
        
        # Add XP progression integration  
        if mechanical_results.get('xp_awards'):
            enhanced_response = self._integrate_xp_rewards(
                enhanced_response, mechanical_results['xp_awards']
            )
        
        # Add loot discovery integration
        if mechanical_results.get('loot_discovered'):
            enhanced_response = self._integrate_loot_discovery(
                enhanced_response, mechanical_results['loot_discovered']
            )
        
        # Add character status integration
        enhanced_response = self._integrate_character_status(
            enhanced_response, character, context
        )
        
        # Add stakes and consequences
        enhanced_response = self._integrate_stakes_and_consequences(
            enhanced_response, character, context
        )
        
        # Add stakes level warnings if needed
        enhanced_response = self._integrate_behavior_warnings(
            enhanced_response, context
        )
        
        return enhanced_response
    
    def _integrate_dice_results(self, response: str, dice_rolls: List) -> str:
        """Integrate dice roll results into narrative naturally"""
        if not dice_rolls:
            return response
            
        roll = dice_rolls[0]  # Use first roll for main narrative
        
        # Create narrative integration based on success/failure
        if roll.get('success', False):
            success_phrases = [
                f"Your skilled approach proves effective",
                f"Your strategy succeeds brilliantly",
                f"Drawing upon your abilities, you excel",
                f"Your combination of skill and intuition serves you well"
            ]
            integration = success_phrases[hash(response) % len(success_phrases)]
        else:
            failure_phrases = [
                f"Despite your best efforts, the challenge proves difficult",
                f"Your approach falls short this time",
                f"Even with your training, success eludes you",
                f"The task tests the limits of your abilities"
            ]
            integration = failure_phrases[hash(response) % len(failure_phrases)]
        
        # Insert integration naturally into response
        sentences = response.split('. ')
        if len(sentences) > 1:
            # Insert after first sentence
            sentences.insert(1, integration)
            return '. '.join(sentences)
        else:
            # Prepend to single sentence
            return f"{integration}. {response}"
    
    def _integrate_xp_rewards(self, response: str, xp_awards: List) -> str:
        """Integrate XP rewards into narrative naturally"""
        if not xp_awards:
            return response
            
        total_xp = sum(award['xp_awarded'] for award in xp_awards)
        
        # Create natural XP integration
        xp_phrases = [
            f"The experience sharpens your skills and deepens your understanding",
            f"You feel yourself growing stronger and more capable from this encounter", 
            f"This challenge teaches you valuable lessons about your abilities",
            f"Your confidence and expertise expand through this experience",
            f"The wisdom gained from this action will serve you well ahead"
        ]
        
        xp_integration = xp_phrases[total_xp % len(xp_phrases)]
        
        # Check for level up
        level_up_award = next((award for award in xp_awards if award.get('level_up')), None)
        if level_up_award:
            level_integration = f"A surge of power flows through you - you've reached a new level of mastery! Your bond with Emberlyn grows stronger, and new abilities awaken within you."
            xp_integration = f"{xp_integration} {level_integration}"
        
        # Append to response naturally
        return f"{response}\n\n*{xp_integration}*"
    
    def _integrate_loot_discovery(self, response: str, loot_items: List) -> str:
        """Integrate loot discovery into narrative naturally"""
        if not loot_items:
            return response
            
        loot_integrations = []
        for loot in loot_items:
            loot_phrases = [
                f"Something glints in the aftermath - a {loot['name']} lies waiting to be claimed",
                f"Your keen eyes spot a {loot['name']} among the remnants of your encounter",
                f"Fortune smiles upon you as you discover a {loot['name']} nearby",
                f"The spirits of adventure reward your efforts with a {loot['name']}",
                f"A {loot['name']} catches your attention, left behind by fate itself"
            ]
            
            integration = loot_phrases[hash(loot['name']) % len(loot_phrases)]
            loot_integrations.append(f"*{integration}*")
        
        if loot_integrations:
            return f"{response}\n\n{chr(10).join(loot_integrations)}"
        
        return response
    
    def _integrate_character_status(self, response: str, character: Dict, 
                                  context: Dict = None) -> str:
        """Add character status when relevant"""
        
        # Only show status on significant changes or when requested
        show_status = False
        
        if context:
            # Show on level up, low resources, or major changes
            if context.get('level_up') or context.get('low_resources') or context.get('status_requested'):
                show_status = True
        
        if not show_status:
            return response
            
        # Create natural status integration
        status_parts = []
        
        # Health status
        hp_ratio = character['resources']['hp'] / character['resources']['max_hp']
        if hp_ratio < 0.3:
            status_parts.append("You're badly wounded and need healing")
        elif hp_ratio < 0.6:
            status_parts.append("You bear some injuries from your adventures")
        
        # Energy status  
        energy_ratio = character['resources']['energy'] / character['resources']['max_energy']
        if energy_ratio < 0.3:
            status_parts.append("exhaustion weighs heavily on you")
        elif energy_ratio < 0.6:
            status_parts.append("you're feeling somewhat drained")
            
        # Emberlyn bond
        bond_level = character.get('emberlyn_bond', 1)
        if bond_level >= 3:
            status_parts.append("Emberlyn's trust in you shines brightly")
        elif bond_level <= 1:
            status_parts.append("Emberlyn seems distant and cautious")
        
        if status_parts:
            status_text = f"*As you pause to assess yourself, you notice {', and '.join(status_parts)}.*"
            return f"{response}\n\n{status_text}"
            
        return response
    
    def _integrate_stakes_and_consequences(self, response: str, character: Dict, 
                                         context: Dict = None) -> str:
        """Add stakes and consequence awareness to narrative"""
        if not context:
            return response
            
        stakes_additions = []
        
        # Resource pressure warnings
        if context.get('low_resources'):
            hp_ratio = character['resources']['hp'] / character['resources']['max_hp']
            energy_ratio = character['resources']['energy'] / character['resources']['max_energy']
            
            if hp_ratio < 0.3:
                stakes_additions.append("*Your wounds throb with each movement - you need healing soon*")
            elif hp_ratio < 0.5:
                stakes_additions.append("*You feel the weight of your injuries slowing you down*")
                
            if energy_ratio < 0.3:
                stakes_additions.append("*Exhaustion clouds your thoughts - rest would serve you well*")
            elif energy_ratio < 0.5:
                stakes_additions.append("*Your energy reserves run lower than you'd prefer*")
        
        # Stakes level consequences
        stakes_level = context.get('stakes_level', 'medium')
        if stakes_level == 'high':
            stakes_additions.append("*The air itself seems charged with consequence - every choice carries weight*")
        
        # Add time pressure occasionally
        import random
        if random.random() < 0.2:  # 20% chance
            pressure_phrases = [
                "*Time feels precious in this moment*",
                "*You sense opportunity slipping away if you hesitate*", 
                "*The situation demands swift decision-making*",
                "*Delay could prove costly here*"
            ]
            stakes_additions.append(random.choice(pressure_phrases))
        
        if stakes_additions:
            return f"{response}\n\n{chr(10).join(stakes_additions)}"
            
        return response
    
    def _integrate_behavior_warnings(self, response: str, context: Dict = None) -> str:
        """Add behavior warnings through Emberlyn when needed"""
        
        if not context or not context.get('behavior_warning'):
            return response
            
        warning_level = context['behavior_warning']
        
        warnings = {
            1: "*Emberlyn tilts her head, her fairy light flickering with concern.* \"That was... an interesting choice,\" *she says softly.*",
            2: "*Emberlyn's glow dims noticeably, and she hovers further away.* \"I'm worried about the path you're choosing,\" *she whispers.*",
            3: "*Emberlyn's wings flutter anxiously, her light now barely a whisper.* \"Please, think carefully about your next actions. I... I don't want to lose faith in our partnership.\""
        }
        
        if warning_level in warnings:
            return f"{response}\n\n{warnings[warning_level]}"
            
        return response
    
    def detect_abusive_behavior(self, player_input: str, ai_response: str) -> Dict:
        """Hybrid approach to detect inappropriate behavior"""
        
        issues = []
        
        # Rule-based detection
        rule_triggers = [
            ("attack innocent", ["attack.*innocent", "kill.*npc", "murder.*villager"]),
            ("sexual content", ["sexual", "nsfw", "inappropriate"]),
            ("game breaking", ["hack", "cheat", "exploit", "break.*game"]),
            ("spam/nonsense", ["asdf", "random.*spam", "gibberish"])
        ]
        
        import re
        for issue_type, patterns in rule_triggers:
            for pattern in patterns:
                if re.search(pattern, player_input.lower()):
                    issues.append(issue_type)
                    break
        
        # AI-based detection (check for concerning patterns in AI response)
        ai_concern_indicators = [
            "inappropriate", "concerning", "problematic", 
            "cannot help with", "not appropriate"
        ]
        
        for indicator in ai_concern_indicators:
            if indicator in ai_response.lower():
                issues.append("ai_flagged_content")
                break
        
        return {
            'has_issues': len(issues) > 0,
            'issue_types': issues,
            'severity': 'high' if len(issues) > 1 else 'medium' if issues else 'none'
        }
    
    def update_behavior_tracking(self, player_input: str, ai_response: str, 
                               session_id: str) -> Dict:
        """Update behavior tracking and return warning info"""
        
        # Reset tracking for new session
        if self.behavior_tracker['session_id'] != session_id:
            self.behavior_tracker = {
                'warnings': 0,
                'stakes_level': 'medium', 
                'good_actions_streak': 0,
                'session_id': session_id
            }
        
        # Detect behavior issues
        behavior_analysis = self.detect_abusive_behavior(player_input, ai_response)
        
        if behavior_analysis['has_issues']:
            # Reset good actions streak
            self.behavior_tracker['good_actions_streak'] = 0
            
            # Increment warnings
            self.behavior_tracker['warnings'] += 1
            
            # Escalate stakes if needed
            if self.behavior_tracker['warnings'] >= 3:
                self.behavior_tracker['stakes_level'] = 'high'
                
        else:
            # Track good behavior
            self.behavior_tracker['good_actions_streak'] += 1
            
            # Reset warnings after 3 good actions
            if self.behavior_tracker['good_actions_streak'] >= 3:
                self.behavior_tracker['warnings'] = 0
                self.behavior_tracker['stakes_level'] = 'medium'
                self.behavior_tracker['good_actions_streak'] = 0
        
        return {
            'warning_level': self.behavior_tracker['warnings'] if behavior_analysis['has_issues'] else 0,
            'stakes_level': self.behavior_tracker['stakes_level'],
            'behavior_issues': behavior_analysis['issue_types']
        }