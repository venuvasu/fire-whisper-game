# Fire Whisper RPG - Gameplay Improvement Plan

## Current Assessment (6.5/10)

### Strengths to Preserve
- Rich documentation and comprehensive systems
- Atmospheric writing and character development (Emberlyn)
- Solid technical foundation (progression tracking, location systems)

### Critical Issues to Address
1. **Repetitive Gameplay Loop** - Player choices feel meaningless with similar outcomes
2. **Disconnected Narrative** - Story elements shift without coherence
3. **Poor Action Resolution** - High-risk actions consistently fail without clear reasons
4. **Technical Bugs** - Location system and state tracking issues

## Core Implementation Strategy

Our implementation strategy will focus on **"Guided Creativity with Guardrails"** - using AI for creative content generation while implementing strict technical controls to maintain game coherence and meaningful player impact.

### 1. Action-Outcome Framework Overhaul

#### Problem: Repetitive responses to player actions
- Currently: High-risk actions consistently fail with similar responses
- Goal: Create varied, meaningful outcomes that respect player choices

#### Implementation:
```python
def resolve_player_action(action_type, risk_level, roll_result, dc):
    # Define outcome categories
    outcomes = {
        "spectacular_success": {
            "threshold": dc + 5,  # Exceeding DC by 5+ is spectacular
            "narrative_templates": [
                "Your {action_type} succeeds brilliantly! {spectacular_effect}",
                "With exceptional skill, you {spectacular_success_verb}! {spectacular_consequence}"
            ],
            "state_changes": {
                "progress_bonus": 2,  # Double progress
                "reputation_bonus": 1,
                "special_reward": True
            }
        },
        "success": {
            "threshold": dc,
            "narrative_templates": [
                "Your {action_type} succeeds. {positive_effect}",
                "You successfully {success_verb}. {positive_consequence}"
            ],
            "state_changes": {
                "progress_bonus": 1,
                "reputation_bonus": 0.5
            }
        },
        "partial_success": {
            "threshold": dc - 2,
            "narrative_templates": [
                "Your {action_type} partially succeeds. {mixed_effect}",
                "You {partial_success_verb}, but {complication}."
            ],
            "state_changes": {
                "progress_bonus": 0.5,
                "minor_complication": True
            }
        },
        "failure": {
            "threshold": dc - 5,
            "narrative_templates": [
                "Your {action_type} fails. {negative_effect}",
                "Despite your efforts, you {failure_verb}. {negative_consequence}"
            ],
            "state_changes": {
                "minor_setback": True
            }
        },
        "spectacular_failure": {
            "threshold": -999,  # Default for anything below failure
            "narrative_templates": [
                "Your {action_type} fails dramatically! {spectacular_negative_effect}",
                "In a turn of bad luck, you {spectacular_failure_verb}! {spectacular_negative_consequence}"
            ],
            "state_changes": {
                "major_setback": True,
                "reputation_penalty": 1,
                "unexpected_opportunity": True  # Even spectacular failures can open new paths
            }
        }
    }
    
    # Adjust DC based on risk level
    if risk_level == "high":
        dc += 2  # Higher risk means higher difficulty
    elif risk_level == "low":
        dc -= 2  # Lower risk means lower difficulty
    
    # Determine outcome category based on roll vs. DC
    for outcome_type, outcome_data in sorted(
        outcomes.items(), 
        key=lambda x: x[1]["threshold"], 
        reverse=True
    ):
        if roll_result >= outcome_data["threshold"]:
            return outcome_type, outcome_data
    
    # Default to spectacular failure if nothing else matches
    return "spectacular_failure", outcomes["spectacular_failure"]
```

### 2. Narrative Coherence System

#### Problem: Disconnected narrative elements and location inconsistencies
- Currently: Story elements shift without explanation, location tracking issues
- Goal: Maintain consistent narrative thread with proper state tracking

