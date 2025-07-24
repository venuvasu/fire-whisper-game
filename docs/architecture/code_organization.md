# Fire Whisper RPG - Code Organization

## Overview

This document describes the code organization of the Fire Whisper RPG codebase. The codebase follows a domain-driven design approach with clear separation of concerns and well-defined interfaces between components.

## Architecture

The codebase is organized into four main layers:

1. **Domain Layer** - Core game logic and business rules
2. **Application Layer** - Orchestration and coordination of domain components
3. **Infrastructure Layer** - External services and technical concerns
4. **Client Layer** - User interfaces and presentation logic

### Layer Dependencies

```
Client Layer → Application Layer → Domain Layer
                                 ↘
                       Infrastructure Layer
```

- The Domain Layer has no dependencies on other layers
- The Application Layer depends on the Domain Layer
- The Infrastructure Layer depends on the Domain Layer
- The Client Layer depends on the Application Layer

## Folder Structure

```
fire-whisper-game/
├── .github/                    # GitHub workflows and templates
├── .kiro/                      # Kiro-specific files
│   ├── specs/                  # Feature specifications
│   └── steering/               # Steering files
├── docs/                       # Documentation
│   ├── api/                    # API documentation
│   ├── architecture/           # Architecture documentation
│   ├── guides/                 # User and developer guides
│   └── tutorials/              # Tutorials
├── scripts/                    # Utility scripts
├── src/                        # Source code
│   ├── client/                 # Client interfaces
│   │   ├── cli/                # Command-line interface
│   │   └── web/                # Web interface
│   ├── application/            # Application layer
│   │   ├── controllers/        # Game controllers
│   │   ├── services/           # Application services
│   │   └── dto/                # Data transfer objects
│   ├── domain/                 # Domain layer
│   │   ├── game/               # Game engine and core mechanics
│   │   ├── story/              # Story engine and narrative systems
│   │   ├── character/          # Character systems
│   │   ├── combat/             # Combat systems
│   │   └── world/              # World systems (locations, items, etc.)
│   ├── infrastructure/         # Infrastructure layer
│   │   ├── ai/                 # AI client and integration
│   │   ├── persistence/        # Data storage
│   │   ├── external/           # External service integration
│   │   └── logging/            # Logging and monitoring
│   └── utils/                  # Utility functions and helpers
├── tests/                      # Test code
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   ├── e2e/                    # End-to-end tests
│   └── fixtures/               # Test fixtures
├── experiments/                # Experimental code (clearly separated)
│   └── archived/               # Archived experiments
├── config/                     # Configuration files
├── logs/                       # Log files
├── .gitignore                  # Git ignore file
├── README.md                   # Project README
├── requirements.txt            # Python dependencies
└── setup.py                    # Package setup
```

## Domain Layer

The Domain Layer contains the core game logic and business rules. It is organized into several domains:

### Game Domain

The Game Domain contains the core game engine and mechanics:

- `GameEngineInterface` - Interface for the game engine
- `GameEngine` - Implementation of the game engine
- `ActionType` - Enum for action types
- `ActionResult` - Result of a player action

### Story Domain

The Story Domain contains the story engine and narrative systems:

- `StoryEngineInterface` - Interface for the story engine
- `StoryEngine` - Implementation of the story engine

### Character Domain

The Character Domain contains character-related systems:

- Character creation
- Character progression
- Character attributes and skills

### Combat Domain

The Combat Domain contains combat-related systems:

- Combat mechanics
- Damage calculation
- Combat resolution

### World Domain

The World Domain contains world-related systems:

- Locations
- Items
- NPCs
- Quests

## Application Layer

The Application Layer orchestrates and coordinates the domain components:

### Controllers

- `GameController` - Orchestrates game flow and integrates domain components

### Services

- `GameServiceInterface` - Interface for the game service
- `GameService` - Implementation of the game service
- `PlayerServiceInterface` - Interface for the player service

### DTOs

- `GameStateDTO` - Data transfer object for game state
- `PlayerActionDTO` - Data transfer object for player action
- `GameResponseDTO` - Data transfer object for game response
- `CharacterDTO` - Data transfer object for character data
- `SagaDTO` - Data transfer object for saga data

## Infrastructure Layer

The Infrastructure Layer contains external services and technical concerns:

### AI

- `AIClientInterface` - Interface for the AI client
- `ClaudeAIClient` - Implementation of the AI client for Claude

### Persistence

- Data storage and retrieval
- Save/load functionality

### External

- Integration with external services

### Logging

- Logging and monitoring

## Client Layer

The Client Layer contains user interfaces and presentation logic:

### CLI

- `GameCLI` - Command-line interface for the game

### Web

- Web interface for the game

## Naming Conventions

### File Naming

- Python modules: `snake_case.py`
- Test files: `test_module_name.py`
- Configuration files: `descriptive_config_name.json/yaml`
- Documentation files: `descriptive-name.md`

### Class Naming

- Classes: `PascalCase`
- Follow domain-driven naming: `EntityName`, `ServiceName`, `RepositoryName`
- Abstract classes/interfaces: `AbstractName` or `NameInterface`

### Function and Method Naming

- Functions and methods: `snake_case`
- Use verb phrases that describe behavior: `calculate_damage`, `process_turn`, `generate_response`
- Private methods: `_method_name` (single underscore prefix)

### Variable Naming

- Variables: `snake_case`
- Boolean variables: use prefixes like `is_`, `has_`, `should_`: `is_active`, `has_permission`
- Collections: use plural names: `users`, `items`, `locations`
- Constants: `UPPER_SNAKE_CASE`

## Interface Design

The codebase follows a clear interface-based design to ensure loose coupling between components:

- Domain interfaces define the contract for domain components
- Application service interfaces define the contract for application services
- Infrastructure interfaces define the contract for infrastructure components

This approach allows for easy substitution of implementations and facilitates testing.

## Error Handling

The codebase follows a consistent error handling strategy:

- Domain exceptions for domain rule violations
- Application exceptions for application-level errors
- Infrastructure exceptions for external service failures
- Client exceptions for user interface errors

## Testing Strategy

The codebase follows a comprehensive testing strategy:

- Unit tests for individual components
- Integration tests for component interactions
- End-to-end tests for complete workflows
- Test fixtures for common test data

## Documentation

The codebase includes comprehensive documentation:

- Module docstrings for module purpose and usage
- Class docstrings for class purpose and usage
- Method docstrings for method purpose, parameters, and return values
- Architecture documentation for high-level design
- API documentation for public APIs
- User guides for end users
- Developer guides for developers