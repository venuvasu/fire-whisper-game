# Fire Whisper RPG - Developer Guide

## Introduction

This guide is intended for developers who want to contribute to the Fire Whisper RPG project. It covers the development environment setup, coding standards, testing guidelines, and common development tasks.

## Development Environment Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-organization/fire-whisper-game.git
cd fire-whisper-game
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env.local` file in the project root with the following content:

```
CLAUDE_API_KEY=your_claude_api_key
DEBUG_MODE=true
```

Replace `your_claude_api_key` with your actual Claude API key.

### Running the Game

#### CLI Interface

To run the game using the CLI interface:

```bash
python -m src.client.cli.game_cli new --character "Warrior" --saga "The Last Dragon's Quest"
```

#### Web Interface

To run the game using the web interface:

```bash
python backend_server.py
```

Then open your browser and navigate to `http://localhost:5000`.

## Project Structure

The project follows a domain-driven design approach with clear separation of concerns. See [Code Organization](../architecture/code_organization.md) for details on the folder structure and organization.

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use docstrings for all modules, classes, and functions

### Naming Conventions

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions and methods: `snake_case`
- Variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

### Import Organization

Organize imports in the following order:

1. Standard library imports
2. Third-party imports
3. Local application imports

Within each group, sort imports alphabetically.

Example:

```python
import os
import sys
from typing import Dict, List, Any

import requests
from flask import Flask

from .module import Class
from ..other_module import function
```

### Documentation

- All modules should have a module-level docstring explaining the purpose of the module
- All classes should have a class-level docstring explaining the purpose and usage of the class
- All public methods and functions should have docstrings explaining:
  - Purpose
  - Parameters
  - Return values
  - Exceptions raised
  - Examples (if applicable)

Example:

```python
def process_action(self, action_input: str) -> ActionResult:
    """
    Process a player action and return the result
    
    Args:
        action_input: Player action text
        
    Returns:
        Result of the action
        
    Raises:
        ValueError: If the action is invalid
        
    Example:
        >>> result = process_action("examine area")
        >>> result.success
        True
    """
    # Implementation
```

## Testing Guidelines

### Test Organization

- Unit tests should be placed in the `tests/unit` directory
- Integration tests should be placed in the `tests/integration` directory
- End-to-end tests should be placed in the `tests/e2e` directory
- Test fixtures should be placed in the `tests/fixtures` directory

### Test Naming

- Test files should be named `test_module_name.py`
- Test classes should be named `TestClassName`
- Test methods should be named `test_method_name`

### Running Tests

To run all tests:

```bash
pytest
```

To run specific tests:

```bash
pytest tests/unit/test_module.py
pytest tests/unit/test_module.py::TestClass::test_method
```

### Test Coverage

To run tests with coverage:

```bash
pytest --cov=src
```

## Common Development Tasks

### Adding a New Domain Component

1. Create a new interface in the appropriate domain directory:

```python
# src/domain/new_domain/new_component_interface.py
from abc import ABC, abstractmethod

class NewComponentInterface(ABC):
    @abstractmethod
    def method(self):
        pass
```

2. Create an implementation of the interface:

```python
# src/domain/new_domain/new_component.py
from .new_component_interface import NewComponentInterface

class NewComponent(NewComponentInterface):
    def method(self):
        # Implementation
        pass
```

3. Add unit tests for the component:

```python
# tests/unit/domain/new_domain/test_new_component.py
import unittest
from src.domain.new_domain.new_component import NewComponent

class TestNewComponent(unittest.TestCase):
    def test_method(self):
        component = NewComponent()
        result = component.method()
        # Assertions
```

### Adding a New Application Service

1. Create a new service interface in the application services directory:

```python
# src/application/services/new_service_interface.py
from abc import ABC, abstractmethod

class NewServiceInterface(ABC):
    @abstractmethod
    def method(self):
        pass
```

2. Create an implementation of the service:

```python
# src/application/services/new_service.py
from .new_service_interface import NewServiceInterface

class NewService(NewServiceInterface):
    def method(self):
        # Implementation
        pass
```

3. Add unit tests for the service:

```python
# tests/unit/application/services/test_new_service.py
import unittest
from src.application.services.new_service import NewService

class TestNewService(unittest.TestCase):
    def test_method(self):
        service = NewService()
        result = service.method()
        # Assertions
```

### Adding a New Client Interface

1. Create a new client interface in the client directory:

```python
# src/client/new_client/new_client.py
from ...application.services.game_service import GameService

class NewClient:
    def __init__(self):
        self.game_service = GameService()
    
    def run(self):
        # Implementation
```

2. Add unit tests for the client:

```python
# tests/unit/client/new_client/test_new_client.py
import unittest
from src.client.new_client.new_client import NewClient

class TestNewClient(unittest.TestCase):
    def test_run(self):
        client = NewClient()
        # Assertions
```

## Troubleshooting

### Common Issues

#### AI API Key Issues

If you encounter issues with the Claude API key:

1. Check that your API key is correctly set in the `.env.local` file
2. Verify that the API key is valid and has the necessary permissions
3. Check the Claude API status for any service disruptions

#### Game Engine Issues

If you encounter issues with the game engine:

1. Check the game state for inconsistencies
2. Verify that all required components are properly initialized
3. Check for any exceptions in the logs

#### Story Engine Issues

If you encounter issues with the story engine:

1. Check the AI client for any errors
2. Verify that the prompts are correctly formatted
3. Check for any exceptions in the logs

### Debugging

To enable debug mode:

1. Set the `DEBUG_MODE` environment variable to `true` in your `.env.local` file
2. Run the game with the `--debug` flag (CLI interface)
3. Check the logs for debug information

## Contributing

### Pull Request Process

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Add tests for your changes
5. Update documentation as needed
6. Run the tests to ensure they pass
7. Submit a pull request

### Code Review Process

All pull requests will be reviewed by at least one maintainer. The review process includes:

1. Code quality review
2. Test coverage review
3. Documentation review
4. Functionality review

### Release Process

1. Update the version number in `version.json`
2. Update the changelog
3. Create a new release tag
4. Build and publish the release

## Resources

- [Code Organization](../architecture/code_organization.md)
- [System Architecture](../architecture/system_architecture.md)
- [API Documentation](../api/README.md)
- [User Guide](../guides/user_guide.md)