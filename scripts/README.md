# Fire Whisper RPG Scripts

This directory contains various scripts for testing, deployment, and running the Fire Whisper RPG system.

## Testing Scripts

### `full_game_flow_test.py` ⭐ **Main Test Script**
Comprehensive end-to-end testing with full character creation, saga creation, and multiple gameplay turns. Outputs detailed YAML results with complete transcripts.

### `test_local_fire_whisper.py`
Local testing script for Fire Whisper RPG functionality.

### `test_real_ai_integration.py` / `test_real_ai_integration_fixed.py`
Scripts for testing real AI integration with the Claude API.

## Demo & Play Scripts

### `play_fire_whisper_custom.py` ⭐ **Main Play Script**
Interactive script to play Fire Whisper RPG locally with custom characters.

### `fire_whisper_local_demo.py`
Local demonstration of Fire Whisper RPG capabilities.

### `final_system_demo.py`
Comprehensive system demonstration script.

### `standalone_demo.py`
Standalone demo that doesn't require AWS infrastructure.

### `context_demo_with_mock_responses.py`
Demonstrates context strategies with mock responses.

## Game Play Scripts

### `play_enhanced_fire_whisper.py`
Enhanced version of the Fire Whisper RPG player.

### `play_real_fire_whisper.py` / `play_real_game.py`
Scripts for playing with real AI integration.

### `play_game.py`
Basic game playing script.

## Deployment Scripts

### `aws_deploy.py`
AWS deployment automation script.

### `deploy_enhanced_system.py`
Enhanced system deployment script.

### `deploy_safe_enhancement.py`
Safe deployment script with rollback capabilities.

## Utility Scripts

### `local_runner.py` / `new_local_runner.py`
Local development runners for testing without AWS.

### `version_manager.py`
Version management utilities.

## Recommended Usage

1. **For Testing**: Use `full_game_flow_test.py` for comprehensive testing
2. **For Playing**: Use `play_fire_whisper_custom.py` for interactive gameplay
3. **For Demos**: Use `fire_whisper_local_demo.py` for demonstrations
4. **For Deployment**: Use `deploy_safe_enhancement.py` for production deployments

## Dependencies

Most scripts require:
- Python 3.8+
- Anthropic API key
- Local mock dependencies (in `backend/local_mocks/`)
- Fire Whisper RPG backend modules