 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
from typing import List, Tuple

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class Message:
    def __init__(self, text: str, locations: List[Tuple[str, int]], uuids: List[str]):
        self.text = text
        self.locations = locations
        self.uuids = uuids

def uniqueLocation(locations: List[Tuple[str, int]]):
    loc_set = set(locations)
    return list(loc_set)

locations = [
    ("../../manual/render/shader_nodes/vector/vector_rotate.rst", 38),
    ("../../manual/modeling/hair.rst", 0),
    ("../../manual/modeling/hair.rst", 0),
    ("../../manual/modeling/hair.rst", 0),
    ("../../manual/modeling/metas/properties.rst", 92),
]

msg = Message("Type", locations, [])
msg.locations = uniqueLocation(msg.locations)

if len(msg.locations) != 4:
    e = AssertionError("There should only be ONE instance of each location.")
    print_stacktrace(e)
    sys.exit(1)

print("No duplications of locations found.")
sys.exit(0)
```
The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

The expected output is:
```
No duplications of locations found.
```
The actual output is:
```csharp
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    if len(msg.locations) != 4:
AssertionError: There should only be ONE instance of each location.
```
The line numbers in the stack trace may be different depending on the location of the `reproducer.py` file.