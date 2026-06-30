import sys
sys.path.insert(0, '/app')
from parse_logs import count_errors


def test_counts_all_errors():
    result = count_errors("/app/server.log")
    assert result == 10, f"Expected 10, got {result}"


def test_returns_nonzero():
    result = count_errors("/app/server.log")
    assert result > 0, "Got 0 — case sensitivity bug still present"


def test_does_not_overcount():
    result = count_errors("/app/server.log")
    assert result < 20, f"Counted {result} — counting INFO lines too"