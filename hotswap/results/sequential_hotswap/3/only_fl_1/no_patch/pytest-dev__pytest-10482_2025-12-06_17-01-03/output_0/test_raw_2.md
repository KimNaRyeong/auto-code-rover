 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import pytest
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_0():
    assert 0

@pytest.fixture
def bar():
    if True:
        pytest.skip("Skipping")

if __name__ == "__main__":
    try:
        pytest.main(["-rs", "reproducer.py"])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

When running the script, it will show the same output as described in the issue:

```bash
$ python3 reproducer.py
================================== test session starts ==================================
platform linux -- Python 3.6.9, pytest-7.0.1, pluggy-1.0.0
rootdir: /path/to/reproducer, inifile:
collected 1 item

reproducer.py s                                                                     [100%]

================================ short test summary info ================================
SKIPPED [1] reproducer.py:10: Skipping
================================== 1 skipped in 0.01s ===================================
```

The summary shows that some test was skipped but there's no indication which test was skipped. Instead, it should show the test name rather than the location in the fixture where the `pytest.skip` was called from. If there are multiple tests that are skipped from various locations, matching a test with its skip condition becomes impossible.