#!/bin/bash
set -e

# Test 1: Empty input should exit with code 1
python process_metrics.py 2>/dev/null; EXIT_CODE=$?
if [ $EXIT_CODE -eq 1 ]; then
  echo "PASS: Empty input handled correctly"
else
  echo "FAIL: Empty input not handled correctly"
  exit 1
fi

# Test 2: Zero metrics should work
OUTPUT=$(python process_metrics.py 0 0 0 2>&1)
if [[ "$OUTPUT" == "Average: 0.0" ]]; then
  echo "PASS: Zero metrics handled correctly"
else
  echo "FAIL: Zero metrics not handled correctly"
  echo "Got: $OUTPUT"
  exit 1
fi

# Test 3: Mixed metrics should work
OUTPUT=$(python process_metrics.py 10 20 30 2>&1)
if [[ "$OUTPUT" == "Average: 20.0" ]]; then
  echo "PASS: Mixed metrics handled correctly"
else
  echo "FAIL: Mixed metrics not handled correctly"
  echo "Got: $OUTPUT"
  exit 1
fi

# Test 4: Single metric should work
OUTPUT=$(python process_metrics.py 42 2>&1)
if [[ "$OUTPUT" == "Average: 42.0" ]]; then
  echo "PASS: Single metric handled correctly"
else
  echo "FAIL: Single metric not handled correctly"
  echo "Got: $OUTPUT"
  exit 1
fi

echo "1" > rewards.txt
exit 0