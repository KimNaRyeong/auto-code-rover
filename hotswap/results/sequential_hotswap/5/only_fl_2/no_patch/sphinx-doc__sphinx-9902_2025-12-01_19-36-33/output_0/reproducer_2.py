import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    # Arrange
    from unittest.mock import patch
    import my_library.module1

    # Act & Assert
    with patch("my_library.module1.Unit", new=object):
        assert my_library.module1.mol.__module__ == "my_library.module1"
        assert my_library.module1.mol.__qualname__ == "my_library.module1.mol"
        assert my_library.module1.mol.__dict__ == {"__module__": "my_library.module1", "__qualname__": "my_library.module1.mol", "value": "'mol'"}
        assert my_library.module1.mol._type_ == my_library.module1.mol.__class__
        assert my_library.module1.mol._type_.__name__ == "object"
        assert my_library.module1.mol._type_ is not my_library.module1.Unit
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
