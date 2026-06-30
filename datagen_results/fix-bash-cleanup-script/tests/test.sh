#!/bin/bash
# Test script for fix-bash-cleanup-script task

# Create test directory structure
mkdir -p temp_dir/subdir
echo "test content" > temp_dir/file1.txt
echo "more content" > temp_dir/subdir/file2.txt

echo "Testing cleanup script..."

# Run the cleanup script
./cleanup.sh

# Check if cleanup was successful
if [ ! -d "temp_dir" ]; then
    echo "PASS"
    echo 1 > rewards.txt
    exit 0
else
    echo "FAIL"
    echo 0 > rewards.txt
    exit 1
fi