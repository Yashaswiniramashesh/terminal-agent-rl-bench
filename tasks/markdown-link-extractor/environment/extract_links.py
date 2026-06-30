
import re
import sys

try:
  with open("/app/document.md", "r") as f:
    content = f.read()

  # Bug: basic regex matching both standard and image markdown links
  links = re.findall(r"\[.*?\].*?\((.*?)\)", content)

  with open("/tmp/links.txt", "w") as out:
    for link in links:
      out.write(link + "\n")
except Exception as e:
  print(f"Extraction failed: {e}", file=sys.stderr)
  sys.exit(1)
