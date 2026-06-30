#!/bin/bash

# Initialize a success flag (0 means success in Bash)
TEST_PASSED=0

# 1. Assert the output file exists
if [ ! -f /tmp/merged_config.json ]; then
    echo "Verification failed: /tmp/merged_config.json does not exist."
    TEST_PASSED=1
fi

# 2. Verify the root key is updated
if [ $TEST_PASSED -eq 0 ] && ! grep -q '"theme": "dark"' /tmp/merged_config.json; then
    echo "Verification failed: 'theme' is not 'dark'."
    TEST_PASSED=1
fi

# 3. Verify the unchanged default nested key is preserved
if [ $TEST_PASSED -eq 0 ] && ! grep -q '"beta_testing": true' /tmp/merged_config.json; then
    echo "Verification failed: 'beta_testing' is not true."
    TEST_PASSED=1
fi

# 4. Verify the updated nested key is merged correctly
if [ $TEST_PASSED -eq 0 ] && ! grep -q '"experiments": true' /tmp/merged_config.json; then
    echo "Verification failed: 'experiments' is not true."
    TEST_PASSED=1
fi

# Ensure the log directory exists before writing the reward file
mkdir -p /logs/verifier

# 5. Output the reward based on the test results
if [ $TEST_PASSED -eq 0 ]; then
    echo "Verification successful!"
    echo 1 > /logs/verifier/reward.txt
    echo "REWARD = 1 (PASS)"
    exit 0
else
    echo 0 > /logs/verifier/reward.txt
    echo "REWARD = 0 (FAIL)"
    exit 1
fi