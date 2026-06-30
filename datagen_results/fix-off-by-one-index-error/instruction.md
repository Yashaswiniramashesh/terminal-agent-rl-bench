You are given a Python script that processes a list of numbers and calculates the sum of elements at even indices. However, there's an off-by-one indexing error in the code that causes incorrect results. Your task is to identify and fix the bug.

The script currently has the following issues:
1. The loop condition incorrectly excludes the last element
2. The indexing logic is wrong for accessing even positions
3. The final result calculation is flawed

Your goal is to correct the indexing logic so that the function properly sums all elements at even indices (0, 2, 4, ...). The function should work correctly for lists of any length including empty lists and single-element lists.