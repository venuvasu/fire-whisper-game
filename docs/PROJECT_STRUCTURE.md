# 🏗️ Fire Whisper RPG - Project Structure

## 📁 Directory Organization

```
fire-whisper-rpg/
├── src/                          # Source code (production)
│   ├── handlers/                 # Lambda function handlers
│   │   ├── character_handler.py  # Character CRUD operations
│   │   ├── game_handler.py       # Game/saga management
│   │   └── gameplay_handler.py   # Turn-based gameplay
│   ├── core/                     # Core game engine
│   │   ├── story_engine.py       # Narrative generation
│   │   ├── dice_system.py        # Dice mechanics
│   │   └── game_state_manager.py # Game state tracking
│   ├── ai/                       # AI integration
│   │   ├── providers/            # AI provider implementations
│   │   ├── prompts/              # System prompts
│   │   └── claude_client.py      # Main AI client
│   ├── data/                     # Data access layer
│   │   ├── characters.py         # Character data operations
│   │   ├── sagas.py              # Game data operations
│   │   └── user_data.py          # User data operations
│   └── utils/                    # Shared utilities
├── config/                       # Configuration files
│   ├── test_configs/             # Test configurations
│   └── deployment/               # Deployment configs
├── tests/                        # Testing framework
│   ├── runners/                  # Test execution scripts
│   ├── fixtures/                 # Test data and mocks
│   ├── results/                  # Test output files
│   └── unit/                     # Unit tests
└── docs/                         # Documentation
```

## 🎯 Design Principles

### **Clear Purpose-Based Organization**
- Each directory has a specific, clear purpose
- File names indicate functionality, not implementation details
- No experimental or temporary files in main structure

### **Developer-Friendly**
- Standard naming conventions
- Logical grouping of related functionality
- Clear separation of concerns
- Easy to navigate and understand

### **Test-Driven Structure**
- Tests are organized by purpose and strategy
- Clear traceability between tests and source code
- Readable output formats for quick diagnosis

## 📋 File Naming Conventions

### **Handlers** (Lambda entry points)
- `character_handler.py` - Character operations
- `game_handler.py` - Game/saga operations  
- `gameplay_handler.py` - Turn-based gameplay

### **Core** (Core game logic)
- `story_engine.py` - Narrative generation
- `dice_system.py` - Dice rolling mechanics
- `game_state_manager.py` - State management

### **AI** (AI integration)
- `claude_client.py` - Main AI interface
- `prompts/` - System prompts organized by function

### **Tests** (Testing framework)
- `run_test.py` - Main test runner
- `{purpose}_{timestamp}.txt` - Test results

## 🧪 Testing Strategy

### **Test Types**
- **Permanent Tests**: Core functionality that must always work
- **Temporary Tests**: Diagnostic tests for specific issues
- **Performance Tests**: Benchmarking and optimization

### **Test Configuration**
Each test is defined by a YAML configuration specifying:
- Purpose and strategy (permanent vs temporary)
- Code files being tested
- Success criteria
- Output format requirements

### **Test Output**
Simple, readable text files with:
- Clear test metadata and code traceability
- Turn-by-turn gameplay transcripts
- Performance metrics and timing
- Success/failure status with details

## 🔄 Development Workflow

1. **Make Changes**: Modify source code in `src/`
2. **Run Tests**: Use `tests/runners/run_test.py <config_name>`
3. **Review Results**: Check readable output in `tests/results/`
4. **Validate**: Ensure all permanent tests still pass
5. **Deploy**: Use deployment configs for production

## 📖 Getting Started

### **For New Developers**
1. Read this document
2. Explore `src/` directory structure
3. Run `python tests/runners/run_test.py --list` to see available tests
4. Run a test: `python tests/runners/run_test.py gameplay_validation`
5. Review test output to understand system behavior

### **For Testing**
1. Choose appropriate test configuration from `config/test_configs/`
2. Run test with `python tests/runners/run_test.py <config_name>`
3. Review readable output in `tests/results/YYYY-MM-DD/`
4. Test results show exactly which code was tested and how it performed

This structure provides a clean, professional codebase that developers can easily understand, navigate, and contribute to.