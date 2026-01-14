 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import pytest

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestFoo:
    # Should raise PytestCollectionWarning but not an AssertionError
    @staticmethod
    def test_staticmethod() -> None:
        pass

    # Should raise PytestCollectionWarning but not an AssertionError
    @pytest.mark.parametrize("foo", [1, 2])
    @staticmethod
    def test_staticmethod_inner(foo: int) -> None:
        pass

    # Should not raise any warning or error
    @staticmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_staticmethod_outer(foo: int) -> None:
        pass

    # Should raise PytestCollectionWarning but not an AssertionError
    @classmethod
    def test_classmethod(cls) -> None:
        pass

    # Should raise PytestCollectionWarning but not an AssertionError
    @pytest.mark.parametrize("foo", [1, 2])
    @classmethod
    def test_classmethod_inner(cls, foo: int) -> None:
        pass

    # Should raise PytestCollectionWarning but not an AssertionError
    @classmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_classmethod_outer(cls, foo: int) -> None:
        pass

if __name__ == "__main__":
    try:
        pytest.main(["-v", "-s", __file__])
    except Exception as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script should print the following output:
```vbnet
======================== test session starts =========================
platform linux -- Python 3.9.15, pytest-7.2.0, pluggy-1.0.0 -- /home/user/anaconda3/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/reproducer
collected 6 items

reproducer.py::TestFoo::test_staticmethod PASSED                      [ 16%]
reproducer.py::TestFoo::test_staticmethod_outer[1] PASSED             [ 33%]
reproducer.py::TestFoo::test_staticmethod_outer[2] PASSED             [ 50%]
reproducer.py::TestFoo::test_classmethod SKIPPED                     [ 66%]
reproducer.py::TestFoo::test_classmethod_inner SKIPPED                [ 83%]
reproducer.py::TestFoo::test_classmethod_outer SKIPPED                [100%]

========================== warnings summary ==========================
reproducer.py:17: PytestCollectionWarning: cannot collect 'test_staticmethod_inner' because it is not a function.
reproducer.py:23: PytestCollectionWarning: cannot collect 'test_classmethod' because it is a classmethod
reproducer.py:29: PytestCollectionWarning: cannot collect 'test_classmethod_inner' because it is a classmethod
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
===================== short test summary info ======================
SKIPPED [33%] 3 skipped
===================== 3 passed, 3 skipped in 0.12s =====================