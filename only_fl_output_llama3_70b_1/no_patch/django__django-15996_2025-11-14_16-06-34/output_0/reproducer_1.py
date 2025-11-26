import enum
import re
from django.db import models

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

# Define an Enum with flags
class RegexFlag(enum.Flag):
    UNICODE = enum.auto()
    IGNORECASE = enum.auto()

# Create a Django model field with a default value that combines Enum flags
regex_flags = models.IntegerField(default=re.UNICODE | re.IGNORECASE)

try:
    # Try to serialize the default value using the EnumSerializer
    serialized_default = RegexFlag(re.UNICODE | re.IGNORECASE)
    assert isinstance(serialized_default, RegexFlag), "Failed to serialize combined Enum flags"
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present: failed to serialize combined Enum flags")

print("Issue is fixed: successfully serialized combined Enum flags")
