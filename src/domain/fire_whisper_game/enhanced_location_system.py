#!/usr/bin/env python3
"""
Enhanced Location System - Improves location detection, transitions, and consistency

This system addresses issues with location tracking by:
1. Improving location detection in AI responses
2. Validating location transitions based on connection rules
3. Ensuring narrative consistency with technical location state
4. Providing rich location descriptions for context
"""
import re
import random
from typing import Dict, List, Set, Any, Optional, Tuple

class LocationConnection:
    """Represents a connection between two locations"""
    
    def __init__(self, source: str, destination: str, difficulty: int = 0, 
                description: str = None, bidirectional: bool = True):
        self.source = source
        self.destination = destination
        self.difficulty = difficulty  # DC for dice roll, 0 means no roll needed
        self.description = description
        self.bidirectional = bidirectional
    
    def is_valid_transition(self, source: str, destination: str) -> bool:
        """Check if this connection allows transition from source to destination"""
        if self.source == source and self.destination == destination:
            return True
        
        if self.bidirectional and self.source == destination and self.destination == source:
            return True
        
        return False
    
    def get_difficulty(self, source: str, destination: str) -> int:
        """Get difficulty for this transition"""
        if not self.is_valid_transition(source, destination):
            return -1  # Invalid transition
        
        return self.difficulty


class Location:
    """Represents a location in the game world"""
    
    def __init__(self, location_id: str, name: str, description: str = None, 
                keywords: List[str] = None, features: List[str] = None):
        self.location_id = location_id
        self.name = name
        self.description = description or f"A location known as {name}"
        self.keywords = keywords or [location_id, name.lower()]
        self.features = features or []
        self.visits = 0
        self.last_visit_turn = None
    
    def visit(self, turn_number: int):
        """Record a visit to this location"""
        self.visits += 1
        self.last_visit_turn = turn_number
    
    def get_description(self, time_of_day: str = None, weather: str = None) -> str:
        """Get description with optional time and weather variations"""
        base_description = self.description
        
        # Add time of day details if provided
        if time_of_day:
            time_descriptions = {
                "morning": "The morning light illuminates",
                "afternoon": "The afternoon sun shines upon",
                "evening": "The evening shadows stretch across",
                "night": "The darkness of night envelops"
            }
            
            time_prefix = time_descriptions.get(time_of_day.lower(), "")
            if time_prefix:
                base_description = f"{time_prefix} {base_description.lower()}"
        
        # Add weather details if provided
        if weather:
            weather_descriptions = {
                "clear": "under clear skies",
                "cloudy": "beneath overcast clouds",
                "rainy": "as rain falls steadily",
                "stormy": "while thunder rumbles in the distance",
                "foggy": "shrouded in a thick mist",
                "snowy": "covered in a blanket of snow"
            }
            
            weather_suffix = weather_descriptions.get(weather.lower(), "")
            if weather_suffix:
                base_description = f"{base_description} {weather_suffix}"
        
        return base_description
    
    def get_feature_description(self) -> Optional[str]:
        """Get description of a random feature of this location"""
        if not self.features:
            return None
        
        return random.choice(self.features)


