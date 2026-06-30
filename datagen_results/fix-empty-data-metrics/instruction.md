You are given a Python script `process_metrics.py` that calculates average values from data metrics. The script crashes with a `ZeroDivisionError` when it encounters empty data sets. Your task is to fix the script so it handles empty data gracefully by returning 0 instead of crashing.

The script currently looks like this:
```python
import sys

def calculate_average(metrics):
    total = sum(metrics)
    count = len(metrics)
    return total / count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python process_metrics.py <metric1> <metric2> ...")
        sys.exit(1)
    
    metrics = [float(x) for x in sys.argv[1:]]
    result = calculate_average(metrics)
    print(f"Average: {result}")
```

When run with no arguments or with empty data, it will crash. You need to modify the script to handle these edge cases properly.