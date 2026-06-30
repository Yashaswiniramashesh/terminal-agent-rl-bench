#!/bin/bash

mkdir -p /logs/verifier

python -m pytest /tests/test_parser.py -v

if [ $? -eq 0 ]; then
    echo 1 > /logs/verifier/reward.txt
    echo "REWARD = 1 (PASS)"
else
    echo 0 > /logs/verifier/reward.txt
    echo "REWARD = 0 (FAIL)"
fi