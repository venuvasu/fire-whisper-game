# Fire Whisper Architecture Redesign
## Moving Game Logic from AI to Code

### PROBLEM IDENTIFIED
- AI context drift causes rule violations after 10+ turns
- XP tracking becomes inconsistent
- Dice results get ignored for narrative convenience
- Character progression becomes unreliable
- Game quality degrades with session length

### SOLUTION: HYBRID ARCHITECTURE
**Code Handles:** Mechanics, Rules, State
**AI Handles:** Narrative, Creativity, Flavor

---

## PHASE 1: CORE GAME ENGINE (Priority 1)

### 1.1 Game State Manager
```python
class GameStateManager:
    - track_character_progression()
    - validate_actions()
    - enforce_rules()
    - manage_session_state()
```

### 1.2 Dice System (Deterministic)
```python
class DiceEngine:
    - roll_with_modifiers()
    - calculate_success_thresholds()
    - apply_character_bonuses()
    - log_all_rolls()
```

### 1.3 XP & Progression Engine
```python
class ProgressionEngine:
    - award_xp(amount, reason)
    - check_level_up()
    - unlock_abilities()
    - track_achievements()
```

### 1.4 Character Sheet Engine
```python
class CharacterEngine:
    - enforce_class_restrictions()
    - calculate_derived_stats()
    - manage_resources(hp, energy)
    - validate_character_changes()
```

---

## PHASE 2: AI INTEGRATION LAYER (Priority 2)

### 2.1 Prompt Engineering System
```python
class PromptBuilder:
    - inject_current_game_state()
    - add_mechanical_constraints()
    - format_available_actions()
    - include_dice_results()
```

### 2.2 Response Parser
```python
class ResponseParser:
    - extract_narrative_content()
    - identify_mechanical_actions()
    - validate_ai_compliance()
    - trigger_rule_corrections()
```

### 2.3 Context Manager
```python
class ContextManager:
    - refresh_constraints_every_5_turns()
    - detect_drift_patterns()
    - reset_context_on_violations()
    - maintain_rule_compliance()
```

---

## PHASE 3: ENHANCED GAME FLOW (Priority 3)

### 3.1 Action Resolution Pipeline
```
1. Player Input → Code validates action
2. Code calculates dice/mechanics
3. Code determines outcomes
4. AI generates narrative description
5. Code updates game state
6. AI presents next choices
```

### 3.2 Session Management
```python
class SessionManager:
    - chunk_sessions_into_episodes()
    - save_state_between_chunks()
    - refresh_ai_context()
    - maintain_continuity()
```

---

## IMPLEMENTATION PRIORITY

### IMMEDIATE (Week 1)
- [ ] Dice Engine with deterministic rolls
- [ ] XP Tracking System
- [ ] Character State Validation
- [ ] Basic Game State Manager

### SHORT TERM (Week 2-3)
- [ ] AI Response Parser
- [ ] Prompt Builder with state injection
- [ ] Context Refresh System
- [ ] Action Resolution Pipeline

### MEDIUM TERM (Month 1)
- [ ] Session Chunking System
- [ ] Advanced Progression Engine
- [ ] Achievement System
- [ ] Drift Detection & Correction

---

## TECHNICAL SPECIFICATIONS

### Game State Structure
```json
{
  "character": {
    "name": "string",
    "level": "number",
    "xp": "number",
    "class": "string",
    "stats": {...},
    "resources": {...}
  },
  "session": {
    "turn_count": "number",
    "episode_number": "number",
    "last_context_refresh": "number"
  },
  "mechanics": {
    "pending_rolls": [...],
    "xp_awards": [...],
    "rule_violations": [...]
  }
}
```

### AI Constraint Injection
```python
def build_ai_prompt(game_state, player_action):
    return f"""
GAME STATE (IMMUTABLE):
{format_character_sheet(game_state.character)}

MECHANICAL RESULTS (MUST USE):
{format_dice_results(game_state.pending_rolls)}

PLAYER ACTION: {player_action}

CONSTRAINTS:
- Use ONLY the provided dice results
- Award ONLY the calculated XP amounts
- Present ONLY the validated action choices
- Generate narrative description ONLY

Your response should be pure narrative - no mechanics.
"""
```

---

## BENEFITS OF THIS APPROACH

### 1. Reliability
- Dice rolls always consistent
- XP tracking never drifts
- Character progression guaranteed
- Rules always enforced

### 2. Scalability
- Sessions can be unlimited length
- No context drift issues
- Consistent quality over time
- Predictable behavior

### 3. Debuggability
- All mechanics logged
- State changes tracked
- Rule violations caught
- Easy to test and verify

### 4. Player Trust
- Mechanics are transparent
- Results are fair and consistent
- Progress is always saved correctly
- No "AI cheating" perception

---

## MIGRATION STRATEGY

### Step 1: Parallel Implementation
- Keep current AI system running
- Build new code engine alongside
- Compare outputs for validation

### Step 2: Gradual Transition
- Move dice system first
- Then XP tracking
- Then character progression
- Finally full integration

### Step 3: Enhanced Features
- Add features impossible with pure AI
- Complex character builds
- Detailed combat systems
- Persistent world state

---

## SUCCESS METRICS

### Technical
- Zero XP tracking errors
- 100% dice roll consistency
- No character progression bugs
- Session length unlimited

### Player Experience
- Consistent game quality
- Trustworthy mechanics
- Smooth progression
- No frustrating inconsistencies

### Business
- Higher player retention
- Longer session times
- Better conversion rates
- Positive reviews about reliability