---
inclusion: always
---

# Implementation Tracking Workflow

To maintain context continuity across multiple implementation sessions, follow this workflow:

## Key Files

- **implementation_status.yaml**: Main status tracking file
- **session_summaries/**: Directory containing session-by-session notes

## Commands

- `./scripts/show_status.py`: Display current implementation status
- `./scripts/update_status.sh`: Helper for updating the status file
- `./scripts/create_session_summary.sh`: Create a new session summary

## Workflow

### Start of Session

1. Run `./scripts/show_status.py` to review current status
2. Check the "next_session_tasks" section to see what needs to be done
3. Review any context notes from the previous session

### During Implementation

1. Make your code changes as normal
2. For significant milestones, update the implementation_status.yaml file
3. Add detailed comments at logical stopping points

### End of Session

1. Run `./scripts/update_status.sh` to remind yourself what to update
2. Update the implementation_status.yaml file with:
   - Current progress
   - Modified files
   - Next session tasks
   - Any context notes
3. Run `./scripts/create_session_summary.sh` to create a detailed session summary
4. Commit your changes with a descriptive message

## Best Practices

1. Always update the status file before ending a session
2. Include enough context for your future self to understand
3. Be specific about next steps
4. Use consistent formatting in your status updates
5. Keep the status file up to date as you make progress

Remember: The goal is to make it easy to pick up where you left off, even if you're returning to the project after a break.