#### Implementation:
```python
class NarrativeStateManager:
    def __init__(self):
        self.active_elements = {
            "locations": {},       # Currently active locations
            "characters": {},      # Active NPCs
            "plot_threads": {},    # Active storylines
            "environmental": {},   # Active environmental elements
            "threats": {}          # Active threats/antagonists
        }
        self.narrative_history = []  # Track important narrative events
        
    def register_element(self, element_type, element_id, element_data):
        """Register a new narrative element as active"""
        if element_type in self.active_elements:
            self.active_elements[element_type][element_id] = {
                "data": element_data,
                "introduced_turn": self.current_turn,
                "last_mentioned_turn": self.current_turn,
                "importance": element_data.get("importance", 1)
            }
    
    def check_continuity_violations(self, ai_response):
        """Check if AI response maintains continuity with active elements"""
        violations = []
        
        # Check each active element type
        for element_type, elements in self.active_elements.items():
            for element_id, element_data in elements.items():
                # Skip if element was just introduced this turn
                if element_data["introduced_turn"] == self.current_turn:
                    continue
                    
                # Skip low importance elements that haven't been mentioned recently
                if (element_data["importance"] < 2 and 
                    self.current_turn - element_data["last_mentioned_turn"] > 3):
                    continue
                
                # Check if important element is maintained in the response
                if (element_data["importance"] >= 3 and
                    not self._element_is_referenced(element_id, element_data, ai_response)):
                    violations.append(f"Active element '{element_id}' disappeared without explanation")
        
        return violations
    
    def enforce_continuity(self, ai_response, violations):
        """Fix continuity violations in AI response"""
        if not violations:
            return ai_response
            
        # Create continuity enforcement prompt
        enforcement_prompt = f"""
        Your previous response has continuity issues that need to be fixed:
        {', '.join(violations)}
        
        Please rewrite your response to maintain these narrative elements while 
        preserving the core action resolution. Important active elements include:
        {self._format_important_elements()}
        
        Original response:
        {ai_response}
        """
        
        # Get corrected response from AI
        corrected_response = ai_client.generate(enforcement_prompt)
        return corrected_response
```

### 3. Dynamic Options Generation

#### Problem: Options don't adapt to the evolving situation
- Currently: Same 4 options regardless of context
- Goal: Generate contextually appropriate options that reflect the current situation

#### Implementation:
```python
def generate_dynamic_options(context, character, location, story_state, recent_actions):
    """Generate contextually appropriate options based on current game state"""
    
    # Extract key contextual elements
    situation_type = analyze_situation_type(context)
    available_resources = get_character_resources(character)
    location_features = get_location_features(location)
    story_phase = story_state.get("current_phase", "introduction")
    recent_action_types = [action["type"] for action in recent_actions[-3:]]
    
    # Base option categories
    option_categories = [
        "investigation", "social", "combat", "movement", 
        "magic", "stealth", "environmental"
    ]
    
    # Select relevant option categories based on context
    relevant_categories = select_relevant_option_categories(
        option_categories, situation_type, location_features, story_phase
    )
    
    # Generate specific options for each relevant category
    options = []
    for category in relevant_categories:
        # Generate 1-2 options per relevant category
        category_options = generate_category_options(
            category, character, location, situation_type, story_phase
        )
        options.extend(category_options)
    
    # Always include a character-class specific option
    class_option = generate_class_specific_option(character["class"], situation_type)
    options.append(class_option)
    
    # Always include an Emberlyn-assisted option
    emberlyn_option = generate_emberlyn_option(situation_type, story_phase)
    options.append(emberlyn_option)
    
    # Ensure variety from recent actions
    options = ensure_option_variety(options, recent_action_types)
    
    # Select final 4-5 options
    final_options = select_final_options(options, character, story_state)
    
    return final_options
```

### 4. Story Progression Acceleration

#### Problem: Story doesn't progress meaningfully despite many turns
- Currently: 11 turns with minimal story advancement
- Goal: Ensure significant story development by turn 5, climactic moments by turn 20

