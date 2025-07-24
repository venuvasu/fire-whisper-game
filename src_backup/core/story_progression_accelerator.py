#!/usr/bin/env python3
"""
Story Progression Accelerator - Ensures stories reach meaningful points by turn 20

This system tracks story progress, ensures appropriate pacing, and forces progression
when necessary to reach climactic moments by turn 20. It uses a non-linear progression
curve to create a satisfying narrative arc.
"""
import math
from typing import Dict, List, Tuple, Any, Optional

class StoryPhase:
    """Represents a phase in a story arc"""
    
    def __init__(self, name: str, description: str, progress_threshold: float):
        self.name = name
        self.description = description
        self.progress_threshold = progress_threshold
        self.entered_turn = None
        self.exited_turn = None
    
    def enter(self, turn_number: int):
        """Mark this phase as entered"""
        self.entered_turn = turn_number
    
    def exit(self, turn_number: int):
        """Mark this phase as exited"""
        self.exited_turn = turn_number
    
    def is_active(self) -> bool:
        """Check if this phase is currently active"""
        return self.entered_turn is not None and self.exited_turn is None
    
    def get_duration(self) -> Optional[int]:
        """Get the duration of this phase in turns"""
        if self.entered_turn is None:
            return None
        
        if self.exited_turn is None:
            return None
        
        return self.exited_turn - self.entered_turn


