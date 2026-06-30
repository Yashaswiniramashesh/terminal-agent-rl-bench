#!/bin/bash
set -e

cat > solution.py << 'EOF'
def sum_even_indices(numbers):
    total = 0
    for i in range(0, len(numbers), 2):  # FIXED: start at 0, step by 2 for even indices
        total += numbers[i]  # FIXED: now accessing even indices correctly
    return total

# Test cases
result1 = sum_even_indices([1, 2, 3, 4, 5])
result2 = sum_even_indices([])
result3 = sum_even_indices([10])
result4 = sum_even_indices([1, 2])
result5 = sum_even_indices([5, 10, 15, 20])

print(f"Test 1: {result1} (expected: 9)")
print(f"Test 2: {result2} (expected: 0)")
print(f"Test 3: {result3} (expected: 10)")
print(f"Test 4: {result4} (expected: 1)")
print(f"Test 5: {result5} (expected: 20)")

# Check if all tests pass
if [ "$result1" -eq 9 ] && [ "$result2" -eq 0 ] && [ "$result3" -eq 10 ] && [ "$result4" -eq 1 ] && [ "$result5" -eq 20 ]; then
    echo "PASS"
    echo "1" > rewards.txt
else
    echo "FAIL"
    echo "0" > rewards.txt
fi
EOF

python solution.py