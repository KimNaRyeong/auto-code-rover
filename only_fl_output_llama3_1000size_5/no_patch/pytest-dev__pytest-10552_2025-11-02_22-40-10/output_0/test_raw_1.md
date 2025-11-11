Here is the reproducer script:

```python
import pytest

def test_staticmethod():
    pass  # passes

@pytest.mark.parametrize("foo", [1, 2])
def test_staticmethod_inner(foo: int):
    assert foo < 3

@staticmethod
@pytest.mark.parametrize("foo", [1, 2])
def test_staticmethod_outer(foo: int):
    assert foo < 3

class TestFoo:
    @classmethod
    def test_classmethod(cls):
        pass  # silently fails to run

    @pytest.mark.parametrize("foo", [1, 2])
    @classmethod
    def test_classmethod_inner(cls, foo: int):
        pass  # silently fails to run

    @classmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_classmethod_outer(cls, foo: int):
        pass  # silently fails to run

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
    pytest.main()
except SystemExit as e:
    if e.code != 0:
        raise
    print_stacktrace(e)
```

This script should be run with `python3 reproducer.py`.