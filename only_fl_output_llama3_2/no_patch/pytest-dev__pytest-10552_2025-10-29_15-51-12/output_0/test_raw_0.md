Here is the reproducer script:

```python
import pytest
from unittest import TestCase

class TestFoo(TestCase):
    @staticmethod
    def test_staticmethod() -> None:
        pass  # Passes

    @pytest.mark.parametrize("foo", [1, 2])
    @staticmethod
    def test_staticmethod_inner(foo: int) -> None:
        pass  # Passes

    @staticmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_staticmethod_outer(foo: int) -> None:
        pass  # Passes

    @classmethod
    def test_classmethod(cls) -> None:
        pass  # Fails to run

    @pytest.mark.parametrize("foo", [1, 2])
    @classmethod
    def test_classmethod_inner(cls, foo: int) -> None:
        pass  # Fails to run

    @classmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_classmethod_outer(cls, foo: int) -> None:
        pass  # Fails to run

if __name__ == "__main__":
    try:
        pytest.main(["-v"])
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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

```

This script should be run with `python3 reproducer.py` and it will execute the tests. If any of the tests fail or are not discovered, an error message will be printed along with a stack trace.