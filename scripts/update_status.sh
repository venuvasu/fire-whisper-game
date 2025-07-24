#!/bin/bash
# Update implementation status helper

echo "📝 Updating implementation status..."
echo "----------------------------------------"

# Display current status
echo "Current status summary:"
cat implementation_status.yaml | grep -A 3 "current_task:"

# Prompt for updates
echo ""
echo "Don't forget to update implementation_status.yaml before ending your session!"
echo "Key areas to update:"
echo "  - last_updated: $(date +%Y-%m-%d)"
echo "  - current_task: [Your current task]"
echo "  - modified_files: [Files you changed]"
echo "  - next_session_tasks: [What to do next]"
echo ""
echo "Run your editor with: nano implementation_status.yaml"