class StoryProgressionAccelerator:
    """Manages story progression to ensure appropriate pacing"""
    
    def __init__(self, story_arc: Dict[str, Any], target_climax_turn: int = 20):
        self.story_arc = story_arc
        self.target_climax_turn = target_climax_turn
        self.current_turn = 0
        self.progress_points = 0.0
        self.forced_progressions = 0
        self.progression_history = []
        
        # Define story phases
        self.phases = self._initialize_story_phases()
        self.current_phase = self.phases["introduction"]
        self.current_phase.enter(0)  # Start in introduction phase
    
    def _initialize_story_phases(self) -> Dict[str, StoryPhase]:
        """Initialize the story phases with appropriate thresholds"""
        return {
            "introduction": StoryPhase(
                "introduction",
                "Setting the scene and introducing key elements",
                0.0  # Starting phase
            ),
            "rising_action": StoryPhase(
                "rising_action",
                "Building tension and developing the conflict",
                0.2  # 20% progress
            ),
            "complication": StoryPhase(
                "complication",
                "Introducing obstacles and raising the stakes",
                0.4  # 40% progress
            ),
            "crisis": StoryPhase(
                "crisis",
                "Reaching a critical point where decisions are crucial",
                0.6  # 60% progress
            ),
            "climax": StoryPhase(
                "climax",
                "The peak of tension and conflict resolution",
                0.8  # 80% progress
            ),
            "resolution": StoryPhase(
                "resolution",
                "Wrapping up loose ends and concluding the story",
                1.0  # 100% progress
            )
        }
    
    def advance_turn(self) -> Dict[str, Any]:
        """
        Advance to the next turn and check if progression needs to be forced
        
        Returns:
            Dict with information about the turn advancement
        """
        self.current_turn += 1
        
        # Calculate expected progress at this turn
        expected_progress = self._calculate_expected_progress()
        
        # Check if we're falling behind
        falling_behind = self.progress_points < expected_progress
        progress_gap = expected_progress - self.progress_points if falling_behind else 0
        
        # Determine if we need to force progression
        force_progression = falling_behind and progress_gap > 0.1  # More than 10% behind
        
        result = {
            "turn": self.current_turn,
            "current_progress": self.progress_points,
            "expected_progress": expected_progress,
            "current_phase": self.current_phase.name,
            "falling_behind": falling_behind,
            "progress_gap": progress_gap,
            "force_progression": force_progression
        }
        
        # Force progression if needed
        if force_progression:
            force_amount = min(progress_gap, 0.15)  # Don't jump too far at once
            self.add_progress(force_amount, "forced_progression")
            self.forced_progressions += 1
            
            result["forced_progression"] = {
                "amount": force_amount,
                "reason": "falling_behind",
                "new_progress": self.progress_points
            }
        
        return result
    
    def _calculate_expected_progress(self) -> float:
        """
        Calculate how far the story should have progressed by current turn
        
        Uses a non-linear progression curve to create a satisfying narrative arc:
        - Slower start to establish the setting
        - Faster middle to build momentum
        - Slightly slower end to allow for proper resolution
        """
        # Calculate basic progress ratio
        progress_ratio = self.current_turn / self.target_climax_turn
        
        # Cap at 1.0 for turns beyond target
        if progress_ratio > 1.0:
            return 1.0
        
        # Apply acceleration curve (starts slower, accelerates in middle, slows at end)
        if progress_ratio < 0.3:
            # Slower start (70% of linear pace)
            adjusted_ratio = progress_ratio * 0.7
        elif progress_ratio < 0.7:
            # Faster middle (130% of linear pace)
            adjusted_ratio = 0.21 + (progress_ratio - 0.3) * 1.3
        else:
            # Slower end (90% of linear pace)
            adjusted_ratio = 0.73 + (progress_ratio - 0.7) * 0.9
        
        return adjusted_ratio
    
    def add_progress(self, amount: float, reason: str) -> Dict[str, Any]:
        """
        Add progress points and update story phase if thresholds are crossed
        
        Args:
            amount: Amount of progress to add (0.0 to 1.0)
            reason: Reason for the progress
            
        Returns:
            Dict with information about the progress update
        """
        old_progress = self.progress_points
        old_phase = self.current_phase.name
        
        # Add progress
        self.progress_points += amount
        
        # Cap at 1.0
        self.progress_points = min(1.0, self.progress_points)
        
        # Record in history
        self.progression_history.append({
            "turn": self.current_turn,
            "amount": amount,
            "reason": reason,
            "new_progress": self.progress_points
        })
        
        # Check if we've crossed into a new phase
        new_phase = self._check_phase_transition()
        phase_changed = new_phase != old_phase
        
        return {
            "old_progress": old_progress,
            "new_progress": self.progress_points,
            "amount": amount,
            "reason": reason,
            "old_phase": old_phase,
            "new_phase": new_phase,
            "phase_changed": phase_changed
        }
    
    def _check_phase_transition(self) -> str:
        """
        Check if we've crossed into a new phase and update accordingly
        
        Returns:
            Name of the current phase after any transitions
        """
        # Check phases in reverse order (from resolution to rising_action)
        for phase_name, phase in sorted(
            self.phases.items(),
            key=lambda x: x[1].progress_threshold,
            reverse=True
        ):
            if self.progress_points >= phase.progress_threshold:
                # Skip if this is already the current phase
                if phase == self.current_phase:
                    return phase_name
                
                # Exit current phase
                self.current_phase.exit(self.current_turn)
                
                # Enter new phase
                phase.enter(self.current_turn)
                self.current_phase = phase
                
                return phase_name
        
        # Should never reach here, but just in case
        return self.current_phase.name
    
    def get_progress_percentage(self) -> float:
        """Get progress as a percentage (0-100)"""
        return self.progress_points * 100
    
    def get_phase_progress(self) -> float:
        """Get progress within the current phase (0.0-1.0)"""
        # Find the next phase threshold
        current_threshold = self.current_phase.progress_threshold
        
        # Find the next phase threshold
        next_threshold = 1.0  # Default to full completion
        for phase in self.phases.values():
            if phase.progress_threshold > current_threshold and phase.progress_threshold < next_threshold:
                next_threshold = phase.progress_threshold
        
        # Calculate progress within current phase
        phase_range = next_threshold - current_threshold
        if phase_range <= 0:
            return 1.0
        
        phase_progress = (self.progress_points - current_threshold) / phase_range
        return min(1.0, max(0.0, phase_progress))
    
    def get_turn_estimate_for_phase(self, phase_name: str) -> Optional[int]:
        """
        Estimate which turn a specific phase will be reached
        
        Args:
            phase_name: Name of the phase
            
        Returns:
            Estimated turn number or None if invalid phase
        """
        if phase_name not in self.phases:
            return None
        
        # If we're already past this phase, return the actual turn it was entered
        if self.phases[phase_name].entered_turn is not None:
            return self.phases[phase_name].entered_turn
        
        # Calculate based on current progress and rate
        target_progress = self.phases[phase_name].progress_threshold
        progress_remaining = target_progress - self.progress_points
        
        if progress_remaining <= 0:
            # We should be in this phase already
            return self.current_turn
        
        # Estimate based on average progress per turn
        if self.current_turn == 0:
            return int(target_progress * self.target_climax_turn)
        
        avg_progress_per_turn = self.progress_points / self.current_turn
        if avg_progress_per_turn <= 0:
            return self.target_climax_turn  # Default to target if no progress
        
        turns_remaining = progress_remaining / avg_progress_per_turn
        return self.current_turn + int(turns_remaining)
    
    def get_phase_summary(self) -> Dict[str, Any]:
        """Get summary of all phases and their status"""
        summary = {}
        
        for phase_name, phase in self.phases.items():
            summary[phase_name] = {
                "description": phase.description,
                "threshold": phase.progress_threshold,
                "entered_turn": phase.entered_turn,
                "exited_turn": phase.exited_turn,
                "is_active": phase.is_active(),
                "estimated_turn": self.get_turn_estimate_for_phase(phase_name)
            }
        
        return summary
    
    def generate_progress_prompt(self) -> str:
        """
        Generate a prompt for AI to advance the story appropriately
        
        Returns:
            Prompt for AI to generate a response that advances the story
        """
        phase = self.current_phase
        phase_progress = self.get_phase_progress()
        
        prompt = f"""
        The story is currently in the {phase.name.upper()} phase ({self.get_progress_percentage():.1f}% overall progress).
        
        Phase Description: {phase.description}
        Progress within this phase: {phase_progress:.1f}%
        
        Please advance the story appropriately for this phase:
        """
        
        # Add phase-specific guidance
        if phase.name == "introduction":
            prompt += """
            - Establish the key elements of the story
            - Introduce important characters and locations
            - Begin to hint at the central conflict
            - Create a sense of the world and its atmosphere
            """
        elif phase.name == "rising_action":
            prompt += """
            - Develop the central conflict more clearly
            - Increase tension and stakes
            - Reveal more about the characters and their motivations
            - Introduce complications and obstacles
            """
        elif phase.name == "complication":
            prompt += """
            - Present significant obstacles to the protagonist
            - Raise the stakes considerably
            - Deepen the conflict and its implications
            - Create moments of doubt or uncertainty
            """
        elif phase.name == "crisis":
            prompt += """
            - Bring the conflict to a critical point
            - Force important decisions with significant consequences
            - Create a sense that events are reaching a turning point
            - Increase the pace and tension dramatically
            """
        elif phase.name == "climax":
            prompt += """
            - Present the decisive moment of the story
            - Resolve the central conflict in a meaningful way
            - Create a moment of highest tension and drama
            - Show the consequences of previous choices
            """
        elif phase.name == "resolution":
            prompt += """
            - Wrap up loose ends and subplots
            - Show the aftermath of the climax
            - Provide closure for characters and situations
            - Hint at future possibilities or consequences
            """
        
        # Add pacing guidance
        if self.current_turn < self.target_climax_turn * 0.5:
            # First half of story
            if phase_progress < 0.5:
                prompt += "\nPacing: Continue developing this phase naturally."
            else:
                prompt += "\nPacing: Begin transitioning toward the next phase."
        else:
            # Second half of story
            if phase_progress < 0.7:
                prompt += "\nPacing: Accelerate developments in this phase."
            else:
                prompt += "\nPacing: Strongly push toward the next phase."
        
        return prompt
    
    def generate_forced_progression_prompt(self) -> str:
        """
        Generate a prompt for AI to force story progression
        
        Returns:
            Prompt for AI to generate a response that forces story progression
        """
        current_phase = self.current_phase.name
        next_phase = None
        
        # Find the next phase
        found_current = False
        for phase_name in ["introduction", "rising_action", "complication", "crisis", "climax", "resolution"]:
            if found_current:
                next_phase = phase_name
                break
            if phase_name == current_phase:
                found_current = True
        
        if not next_phase:
            next_phase = "resolution"  # Default to resolution if at the end
        
        prompt = f"""
        The story needs to progress more quickly toward the {next_phase.upper()} phase.
        
        Current phase: {current_phase}
        Target phase: {next_phase}
        Current turn: {self.current_turn}
        Target for climax: Turn {self.target_climax_turn}
        
        Please create a response that:
        1. Introduces a significant development that moves the story forward
        2. Accelerates the narrative toward the {next_phase} phase
        3. Maintains continuity with established elements
        4. Creates a sense of momentum and urgency
        
        Specific ways to advance the story:
        """
        
        # Add phase-specific advancement suggestions
        if current_phase == "introduction":
            prompt += """
            - Reveal the central conflict clearly
            - Introduce a threat or challenge that demands action
            - Have an NPC provide crucial information that changes the situation
            - Create an inciting incident that pushes the story forward
            """
        elif current_phase == "rising_action":
            prompt += """
            - Escalate the conflict significantly
            - Introduce a complication that raises the stakes
            - Reveal hidden information that changes understanding of the situation
            - Force the protagonist to make an important choice
            """
        elif current_phase == "complication":
            prompt += """
            - Bring complications to a head
            - Create a moment where multiple problems converge
            - Introduce a ticking clock or deadline
            - Have an ally or resource become unavailable
            """
        elif current_phase == "crisis":
            prompt += """
            - Force a critical decision point
            - Create a moment where failure seems likely
            - Reveal the true nature of the antagonist or threat
            - Remove safety nets or backup options
            """
        elif current_phase == "climax":
            prompt += """
            - Bring the protagonist face-to-face with the main challenge
            - Create the final confrontation
            - Force the ultimate choice or test
            - Reveal the final twist or truth
            """
        
        return prompt


