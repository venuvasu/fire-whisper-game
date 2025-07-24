# Fire Whisper RPG - Story Arc Expansion Plan

## Overview

This document outlines the plan to expand the current 5 story arcs to the full 50 arcs mentioned in the implementation status. The expansion will maintain the existing story arc system architecture while adding new content and variety.

## Current Implementation

The current system has 5 core story arcs:
1. **The Sacred Flame Restoration** (Nature Magic) - Difficulty 2
2. **The Last Dragon's Quest** (Classic Fantasy) - Difficulty 3  
3. **Songs of the Silent Stones** (Musical Mystery) - Difficulty 2
4. **The Memory Thief** (Psychological Mystery) - Difficulty 3
5. **The Crimson Prophecy** (Epic Fantasy) - Difficulty 4

Each arc has:
- A name
- A type/genre
- A hook (introductory text)
- Key elements
- A climax
- Difficulty rating
- Expected number of turns

## Expansion Strategy

### Phase 1: Arc Categories (10 categories, 5 arcs each)

Organize the 50 arcs into 10 thematic categories with 5 arcs per category:

1. **Classic Fantasy** - Traditional fantasy adventures
2. **Dark Fantasy** - Grimmer, more dangerous quests
3. **Magical Mystery** - Arcane puzzles and magical investigations
4. **Epic Quests** - World-changing adventures
5. **Character-Driven** - Personal growth and relationship stories
6. **Location-Based** - Adventures centered around specific locations
7. **Creature-Focused** - Stories featuring specific monsters or beings
8. **Historical Fantasy** - Stories set in fantasy versions of historical periods
9. **Elemental Themes** - Quests focused on elemental powers
10. **Mythological** - Stories based on various mythologies

### Phase 2: Difficulty Distribution

Ensure a balanced distribution of difficulty levels:
- Difficulty 1 (Beginner): 10 arcs
- Difficulty 2 (Easy): 15 arcs
- Difficulty 3 (Medium): 15 arcs
- Difficulty 4 (Hard): 7 arcs
- Difficulty 5 (Expert): 3 arcs

### Phase 3: Implementation Schedule

1. **Sprint 1 (Weeks 1-2)**: Design and implement 15 new arcs (3 categories)
2. **Sprint 2 (Weeks 3-4)**: Design and implement 15 more arcs (3 categories)
3. **Sprint 3 (Weeks 5-6)**: Design and implement final 15 arcs (4 categories)
4. **Sprint 4 (Weeks 7-8)**: Testing, balancing, and integration

## Arc Template

Each new arc will follow this template:

```
Name: [Arc Name]
Type: [Arc Type/Genre]
Hook: [Introductory text to set up the story]
Key Elements: [Element 1], [Element 2], [Element 3], [Element 4], [Element 5]
Climax: [Description of the arc's conclusion]
Difficulty: [1-5]
Turns: [Expected number of turns to complete]
Location Start: [Recommended starting location]
Character Level: [Recommended character level range]
```

## New Arc Examples

### Dark Fantasy Category

1. **The Whispering Shadows**
   - Type: Dark Fantasy
   - Hook: The shadows in Ashbrook Village have begun to whisper secrets that drive people mad.
   - Key Elements: Shadow magic, village corruption, madness, ancient curse, hidden shrine
   - Climax: Confronting the shadow entity in its own realm
   - Difficulty: 3
   - Turns: 12
   - Location Start: village_tavern
   - Character Level: 2-4

2. **Blood Moon Rising**
   - Type: Dark Fantasy
   - Hook: A crimson moon hangs in the sky for three nights, causing the dead to stir.
   - Key Elements: Undead, blood magic, lunar cycles, ancestral spirits, necromancer
   - Climax: Performing a ritual during the peak of the blood moon
   - Difficulty: 4
   - Turns: 15
   - Location Start: sacred_grove
   - Character Level: 3-5

### Elemental Themes Category

1. **The Ember's Heart**
   - Type: Elemental/Fire
   - Hook: The heart of the Ember Woods is dying as its eternal flame fades.
   - Key Elements: Fire magic, forest spirits, elemental balance, ancient guardian, flame ritual
   - Climax: Rekindling the central flame with a personal sacrifice
   - Difficulty: 2
   - Turns: 10
   - Location Start: ember_woods
   - Character Level: 1-3

## Technical Implementation

1. **File Structure**:
   - Expand `src/ai/prompts/story_arcs.txt` with new arcs
   - Update documentation in `docs/story_arcs.md`

2. **Code Changes**:
   - Enhance `select_story_arc()` function to consider more context variables
   - Add location-specific arc selection logic
   - Implement character level requirements

3. **Testing**:
   - Create test cases for each new arc
   - Verify proper arc selection based on context
   - Test arc progression and completion

## Success Criteria

- All 50 arcs implemented and testable
- Balanced distribution across difficulty levels
- Each arc has unique elements and climax
- Proper integration with existing game systems
- Documentation updated to reflect all available arcs

## Next Steps

1. Begin detailed design of the first batch of new arcs
2. Update the arc selection algorithm to handle the expanded set
3. Create test cases for the new arcs
4. Implement the first batch and gather feedback