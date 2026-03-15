#!/usr/bin/env python3
"""Extract actual h2 headings from each document in data.js to find valid anchors."""
import re

with open('data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all document keys and their body positions
doc_pattern = re.compile(r'"(\d\d_[^"]+)":\s*\{')
body_start_pattern = '"body": "'

for m in doc_pattern.finditer(content):
    doc_key = m.group(1)
    pos = m.start()
    
    # Find body start
    bs = content.find(body_start_pattern, pos)
    if bs == -1 or bs > pos + 200:
        continue
    bs += len(body_start_pattern)
    
    # Find icon (end of body)
    be = content.find('"icon":', bs)
    if be == -1:
        continue
    
    body = content[bs:be]
    
    # Extract h2 headings
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body)
    
    # Extract first </table> position
    first_table = body.find('</table>')
    has_table = first_table != -1
    
    print(f"\n=== {doc_key} ===")
    print(f"  Has </table>: {has_table}")
    if h2s:
        for i, h in enumerate(h2s[:5]):
            # Clean up any HTML tags inside heading
            clean = re.sub(r'<[^>]+>', '', h).strip()
            print(f"  H2[{i}]: {clean}")
    else:
        # Try h3
        h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', body)
        for i, h in enumerate(h3s[:3]):
            clean = re.sub(r'<[^>]+>', '', h).strip()
            print(f"  H3[{i}]: {clean}")
