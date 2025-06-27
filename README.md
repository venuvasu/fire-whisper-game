# 🔥 Fire Whisper RPG

> An AI-powered text-based RPG with deterministic mechanics and intelligent narrative generation

[![Version](https://img.shields.io/badge/version-1.0.0.0-blue.svg)](./version.json)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](./tests/results/)
[![AI Behavior](https://img.shields.io/badge/AI%20behavior-validated-green.svg)](./tests/ai_behavior/)
[![Branch](https://img.shields.io/badge/branch-v1-orange.svg)](https://github.com/echang-home/fire-whisper-game/tree/v1)

## 🚀 **Version 1.0 - Major System Redesign**

This branch represents a complete architectural overhaul of the original Fire Whisper concept, transforming it from separate API/UI components into a unified, AI-integrated RPG system.

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

- [🏗️ Project Structure](#️-project-structure)
- [🏷️ Versioning System](#️-versioning-system)
- [🧪 Testing Strategy](#-testing-strategy)
- [🚀 Getting Started](#-getting-started)
- [🔧 Development Workflow](#-development-workflow)
- [📚 Documentation](#-documentation)

## 🏗️ Project Structure

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

## 🚀 Getting Started

Fire Whisper RPG supports two operation modes:

### 🏠 **Local Mode (Development)**
Run the game locally for development and testing

### ☁️ **AWS Mode (Production)**
Deploy to AWS Lambda for scalable production use

---

## 🏠 Local Development Setup

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

4. **Run the game locally**:
   ```bash
   python3 scripts/local_runner.py
   ```

### Local Development Features
- **Direct Python execution** - No AWS dependencies
- **Debug mode** - See dice rolls and mechanical results
- **Fast iteration** - Immediate code changes
- **Character sheet command** - Type 'character' to see stats
- **Easy exit** - Type 'quit' or 'q' to exit

### Local Testing

```bash
# Test AI behavior validation
python3 tests/ai_behavior/ai_behavior_validation_test.py

# Run all tests with automatic selection
python3 tests/automation/test_runner.py

# Run specific test categories
python3 tests/automation/test_runner.py ai_behavior integration
```

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

## 🔧 Development Workflow

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

## 📚 Documentation

### Key Files

- **`version.json`** - Version tracking and changelog
- **`prompts/`** - Versioned AI prompt templates
- **`tests/results/`** - Historical test results
- **`TESTING_WORKFLOW.md`** - Detailed testing procedures
- **`ARCHITECTURE_REDESIGN.md`** - System architecture overview

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

## 🤝 Contributing

1. Make your changes
2. Run relevant tests: `python3 tests/automation/test_runner.py`
3. Bump version: `python3 scripts/version_manager.py bump-[type] "Description"`
4. Commit with version tag: `git tag v{version}`
5. Submit PR with test results

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🎮 Ready to play? Run the tests and start your adventure!**