#### Implementation:
```python
class StoryProgressionManager:
    def __init__(self, story_arc, target_climax_turn=20):
        self.story_arc = story_arc
        self.current_phase = "introduction"
        self.progress_points = 0
        self.target_climax_turn = target_climax_turn
        self.current_turn = 0
        self.phase_thresholds = self._calculate_phase_thresholds()
        
    def _calculate_phase_thresholds(self):
        """Calculate progress thresholds for story phases based on target climax turn"""
        return {
            "introduction": 0,
            "rising_action": self.target_climax_turn * 0.2,  # 20% of target
            "complication": self.target_climax_turn * 0.4,   # 40% of target
            "crisis": self.target_climax_turn * 0.6,         # 60% of target
            "climax": self.target_climax_turn * 0.8,         # 80% of target
            "resolution": self.target_climax_turn            # 100% of target
        }
    
    def advance_turn(self):
        """Track turn progression and force story advancement if needed"""
        self.current_turn += 1
        
        # Calculate expected progress at this turn
        expected_progress = self._calculate_expected_progress()
        
        # If we're falling behind, force progression
        if self.progress_points < expected_progress:
            force_amount = max(1, (expected_progress - self.progress_points) / 2)
            self.add_progress(force_amount, "forced_progression")
            return True, force_amount
        
        return False, 0
    
    def _calculate_expected_progress(self):
        """Calculate how far the story should have progressed by current turn"""
        # Non-linear progression curve - faster at beginning and end
        progress_ratio = self.current_turn / self.target_climax_turn
        
        # Apply acceleration curve (starts slower, accelerates in middle, slows at end)
        if progress_ratio < 0.3:
            # Slower start
            adjusted_ratio = progress_ratio * 0.7
        elif progress_ratio < 0.7:
            # Faster middle
            adjusted_ratio = 0.21 + (progress_ratio - 0.3) * 1.3
        else:
            # Slower end
            adjusted_ratio = 0.73 + (progress_ratio - 0.7) * 0.9
        
        return adjusted_ratio * self.phase_thresholds["resolution"]
    
    def add_progress(self, amount, reason):
        """Add progress points and update story phase if thresholds are crossed"""
        self.progress_points += amount
        
        # Check if we've crossed into a new phase
        for phase, threshold in sorted(
            self.phase_thresholds.items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            if self.progress_points >= threshold and phase != self.current_phase:
                old_phase = self.current_phase
                self.current_phase = phase
                return True, old_phase, phase
        
        return False, self.current_phase, self.current_phase
```

### 5. Location System Overhaul

#### Problem: Location tracking issues and narrative mismatch
- Currently: Technical state shows one location while narrative describes another
- Goal: Ensure location transitions are clear, validated, and reflected in narrative

