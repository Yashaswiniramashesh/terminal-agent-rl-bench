# Broken Log Parser

The script `/app/parse_logs.py` is supposed to count ERROR lines
in the server log at `/app/server.log`, but it always returns 0
even though errors clearly exist in the log.

## Your Task

Fix `parse_logs.py` so that `count_errors("/app/server.log")`
returns the correct number of ERROR lines.

## Constraints
- Do not modify `server.log`
- The fix should be minimal