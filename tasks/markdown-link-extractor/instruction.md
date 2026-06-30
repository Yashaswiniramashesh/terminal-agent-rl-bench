# Task: Extract Markdown Hyperlinks

A Python utility at `/app/extract_links.py` is configured to scan a Markdown file located at `/app/document.md` to extract all standard hyperlinks and write them to `/tmp/links.txt`.

Currently, the script contains a bug where it extracts image links (e.g., `![Logo Banner](image.png)`) along with regular hyperlinks (e.g., `[Google Link](https://google.com)`). 

Your objective is to:
1. Debug and modify the regular expression pattern inside `/app/extract_links.py` so it only extracts standard hyperlinks, ignoring image links entirely.
2. Execute the script to generate `/tmp/links.txt` with the clean list of extracted hyperlinks.

Constraints:
* Do not delete or rename `document.md`.
* Do not modify the script's output file path (`/tmp/links.txt`).
