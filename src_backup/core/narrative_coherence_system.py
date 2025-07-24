#!/usr/bin/env python3
"""
Narrative Coherence System - Maintains consistent narrative elements across turns

This system tracks active narrative elements (NPCs, locations, threats, etc.) and
ensures they remain consistent across AI responses. It detects when important elements
are "forgotten" by the AI and forces corrections to maintain narrative coherence.
"""
import re
from typing import Dict, List, Set, Any, Optional, Tuple

class NarrativeElement:
    """Represents a tracked narrative element"""
    
    def __init__(self, element_id: str, element_type: str, data: Dict[str, Any], 
                importance: int = 1, keywords: List[str] = None):
        self.element_id = element_id
        self.element_type = element_type
        self.data = data
        self.importance = importance  # 1-5 scale, 5 being most important
        self.keywords = keywords or []
        self.introduced_turn = 0
        self.last_mentioned_turn = 0
        self.mention_count = 0
    
    def update_mention(self, turn_number: int):
        """Update when this element was last mentioned"""
        self.last_mentioned_turn = turn_number
        self.mention_count += 1
    
    def get_summary(self) -> str:
        """Get a summary of this element for AI context"""
        if self.element_type == "character":
            return f"{self.data.get('name', self.element_id)}: {self.data.get('description', 'An NPC')}"
        elif self.element_type == "location":
            return f"{self.data.get('name', self.element_id)}: {self.data.get('description', 'A location')}"
        elif self.element_type == "threat":
            return f"{self.data.get('name', self.element_id)}: {self.data.get('description', 'A threat')}"
        else:
            return f"{self.element_id}: {self.data.get('description', 'A narrative element')}"
    
    def should_be_maintained(self, current_turn: int) -> bool:
        """Determine if this element should be maintained in the narrative"""
        # Always maintain very important elements
        if self.importance >= 4:
            return True
        
        # Maintain elements mentioned in the last 3 turns
        if current_turn - self.last_mentioned_turn <= 3:
            return True
        
        # Maintain elements mentioned multiple times
        if self.mention_count >= 3:
            return True
        
        # Don't maintain low-importance elements mentioned long ago
        if self.importance <= 2 and current_turn - self.last_mentioned_turn > 5:
            return False
        
        # Default to maintaining
        return True


