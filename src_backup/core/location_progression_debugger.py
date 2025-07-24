"""
Location Progression Debugger - Fixes location transition issues
Ensures dice system works properly with location changes and provides debugging
"""
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class TransitionType(Enum):
    PLAYER_MOVEMENT = "player_movement"
    STORY_PROGRESSION = "story_progression"
    FORCED_PROGRESSION = "forced_progression"
    DICE_RESULT = "dice_result"
    AI_NARRATIVE = "ai_narrative"

@dataclass
class LocationTransition:
    from_location: str
    to_location: str
    transition_type: TransitionType
    trigger_text: str
    dice_roll_involved: bool = False
    dice_result: Optional[Dict] = None
    success: bool = True
    turn_number: int = 0
    timestamp: float = 0

class LocationProgressionDebugger:
    """Debug and fix location transition issues"""
    
    def __init__(self):
        self.transition_history: List[LocationTransition] = []
        self.location_patterns = self._initialize_location_patterns()
        self.movement_keywords = self._initialize_movement_keywords()
        self.debug_mode = True
        self.transition_rules = self._initialize_transition_rules()
    
    def _initialize_location_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for detecting location mentions"""
        return {
            'ashbrook_village': [
                r'ashbrook\s+village',
                r'the\s+village',
                r'village\s+center',
                r'village\s+square',
                r'into\s+ashbrook',
                r'reach\s+ashbrook',
                r'arrive\s+at\s+ashbrook',
                r'enter\s+ashbrook'
            ],
            'village_outskirts': [
                r'village\s+outskirts',
                r'outskirts\s+of\s+the\s+village',
                r'edge\s+of\s+the\s+village',
                r'path\s+to\s+the\s+village',
                r'approaching\s+the\s+village'
            ],
            'crystal_cave': [
                r'crystal\s+cave',
                r'the\s+cave',
                r'cave\s+entrance',
                r'into\s+the\s+cave',
                r'enter\s+the\s+cave',
                r'cave\s+interior',
                r'deeper\s+into\s+the\s+cave'
            ],
            'ember_woods': [
                r'ember\s+woods',
                r'the\s+woods',
                r'forest',
                r'into\s+the\s+woods',
                r'through\s+the\s+forest',
                r'deeper\s+into\s+the\s+woods'
            ],
            'sacred_grove': [
                r'sacred\s+grove',
                r'the\s+grove',
                r'ancient\s+grove',
                r'reach\s+the\s+grove',
                r'arrive\s+at\s+the\s+grove'
            ],
            'village_tavern': [
                r'tavern',
                r'inn',
                r'rusty\s+sword',
                r'into\s+the\s+tavern',
                r'enter\s+the\s+inn'
            ]
        }
    
    def _initialize_movement_keywords(self) -> List[str]:
        """Initialize keywords that indicate movement"""
        return [
            'move', 'moving', 'walk', 'walking', 'travel', 'traveling',
            'head', 'heading', 'go', 'going', 'proceed', 'proceeding',
            'advance', 'advancing', 'approach', 'approaching',
            'enter', 'entering', 'leave', 'leaving', 'exit', 'exiting',
            'arrive', 'arriving', 'reach', 'reaching', 'journey',
            'venture', 'venturing', 'step', 'stepping'
        ]
    
    def _initialize_transition_rules(self) -> Dict[str, Dict]:
        """Initialize rules for valid location transitions"""
        return {
            'village_outskirts': {
                'connected_to': ['ashbrook_village', 'ember_woods'],
                'movement_difficulty': 'trivial',
                'requires_dice': False
            },
            'ashbrook_village': {
                'connected_to': ['village_outskirts', 'village_tavern'],
                'movement_difficulty': 'trivial',
                'requires_dice': False
            },
            'village_tavern': {
                'connected_to': ['ashbrook_village'],
                'movement_difficulty': 'trivial',
                'requires_dice': False
            },
            'ember_woods': {
                'connected_to': ['village_outskirts', 'crystal_cave', 'sacred_grove'],
                'movement_difficulty': 'easy',
                'requires_dice': True
            },
            'crystal_cave': {
                'connected_to': ['ember_woods'],
                'movement_difficulty': 'normal',
                'requires_dice': True
            },
            'sacred_grove': {
                'connected_to': ['ember_woods'],
                'movement_difficulty': 'easy',
                'requires_dice': False
            }
        }
    
    def debug_location_transition(self, ai_response: str, current_location: str, 
                                dice_rolls: List[Dict] = None, turn_number: int = 0) -> Dict[str, Any]:
        """Debug and validate location transitions from AI response"""
        
        debug_result = {
            'transition_detected': False,
            'new_location': None,
            'transition_valid': False,
            'debug_info': [],
            'fixes_applied': [],
            'dice_integration_status': 'not_needed'
        }
        
        # Step 1: Detect location mentions in AI response
        detected_locations = self._detect_locations_in_text(ai_response)
        debug_result['debug_info'].append(f"Detected locations: {detected_locations}")
        
        # Step 2: Check for movement indicators
        movement_detected = self._detect_movement_in_text(ai_response)
        debug_result['debug_info'].append(f"Movement detected: {movement_detected}")
        
        # Step 3: Determine if transition should occur
        if detected_locations and movement_detected:
            target_location = self._determine_target_location(detected_locations, current_location, ai_response)
            
            if target_location and target_location != current_location:
                debug_result['transition_detected'] = True
                debug_result['new_location'] = target_location
                
                # Step 4: Validate transition
                validation_result = self._validate_transition(current_location, target_location, dice_rolls)
                debug_result.update(validation_result)
                
                # Step 5: Apply fixes if needed
                if not validation_result['transition_valid']:
                    fixes = self._apply_transition_fixes(current_location, target_location, ai_response, dice_rolls)
                    debug_result['fixes_applied'] = fixes
                    debug_result['transition_valid'] = fixes.get('fixed', False)
        
        # Step 6: Log transition for debugging
        if debug_result['transition_detected']:
            self._log_transition(current_location, debug_result['new_location'], 
                               ai_response, dice_rolls, turn_number, debug_result['transition_valid'])
        
        return debug_result
    
    def _detect_locations_in_text(self, text: str) -> List[str]:
        """Detect location mentions in text using patterns"""
        detected = []
        text_lower = text.lower()
        
        for location, patterns in self.location_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    detected.append(location)
                    break  # Don't double-count same location
        
        return detected
    
    def _detect_movement_in_text(self, text: str) -> bool:
        """Detect movement keywords in text"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.movement_keywords)
    
    def _determine_target_location(self, detected_locations: List[str], 
                                 current_location: str, ai_response: str) -> Optional[str]:
        """Determine the most likely target location"""
        
        # Remove current location from candidates
        candidates = [loc for loc in detected_locations if loc != current_location]
        
        if not candidates:
            return None
        
        if len(candidates) == 1:
            return candidates[0]
        
        # Multiple candidates - use context to decide
        ai_response_lower = ai_response.lower()
        
        # Look for directional or arrival language
        arrival_patterns = [
            (r'arrive\s+at\s+(\w+)', 2.0),
            (r'reach\s+(\w+)', 2.0),
            (r'enter\s+(\w+)', 1.8),
            (r'into\s+(\w+)', 1.5),
            (r'toward\s+(\w+)', 1.2),
            (r'approaching\s+(\w+)', 1.2)
        ]
        
        location_scores = {loc: 1.0 for loc in candidates}
        
        for pattern, weight in arrival_patterns:
            matches = re.finditer(pattern, ai_response_lower)
            for match in matches:
                location_word = match.group(1)
                for candidate in candidates:
                    if location_word in candidate or candidate.split('_')[-1] in location_word:
                        location_scores[candidate] += weight
        
        # Return highest scoring location
        return max(location_scores.items(), key=lambda x: x[1])[0]
    
    def _validate_transition(self, from_location: str, to_location: str, 
                           dice_rolls: List[Dict] = None) -> Dict[str, Any]:
        """Validate if transition is allowed and properly supported"""
        
        validation = {
            'transition_valid': False,
            'validation_errors': [],
            'dice_integration_status': 'not_needed'
        }
        
        # Check if locations are connected
        from_rules = self.transition_rules.get(from_location, {})
        connected_locations = from_rules.get('connected_to', [])
        
        if to_location not in connected_locations:
            validation['validation_errors'].append(f"No direct path from {from_location} to {to_location}")
            return validation
        
        # Check if dice roll is required
        requires_dice = from_rules.get('requires_dice', False)
        
        if requires_dice:
            validation['dice_integration_status'] = 'required'
            
            if not dice_rolls:
                validation['validation_errors'].append("Dice roll required for this transition but none provided")
                return validation
            
            # Check if dice roll is appropriate
            dice_validation = self._validate_dice_for_transition(from_location, to_location, dice_rolls)
            if not dice_validation['valid']:
                validation['validation_errors'].extend(dice_validation['errors'])
                return validation
            
            validation['dice_integration_status'] = 'validated'
        
        validation['transition_valid'] = True
        return validation
    
    def _validate_dice_for_transition(self, from_location: str, to_location: str, 
                                    dice_rolls: List[Dict]) -> Dict[str, Any]:
        """Validate dice rolls for location transitions"""
        
        validation = {'valid': False, 'errors': []}
        
        # Find relevant dice roll
        movement_roll = None
        for roll in dice_rolls:
            roll_type = roll.get('roll_type', '').lower()
            if any(keyword in roll_type for keyword in ['movement', 'navigation', 'athletics', 'survival']):
                movement_roll = roll
                break
        
        if not movement_roll:
            validation['errors'].append("No movement-related dice roll found")
            return validation
        
        # Check if roll was successful
        if not movement_roll.get('success', False):
            validation['errors'].append("Movement dice roll failed - transition should not succeed")
            return validation
        
        # Check difficulty appropriateness
        from_rules = self.transition_rules.get(from_location, {})
        expected_difficulty = from_rules.get('movement_difficulty', 'normal')
        
        roll_target = movement_roll.get('target', 12)
        difficulty_targets = {'trivial': 5, 'easy': 8, 'normal': 12, 'hard': 15, 'extreme': 18}
        expected_target = difficulty_targets.get(expected_difficulty, 12)
        
        if abs(roll_target - expected_target) > 3:  # Allow some variance
            validation['errors'].append(f"Dice difficulty mismatch: expected {expected_difficulty} (target {expected_target}), got target {roll_target}")
            return validation
        
        validation['valid'] = True
        return validation
    
    def _apply_transition_fixes(self, from_location: str, to_location: str, 
                              ai_response: str, dice_rolls: List[Dict] = None) -> Dict[str, Any]:
        """Apply fixes to make transition work properly"""
        
        fixes = {
            'fixed': False,
            'applied_fixes': [],
            'suggested_dice_roll': None,
            'alternative_narrative': None
        }
        
        from_rules = self.transition_rules.get(from_location, {})
        
        # Fix 1: Generate missing dice roll
        if from_rules.get('requires_dice', False) and not dice_rolls:
            suggested_roll = self._generate_suggested_dice_roll(from_location, to_location)
            fixes['suggested_dice_roll'] = suggested_roll
            fixes['applied_fixes'].append("Generated missing dice roll")
        
        # Fix 2: Validate connection
        connected_locations = from_rules.get('connected_to', [])
        if to_location not in connected_locations:
            # Find alternative path
            alternative_path = self._find_alternative_path(from_location, to_location)
            if alternative_path:
                fixes['alternative_narrative'] = f"To reach {to_location}, you must first go through {alternative_path[0]}"
                fixes['applied_fixes'].append("Suggested alternative path")
            else:
                fixes['alternative_narrative'] = f"Direct travel to {to_location} is not possible from {from_location}"
                fixes['applied_fixes'].append("Blocked invalid transition")
                return fixes
        
        # Fix 3: Adjust narrative for dice result
        if dice_rolls:
            movement_roll = next((roll for roll in dice_rolls 
                                if 'movement' in roll.get('roll_type', '').lower()), None)
            if movement_roll and not movement_roll.get('success', True):
                fixes['alternative_narrative'] = self._generate_failure_narrative(from_location, to_location, movement_roll)
                fixes['applied_fixes'].append("Generated failure narrative")
                return fixes
        
        fixes['fixed'] = True
        return fixes
    
    def _generate_suggested_dice_roll(self, from_location: str, to_location: str) -> Dict[str, Any]:
        """Generate appropriate dice roll for transition"""
        
        from_rules = self.transition_rules.get(from_location, {})
        difficulty = from_rules.get('movement_difficulty', 'normal')
        
        difficulty_targets = {'trivial': 5, 'easy': 8, 'normal': 12, 'hard': 15, 'extreme': 18}
        target = difficulty_targets.get(difficulty, 12)
        
        # Determine appropriate skill
        skill_mapping = {
            'ember_woods': 'Survival',
            'crystal_cave': 'Athletics',
            'sacred_grove': 'Navigation'
        }
        
        skill = skill_mapping.get(to_location, 'Athletics')
        
        return {
            'roll_type': f'movement_to_{to_location}',
            'stat_used': 'dexterity',
            'skill_used': skill,
            'target': target,
            'difficulty': difficulty,
            'context': f"Moving from {from_location} to {to_location}"
        }
    
    def _find_alternative_path(self, from_location: str, to_location: str) -> Optional[List[str]]:
        """Find alternative path between locations"""
        
        # Simple pathfinding - check if there's a one-hop path
        from_rules = self.transition_rules.get(from_location, {})
        connected = from_rules.get('connected_to', [])
        
        for intermediate in connected:
            intermediate_rules = self.transition_rules.get(intermediate, {})
            if to_location in intermediate_rules.get('connected_to', []):
                return [intermediate]
        
        return None
    
    def _generate_failure_narrative(self, from_location: str, to_location: str, 
                                  failed_roll: Dict) -> str:
        """Generate narrative for failed movement"""
        
        failure_narratives = {
            'ember_woods': "You attempt to navigate the dense woods but lose your way among the twisted paths.",
            'crystal_cave': "The cave entrance proves treacherous, and you struggle to find secure footing.",
            'sacred_grove': "The mystical energies of the grove seem to resist your approach."
        }
        
        base_narrative = failure_narratives.get(to_location, 
            f"Your attempt to reach {to_location} encounters unexpected difficulties.")
        
        roll_result = failed_roll.get('base_roll', 0)
        if roll_result <= 5:
            return base_narrative + " You make little progress and must reconsider your approach."
        else:
            return base_narrative + " You make some progress but haven't reached your destination yet."
    
    def _log_transition(self, from_location: str, to_location: str, trigger_text: str,
                       dice_rolls: List[Dict], turn_number: int, success: bool):
        """Log transition for debugging history"""
        
        import time
        
        dice_involved = bool(dice_rolls)
        dice_result = dice_rolls[0] if dice_rolls else None
        
        transition = LocationTransition(
            from_location=from_location,
            to_location=to_location,
            transition_type=TransitionType.AI_NARRATIVE,
            trigger_text=trigger_text[:200],  # Truncate for storage
            dice_roll_involved=dice_involved,
            dice_result=dice_result,
            success=success,
            turn_number=turn_number,
            timestamp=time.time()
        )
        
        self.transition_history.append(transition)
        
        # Keep only last 20 transitions
        if len(self.transition_history) > 20:
            self.transition_history.pop(0)
    
    def get_transition_debug_report(self) -> Dict[str, Any]:
        """Generate debug report for location transitions"""
        
        if not self.transition_history:
            return {'no_transitions': True}
        
        recent_transitions = self.transition_history[-10:]
        
        success_rate = sum(1 for t in recent_transitions if t.success) / len(recent_transitions)
        dice_integration_rate = sum(1 for t in recent_transitions if t.dice_roll_involved) / len(recent_transitions)
        
        common_issues = []
        for transition in recent_transitions:
            if not transition.success:
                if not transition.dice_roll_involved and self.transition_rules.get(transition.from_location, {}).get('requires_dice'):
                    common_issues.append("Missing required dice roll")
                elif transition.dice_roll_involved and transition.dice_result and not transition.dice_result.get('success'):
                    common_issues.append("Failed dice roll not handled properly")
        
        return {
            'total_transitions': len(self.transition_history),
            'recent_transitions': len(recent_transitions),
            'success_rate': success_rate,
            'dice_integration_rate': dice_integration_rate,
            'common_issues': list(set(common_issues)),
            'recent_transition_summary': [
                {
                    'from': t.from_location,
                    'to': t.to_location,
                    'success': t.success,
                    'dice_involved': t.dice_roll_involved,
                    'turn': t.turn_number
                }
                for t in recent_transitions
            ]
        }
    
    def force_valid_transition(self, from_location: str, target_location: str) -> Dict[str, Any]:
        """Force a valid transition by finding the best path"""
        
        # Check direct connection first
        from_rules = self.transition_rules.get(from_location, {})
        if target_location in from_rules.get('connected_to', []):
            return {
                'transition_possible': True,
                'direct_path': True,
                'target_location': target_location,
                'requires_dice': from_rules.get('requires_dice', False),
                'difficulty': from_rules.get('movement_difficulty', 'normal')
            }
        
        # Find alternative path
        alternative_path = self._find_alternative_path(from_location, target_location)
        if alternative_path:
            intermediate = alternative_path[0]
            intermediate_rules = self.transition_rules.get(intermediate, {})
            
            return {
                'transition_possible': True,
                'direct_path': False,
                'intermediate_location': intermediate,
                'target_location': target_location,
                'requires_dice': from_rules.get('requires_dice', False),
                'difficulty': from_rules.get('movement_difficulty', 'normal'),
                'narrative_suggestion': f"To reach {target_location}, first travel to {intermediate}"
            }
        
        return {
            'transition_possible': False,
            'reason': f"No valid path from {from_location} to {target_location}",
            'available_destinations': from_rules.get('connected_to', [])
        }
    
    def get_location_connectivity_map(self) -> Dict[str, Any]:
        """Get complete map of location connections for debugging"""
        
        return {
            'locations': list(self.transition_rules.keys()),
            'connections': {
                location: {
                    'connected_to': rules.get('connected_to', []),
                    'requires_dice': rules.get('requires_dice', False),
                    'difficulty': rules.get('movement_difficulty', 'normal')
                }
                for location, rules in self.transition_rules.items()
            },
            'total_connections': sum(len(rules.get('connected_to', [])) for rules in self.transition_rules.values())
        }