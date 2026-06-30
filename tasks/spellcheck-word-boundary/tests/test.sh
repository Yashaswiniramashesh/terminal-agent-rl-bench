#!/bin/bash

# Run the verification steps in a subshell/block to capture overall success
{
    # Assert the output file exists
    if [ ! -f /tmp/corrected_draft.txt ]; then
        echo "Verification failed: /tmp/corrected_draft.txt does not exist."
        exit 1
    fi

    # Verify the starting capitalized "Recieve" was corrected to "Receive"
    cat /tmp/corrected_draft.txt | grep "Receive this packet" || exit 1

    # Verify the lowercase "recieve" was corrected to "receive"
    cat /tmp/corrected_draft.txt | grep "expect to receive" || exit 1
    cat /tmp/corrected_draft.txt | grep "do not receive" || exit 1

    # Make sure no raw "recieve" strings are left
    # If grep finds "recieve", it returns 0, so we invert it or exit if found
    if cat /tmp/corrected_draft.txt | grep -i "recieve"; then
        exit 1
    fi

    echo "Verification successful!"
}

# Capture the exit status of the verification block
if [ $? -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
    echo "REWARD = 1 (PASS)"
    exit 0
else
    echo 0 > /logs/verifier/reward.txt
    echo "REWARD = 0 (FAIL)"
    exit 1
fi