#!/bin/bash

cat > /app/parse_logs.py << 'EOF'
import re


def count_errors(log_file):
    """
    Counts ERROR lines in a log file.
    FIXED: re.IGNORECASE catches uppercase ERROR.
    """
    count = 0
    with open(log_file) as f:
        for line in f:
            if re.search(r'error', line, re.IGNORECASE):
                count += 1
    return count


if __name__ == "__main__":
    result = count_errors("/app/server.log")
    print(f"Error count: {result}")
EOF

echo "Fix applied"
