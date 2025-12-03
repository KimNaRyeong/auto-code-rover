import sys
import traceback
import pytest

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_black():
    args = ['-m', 'pytest', '--black']
    result = pytest.main(args)
    assert result == 0, "Black plugin failed"

def test_checkdocs():
    args = ['-m', 'pytest']
    result = pytest.main(args)
    assert result == 0, "Checkdocs plugin failed"

try:
    test_black()
    test_checkdocs()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
