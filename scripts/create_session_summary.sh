#!/bin/bash
# Create a session summary

DATE=$(date +%Y-%m-%d)
SUMMARY_FILE="session_summaries/summary_${DATE}.md"

# Create directory if it doesn't exist
mkdir -p session_summaries

echo "Creating session summary at ${SUMMARY_FILE}"

# Create the summary file with template
cat > "${SUMMARY_FILE}" << EOF
# Session Summary - ${DATE}

## What I Accomplished
- 
- 
- 

## Current Challenges
- 
- 

## Next Steps
- 
- 

## Implementation Decisions
- 

## Notes for Next Session
- 

EOF

echo "Summary template created at ${SUMMARY_FILE}"
echo "Don't forget to fill it out before ending your session!"

# Open the file in the default editor if specified
if [ ! -z "\${EDITOR}" ]; then
  \${EDITOR} "${SUMMARY_FILE}"
else
  echo "Use your editor to open: ${SUMMARY_FILE}"
fi