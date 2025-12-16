import sys
import traceback
from typing import List, Tuple

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
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

def main():
    text = "Type"
    locations = [
        ("../../manual/render/shader_nodes/vector/vector_rotate.rst", 38),
        ("../../manual/modeling/hair.rst", 0),
        ("../../manual/modeling/hair.rst", 0),
        ("../../manual/modeling/hair.rst", 0),
        ("../../manual/modeling/metas/properties.rst", 92),
    ]
    uuids = []

    msg = Message(text, locations, uuids)

    # Replace the following line with `msg.locations = uniqueLocation(locations)` to fix the issue
    msg.locations = locations

    # Check if the issue is present
    assert len(locations) != len(set(locations)), "Locations should be duplicated"
    assert len(msg.locations) == len(set(msg.locations)), "Locations should not be duplicated"

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
