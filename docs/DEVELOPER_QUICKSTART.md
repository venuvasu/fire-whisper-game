# 🚀 Developer Quick Start Guide

## 🎯 Understanding the Codebase

Fire Whisper RPG is an AI-powered text-based RPG with a clean, purpose-driven architecture.

### **5-Minute Overview**
1. **`src/handlers/`** - Lambda functions (API entry points)
2. **`src/engine/`** - Game mechanics (dice, story, state)
3. **`src/ai/`** - AI integration (Claude API, prompts)
4. **`src/data/`** - Database operations
5. **`tests/`** - Config-driven testing framework

## 🧪 Running Your First Test

```bash
# See all available tests
python tests/runners/run_test.py --list

# Run core gameplay validation
python tests/runners/run_test.py gameplay_validation

# View results (readable text format)
cat tests/results/2025-07-07/core_gameplay_validation_*.txt
```

## 📖 Reading Test Results

Test output is designed to be human-readable:

```
=== FIRE WHISPER RPG TEST RESULTS ===
Test: Core Gameplay Validation
Purpose: Ensure character creation -> saga creation -> gameplay turns work correctly
Git Commit: a1b2c3d4 (main)

CODE FILES UNDER TEST:
  - src/handlers/character_handler.py
  - src/handlers/gameplay_handler.py
  - src/engine/story_engine.py

=== TURN 1 ===
PLAYER: "I examine my surroundings"
AI: *Your boots crunch on autumn leaves...*
DICE: None
TIME: 2.3s
STATUS: Success

=== TURN 2 ===
PLAYER: "I ask Emberlyn for guidance"
AI: *Turning to Emberlyn, you seek her wisdom...*
DICE: Generated 67, needed 55 (SUCCESS)
TIME: 1.8s
STATUS: Success
```

## 🔧 Making Changes

### **Modifying Game Logic**
1. Edit files in `src/engine/` for game mechanics
2. Edit files in `src/ai/` for AI behavior
3. Run `gameplay_validation` test to verify changes
4. Check test output for any issues

### **Adding New Features**
1. Add code to appropriate `src/` directory
2. Update relevant test configuration if needed
3. Run tests to ensure nothing breaks
4. Document changes in code comments

### **Testing Strategy**
- **Permanent Tests**: Must always pass (core functionality)
- **Temporary Tests**: For debugging specific issues
- **Performance Tests**: For optimization work

## 🎮 Understanding Game Flow

```
Player Request → Handler → Engine → AI → Response
     ↓              ↓        ↓      ↓       ↓
   Lambda      Game Logic  Story  Claude  Player
  Function     Dice/XP    Context  API   Receives
```

### **Key Principle**: AI does story, code does mechanics
- AI generates narrative and dialogue
- Code controls all dice rolls, XP, and game balance
- Strict separation prevents AI "hallucinations"

## 📁 Important Files

### **Core Handlers**
- `src/handlers/gameplay_handler.py` - Main game loop
- `src/handlers/character_handler.py` - Character operations
- `src/handlers/game_handler.py` - Game/saga management

### **Game Engine**
- `src/engine/story_engine.py` - Narrative generation
- `src/engine/dice_system.py` - Dice mechanics
- `src/utils/game_manager.py` - Game state management

### **AI Integration**
- `src/ai/claude_client.py` - AI API interface
- `src/ai/prompts/` - System prompts that control AI behavior

### **Testing**
- `config/test_configs/` - Test configurations
- `tests/runners/run_test.py` - Main test runner
- `tests/results/` - Test output files

## 🚨 Common Issues

### **Test Failures**
1. Check test output file for specific error
2. Verify all files under test exist
3. Ensure API keys are configured
4. Run simpler tests first to isolate issues

### **AI Constraint Violations**
1. Run `ai_constraint_validation` test
2. Check if AI is trying to control dice/XP
3. Review AI prompts in `src/ai/prompts/`
4. Ensure proper separation of concerns

### **Performance Issues**
1. Run `performance_benchmark` test
2. Check response times in test output
3. Look for bottlenecks in API calls
4. Consider caching or optimization

## 🎯 Next Steps

1. **Explore the code**: Start with `src/handlers/gameplay_handler.py`
2. **Run tests**: Try different test configurations
3. **Read test outputs**: Understand how the system behaves
4. **Make small changes**: Edit prompts or game logic
5. **Test your changes**: Verify everything still works

## 💡 Pro Tips

- **Always run tests** after making changes
- **Read test outputs** to understand system behavior
- **Use meaningful commit messages** (they appear in test results)
- **Keep changes small** and test frequently
- **Document your changes** in code comments

The codebase is designed to be developer-friendly. If something is confusing or hard to find, that's a bug in our organization - let us know!