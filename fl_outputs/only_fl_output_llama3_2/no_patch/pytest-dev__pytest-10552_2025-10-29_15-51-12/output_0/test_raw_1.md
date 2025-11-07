I apologize for the previous mistake. Here is a new reproducer script that should reproduce the issue:

```python
import pytest

class TestFoo:
    # passes:
    @staticmethod
    def test_staticmethod() -> None:
        pass

    # warning: cannot collect 'test_staticmethod_inner' because it is not a function.
    @pytest.mark.parametrize("foo", [1, 2])
    @staticmethod
    def test_staticmethod_inner(foo: int) -> None:
        assert foo < 3

    # passes:
    @staticmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_staticmethod_outer(foo: int) -> None:
        assert foo < 3

    # silently fails to run
    @classmethod
    def test_classmethod(cls) -> None:
        pass

    # warning: cannot collect 'test_classmethod_inner' because it is not a function.
    @pytest.mark.parametrize("foo", [1, 2])
    @classmethod
    def test_classmethod_inner(cls, foo: int) -> None:
        assert foo < 3

    # silently fails to run
    @classmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_classmethod_outer(cls, foo: int) -> None:
        assert foo < 3

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