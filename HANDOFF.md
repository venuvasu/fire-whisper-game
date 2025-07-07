# 🔄 Developer Handoff Guide

> **New developer taking over Fire Whisper RPG? Start here!**

## 🎯 What You're Inheriting

**Fire Whisper RPG** is an AI-powered text-based RPG where:
- **AI (Claude)** generates story content and dialogue
- **Python code** controls ALL game mechanics (dice, XP, HP, stats)
- **React frontend** provides the user interface
- **AWS Lambda** hosts the production system

### 🔑 Core Principle
**AI does story, code does mechanics.** The AI never controls dice rolls, XP, or game balance.

## 🚀 Get Running in 10 Minutes

### 1. Clone and Setup
```bash
git clone <repository-url>
cd fire-whisper-game
pip install -r backend/requirements.txt
```

### 2. Get API Key
- Sign up at [Anthropic](https://console.anthropic.com/)
- Get Claude API key
- Add to `.env.local`:
```bash
cp .env.example .env.local
# Edit .env.local and add: CLAUDE_API_KEY=your_key_here
```

### 3. Play the Game (IMPORTANT!)
```bash
python3 scripts/play_fire_whisper_custom.py
```
**Play for 10-15 minutes to understand the user experience.**

### 4. See How It Works Internally
```bash
python3 scripts/full_game_flow_test.py
```
This creates a YAML file with complete transcripts showing exactly how the system works.

### 5. Read the Results
```bash
cat test_results/full_game_flow_test_results_*.yaml
```
This shows you:
- Complete character creation process
- Full game transcripts
- AI responses and validation
- Performance metrics

## 📁 Critical Files to Understand

### 🎯 Start With These (in order):

1. **`backend/take_turn_enhanced.py`**
   - Main game logic
   - How player input becomes AI response
   - Where dice rolls happen

2. **`backend/engine/`**
   - Core game mechanics
   - Dice rolling logic
   - XP and HP calculations

3. **`backend/prompts/`**
   - AI behavior control
   - System prompts that guide Claude
   - Constraint definitions

4. **`test_results/README.md`**
   - Latest test findings
   - System behavior analysis

### 🔧 Configuration Files:

- **`.env.local`** - Your API keys and settings
- **`version.json`** - Version tracking and changelog
- **`template.yaml`** - AWS deployment configuration

## 🏗️ Architecture Deep Dive

### Request Flow:
```
Player Input → Lambda Function → Game Engine → AI (Claude) → Validation → Response
```

### Key Components:

1. **Frontend (React)**
   - User interface
   - Sends requests to backend
   - Displays responses

2. **Backend (Python Lambda)**
   - `take_turn_enhanced.py` - Main handler
   - `engine/` - Game mechanics
   - `utils/` - Shared utilities

3. **AI Integration**
   - Claude API for narrative generation
   - Strict prompt engineering
   - Response validation

4. **Data Storage**
   - Character data in DynamoDB
   - Game state management
   - User progress tracking

## 🧪 Testing Strategy

### Test Types:

1. **Full Game Flow Test** (Most Important)
   ```bash
   python3 scripts/full_game_flow_test.py
   ```
   - Complete character creation → saga creation → gameplay
   - Full transcripts in YAML format
   - Shows exactly how everything works

2. **AI Behavior Tests**
   ```bash
   python3 tests/ai_behavior/ai_behavior_validation_test.py
   ```
   - Validates AI constraint compliance
   - Prevents "hallucinations" of game mechanics

3. **Integration Tests**
   ```bash
   python3 tests/automation/test_runner.py
   ```
   - End-to-end system validation
   - Automatic test selection based on changes

### Reading Test Results:

Test results in `test_results/` show:
- **Character Creation**: Full character sheets with all attributes
- **Gameplay Turns**: Player actions and AI responses
- **Quality Analysis**: How well the AI follows constraints
- **Performance Metrics**: Response times and token usage

## 🔄 Development Workflow

### Making Changes:

1. **Small Changes First**
   - Edit prompts in `backend/prompts/`
   - Modify game mechanics in `backend/engine/`
   - Test immediately

2. **Test Your Changes**
   ```bash
   python3 scripts/full_game_flow_test.py
   ```

3. **Version Your Changes**
   ```bash
   python3 scripts/version_manager.py bump-prompt "Updated dialogue constraints"
   ```

4. **Document Findings**
   - Update relevant README files
   - Note any behavior changes

### Version System:
- **MAJOR.MINOR.PROMPT.UI** format
- Bump PROMPT for AI changes
- Bump MINOR for new features
- Bump UI for frontend changes
- Bump MAJOR for architecture changes

## 🚨 Critical Things to Know

### ⚠️ Never Let AI Control Mechanics
- AI should NEVER roll dice
- AI should NEVER calculate XP
- AI should NEVER modify HP/stats
- All mechanics are code-controlled

### 🔍 Always Validate AI Responses
- Check for constraint violations
- Look for "hallucinated" mechanics
- Validate against expected patterns

### 📊 Monitor AI Behavior
- AI can be unpredictable
- Small prompt changes can have big effects
- Always test thoroughly

### 🏷️ Version Everything
- Especially prompt changes
- Track AI behavior over time
- Keep detailed changelogs

## 🛠️ Common Tasks

### Adding New Game Features:
1. Add mechanics to `backend/engine/`
2. Update prompts to guide AI behavior
3. Test with full game flow test
4. Version and document

### Modifying AI Behavior:
1. Edit prompts in `backend/prompts/`
2. Run AI behavior tests
3. Check for constraint violations
4. Version as PROMPT change

### Debugging Issues:
1. Run full game flow test
2. Check YAML output for patterns
3. Look at AI responses for violations
4. Validate game mechanics separately

## 📚 Learning Resources

### Essential Reading:
1. **This file** - Overview and setup
2. **`README.md`** - Comprehensive documentation
3. **`ARCHITECTURE_REDESIGN.md`** - Detailed architecture
4. **`TESTING_WORKFLOW.md`** - Testing procedures
5. **`test_results/README.md`** - Latest findings

### Code Exploration Path:
1. Play the game to understand UX
2. Run tests to see internals
3. Read main handler (`take_turn_enhanced.py`)
4. Explore game engine (`backend/engine/`)
5. Study AI prompts (`backend/prompts/`)
6. Review test results (`test_results/`)

## 🆘 Getting Help

### When Things Break:
1. **Check test results** - Often show what went wrong
2. **Run AI behavior tests** - Catch constraint violations
3. **Review recent changes** - Check version history
4. **Validate mechanics separately** - Isolate AI vs code issues

### Understanding AI Behavior:
1. **Read full transcripts** - In test results YAML files
2. **Compare versions** - See how changes affect behavior
3. **Test edge cases** - AI can behave unexpectedly
4. **Monitor constraints** - Ensure AI follows rules

## ✅ Handoff Checklist

- [ ] Repository cloned and dependencies installed
- [ ] API key configured in `.env.local`
- [ ] Game played and understood from user perspective
- [ ] Full game flow test run successfully
- [ ] Test results reviewed and understood
- [ ] Key files read and architecture understood
- [ ] Small test change made and validated
- [ ] Version system understood and tested
- [ ] Documentation reviewed

## 🎯 Next Steps

1. **Get familiar** - Play and test for a few hours
2. **Make small changes** - Edit prompts, test behavior
3. **Understand patterns** - How AI responds to different inputs
4. **Plan improvements** - Based on test results and user experience
5. **Document everything** - Keep detailed notes of findings

---

**🎮 Welcome to Fire Whisper RPG! The game is yours now - start playing and testing to understand what you've inherited.**