import enum
import re
from enum import Enum, auto

class RegexFlag(Enum):
    UNICODE = auto()
    IGNORECASE = auto()

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

try:
    regex_flags = re.UNICODE | re.IGNORECASE
    serialized_regex_flags = [flag.name for flag in RegexFlag]
    deserialized_regex_flags = getattr(RegexFlag, '|'.join(serialized_regex_flags))
    assert deserialized_regex_flags == regex_flags
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
else:
    print("Issue is fixed")
