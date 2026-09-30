"""Remove Co-authored-by: Cursor lines from stdin (git filter-branch --msg-filter)."""
import sys

lines = sys.stdin.readlines()
out = [
    line
    for line in lines
    if "cursoragent" not in line.lower() and "co-authored-by: cursor" not in line.lower()
]
text = "".join(out).rstrip()
if text:
    sys.stdout.write(text + "\n")
