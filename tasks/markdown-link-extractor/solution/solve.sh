#!/bin/bash

# Fix the regex string inside /app/extract_links.py using a negative lookbehind (?<!\!)
sed -i 's/re.findall(r"\\\[.*?\\\\\].*?\\\\((.*?)\\\\)", content)/re.findall(r"(?<!\\\\!)\\\\\[.*?\\\\\\\].*?\\\\((.*?)\\\\)", content)/g' /app/extract_links.py

# Run the python script
python3 /app/extract_links.py