#### Implementation:
```python
class EnhancedLocationSystem:
    def __init__(self, location_data):
        self.locations = location_data
        self.current_location = "village_outskirts"  # Default starting location
        self.previous_location = None
        self.transition_history = []
        self.location_descriptions = {}  # Cached descriptions
        
    def detect_location_change(self, ai_response, player_action, dice_roll=None):
        """Detect if the AI response indicates a location change"""
        # Extract location keywords from response
        response_lower = ai_response.lower()
        
        # Check for explicit movement indicators
        movement_verbs = ["go", "walk", "travel", "enter", "arrive", "reach", "move"]
        has_movement = any(verb in response_lower for verb in movement_verbs)
        
        if not has_movement:
            return {"location_changed": False, "reason": "No movement detected"}
        
        # Detect target location from response
        target_location = None
        confidence = 0
        
        for loc_id, loc_data in self.locations.items():
            # Skip current location
            if loc_id == self.current_location:
                continue
                
            # Check for location keywords
            loc_keywords = loc_data["keywords"]
            matches = sum(keyword in response_lower for keyword in loc_keywords)
            
            # Calculate confidence based on number of matches
            loc_confidence = matches / len(loc_keywords) if loc_keywords else 0
            
            if loc_confidence > confidence and loc_confidence > 0.3:  # Minimum threshold
                target_location = loc_id
                confidence = loc_confidence
        
        if not target_location:
            return {"location_changed": False, "reason": "No target location detected"}
        
        # Validate connection
        if not self._is_valid_connection(self.current_location, target_location):
            return {
                "location_changed": False,
                "reason": f"Invalid connection: {self.current_location} -> {target_location}",
                "valid_connections": self._get_valid_connections(self.current_location)
            }
        
        # Check if dice roll is needed and provided
        difficulty = self._get_connection_difficulty(self.current_location, target_location)
        if difficulty > 0:
            if not dice_roll:
                return {
                    "location_changed": False,
                    "reason": f"Dice roll required (DC {difficulty})",
                    "dice_needed": True,
                    "target_location": target_location,
                    "difficulty": difficulty
                }
            
            if dice_roll < difficulty:
                return {
                    "location_changed": False,
                    "reason": f"Failed dice roll: {dice_roll} vs DC {difficulty}",
                    "dice_roll": dice_roll,
                    "difficulty": difficulty
                }
        
        # Process valid location change
        self._change_location(target_location, dice_roll)
        
        return {
            "location_changed": True,
            "from": self.previous_location,
            "to": self.current_location,
            "confidence": confidence,
            "dice_roll": dice_roll,
            "difficulty": difficulty
        }
    
    def _change_location(self, new_location, dice_roll=None):
        """Process a location change"""
        self.previous_location = self.current_location
        self.current_location = new_location
        
        # Record transition
        self.transition_history.append({
            "from": self.previous_location,
            "to": new_location,
            "turn": len(self.transition_history) + 1,
            "dice_roll": dice_roll
        })
    
    def enforce_location_consistency(self, ai_response):
        """Ensure AI response correctly reflects the current location"""
        # Check if response mentions the current location
        current_loc_data = self.locations[self.current_location]
        current_loc_keywords = current_loc_data["keywords"]
        
        response_lower = ai_response.lower()
        mentions_current_location = any(keyword in response_lower for keyword in current_loc_keywords)
        
        if mentions_current_location:
            return ai_response  # Already consistent
        
        # Create location enforcement prompt
        enforcement_prompt = f"""
        Your response needs to be updated to clearly reflect the current location:
        {current_loc_data['name']} ({self.current_location})
        
        Key features of this location:
        {current_loc_data['description']}
        
        Please rewrite your response to incorporate these location details while
        preserving the core action resolution and narrative elements.
        
        Original response:
        {ai_response}
        """
        
        # Get corrected response from AI
        corrected_response = ai_client.generate(enforcement_prompt)
        return corrected_response
```

### 6. AI Prompt Engineering for Varied Outcomes

#### Problem: AI responses are repetitive and lack meaningful consequences
- Currently: "Despite your best efforts, the challenge proves difficult" pattern
- Goal: Create varied, engaging responses with clear consequences

#### Implementation:
```python
def generate_action_resolution_prompt(action_data, outcome_type, character, location, story_state):
    """Generate a prompt for AI to create varied, engaging action resolutions"""
    
    # Base prompt structure
    prompt = f"""
    Create an engaging, varied response for a {outcome_type} outcome to the player's {action_data['type']} action.
    
    ## Action Context
    - Action: {action_data['description']}
    - Character: {character['name']}, a {character['race']} {character['class']}
    - Location: {location['name']} - {location['brief_description']}
    - Story Phase: {story_state['current_phase']}
    
    ## Outcome Type: {outcome_type.upper()}
    
    ## Required Elements
    1. Describe the outcome with vivid, specific details (avoid generic descriptions)
    2. Include clear consequences that affect the game world
    3. Reference the specific location and its features
    4. Maintain continuity with previously established elements
    5. Include Emberlyn's reaction to the outcome
    
    ## Prohibited Patterns
    - DO NOT use phrases like "Despite your best efforts" or "The task tests the limits of your abilities"
    - DO NOT use generic failure descriptions
    - ALWAYS provide specific details about what happened and why
    - NEVER contradict established facts about the world or characters
    
    ## Tone Guidelines
    - {outcome_type} outcomes should feel {get_tone_for_outcome(outcome_type)}
    - Maintain the established fantasy atmosphere
    - Keep Emberlyn's personality consistent (helpful, slightly anxious, knowledgeable)
    
    ## Response Format
    *Emberlyn's reaction and description of the outcome*
    
    "Emberlyn's dialogue about what happened and its implications"
    
    *Additional environmental details and consequences*
    """
    
    # Add outcome-specific instructions
    if outcome_type == "spectacular_success":
        prompt += """
        ## Spectacular Success Guidelines
        - Describe how the character exceeds expectations dramatically
        - Include a significant positive consequence or reward
        - Show how this success advances the story in a meaningful way
        - Have Emberlyn express delighted surprise at the outcome
        """
    elif outcome_type == "spectacular_failure":
        prompt += """
        ## Spectacular Failure Guidelines
        - Make the failure dramatic but NOT humiliating
        - Include an unexpected opportunity that arises from the failure
        - Ensure the story can still progress despite this setback
        - Have Emberlyn be supportive rather than critical
        """
    
    return prompt
```

