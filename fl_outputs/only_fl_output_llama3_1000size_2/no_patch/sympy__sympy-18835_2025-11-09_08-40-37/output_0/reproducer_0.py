import sys
from collections import Counter

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_uniq_modifies_list():
    original_count = Counter('THISTLE')
    for i in list(original_count):
        if i == 'T':
            original_count.pop(i)
        else:
            break
    assert len(original_count) == 0, "Error: Dictionary changed size during iteration"

try:
    test_uniq_modifies_list()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
