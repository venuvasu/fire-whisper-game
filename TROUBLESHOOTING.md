# 🔧 Troubleshooting Guide

> Quick solutions for common issues when taking over Fire Whisper RPG

## 🚨 Setup Issues

### "Module not found" errors
```bash
# Install all dependencies
pip install -r backend/requirements.txt
pip install python-dotenv anthropic pyyaml

# If still failing, try:
pip install --upgrade pip
pip install -r backend/requirements.txt --force-reinstall
```

### "API key not found" errors
```bash
# Check your .env.local file exists
ls -la .env.local

# Should contain:
CLAUDE_API_KEY=your_key_here

# Test API key:
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv('.env.local')
print('API Key:', os.getenv('CLAUDE_API_KEY')[:10] + '...')
"
```

### "Permission denied" on scripts
```bash
# Make scripts executable
chmod +x scripts/*.py

# Or run with python3 explicitly
python3 scripts/play_fire_whisper_custom.py
```

## 🎮 Game Issues

### Game won't start
```bash
# Test basic functionality
python3 -c "
import sys
sys.path.append('backend')
from local_mocks import mock_claude_local
print('Mocks loaded successfully')
"

# If that works, try:
python3 scripts/play_fire_whisper_custom.py
```

### AI responses seem broken
```bash
# Run AI behavior test
python3 tests/ai_behavior/ai_behavior_validation_test.py

# Check for constraint violations in output
# Look for patterns like AI trying to roll dice
```

### Character creation fails
```bash
# Test character creation directly
python3 -c "
import sys, os
sys.path.append('backend')
os.chdir('backend')
from create_character import handler
print('Character creation module loaded')
"
```

## 🧪 Testing Issues

### Tests fail to run
```bash
# Check Python path
python3 -c "import sys; print(sys.path)"

# Run from correct directory
cd fire-whisper-game
python3 scripts/full_game_flow_test.py
```

### No test results generated
```bash
# Check if test_results directory exists
mkdir -p test_results

# Run test with verbose output
python3 scripts/full_game_flow_test.py 2>&1 | tee test_output.log
```

### YAML files unreadable
```bash
# Install YAML support
pip install pyyaml

# Test YAML reading
python3 -c "
import yaml
with open('test_results/full_game_flow_test_results_*.yaml', 'r') as f:
    data = yaml.safe_load(f)
    print('YAML loaded successfully')
"
```

## 🔍 Understanding Issues

### AI behavior seems random
**This is normal!** AI can be unpredictable. Check:
1. **Prompts** - Are they clear and specific?
2. **Constraints** - Are they being enforced?
3. **Test results** - Do they show patterns?

### Game mechanics not working
Check the separation:
- **AI should only generate story text**
- **Code should handle all dice, XP, HP**
- Look for constraint violations in test results

### Version confusion
```bash
# Check current version
python3 scripts/version_manager.py info

# See version history
cat version.json
```

## 📊 Debugging Workflow

### When something breaks:

1. **Run full game flow test**
   ```bash
   python3 scripts/full_game_flow_test.py
   ```

2. **Check the YAML output**
   ```bash
   cat test_results/full_game_flow_test_results_*.yaml | grep -A5 -B5 "error\|fail\|exception"
   ```

3. **Test components separately**
   ```bash
   # Test AI integration
   python3 tests/ai_behavior/ai_behavior_validation_test.py
   
   # Test game mechanics
   python3 -c "
   import sys
   sys.path.append('backend')
   from engine import dice_roller
   print('Dice roll:', dice_roller.roll_d20())
   "
   ```

4. **Check recent changes**
   ```bash
   git log --oneline -10
   git diff HEAD~1
   ```

## 🆘 Emergency Recovery

### If everything is broken:
```bash
# Reset to known good state
git stash
git checkout main  # or last known good commit

# Clean install
rm -rf __pycache__ backend/__pycache__
pip uninstall -y -r backend/requirements.txt
pip install -r backend/requirements.txt

# Test basic functionality
python3 scripts/play_fire_whisper_custom.py
```

### If AI is misbehaving:
1. Check `backend/prompts/` for recent changes
2. Run AI behavior validation tests
3. Look for constraint violations in test results
4. Revert prompt changes if needed

### If tests are failing:
1. Check Python environment and dependencies
2. Verify API key is working
3. Run tests individually to isolate issues
4. Check test_results directory permissions

## 📞 Getting More Help

### Useful Commands for Diagnosis:
```bash
# System info
python3 --version
pip list | grep -E "(anthropic|yaml|dotenv)"

# Environment check
env | grep -E "(CLAUDE|API)"

# File permissions
ls -la scripts/
ls -la backend/

# Recent activity
git log --oneline -5
git status
```

### Log Analysis:
```bash
# Find errors in test output
grep -i error test_results/*.yaml
grep -i fail test_results/*.yaml

# Check AI responses for issues
grep -A10 -B10 "ai_response" test_results/*.yaml | head -50
```

### Performance Issues:
```bash
# Check API response times
grep "response_time" test_results/*.yaml

# Monitor token usage
grep "tokens" test_results/*.yaml
```

---

**💡 Remember: When in doubt, run the full game flow test and read the YAML output. It shows exactly what's happening in the system.**