#!/bin/bash

# Ensure the log directory exists
mkdir -p /logs/verifier

# --- Verification Logic ---

# Assert the output file exists
if [ ! -f /tmp/links.txt ]; then
    echo "Verification failed: /tmp/links.txt does not exist."
    VERIFY_STATUS=1
else
    # Load content and assert exact matched links are present (excluding the logo)
    IFS=$'\n' read -d '' -r -a lines < /tmp/links.txt

    if [ ${#lines[@]} -ne 3 ]; then
        echo "Verification failed: Expected 3 links, found ${#lines[@]}."
        VERIFY_STATUS=1
    elif [ "${lines[0]}" != "https://google.com" ] || \
         [ "${lines[1]}" != "https://wikipedia.org" ] || \
         [ "${lines[2]}" != "https://github.com/guide.md" ]; then
        echo "Verification failed: Extracted links mismatch: ${lines[*]}"
        VERIFY_STATUS=1
    else
        echo "Verification successful!"
        VERIFY_STATUS=0
    fi
fi

# --- Reward Logic ---

if [ $VERIFY_STATUS -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
    echo "REWARD = 1 (PASS)"
    exit 0
else
    echo 0 > /logs/verifier/reward.txt
    echo "REWARD = 0 (FAIL)"
    exit 1
fi