# 🧪 Experiments Directory

This directory contains experimental features and research projects that are integrated with the core Fire Whisper RPG system but not part of the main production codebase.

## 📁 Structure

```
experiments/
├── looma/                    # AI Guardrails Framework
│   ├── core/                # Core framework components
│   ├── *.py                 # Test files and demos
│   └── README.md            # Framework documentation
├── archived/                # Completed/abandoned experiments
└── README.md               # This file
```

## 🔬 Active Experiments

### Looma - AI Guardrails Framework
- **Purpose**: Abstract Fire Whisper's AI integration patterns into reusable framework
- **Status**: Research/Development
- **Integration**: Uses `sys.path` to access core Fire Whisper components
- **Files**: `experiments/looma/`

## 🗂️ Guidelines for Experiments

### Adding New Experiments
1. Create subdirectory under `experiments/`
2. Include README.md explaining purpose and status
3. Use relative imports to access core system: `sys.path.append('../../src')`
4. Document integration points with main system

### Integration with Core System
- Experiments can import from `src/` using path manipulation
- Core system should NOT import from experiments
- Use configuration flags to enable experimental features in production

### Lifecycle Management
- **Active**: Currently being developed/tested
- **Archived**: Move to `experiments/archived/` when complete/abandoned
- **Graduated**: Move successful experiments to `src/` as production features

## 🚀 Benefits

- ✅ **Separation**: Keeps experimental code separate from production
- ✅ **Integration**: Still has access to core system components  
- ✅ **Organization**: Clear structure for research and development
- ✅ **Safety**: Production code remains clean and stable
- ✅ **Innovation**: Encourages experimentation without risk

## 📋 Current Status

- **looma/**: AI framework research - Active development
- **archived/**: Empty - Ready for completed experiments