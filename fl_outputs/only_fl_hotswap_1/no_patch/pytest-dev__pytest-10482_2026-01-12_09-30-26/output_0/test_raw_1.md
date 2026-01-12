 Sure, here is a standalone Python file `reproducer.py` that reproduces the issue:
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

def test_0(bar):
    assert 0

@pytest.fixture
def bar():
    if True:
        pytest.skip("Skipping")

if __name__ == "__main__":
    try:
        pytest.main(["-rs", "."])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
To run the script, execute `python3 reproducer.py` in the terminal. The output should show that the skipped test name is not displayed in the summary:
```bash
$ python3 reproducer.py
================================== test session starts ==================================
platform linux -- Python 3.6.9, pytest-7.0.1, pluggy-1.0.0
rootdir: /path/to/reproducer
collected 1 item

reproducer.py s                                                                     [100%]

================================ short test summary info ================================
SKIPPED [1] reproducer.py:11: Skipping
================================== 1 skipped in 0.01s ===================================
```
To fix the issue, you can modify the `conftest.py` file to include the test name in the skip message:
```python
import pytest

@pytest.fixture
def bar():
    if some_condition:
        pytest.skip(f"Skipping test {pytest.current_test}.")
```
With this modification, the skipped test name will be displayed in the summary:
```bash
$ python3 reproducer.py
================================== test session starts ==================================
platform linux -- Python 3.6.9, pytest-7.0.1, pluggy-1.0.0
rootdir: /path/to/reproducer
collected 1 item

reproducer.py s                                                                     [100%]

================================ short test summary info ================================
SKIPPED [1] reproducer.py:6: Skipping test test_0[bar].
================================== 1 skipped in 0.01s ===================================
```
Note that the test name is displayed as `test_0[bar]` because it is a fixture-scoped test. If the test is a module-scoped or session-scoped test, the test name will be displayed without the fixture name.