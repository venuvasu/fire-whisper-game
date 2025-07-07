# Fire Whisper RPG - Changelog

## [1.1.0] - 2025-07-07 - DICE SYSTEM & REAL CONSEQUENCES

### 🎲 Major Features Added
- **Real Dice Rolling System**: Implemented proper D20 mechanics with difficulty classes
- **Meaningful Action Consequences**: Success/failure now affects character stats and world state
- **Risk/Reward Gameplay**: Eliminated auto-success, players can now fail actions
- **Character Progression Tracking**: Social standing, investigation progress, HP/mana changes
- **Location Progression**: Movement actions can change locations when dice rolls succeed

### 🔧 Technical Improvements
- **New Core Systems**:
  - `src/core/dice_system.py` - Pure randomness D20 system with difficulty classes
  - `src/core/action_system.py` - Action processing with real consequences
  - Enhanced AI integration to use dice results for narrative

### 🏗️ Code Organization
- **File Renames** (for clarity):
  - `enhanced_game_engine_adapter.py` → `game_engine_with_dice_system.py`
  - `smart_action_analyzer.py` → `legacy_action_analyzer.py`
  - `enhanced_narrative_integration.py` → `narrative_enhancer.py`
- **Removed Unused Files**:
  - `enhanced_narrative_integration_broken.py`
  - `ai_integration_legacy.py`
- **Cleanup**: Removed temp files, old logs, cache files

### 🎮 Gameplay Changes
- **Before**: All actions auto-succeeded with no consequences
- **After**: Actions require dice rolls, can fail, have meaningful outcomes
- **Player Experience**: Real tension, meaningful choices, character development

### 🐛 Bug Fixes
- Fixed dice system integration with AI narrative generation
- Fixed mechanical results processing and state application
- Fixed narrative enhancer to handle dictionary-based roll results

### 📋 Known Issues
- **Story Arc Integration**: Still using AI generation instead of 50 predefined story arcs
- **Location Progression**: Dice system works but location transitions need debugging
- **Options Generation**: Still using static options instead of AI-generated contextual choices

### 🎯 Next Priorities
1. Integrate 50 predefined story arcs from `src/ai/prompts/story_arcs.txt`
2. Fix location progression system to enable world exploration
3. Implement AI-generated contextual options based on story state

---

## [1.0.0] - Previous Version
- Initial AI-powered RPG system
- Basic character creation and narrative generation
- AWS deployment infrastructure
- Testing framework