class NarrativeCoherenceSystem:
    """Manages narrative coherence across turns"""
    
    def __init__(self):
        # Active narrative elements by type
        self.active_elements: Dict[str, Dict[str, NarrativeElement]] = {
            "character": {},  # NPCs and important characters
            "location": {},   # Locations and important places
            "threat": {},     # Threats, antagonists, and dangers
            "object": {},     # Important objects and items
            "concept": {}     # Abstract concepts, quests, goals
        }
        
        self.current_turn = 0
        self.narrative_history = []  # Track important narrative events
        self.current_location = None
    
    def advance_turn(self):
        """Advance to the next turn"""
        self.current_turn += 1
    
    def register_element(self, element_id: str, element_type: str, 
                        data: Dict[str, Any], importance: int = 1,
                        keywords: List[str] = None) -> NarrativeElement:
        """
        Register a new narrative element as active
        
        Args:
            element_id: Unique identifier for the element
            element_type: Type of element (character, location, threat, object, concept)
            data: Data associated with the element
            importance: Importance level (1-5)
            keywords: Keywords associated with this element
            
        Returns:
            The created NarrativeElement
        """
        if element_type not in self.active_elements:
            raise ValueError(f"Unknown element type: {element_type}")
        
        # Create element
        element = NarrativeElement(
            element_id=element_id,
            element_type=element_type,
            data=data,
            importance=importance,
            keywords=keywords or []
        )
        
        # Set initial turn data
        element.introduced_turn = self.current_turn
        element.last_mentioned_turn = self.current_turn
        element.mention_count = 1
        
        # Add to active elements
        self.active_elements[element_type][element_id] = element
        
        return element
    
    def update_element(self, element_id: str, element_type: str, 
                      data: Dict[str, Any] = None, importance: int = None,
                      keywords: List[str] = None) -> Optional[NarrativeElement]:
        """
        Update an existing narrative element
        
        Args:
            element_id: Unique identifier for the element
            element_type: Type of element
            data: New data to merge with existing data
            importance: New importance level
            keywords: New keywords to add
            
        Returns:
            The updated NarrativeElement or None if not found
        """
        if element_type not in self.active_elements:
            return None
        
        if element_id not in self.active_elements[element_type]:
            return None
        
        element = self.active_elements[element_type][element_id]
        
        # Update data
        if data:
            element.data.update(data)
        
        # Update importance
        if importance is not None:
            element.importance = importance
        
        # Update keywords
        if keywords:
            element.keywords.extend(keywords)
            # Remove duplicates
            element.keywords = list(set(element.keywords))
        
        # Update mention
        element.update_mention(self.current_turn)
        
        return element
    
    def remove_element(self, element_id: str, element_type: str) -> bool:
        """
        Remove a narrative element
        
        Args:
            element_id: Unique identifier for the element
            element_type: Type of element
            
        Returns:
            True if element was removed, False otherwise
        """
        if element_type not in self.active_elements:
            return False
        
        if element_id not in self.active_elements[element_type]:
            return False
        
        del self.active_elements[element_type][element_id]
        return True
    
    def set_current_location(self, location_id: str, location_data: Dict[str, Any] = None):
        """Set the current location"""
        self.current_location = location_id
        
        # If we have data, register or update the location
        if location_data:
            if location_id in self.active_elements["location"]:
                self.update_element(location_id, "location", location_data)
            else:
                self.register_element(location_id, "location", location_data, importance=4)
    
    def check_element_mentioned(self, element: NarrativeElement, text: str) -> bool:
        """Check if an element is mentioned in the text"""
        # Check element ID
        if element.element_id.lower() in text.lower():
            return True
        
        # Check element name
        if "name" in element.data and element.data["name"].lower() in text.lower():
            return True
        
        # Check keywords
        for keyword in element.keywords:
            if keyword.lower() in text.lower():
                return True
        
        return False
    
    def update_mentions(self, text: str):
        """Update which elements are mentioned in the text"""
        text_lower = text.lower()
        
        for element_type, elements in self.active_elements.items():
            for element_id, element in elements.items():
                if self.check_element_mentioned(element, text_lower):
                    element.update_mention(self.current_turn)
    
    def check_continuity_violations(self, ai_response: str) -> List[str]:
        """
        Check if AI response maintains continuity with active elements
        
        Args:
            ai_response: The AI response to check
            
        Returns:
            List of continuity violations
        """
        violations = []
        
        # Check each active element type
        for element_type, elements in self.active_elements.items():
            for element_id, element in elements.items():
                # Skip if element was just introduced this turn
                if element.introduced_turn == self.current_turn:
                    continue
                    
                # Skip elements that don't need to be maintained
                if not element.should_be_maintained(self.current_turn):
                    continue
                
                # Check if important element is maintained in the response
                if element.importance >= 3 and not self.check_element_mentioned(element, ai_response):
                    violations.append(f"Active element '{element_id}' disappeared without explanation")
        
        # Check if current location is maintained
        if self.current_location and self.current_location in self.active_elements["location"]:
            location_element = self.active_elements["location"][self.current_location]
            if not self.check_element_mentioned(location_element, ai_response):
                violations.append(f"Current location '{self.current_location}' not reflected in response")
        
        return violations
    
    def _format_important_elements(self) -> str:
        """Format important active elements for AI context"""
        important_elements = []
        
        for element_type, elements in self.active_elements.items():
            for element_id, element in elements.items():
                if element.should_be_maintained(self.current_turn):
                    important_elements.append(f"- {element.get_summary()}")
        
        return "\n".join(important_elements)
    
    def generate_continuity_enforcement_prompt(self, ai_response: str, violations: List[str]) -> str:
        """
        Generate a prompt to enforce continuity in AI response
        
        Args:
            ai_response: The original AI response
            violations: List of continuity violations
            
        Returns:
            Prompt for AI to fix continuity issues
        """
        enforcement_prompt = f"""
        Your previous response has continuity issues that need to be fixed:
        {', '.join(violations)}
        
        Please rewrite your response to maintain these narrative elements while 
        preserving the core action resolution. Important active elements include:
        {self._format_important_elements()}
        
        Original response:
        {ai_response}
        
        Rewritten response that maintains continuity:
        """
        
        return enforcement_prompt
    
    def enforce_continuity(self, ai_response: str) -> Tuple[str, List[str]]:
        """
        Check for continuity violations and generate enforcement prompt if needed
        
        Args:
            ai_response: The AI response to check
            
        Returns:
            Tuple of (enforcement_prompt or None, violations)
        """
        violations = self.check_continuity_violations(ai_response)
        
        if not violations:
            return None, []
        
        enforcement_prompt = self.generate_continuity_enforcement_prompt(ai_response, violations)
        return enforcement_prompt, violations
    
    def extract_narrative_elements(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract potential narrative elements from text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of extracted elements by type
        """
        extracted_elements = {
            "character": [],
            "location": [],
            "threat": [],
            "object": [],
            "concept": []
        }
        
        # Extract character names (capitalized names)
        character_pattern = r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b'
        character_matches = re.findall(character_pattern, text)
        
        for match in character_matches:
            # Skip common words that might be capitalized
            if match.lower() in ["i", "you", "he", "she", "they", "we", "it"]:
                continue
                
            # Skip if it's a known element ID
            if any(match.lower() == element_id.lower() 
                  for elements in self.active_elements.values() 
                  for element_id in elements):
                continue
            
            extracted_elements["character"].append({
                "id": match,
                "name": match,
                "description": f"Character mentioned in narrative"
            })
        
        # Extract locations (places with descriptive words)
        location_pattern = r'\b((?:the\s)?[A-Z][a-z]+(?:\s[a-z]+)*(?:\s[A-Z][a-z]+)*)\b'
        location_matches = re.findall(location_pattern, text)
        
        location_keywords = ["village", "town", "city", "forest", "cave", "mountain", 
                           "river", "lake", "temple", "castle", "house", "tavern"]
        
        for match in location_matches:
            if any(keyword in match.lower() for keyword in location_keywords):
                extracted_elements["location"].append({
                    "id": match,
                    "name": match,
                    "description": f"Location mentioned in narrative"
                })
        
        # Extract threats (danger words)
        threat_keywords = ["danger", "threat", "enemy", "monster", "creature", 
                         "beast", "villain", "shadow", "evil", "dark"]
        
        for keyword in threat_keywords:
            if keyword in text.lower():
                # Find surrounding context
                pattern = r'[^.!?]*\b' + keyword + r'\b[^.!?]*[.!?]'
                matches = re.findall(pattern, text.lower())
                
                for match in matches:
                    extracted_elements["threat"].append({
                        "id": f"{keyword}_threat",
                        "name": match.strip(),
                        "description": f"Threat mentioned in narrative: {match.strip()}"
                    })
        
        return extracted_elements
    
    def suggest_new_elements(self, text: str) -> List[Dict[str, Any]]:
        """
        Suggest new narrative elements based on text analysis
        
        Args:
            text: Text to analyze
            
        Returns:
            List of suggested new elements
        """
        extracted = self.extract_narrative_elements(text)
        suggestions = []
        
        # Process extracted elements
        for element_type, elements in extracted.items():
            for element in elements:
                element_id = element["id"].lower().replace(" ", "_")
                
                # Skip if already tracked
                if element_id in self.active_elements.get(element_type, {}):
                    continue
                
                # Create suggestion
                suggestions.append({
                    "element_id": element_id,
                    "element_type": element_type,
                    "data": element,
                    "confidence": 0.7  # Default confidence
                })
        
        return suggestions
    
    def get_active_elements_summary(self) -> Dict[str, int]:
        """Get summary of active elements by type"""
        return {
            element_type: len(elements)
            for element_type, elements in self.active_elements.items()
        }
    
    def get_important_elements(self, min_importance: int = 3) -> List[NarrativeElement]:
        """Get list of important narrative elements"""
        important_elements = []
        
        for elements in self.active_elements.values():
            for element in elements.values():
                if element.importance >= min_importance:
                    important_elements.append(element)
        
        return important_elements
    
    def generate_narrative_context(self) -> str:
        """Generate narrative context for AI prompt"""
        context_parts = []
        
        # Add current location
        if self.current_location and self.current_location in self.active_elements["location"]:
            location = self.active_elements["location"][self.current_location]
            context_parts.append(f"Current Location: {location.get_summary()}")
        
        # Add important characters
        important_characters = [
            element for element in self.active_elements["character"].values()
            if element.importance >= 3
        ]
        
        if important_characters:
            context_parts.append("Important Characters:")
            for character in important_characters:
                context_parts.append(f"- {character.get_summary()}")
        
        # Add active threats
        active_threats = [
            element for element in self.active_elements["threat"].values()
            if element.should_be_maintained(self.current_turn)
        ]
        
        if active_threats:
            context_parts.append("Active Threats:")
            for threat in active_threats:
                context_parts.append(f"- {threat.get_summary()}")
        
        # Add recent narrative events
        if self.narrative_history:
            context_parts.append("Recent Events:")
            for event in self.narrative_history[-3:]:  # Last 3 events
                context_parts.append(f"- {event}")
        
        return "\n\n".join(context_parts)


# Example usage
if __name__ == "__main__":
    # Create system
    coherence_system = NarrativeCoherenceSystem()
    
    # Register some elements
    coherence_system.register_element(
        "emberlyn", "character",
        {"name": "Emberlyn", "description": "A fairy companion with flame-colored wings"},
        importance=5,
        keywords=["fairy", "companion", "wings", "flame-colored"]
    )
    
    coherence_system.register_element(
        "shadow_blight", "threat",
        {"name": "Shadow Blight", "description": "A corruption spreading through the shadows"},
        importance=4,
        keywords=["shadow", "corruption", "darkness", "blight"]
    )
    
    coherence_system.set_current_location(
        "village_outskirts",
        {"name": "Village Outskirts", "description": "The path leading to Ashbrook village"}
    )
    
    # Test continuity checking
    print("Testing Narrative Coherence System:")
    
    # Good response that maintains continuity
    good_response = """
    *Emberlyn flutters nervously as she points toward the writhing shadows*
    
    "The Shadow Blight is spreading faster than I feared. We need to warn the villagers 
    before it reaches Ashbrook," she whispers urgently.
    
    *The path ahead winds through the Village Outskirts, where fallen autumn leaves 
    crunch beneath your feet*
    """
    
    # Bad response that drops important elements
    bad_response = """
    *A gentle breeze rustles through the trees*
    
    "We should continue on our journey," she suggests. "The village isn't far now."
    
    *The afternoon sun casts long shadows across the path ahead*
    """
    
    # Check good response
    coherence_system.advance_turn()
    violations_good = coherence_system.check_continuity_violations(good_response)
    print("\nGood Response Violations:", violations_good)
    
    # Check bad response
    coherence_system.advance_turn()
    violations_bad = coherence_system.check_continuity_violations(bad_response)
    print("\nBad Response Violations:", violations_bad)
    
    # Generate enforcement prompt
    if violations_bad:
        enforcement_prompt, _ = coherence_system.enforce_continuity(bad_response)
        print("\nEnforcement Prompt:")
        print(enforcement_prompt)
    
    # Extract narrative elements
    new_text = """
    Elder Marcus from Ashbrook village warned about the Crimson Cult that has been 
    performing rituals in the Dark Hollow. They've been using the Ancient Amulet 
    to channel dark energies.
    """
    
    suggestions = coherence_system.suggest_new_elements(new_text)
    print("\nSuggested New Elements:")
    for suggestion in suggestions:
        print(f"- {suggestion['element_type']}: {suggestion['element_id']} ({suggestion['data']['name']})")