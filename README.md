# 🔥 Fire Whisper RPG

> An AI-powered text-based RPG with deterministic mechanics and intelligent narrative generation

[![Version](https://img.shields.io/badge/version-1.0.0.0-blue.svg)](./version.json)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](./tests/results/)
[![AI Behavior](https://img.shields.io/badge/AI%20behavior-validated-green.svg)](./tests/ai_behavior/)
[![Branch](https://img.shields.io/badge/branch-v1-orange.svg)](https://github.com/echang-home/fire-whisper-game/tree/v1)

## 🎯 **RESTRUCTURING COMPLETE** ✅

**The codebase has been completely restructured for professional development:**
- 🏗️ Clean, readable project structure
- 🧪 Config-driven testing system  
- 👥 Developer-friendly organization
- 📚 Comprehensive documentation

**See [RESTRUCTURING_COMPLETE.md](RESTRUCTURING_COMPLETE.md) for full details.**

## 🚀 **Version 1.0 - Major System Redesign**

This branch represents a complete architectural overhaul of the original Fire Whisper concept, transforming it from separate API/UI components into a unified, AI-integrated RPG system.

### 🔧 **Latest Updates - Core Game Engine Fixes**
- **✅ Fixed State Management**: Location tracking, turn counting, and story progression now work correctly
- **✅ Fixed Choice Processing**: Player choices are properly parsed and responded to
- **✅ Fixed Debug Information**: All game state tracking is visible and accurate
- **✅ Enhanced Story Progression**: Story advances based on meaningful player actions
- **✅ Improved Continuity**: AI responses maintain narrative consistency

### **🔄 What Changed from Original:**
- **🏗️ Unified Architecture**: Merged backend API + frontend into cohesive game system
- **🤖 AI Integration**: Added Claude AI with strict constraint validation
- **🎲 Deterministic Mechanics**: Code-controlled dice rolls and XP, AI handles narrative only
- **🧪 Comprehensive Testing**: AI behavior validation, integration tests, performance testing
- **📦 Dual Deployment**: Local development mode + AWS production deployment
- **🏷️ Smart Versioning**: MAJOR.MINOR.PROMPT.UI versioning for AI-integrated projects
- **🔧 Developer Experience**: Organized project structure, automated test selection, version management

### **🎯 Key Innovations:**
- **AI Constraint System**: Prevents AI from "hallucinating" game mechanics
- **Prompt Versioning**: Track AI behavior changes with dedicated version component
- **Intelligent Testing**: Automatically selects relevant tests based on code changes
- **Environment Management**: Seamless switching between local and AWS modes

## 🎯 Overview

Fire Whisper RPG combines the creativity of AI storytelling with the reliability of deterministic game mechanics. Players experience rich, dynamic narratives while the system maintains strict control over game balance and progression.

### ✨ Key Features
- **🤖 AI-Driven Narratives**: Claude AI generates immersive story content
- **🎲 Deterministic Mechanics**: All dice rolls and XP calculated by code, not AI
- **🛡️ Constraint Validation**: AI behavior is continuously monitored and validated
- **📊 Comprehensive Testing**: Multi-layered testing ensures reliability
- **🏷️ Smart Versioning**: MAJOR.MINOR.PROMPT.UI versioning for AI-integrated projects

## 📋 Table of Contents

- [🚀 Quick Start for New Developers](#-quick-start-for-new-developers)
- [🏗️ Architecture Overview](#️-architecture-overview)
- [🎯 Entry Points](#-entry-points)
- [🧪 Testing Strategy](#-testing-strategy)
- [🔧 Development Setup](#-development-setup)
- [🏷️ Versioning System](#️-versioning-system)
- [📚 Documentation](#-documentation)

## 🚀 Quick Start for New Developers

**New to this codebase? Start here!**

### 1. **Understand What This Is**
Fire Whisper RPG is an AI-powered text-based RPG where:
- **AI (Claude)** generates story content and dialogue
- **Code** controls all game mechanics (dice rolls, XP, stats)
- **Players** make choices and the AI responds with narrative

### 2. **Get It Running in 5 Minutes**
```bash
# 1. Clone and enter directory
git clone <repo-url> && cd fire-whisper-game

# 2. Install Python dependencies
pip install -r backend/requirements.txt

# 3. Set up your API key
cp .env.example .env.local
# Edit .env.local and add: CLAUDE_API_KEY=your_key_here

# 4. Play the game!
python3 scripts/play_fire_whisper_custom.py
```

### 3. **Run Tests to Understand the System**
```bash
# Run comprehensive test with full transcripts
python3 scripts/full_game_flow_test.py

# Check the results (shows how everything works)
cat test_results/full_game_flow_test_results_*.yaml
```

### 4. **Key Files to Read First**
1. **`backend/take_turn_enhanced.py`** - Main game logic
2. **`backend/engine/`** - Core game mechanics
3. **`backend/prompts/`** - AI prompts that control behavior
4. **`test_results/README.md`** - Latest test results and findings

### 5. **Architecture at a Glance**
```
Player Input → Lambda Function → Game Engine → AI (Claude) → Response
     ↑              ↓              ↓           ↓         ↓
  Frontend ←── API Gateway ←── Dice/XP ←── Prompt ←── Validation
```

## 🏗️ Architecture Overview

### System Flow
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   Player    │───▶│   Frontend   │───▶│   Backend   │───▶│   Claude AI  │
│   Input     │    │   (React)    │    │  (Lambda)   │    │  (Narrative) │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
                           │                    │                   │
                           ▼                    ▼                   ▼
                   ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
                   │   UI State   │    │Game Engine  │    │  Validation  │
                   │  Management  │    │(Dice/XP/HP)│    │ & Constraints│
                   └──────────────┘    └─────────────┘    └──────────────┘
```

### Key Principle: **AI for Story, Code for Mechanics**
- **AI (Claude)**: Generates narrative, dialogue, descriptions
- **Code**: Handles all dice rolls, XP calculation, HP tracking, game rules
- **Validation**: Ensures AI never "hallucinates" game mechanics

### Project Structure

```
fire-whisper-game/
├── backend/                    # Python AWS Lambda functions
│   ├── engine/                # Core game mechanics
│   ├── claude_direct/         # AI integration layer
│   ├── utils/                 # Shared utilities
│   └── testing/               # Backend-specific tests
├── frontend/                  # React TypeScript UI
├── tests/                     # Organized test suites
│   ├── ai_behavior/          # AI constraint validation
│   ├── integration/          # Full system tests
│   ├── performance/          # Load and stress tests
│   ├── results/              # Versioned test outputs
│   └── automation/           # Test runners and utilities
├── prompts/                   # Versioned AI prompt templates
├── scripts/                   # Development and deployment scripts
├── docs/                      # Project documentation
└── version.json              # Version tracking and changelog
```

## 🎯 Entry Points

### 🏠 **Local Development**
**Primary Entry Point**: `scripts/local_runner.py`
```bash
python3 scripts/local_runner.py
```
- Complete local game experience without AWS dependencies
- Direct Python execution with debug capabilities
- Character sheet commands and easy exit options

### ☁️ **AWS Production**
**Lambda Function Handlers** (defined in `template.yaml`):

**Core Game Functions:**
- `backend/take_turn.py` → `take_turn.handler` - Main game logic
- `backend/create_saga.py` → `create_saga.handler` - Game creation
- `backend/get_game.py` → `get_game.handler` - Game state retrieval

**Character Management:**
- `backend/create_character.py` → `create_character.handler`
- `backend/get_character.py` → `get_character.handler`
- `backend/update_character_from_game.py` → `update_character_from_game.handler`
- `backend/delete_character.py` → `delete_character.handler`

**User Management:**
- `backend/get_user_data.py` → `get_user_data.handler`

### 🌐 **Frontend**
**React TypeScript Application**:
```bash
npm run dev  # Start development server
```
- Entry point: `frontend/src/main.tsx`
- Vite-powered development environment

### 🧪 **Testing**
**Automated Test Runner**: `tests/automation/test_runner.py`
```bash
python3 tests/automation/test_runner.py
```
- Intelligent test selection based on code changes
- Multiple test categories: AI behavior, integration, performance

### 📦 **Essential Commands**

| Purpose | Command | Description |
|---------|---------|-------------|
| **🎮 Play Game** | `python3 scripts/play_fire_whisper_custom.py` | Interactive gameplay (BEST for learning) |
| **🧪 Run Tests** | `python3 scripts/full_game_flow_test.py` | Comprehensive test with full transcripts |
| **🏠 Local Dev** | `python3 scripts/local_runner.py` | Local development server |
| **☁️ Deploy AWS** | `npm run deploy` | Deploy to production |
| **🌐 Frontend** | `npm run dev` | React development server |
| **📊 Test Results** | `cat test_results/*.yaml` | View latest test results |

## 🏷️ Versioning System

Fire Whisper uses a **MAJOR.MINOR.PROMPT.UI** versioning scheme optimized for AI-integrated projects:

### Version Format: `X.Y.Z.U`

- **X (Major)** — Breaking architectural changes (e.g., new AI model, major system overhaul)
- **Y (Minor)** — New features or flow changes that are backward compatible
- **Z (Prompt)** — Changes to AI prompts or logic that affect AI behavior/output
- **U (UI)** — Pure UI/UX changes (frontend visuals, layout adjustments)

### Examples

| Change | Version Impact |
|--------|----------------|
| Update AI prompt for NPC dialogue | `1.3.4.2` → `1.3.5.2` |
| Add new AI-powered quest system | `1.3.5.2` → `1.4.0.2` |
| Revamp frontend battle UI only | `1.4.0.2` → `1.4.0.3` |
| Migrate from Claude 3 to Claude 4 | `1.4.0.3` → `2.0.0.0` |

### Version Management

```bash
# Check current version
python3 scripts/version_manager.py info

# Bump versions with automatic changelog
python3 scripts/version_manager.py bump-prompt "Updated NPC dialogue constraints"
python3 scripts/version_manager.py bump-minor "Added new combat system"
python3 scripts/version_manager.py bump-ui "Redesigned character sheet layout"
python3 scripts/version_manager.py bump-major "Migrated to GPT-4"
```

## 🧪 Testing Strategy

### Test Categories

#### 🤖 AI Behavior Tests (`tests/ai_behavior/`)
**Purpose**: Validate AI constraint compliance and prevent hallucinations
- **Triggers**: Changes to AI integration, prompts, or constraint logic
- **Tests**: `ai_behavior_validation_test.py`
- **Focus**: Tricky inputs, edge cases, constraint violations

#### 🔗 Integration Tests (`tests/integration/`)
**Purpose**: End-to-end system validation
- **Triggers**: Changes to game engine, mechanics, or core systems
- **Tests**: `hybrid_game_test.py`, `enhanced_game_test.py`, `deterministic_game_test.py`
- **Focus**: Full gameplay flows, character progression, narrative consistency

#### ⚡ Performance Tests (`tests/performance/`)
**Purpose**: Load testing and performance validation
- **Triggers**: Changes to AI integration, backend engine, or API layers
- **Tests**: `comprehensive_stress_test.py`
- **Focus**: Response times, concurrent users, resource usage

### Automated Test Selection

The test runner automatically selects relevant tests based on code changes:

```bash
# Run tests based on git changes (automatic detection)
python3 tests/automation/test_runner.py

# Run specific test categories
python3 tests/automation/test_runner.py ai_behavior integration
python3 tests/automation/test_runner.py performance
```

### Test Results

All test results are versioned and stored in `tests/results/`:
- **Filename**: `test_results_v{version}_{timestamp}.json`
- **Content**: Full test transcripts, AI responses, mechanical results
- **Tracking**: Version tested against, pass/fail status, detailed logs

## 🔧 Development Setup

### Prerequisites
- **Python 3.9+** (check: `python3 --version`)
- **Claude API key** from Anthropic
- **Git** for version control
- **Node.js 16+** (for frontend, optional)

### 🏠 Local Development Setup (Recommended)

### Prerequisites
- Python 3.9+
- Claude API key
- Git

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd fire-whisper-game
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   pip install python-dotenv  # For environment variable management
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local and add your Claude API key
   ```

4. **Test the setup**:
   ```bash
   # Quick test to verify everything works
   python3 scripts/play_fire_whisper_custom.py
   
   # Or run comprehensive test
   python3 scripts/full_game_flow_test.py
   ```

### 🎯 What to Do First

1. **Play the game** to understand user experience:
   ```bash
   python3 scripts/play_fire_whisper_custom.py
   ```

2. **Run tests** to see how it works internally:
   ```bash
   python3 scripts/full_game_flow_test.py
   # Then check: test_results/full_game_flow_test_results_*.yaml
   ```

3. **Read the code** in this order:
   - `backend/take_turn_enhanced.py` (main game logic)
   - `backend/engine/` (game mechanics)
   - `backend/prompts/` (AI behavior control)

4. **Make a small change** and test it:
   - Edit a prompt in `backend/prompts/`
   - Run tests to see the impact
   - Use version manager to track changes

### Local Development Features
- **Direct Python execution** - No AWS dependencies
- **Debug mode** - See dice rolls and mechanical results
- **Fast iteration** - Immediate code changes
- **Character sheet command** - Type 'character' to see stats
- **Easy exit** - Type 'quit' or 'q' to exit

### 🧪 Testing Your Changes

```bash
# Best test for understanding the system
python3 scripts/full_game_flow_test.py

# Quick validation tests
python3 tests/ai_behavior/ai_behavior_validation_test.py

# Automated test selection based on your changes
python3 tests/automation/test_runner.py
```

### 🔍 Understanding Test Results

After running tests, check `test_results/` directory:
- **YAML files**: Complete game transcripts showing AI responses
- **README.md**: Explanation of what was tested
- Look for patterns in AI behavior and game mechanics

---

## ☁️ AWS Production Deployment

### Prerequisites
- AWS CLI installed and configured
- AWS account with appropriate permissions
- All local setup completed

### AWS Configuration

1. **Update environment for AWS**:
   ```bash
   # Edit .env.local and add AWS settings:
   DEPLOYMENT_MODE=aws
   AWS_REGION=us-east-1
   AWS_LAMBDA_FUNCTION_NAME=fire-whisper-game
   AWS_S3_BUCKET=your-bucket-name
   ```

2. **Deploy to AWS**:
   ```bash
   python3 scripts/aws_deploy.py
   ```

### AWS Deployment Features
- **Lambda Functions** - Serverless game logic
- **CloudFormation** - Infrastructure as code
- **Environment Variables** - Secure API key management
- **Auto-scaling** - Handles multiple concurrent players

### AWS Testing

```bash
# Test deployed Lambda function
aws lambda invoke --function-name fire-whisper-game \
  --payload '{"action": "start_game"}' \
  response.json
```

---

## 🔧 Environment Configuration

### Required Variables
```bash
# .env.local
CLAUDE_API_KEY=your_api_key_here
DEPLOYMENT_MODE=local  # or 'aws'
```

### Optional Variables
```bash
# Development
DEBUG_MODE=true
LOG_LEVEL=DEBUG
MAX_TURNS_PER_GAME=100

# AWS (only needed for AWS mode)
AWS_REGION=us-east-1
AWS_LAMBDA_FUNCTION_NAME=fire-whisper-game
AWS_S3_BUCKET=your-bucket
```

### Security Notes
- **Never commit .env.local** - Contains sensitive API keys
- **Use AWS IAM roles** - For production Lambda execution
- **Rotate API keys regularly** - For security best practices

## 🔄 Development Workflow

### For New Developers

1. **Understand the system**: Play the game and run tests
2. **Make small changes**: Start with prompt modifications
3. **Test your changes**: Use `full_game_flow_test.py`
4. **Version your changes**: Use the version manager
5. **Document your findings**: Update relevant docs

### Typical Development Cycle

### 1. Making Changes

When you modify code, the system automatically determines which tests to run:

- **Prompt changes** → AI behavior tests
- **Engine changes** → Integration tests  
- **API changes** → Performance tests
- **Frontend changes** → UI tests (when implemented)

### 2. Version Bumping

After making changes, bump the appropriate version:

```bash
# For AI prompt modifications
python3 scripts/version_manager.py bump-prompt "Improved character dialogue constraints"

# For new game features
python3 scripts/version_manager.py bump-minor "Added magic system"

# For UI improvements
python3 scripts/version_manager.py bump-ui "Enhanced character sheet design"
```

### 3. Testing

Run tests automatically or manually:

```bash
# Automatic test selection based on changes
python3 tests/automation/test_runner.py

# Manual test selection
python3 tests/automation/test_runner.py ai_behavior integration
```

### 4. Results Review

Check test results in `tests/results/` for:
- Detailed test transcripts
- AI response validation
- Performance metrics
- Version compatibility

## 📚 Documentation & Key Files

### 🎯 New Developer? Start Here!

1. **`docs/DEVELOPER_QUICKSTART.md`** - 🔥 **START HERE** - 5-minute developer onboarding
2. **`docs/PROJECT_STRUCTURE.md`** - Clean project organization guide
3. **This README** - Overview and setup
4. **`TROUBLESHOOTING.md`** - Quick fixes for common issues
5. **`tests/results/`** - Latest test results (readable format)
6. **`ARCHITECTURE_REDESIGN.md`** - Detailed system architecture

### 📁 Important Directories

- **`backend/`** - All game logic (Python)
  - `take_turn_enhanced.py` - Main game handler
  - `engine/` - Core mechanics (dice, XP, HP)
  - `prompts/` - AI behavior control
- **`test_results/`** - Latest test outputs with full transcripts
- **`scripts/`** - Development and testing tools
- **`frontend/`** - React UI (optional for backend work)

### 🔧 Configuration Files

- **`version.json`** - Version tracking and changelog
- **`.env.local`** - Your local environment (API keys)
- **`template.yaml`** - AWS deployment configuration
- **`enhanced_system_config.json`** - System configuration

### AI Constraint System

The game uses a sophisticated constraint validation system:

1. **Pre-calculated Mechanics**: All dice rolls and XP awards calculated by code
2. **AI Response Validation**: Real-time detection of constraint violations
3. **Fallback Responses**: Safe responses when AI violates constraints
4. **Continuous Monitoring**: Every AI response is validated against patterns

### Prompt Management

AI prompts are versioned and stored separately:
- **File naming**: `{prompt_name}.v{version}.txt`
- **Version tracking**: Linked to overall system version
- **Change detection**: Prompt changes trigger appropriate tests

## 🤝 Contributing & Handoff Notes

### For New Developers Taking Over

1. **Start with gameplay**: `python3 scripts/play_fire_whisper_custom.py`
2. **Run comprehensive tests**: `python3 scripts/full_game_flow_test.py`
3. **Read test results**: Check `test_results/*.yaml` for full transcripts
4. **Understand the architecture**: AI does story, code does mechanics
5. **Make small changes**: Edit prompts, test, observe behavior

### Development Process

1. **Make your changes**
2. **Test thoroughly**: `python3 scripts/full_game_flow_test.py`
3. **Version your changes**: `python3 scripts/version_manager.py bump-[type] "Description"`
4. **Document findings**: Update relevant README files
5. **Commit with context**: Include test results in commit message

### 🚨 Critical Things to Know

- **Never let AI control game mechanics** (dice, XP, HP)
- **Always validate AI responses** for constraint violations
- **Test changes thoroughly** - AI behavior can be unpredictable
- **Version everything** - Especially prompt changes
- **Keep test results** - They show how the system behaves over time

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎯 TL;DR for New Developers

```bash
# 1. Get it running
git clone <repo> && cd fire-whisper-game
pip install -r backend/requirements.txt
cp .env.example .env.local  # Add your CLAUDE_API_KEY

# 2. Understand it
python3 scripts/play_fire_whisper_custom.py  # Play the game
python3 scripts/full_game_flow_test.py       # See how it works
cat test_results/*.yaml                       # Read the results

# 3. Key files to read
# - backend/take_turn_enhanced.py (main logic)
# - backend/engine/ (game mechanics)
# - backend/prompts/ (AI control)
# - test_results/README.md (latest findings)
```

**🎮 Ready to take over? Start with the game, then the tests!**