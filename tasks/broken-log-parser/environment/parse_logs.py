import re


def count_errors(log_file):
    """
    Counts ERROR lines in a log file.
    """
    count = 0
    with open(log_file) as f:
        for line in f:
            if re.search(r'error', line):
                count += 1
    return count

if __name__ == "__main__":
    result = count_errors("/app/server.log")
    print(f"Error count: {result}")