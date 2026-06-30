#!/bin/bash

# Overwrite the python script to use regular expression case-insensitive substitution
RUN_CONTENT='import re
import sys

try:
    with open("/app/draft.txt", "r") as f:
        text = f.read()
    
    # Correct using regex case-insensitive sub mapping first character capitalization
    corrected_text = re.sub(
        r"(?i)recieve",
        lambda m: "Receive" if m.group(0)[0].isupper() else "receive",
        text
    )
    
    with open("/tmp/corrected_draft.txt", "w") as out:
        out.write(corrected_text)
except Exception as e:
    print(f"Failed to run spellcheck: {e}", file=sys.stderr)
    sys.exit(1)'

echo -e "$RUN_CONTENT" > /app/spellcheck.py

# Run the python script
python3 /app/spellcheck.py
