A Python utility at `/app/spellcheck.py` is configured to scan a text file at `/app/draft.txt`, correct all instances of the common misspelling `"recieve"` to `"receive"`, and write the results to `/tmp/corrected_draft.txt`.

Currently, the script is broken because it uses case-sensitive text replacement:
`text.replace("recieve", "receive")`

This buggy approach completely misses capitalized instances (e.g. `"Recieve"` at the start of a sentence), leaving them uncorrected.

Your objective:
1. Modify `/app/spellcheck.py` so it performs a case-insensitive replacement, ensuring that both lowercase and capitalized misspellings are corrected (while preserving sentence casing, i.e., `"Recieve"` becomes `"Receive"` and `"recieve"` becomes `"receive"`).
2. Execute the script to output the corrected text to `/tmp/corrected_draft.txt`.

Constraints:
* Do not alter the input path (`/app/draft.txt`) or output path (`/tmp/corrected_draft.txt`).
