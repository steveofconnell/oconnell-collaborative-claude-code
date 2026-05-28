#!/bin/bash
# Hook: PreToolUse (Edit, Write)
# Blocks writes to any 1rawdata/ directory to prevent accidental modification of source data.

# The tool input is passed via stdin as JSON
INPUT=$(cat)

# Extract the file path from the tool input
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('file_path','') or d.get('filePath',''))" 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Check if the path contains /1rawdata/
if echo "$FILE_PATH" | grep -q '/1rawdata/'; then
    echo "BLOCKED: Writing to 1rawdata/ is not allowed. Raw data must remain unmodified."
    echo "File: $FILE_PATH"
    echo "If you need to transform this data, write to 2processing/ or 3data/ instead."
    exit 2
fi

exit 0
