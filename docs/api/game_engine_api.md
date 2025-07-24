# Game Engine API

The Game Engine API provides access to the core game mechanics and state management. It is defined by the `GameEngineInterface` class.

## GameEngineInterface

```python
class GameEngineInterface(ABC):
    """Interface for the game engine component"""
    
    @abstractmethod
    def get_current_location(self) -> Any:
        """
        Get the current location data
        
        Returns:
            Location data object
        """
        pass
    
    @abstractmethod
    def get_available_actions(self) -> List[Dict[str, Any]]:
        """
        Get available actions based on current location and state
        
        Returns:
            List of available actions
        """
        pass
    
    @abstractmethod
    def process_action(self, action_input: str) -> ActionResult:
        """
        Process a player action and return the result
        
        Args:
            action_input: Player action text
            
        Returns:
            Result of the action
        """
        pass
    
    @abstractmethod
    def get_ai_context(self) -> Dict[str, Any]:
        """
        Get structured context for AI narrative generation
        
        Returns:
            Dictionary containing context information for AI
        """
        pass
    
    @abstractmethod
    def get_game_state_summary(self) -> str:
        """
        Get human-readable game state summary
        
        Returns:
            String summary of the current game state
        """
        pass
    
    @abstractmethod
    def save_game_state(self) -> Dict[str, Any]:
        """
        Export current game state for saving
        
        Returns:
            Dictionary containing game state data
        """
        pass
    
    @abstractmethod
    def load_game_state(self, save_data: Dict[str, Any]) -> None:
        """
        Load game state from save data
        
        Args:
            save_data: Dictionary containing game state data
        """
        pass
```

## ActionType

```python
class ActionType(Enum):
    """Types of actions a player can take"""
    EXAMINE = "examine"
    MOVE = "move"
    COMBAT = "combat"
    SOCIAL = "social"
    USE_ITEM = "use_item"
    WAIT = "wait"
```

## ActionResult

```python
class ActionResult:
    """Result of a player action"""
    
    def __init__(
        self,
        success: bool,
        action_type: ActionType,
        description: str,
        discoveries: List[str] = None,
        state_changes: Dict[str, Any] = None,
        narrative_focus: List[str] = None,
        next_options: List[str] = None,
        requires_dice_roll: bool = False,
        dice_result: Optional[Dict] = None
    ):
        self.success = success
        self.action_type = action_type
        self.description = description
        self.discoveries = discoveries or []
        self.state_changes = state_changes or {}
        self.narrative_focus = narrative_focus or []
        self.next_options = next_options or []
        self.requires_dice_roll = requires_dice_roll
        self.dice_result = dice_result
```

## Methods

### get_current_location

```python
def get_current_location(self) -> Any:
    """
    Get the current location data
    
    Returns:
        Location data object
    """
```

This method returns the current location data. The location data object contains information about the current location, such as its name, description, exits, and special features.

Example:

```python
location = game_engine.get_current_location()
print(f"Current location: {location.name}")
```

### get_available_actions

```python
def get_available_actions(self) -> List[Dict[str, Any]]:
    """
    Get available actions based on current location and state
    
    Returns:
        List of available actions
    """
```

This method returns a list of available actions based on the current location and game state. Each action is represented as a dictionary with the following keys:

- `id`: Unique identifier for the action
- `text`: Human-readable description of the action
- `type`: Type of action (examine, move, combat, social, use_item, wait)
- `risk`: Risk level of the action (none, low, medium, high)

Example:

```python
actions = game_engine.get_available_actions()
for action in actions:
    print(f"{action['text']} ({action['risk']})")
```

### process_action

```python
def process_action(self, action_input: str) -> ActionResult:
    """
    Process a player action and return the result
    
    Args:
        action_input: Player action text
        
    Returns:
        Result of the action
    """
```

This method processes a player action and returns the result. The action input can be a free-form text string or a specific action ID. The method parses the input, determines the appropriate action to take, and returns an `ActionResult` object with the outcome.

Example:

```python
result = game_engine.process_action("examine area")
if result.success:
    print(f"Success! {result.description}")
else:
    print(f"Failed: {result.description}")
```

### get_ai_context

```python
def get_ai_context(self) -> Dict[str, Any]:
    """
    Get structured context for AI narrative generation
    
    Returns:
        Dictionary containing context information for AI
    """
```

This method returns a structured context for AI narrative generation. The context includes information about the current location, game state, and immediate context (enemies, NPCs, items, special features).

Example:

```python
context = game_engine.get_ai_context()
narrative = story_engine.generate_narrative(context)
```

### get_game_state_summary

```python
def get_game_state_summary(self) -> str:
    """
    Get human-readable game state summary
    
    Returns:
        String summary of the current game state
    """
```

This method returns a human-readable summary of the current game state. The summary includes information about the current turn, location, situation, and any active threats.

Example:

```python
summary = game_engine.get_game_state_summary()
print(f"Game state: {summary}")
```

### save_game_state

```python
def save_game_state(self) -> Dict[str, Any]:
    """
    Export current game state for saving
    
    Returns:
        Dictionary containing game state data
    """
```

This method exports the current game state for saving. The returned dictionary contains all the necessary information to restore the game state later.

Example:

```python
save_data = game_engine.save_game_state()
with open("save_game.json", "w") as f:
    json.dump(save_data, f)
```

### load_game_state

```python
def load_game_state(self, save_data: Dict[str, Any]) -> None:
    """
    Load game state from save data
    
    Args:
        save_data: Dictionary containing game state data
    """
```

This method loads the game state from save data. The save data should be in the format returned by `save_game_state`.

Example:

```python
with open("save_game.json", "r") as f:
    save_data = json.load(f)
game_engine.load_game_state(save_data)
```

## Usage Example

```python
# Create a game engine
game_engine = GameEngine()

# Get the current location
location = game_engine.get_current_location()
print(f"Current location: {location.name}")

# Get available actions
actions = game_engine.get_available_actions()
for i, action in enumerate(actions, 1):
    print(f"{i}. {action['text']} ({action['risk']})")

# Process a player action
result = game_engine.process_action("examine area")
if result.success:
    print(f"Success! {result.description}")
    if result.discoveries:
        print(f"Discoveries: {', '.join(result.discoveries)}")
else:
    print(f"Failed: {result.description}")

# Get AI context
context = game_engine.get_ai_context()

# Get game state summary
summary = game_engine.get_game_state_summary()
print(f"Game state: {summary}")

# Save game state
save_data = game_engine.save_game_state()
with open("save_game.json", "w") as f:
    json.dump(save_data, f)

# Load game state
with open("save_game.json", "r") as f:
    save_data = json.load(f)
game_engine.load_game_state(save_data)
```