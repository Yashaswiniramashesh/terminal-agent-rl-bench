import sys

try:
  with open("/app/draft.txt", "r") as f:
    text = f.read()

  # Bug: basic string replace is case-sensitive and misses "Recieve"
  corrected_text = text.replace("recieve", "receive")

  with open("/tmp/corrected_draft.txt", "w") as out:
    out.write(corrected_text)
except Exception as e:
  print(f"Failed to run spellcheck: {e}", file=sys.stderr)
  sys.exit(1)
