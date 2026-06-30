#!/bin/bash

cat > process_metrics.py << 'EOF'
import sys

def calculate_average(metrics):
    if len(metrics) == 0:
        return 0
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
EOF

echo "Solution applied successfully"