class EnhancedLocationSystem:
    """Manages locations, transitions, and consistency"""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.connections: List[LocationConnection] = []
        self.current_location_id = None
        self.previous_location_id = None
        self.transition_history = []
        self.current_turn = 0
        
        # Track stuck turns (same location)
        self.turns_in_current_location = 0
        self.max_turns_before_forcing = 5
    
    def add_location(self, location_id: str, name: str, description: str = None,
                   keywords: List[str] = None, features: List[str] = None) -> Location:
        """
        Add a new location
        
        Args:
            location_id: Unique identifier for the location
            name: Display name for the location
            description: Description of the location
            keywords: Keywords that identify this location in text
            features: Notable features of this location
            
        Returns:
            The created Location
        """
        location = Location(
            location_id=location_id,
            name=name,
            description=description,
            keywords=keywords,
            features=features
        )
        
        self.locations[location_id] = location
        return location
    
    def add_connection(self, source: str, destination: str, difficulty: int = 0,
                     description: str = None, bidirectional: bool = True) -> LocationConnection:
        """
        Add a connection between locations
        
        Args:
            source: Source location ID
            destination: Destination location ID
            difficulty: DC for dice roll (0 means no roll needed)
            description: Description of the connection
            bidirectional: Whether the connection works in both directions
            
        Returns:
            The created LocationConnection
        """
        # Verify locations exist
        if source not in self.locations:
            raise ValueError(f"Source location not found: {source}")
        
        if destination not in self.locations:
            raise ValueError(f"Destination location not found: {destination}")
        
        connection = LocationConnection(
            source=source,
            destination=destination,
            difficulty=difficulty,
            description=description,
            bidirectional=bidirectional
        )
        
        self.connections.append(connection)
        return connection
    
    def set_current_location(self, location_id: str, turn_number: int = None):
        """
        Set the current location
        
        Args:
            location_id: Location ID
            turn_number: Current turn number (optional)
        """
        if location_id not in self.locations:
            raise ValueError(f"Location not found: {location_id}")
        
        # Update location tracking
        self.previous_location_id = self.current_location_id
        self.current_location_id = location_id
        
        # Reset stuck counter
        self.turns_in_current_location = 0
        
        # Record visit
        if turn_number is not None:
            self.locations[location_id].visit(turn_number)
        
        # Record transition if this is a change
        if self.previous_location_id and self.previous_location_id != location_id:
            self.transition_history.append({
                "from": self.previous_location_id,
                "to": location_id,
                "turn": turn_number if turn_number is not None else len(self.transition_history) + 1
            })
    
    def advance_turn(self):
        """Advance to the next turn"""
        self.current_turn += 1
        self.turns_in_current_location += 1
    
    def get_current_location(self) -> Optional[Location]:
        """Get the current location"""
        if not self.current_location_id:
            return None
        
        return self.locations.get(self.current_location_id)
    
    def get_valid_connections(self, location_id: str = None) -> List[str]:
        """
        Get valid connections from a location
        
        Args:
            location_id: Source location ID (defaults to current location)
            
        Returns:
            List of destination location IDs
        """
        if location_id is None:
            location_id = self.current_location_id
        
        if not location_id:
            return []
        
        valid_destinations = []
        
        for connection in self.connections:
            # Check direct connections
            if connection.source == location_id:
                valid_destinations.append(connection.destination)
            
            # Check reverse connections for bidirectional
            if connection.bidirectional and connection.destination == location_id:
                valid_destinations.append(connection.source)
        
        return valid_destinations
    
    def get_connection_difficulty(self, source: str, destination: str) -> int:
        """
        Get difficulty for a transition between locations
        
        Args:
            source: Source location ID
            destination: Destination location ID
            
        Returns:
            Difficulty (DC) or -1 if invalid connection
        """
        for connection in self.connections:
            if connection.is_valid_transition(source, destination):
                return connection.get_difficulty(source, destination)
        
        return -1  # Invalid connection
    
    def is_valid_transition(self, source: str, destination: str) -> bool:
        """Check if transition between locations is valid"""
        return self.get_connection_difficulty(source, destination) >= 0
    
    def detect_location_change(self, ai_response: str, player_action: str, 
                             dice_roll: int = None) -> Dict[str, Any]:
        """
        Detect if the AI response indicates a location change
        
        Args:
            ai_response: AI response text
            player_action: Player action text
            dice_roll: Result of dice roll (if applicable)
            
        Returns:
            Dict with location change information
        """
        # Default result
        result = {
            "location_changed": False,
            "reason": "No movement detected",
            "current_location": self.current_location_id
        }
        
        # If no current location, can't detect change
        if not self.current_location_id:
            result["reason"] = "No current location set"
            return result
        
        # Extract location keywords from response
        response_lower = ai_response.lower()
        
        # Check for explicit movement indicators
        movement_verbs = ["go", "walk", "travel", "enter", "arrive", "reach", "move", "approach"]
        has_movement = any(verb in response_lower for verb in movement_verbs)
        
        if not has_movement:
            return result
        
        # Detect target location from response
        target_location_id = None
        confidence = 0
        
        for loc_id, location in self.locations.items():
            # Skip current location
            if loc_id == self.current_location_id:
                continue
                
            # Check for location keywords
            matches = sum(keyword.lower() in response_lower for keyword in location.keywords)
            
            # Calculate confidence based on number of matches
            loc_confidence = matches / len(location.keywords) if location.keywords else 0
            
            if loc_confidence > confidence and loc_confidence > 0.3:  # Minimum threshold
                target_location_id = loc_id
                confidence = loc_confidence
        
        if not target_location_id:
            result["reason"] = "No target location detected"
            return result
        
        # Validate connection
        if not self.is_valid_transition(self.current_location_id, target_location_id):
            result["reason"] = f"Invalid connection: {self.current_location_id} -> {target_location_id}"
            result["valid_connections"] = self.get_valid_connections()
            return result
        
        # Check if dice roll is needed and provided
        difficulty = self.get_connection_difficulty(self.current_location_id, target_location_id)
        if difficulty > 0:
            if dice_roll is None:
                result["reason"] = f"Dice roll required (DC {difficulty})"
                result["dice_needed"] = True
                result["target_location"] = target_location_id
                result["difficulty"] = difficulty
                return result
            
            if dice_roll < difficulty:
                result["reason"] = f"Failed dice roll: {dice_roll} vs DC {difficulty}"
                result["dice_roll"] = dice_roll
                result["difficulty"] = difficulty
                return result
        
        # Process valid location change
        old_location_id = self.current_location_id
        self.set_current_location(target_location_id, self.current_turn)
        
        # Reset stuck counter
        self.turns_in_current_location = 0
        
        return {
            "location_changed": True,
            "from": old_location_id,
            "to": target_location_id,
            "confidence": confidence,
            "dice_roll": dice_roll,
            "difficulty": difficulty
        }
    
    def should_force_location_change(self) -> Dict[str, Any]:
        """
        Check if a location change should be forced
        
        Returns:
            Dict with force information
        """
        if self.turns_in_current_location < self.max_turns_before_forcing:
            return {
                "should_force": False,
                "turns_stuck": self.turns_in_current_location
            }
        
        # Get valid connections
        valid_destinations = self.get_valid_connections()
        
        if not valid_destinations:
            return {
                "should_force": False,
                "reason": "No valid destinations",
                "turns_stuck": self.turns_in_current_location
            }
        
        # Choose a random destination
        destination = random.choice(valid_destinations)
        
        return {
            "should_force": True,
            "reason": f"stuck_at_{self.current_location_id}_for_{self.turns_in_current_location}_turns",
            "turns_stuck": self.turns_in_current_location,
            "forced_destination": destination
        }
    
    def force_location_change(self, destination: str = None) -> Dict[str, Any]:
        """
        Force a location change
        
        Args:
            destination: Destination location ID (optional)
            
        Returns:
            Dict with location change information
        """
        if not self.current_location_id:
            return {
                "location_changed": False,
                "reason": "No current location set"
            }
        
        # If no destination provided, get valid connections
        if not destination:
            valid_destinations = self.get_valid_connections()
            
            if not valid_destinations:
                return {
                    "location_changed": False,
                    "reason": "No valid destinations"
                }
            
            destination = random.choice(valid_destinations)
        
        # Validate connection
        if not self.is_valid_transition(self.current_location_id, destination):
            return {
                "location_changed": False,
                "reason": f"Invalid connection: {self.current_location_id} -> {destination}"
            }
        
        # Process forced location change
        old_location_id = self.current_location_id
        self.set_current_location(destination, self.current_turn)
        
        # Reset stuck counter
        self.turns_in_current_location = 0
        
        return {
            "location_changed": True,
            "forced": True,
            "from": old_location_id,
            "to": destination,
            "reason": "forced_progression"
        }
    
    def check_location_consistency(self, ai_response: str) -> bool:
        """
        Check if AI response correctly reflects the current location
        
        Args:
            ai_response: AI response text
            
        Returns:
            True if consistent, False otherwise
        """
        if not self.current_location_id:
            return True  # No location to check against
        
        current_location = self.locations[self.current_location_id]
        response_lower = ai_response.lower()
        
        # Check if response mentions the current location
        mentions_location = any(keyword.lower() in response_lower for keyword in current_location.keywords)
        
        return mentions_location
    
    def generate_location_enforcement_prompt(self, ai_response: str) -> str:
        """
        Generate a prompt to enforce location consistency in AI response
        
        Args:
            ai_response: The original AI response
            
        Returns:
            Prompt for AI to fix location inconsistencies
        """
        if not self.current_location_id:
            return ""  # No location to enforce
        
        current_location = self.locations[self.current_location_id]
        
        enforcement_prompt = f"""
        Your response needs to be updated to clearly reflect the current location:
        {current_location.name} ({self.current_location_id})
        
        Key features of this location:
        {current_location.description}
        
        Please rewrite your response to incorporate these location details while
        preserving the core action resolution and narrative elements.
        
        Original response:
        {ai_response}
        
        Rewritten response that clearly reflects the current location:
        """
        
        return enforcement_prompt
    
    def enforce_location_consistency(self, ai_response: str) -> Tuple[str, bool]:
        """
        Check for location inconsistencies and generate enforcement prompt if needed
        
        Args:
            ai_response: The AI response to check
            
        Returns:
            Tuple of (enforcement_prompt or None, needs_enforcement)
        """
        is_consistent = self.check_location_consistency(ai_response)
        
        if is_consistent:
            return None, False
        
        enforcement_prompt = self.generate_location_enforcement_prompt(ai_response)
        return enforcement_prompt, True
    
    def get_location_debug_report(self) -> str:
        """Get a debug report of location transitions"""
        if not self.transition_history:
            return "No location transitions recorded."
        
        report = f"\n🗺️  LOCATION DEBUG REPORT ({len(self.transition_history)} transitions):\n"
        
        # Show last 5 transitions
        for i, transition in enumerate(self.transition_history[-5:], 1):
            from_name = self.locations[transition["from"]].name if transition["from"] in self.locations else transition["from"]
            to_name = self.locations[transition["to"]].name if transition["to"] in self.locations else transition["to"]
            
            report += f"  {i}. {from_name} → {to_name} (Turn {transition['turn']})\n"
        
        return report
    
    def generate_location_context(self, time_of_day: str = None, weather: str = None) -> str:
        """
        Generate location context for AI prompt
        
        Args:
            time_of_day: Time of day (morning, afternoon, evening, night)
            weather: Weather condition (clear, cloudy, rainy, etc.)
            
        Returns:
            Location context string
        """
        if not self.current_location_id:
            return ""
        
        current_location = self.locations[self.current_location_id]
        
        context = f"Location: {current_location.name} ({self.current_location_id}) | "
        context += f"Description: {current_location.get_description(time_of_day, weather)}"
        
        # Add a random feature if available
        feature = current_location.get_feature_description()
        if feature:
            context += f" | Feature: {feature}"
        
        return context


