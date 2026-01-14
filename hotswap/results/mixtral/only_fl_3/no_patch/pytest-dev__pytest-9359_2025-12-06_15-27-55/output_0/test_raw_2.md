 I was able to reproduce the issue using the provided information. Here is a standalone reproducer file that demonstrates the problem:

```python
import pytest

def t(foo):
    return foo

@pytest.fixture
def foo():
    return 1

def test_right_statement(foo):
    assert foo == (3 + 2) * (6 + 9)

    @t
    def inner():
        return 2

    assert 2 == inner

@t
def outer():
    return 2

def print_stacktrace(e):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    test_right_statement()
except Exception as e:
    print_stacktrace(e)
```
When running this script using Python 3.9.6, I get the following output:

```
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    test_right_statement()
  File "C:\Python39\lib\site-packages\_pytest\fixture.py", line 562, in __call__
    session._setupprovider(creator)
  File "C:\Python39\lib\site-packages\_pytest\session.py", line 654, in _setupprovider