# Example usage
if __name__ == "__main__":
    # Create a sample story arc
    story_arc = {
        "name": "The Crimson Prophecy",
        "type": "Epic Fantasy",
        "hook": "An ancient prophecy speaks of a crimson blade that will either save or doom the realm.",
        "elements": ["Rival seekers", "moral choices about power", "ancient weapon", "prophecy interpretation"],
        "climax": "Confrontation at the Sundering Peaks where the blade's true nature is revealed"
    }
    
    # Create accelerator with target climax at turn 20
    accelerator = StoryProgressionAccelerator(story_arc, target_climax_turn=20)
    
    # Simulate a story with varied progression
    print("Simulating story progression:")
    print(f"Target climax turn: {accelerator.target_climax_turn}")
    print(f"Starting phase: {accelerator.current_phase.name}")
    
    # Progress through turns with different amounts of progress
    progress_amounts = [
        0.05, 0.03, 0.02, 0.04, 0.03,  # Turns 1-5
        0.05, 0.07, 0.06, 0.04, 0.05,  # Turns 6-10
        0.03, 0.02, 0.04, 0.06, 0.08,  # Turns 11-15
        0.10, 0.12, 0.15, 0.20, 0.10   # Turns 16-20
    ]
    
    for i, amount in enumerate(progress_amounts, 1):
        # Advance turn
        turn_result = accelerator.advance_turn()
        
        # Add some progress (simulating player actions)
        progress_result = accelerator.add_progress(amount, "player_action")
        
        # Print status
        print(f"\nTurn {i}:")
        print(f"  Phase: {accelerator.current_phase.name}")
        print(f"  Progress: {accelerator.get_progress_percentage():.1f}%")
        print(f"  Expected: {turn_result['expected_progress'] * 100:.1f}%")
        
        if turn_result.get("force_progression"):
            print(f"  FORCED PROGRESSION: +{turn_result['forced_progression']['amount'] * 100:.1f}%")
        
        if progress_result["phase_changed"]:
            print(f"  PHASE CHANGE: {progress_result['old_phase']} → {progress_result['new_phase']}")
    
    # Print final phase summary
    print("\nFinal Phase Summary:")
    phase_summary = accelerator.get_phase_summary()
    
    for phase_name, data in phase_summary.items():
        status = "ACTIVE" if data["is_active"] else "COMPLETED" if data["exited_turn"] is not None else "UPCOMING"
        turn_info = f"Turns {data['entered_turn']}-{data['exited_turn']}" if data["entered_turn"] is not None else f"Est. Turn {data['estimated_turn']}"
        
        print(f"  {phase_name.upper()} ({status}): {turn_info}")
    
    # Print statistics
    print(f"\nForced Progressions: {accelerator.forced_progressions}")
    print(f"Final Progress: {accelerator.get_progress_percentage():.1f}%")
    print(f"Final Phase: {accelerator.current_phase.name}")