# Example usage
if __name__ == "__main__":
    # Create location system
    location_system = EnhancedLocationSystem()
    
    # Add locations
    location_system.add_location(
        "village_outskirts",
        "Village Outskirts",
        "A peaceful path leading to Ashbrook village, surrounded by autumn trees",
        ["outskirts", "path", "road", "outside village"],
        ["Tall oak trees line the path", "A small stream crosses under a wooden bridge", "Wild flowers grow along the edges"]
    )
    
    location_system.add_location(
        "ashbrook_village",
        "Ashbrook Village",
        "A quaint village with thatched-roof cottages and friendly inhabitants",
        ["ashbrook", "village", "town", "settlement"],
        ["The village square has a central well", "Smoke rises from cottage chimneys", "Children play near the community hall"]
    )
    
    location_system.add_location(
        "village_tavern",
        "The Rusty Sword Tavern",
        "A warm, inviting tavern filled with the scent of ale and hearty stew",
        ["tavern", "inn", "rusty sword", "pub"],
        ["A large fireplace crackles at one end", "The bartender polishes mugs behind the counter", "Patrons share stories at wooden tables"]
    )
    
    # Add connections
    location_system.add_connection("village_outskirts", "ashbrook_village", 0)
    location_system.add_connection("ashbrook_village", "village_tavern", 0)
    
    # Set current location
    location_system.set_current_location("village_outskirts")
    
    # Test location detection
    print("Testing Enhanced Location System:")
    
    # Good response that indicates movement
    good_response = """
    You walk along the path, following Emberlyn's guidance. After a short journey, 
    you arrive at Ashbrook Village. The quaint cottages with their thatched roofs 
    come into view, and you can see villagers going about their daily business in 
    the village square.
    """
    
    # Bad response that doesn't clearly indicate location
    bad_response = """
    You continue on your journey. The path winds through some trees, and you can 
    see buildings in the distance. Emberlyn flutters ahead, eager to reach the 
    destination.
    """
    
    # Test good response
    location_system.advance_turn()
    good_result = location_system.detect_location_change(good_response, "I walk to the village")
    print("\nGood Response Result:")
    for key, value in good_result.items():
        print(f"  {key}: {value}")
    
    # Test bad response
    location_system.advance_turn()
    bad_result = location_system.detect_location_change(bad_response, "I continue walking")
    print("\nBad Response Result:")
    for key, value in bad_result.items():
        print(f"  {key}: {value}")
    
    # Test location consistency
    consistent = location_system.check_location_consistency(good_response)
    print(f"\nLocation Consistency (Good): {consistent}")
    
    inconsistent = location_system.check_location_consistency(bad_response)
    print(f"Location Consistency (Bad): {inconsistent}")
    
    # Test enforcement
    if not inconsistent:
        enforcement_prompt, needs_enforcement = location_system.enforce_location_consistency(bad_response)
        if needs_enforcement:
            print("\nEnforcement Prompt:")
            print(enforcement_prompt)
    
    # Test debug report
    debug_report = location_system.get_location_debug_report()
    print(debug_report)