## Technical Implementation Plan

### Phase 1: Core Systems Overhaul (Weeks 1-2)
1. **Action-Outcome Framework**
   - Implement varied outcome categories with clear consequences
   - Create templates for different outcome types
   - Develop state change tracking for outcomes

2. **Narrative Coherence System**
   - Build active elements tracking system
   - Implement continuity violation detection
   - Create continuity enforcement mechanism

### Phase 2: Gameplay Experience Enhancement (Weeks 3-4)
1. **Dynamic Options Generation**
   - Implement context-aware option categories
   - Create class-specific and situation-specific options
   - Ensure option variety across turns

2. **Story Progression Acceleration**
   - Implement non-linear progression curve
   - Create forced progression mechanism
   - Develop phase transition handling

### Phase 3: Location and World Interaction (Weeks 5-6)
1. **Location System Overhaul**
   - Implement enhanced location detection
   - Create location consistency enforcement
   - Develop connection validation system

2. **AI Prompt Engineering**
   - Create templates for varied outcomes
   - Implement prohibited pattern detection
   - Develop tone and style guidelines

### Phase 4: Testing and Refinement (Weeks 7-8)
1. **Comprehensive Testing**
   - Test all systems with varied player inputs
   - Verify story progression reaches meaningful points
   - Ensure location transitions work correctly

2. **Refinement Based on Feedback**
   - Adjust difficulty curves
   - Fine-tune AI prompts
   - Optimize performance

## AI Integration Strategy

### Leveraging Claude's Strengths
1. **Creative Content Generation**
   - Use AI for rich, atmospheric descriptions
   - Generate varied NPC dialogue and personalities
   - Create dynamic environmental storytelling

2. **Narrative Adaptation**
   - Allow AI to adapt story details based on player choices
   - Generate emotional reactions and consequences
   - Create varied descriptions of similar outcomes

### Mitigating Claude's Weaknesses
1. **Strict Technical Controls**
   - Implement state tracking independent of AI
   - Validate all AI outputs against game state
   - Force corrections when continuity is broken

2. **Structured Prompting**
   - Use detailed, structured prompts with clear instructions
   - Explicitly prohibit problematic patterns
   - Provide templates for different outcome types

3. **Fallback Mechanisms**
   - Implement manual fallbacks for critical failures
   - Create template-based responses for common scenarios
   - Develop recovery strategies for incoherent outputs

## Success Metrics

The implementation will be considered successful when:

1. **Player Choice Impact**
   - High-risk actions succeed spectacularly at least 30% of the time
   - Each choice leads to visibly different outcomes
   - Players can see clear consequences of their decisions

2. **Narrative Coherence**
   - Location descriptions match technical location state
   - Important NPCs and threats remain consistent
   - Story elements connect logically across turns

3. **Story Progression**
   - Significant story developments occur by turn 5
   - Story reaches crisis phase by turn 10-12
   - Climactic moments occur around turn 15-20

4. **Technical Performance**
   - Location detection accuracy >95%
   - Continuity violations <5% of responses
   - Prompt engineering reduces generic responses by 90%

## Next Steps

1. Begin implementing the Action-Outcome Framework
2. Develop the Narrative Coherence System
3. Create test cases for varied player inputs
4. Implement the first version of enhanced AI prompts