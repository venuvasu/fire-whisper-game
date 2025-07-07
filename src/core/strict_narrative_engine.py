"""
Strict Narrative Engine - Pre-defined outcomes to eliminate AI hallucinations
"""

class StrictNarrativeEngine:
    def __init__(self):
        self.scenario_templates = {
            'stealth_success': "You move silently through the shadows, your footsteps making no sound. Your stealth training pays off as you avoid detection.",
            'stealth_failure': "Your armor clanks softly as you try to move quietly. The sound echoes slightly, potentially alerting nearby enemies.",
            'combat_success': "Your attack connects solidly! Your weapon finds its mark, dealing significant damage to your opponent.",
            'combat_failure': "Your attack misses its target. Your opponent dodges or blocks your strike effectively.",
            'magic_success': "Your magical energy flows smoothly, and the spell takes effect as intended.",
            'magic_failure': "The magical energy dissipates before you can properly channel it. The spell fails to manifest.",
            'social_success': "Your words are persuasive and well-chosen. The target responds positively to your approach.",
            'social_failure': "Your words don't have the intended effect. The target remains unconvinced or suspicious.",
            'skill_success': "Your training and natural ability serve you well. You successfully accomplish what you set out to do.",
            'skill_failure': "Despite your best efforts, you're unable to complete the task successfully. You learn from the attempt."
        }
        
        self.choice_templates = {
            'combat_choices': [
                "Attack with a powerful strike (Strength + Combat)",
                "Attempt a precise, aimed attack (Dexterity + Combat)", 
                "Try to intimidate your opponent (Charisma + Intimidation)",
                "Look for tactical advantages (Intelligence + Tactics)"
            ],
            'exploration_choices': [
                "Search the area thoroughly (Intelligence + Investigation)",
                "Move stealthily to avoid detection (Dexterity + Stealth)",
                "Use brute force to overcome obstacles (Strength + Athletics)",
                "Try to charm or negotiate with anyone you meet (Charisma + Persuasion)"
            ],
            'social_choices': [
                "Attempt to persuade them (Charisma + Persuasion)",
                "Try to intimidate them (Charisma + Intimidation)",
                "Use deception to mislead them (Charisma + Deception)",
                "Appeal to their knowledge or reason (Intelligence + Knowledge)"
            ],
            'magic_choices': [
                "Cast an offensive spell (Charisma + Magic)",
                "Attempt a protective enchantment (Charisma + Magic)",
                "Try to heal yourself or others (Charisma + Healing)",
                "Use magic to enhance your abilities (Charisma + Magic)"
            ]
        }
    
    def generate_outcome_narrative(self, action_type, stat_used, skill_used, success, dice_roll):
        """Generate strictly controlled narrative based on mechanical results"""
        
        # Determine base template
        if action_type.value == 'combat':
            template_key = 'combat_success' if success else 'combat_failure'
        elif action_type.value == 'magic':
            template_key = 'magic_success' if success else 'magic_failure'
        elif action_type.value == 'social':
            template_key = 'social_success' if success else 'social_failure'
        elif 'stealth' in skill_used.lower():
            template_key = 'stealth_success' if success else 'stealth_failure'
        else:
            template_key = 'skill_success' if success else 'skill_failure'
        
        base_narrative = self.scenario_templates[template_key]
        
        # Add dice roll details
        modifiers_text = " + ".join([f"{k}(+{v})" for k, v in dice_roll.modifiers.items()])
        result_text = "SUCCESS" if success else "FAILURE"
        
        dice_narrative = f"""
🎲 {action_type.value.title()} Roll: {dice_roll.base_roll} + {sum(dice_roll.modifiers.values())} = {dice_roll.base_roll + sum(dice_roll.modifiers.values())} vs {dice_roll.target}
Modifiers: {modifiers_text}
Result: {result_text}
"""
        
        return f"*Emberlyn watches as you attempt your {action_type.value}*\n\n{dice_narrative}\n{base_narrative}"
    
    def generate_choices(self, current_context="exploration"):
        """Generate pre-defined choice sets"""
        if current_context in self.choice_templates:
            choices = self.choice_templates[current_context]
        else:
            choices = self.choice_templates['exploration_choices']
        
        choice_text = "\nWhat do you do next?\n"
        for i, choice in enumerate(choices, 1):
            choice_text += f"{i}. {choice}\n"
        
        return choice_text
    
    def build_complete_response(self, action_type, stat_used, skill_used, success, dice_roll, xp_awards):
        """Build complete response with no AI creativity"""
        
        # Narrative outcome
        narrative = self.generate_outcome_narrative(action_type, stat_used, skill_used, success, dice_roll)
        
        # XP announcement
        if xp_awards:
            for xp_award in xp_awards:
                narrative += f"\n\n✨ You gain {xp_award['xp_awarded']} XP for {xp_award['reason']}!"
                narrative += f"\nTotal XP: {xp_award['new_xp']}"
                
                if xp_award['level_up']:
                    narrative += f"\n🎉 LEVEL UP! You are now Level {xp_award['new_level']}!"
        
        # Next choices
        narrative += self.generate_choices()
        
        return narrative