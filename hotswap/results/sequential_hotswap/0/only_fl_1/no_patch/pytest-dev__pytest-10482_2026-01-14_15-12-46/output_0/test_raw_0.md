Creating a standalone Python script that reproduces the issue as described involves a bit of creativity, since we need to simulate running pytest and catching the output, within a Python script itself. To address this, I will create a script that programmatically invokes pytest on a separate test file we generate on-the-fly. This approach allows us to encapsulate the entire reproduction scenario within a single executable script, while still accurately reflecting the issue described.

Please note, this script assumes you have `pytest` installed in your Python environment. If not, you'll need to install it first using `pip install pytest`.

```python
import os
import subprocess
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Create test files
    test_dir = "./temp_pytest_reproducer"
    os.makedirs(test_dir, exist_ok=True)
    with open(os.path.join(test_dir, "test_foo.py"), "w") as f:
        f.write("""
def test_0(bar):
    assert 0
""")

    with open(os.path.join(test_dir, "conftest.py"), "w") as f:
        f.write("""
import pytest

@pytest.fixture
def bar():
    some_condition = True
    if some_condition:
        pytest.skip("Skipping")
""")

    # Run pytest programmatically
    try:
        result = subprocess.run(["pytest", test_dir, "-rs"], capture_output=True, text=True)
        output = result.stdout + result.stderr

        # Check if the issue is present
        if "test_foo.py::test_0" not in output:
            raise AssertionError("Test name not shown in skip summary")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    # Cleanup
    finally:
        if os.path.exists(test_dir):
            for root, dirs, files in os.walk(test_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(test_dir)

    print("Issue is not present. Exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

This script dynamically creates a temporary directory with the necessary test file and fixture definition, then runs pytest against this directory capturing its output. It checks the output for the presence of the test name alongside the skip reason. If the expected output isn't found, it raises an `AssertionError`. Regardless of the test outcome, it cleans up after itself by deleting the temporary files and directory it created.