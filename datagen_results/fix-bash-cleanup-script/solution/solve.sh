#!/bin/bash
# Corrected cleanup script

# Create some test files and directories
mkdir -p temp_dir/subdir
echo "test content" > temp_dir/file1.txt
echo "more content" > temp_dir/subdir/file2.txt

echo "Cleaning up temp_dir..."

# Fixed: Use -r flag to remove directory recursively
rm -rf temp_dir

if [ $? -eq 0 ]; then
    echo "Cleanup completed successfully"
    exit 0
else
    echo "Cleanup failed"
    exit 1
fi