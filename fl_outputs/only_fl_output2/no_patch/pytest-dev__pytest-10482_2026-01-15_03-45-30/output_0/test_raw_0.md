The following Python script, `reproducer.py`, is crafted to reproduce the issue as described. The script dynamically creates a test module and a fixture in a `conftest.py` file, then runs pytest on these using the subprocess module. It checks the output of the pytest command to see if the test name is absent from the skipped tests summary. If the issue is present (the test name is not shown), it raises an `AssertionError`; otherwise, it will just indicate that the issue is fixed.

Paste the contents into a file named `reproducer.py` and execute it with `python3`.

```python
import subprocess
import os

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

def main():
    test_code = """
def test_example(bar):
    assert 0
"""

    conftest_code = """
import pytest

@pytest.fixture
def bar():
    pytest.skip("Skipping for demonstration")
"""

    # Write the test and conftest files
    with open("test_example.py", "w") as f:
        f.write(test_code)

    with open("conftest.py", "w") as f:
        f.write(conftest_code)

    try:
        # Run pytest and capture the output
        result = subprocess.run(["pytest", ".", "-rs"], capture_output=True, text=True)
        output = result.stdout

        # Check if the test name is present in the output
        if "test_example" not in output:
            raise AssertionError("Test name is not shown in the skipped test summary.")

        print("The issue is fixed. Test name is shown in the skipped test summary.")

    except Exception as e:
        print_stacktrace(e)
        os.remove("test_example.py")
        os.remove("conftest.py")
        exit(1)

    # Cleanup
    os.remove("test_example.py")
    os.remove("conftest.py")

if __name__ == "__main__":
    main()
```

Before running this script, ensure you have pytest installed in your environment (`pip install pytest`) and that your Python version and pytest version match those mentioned in the issue (although the script does not specifically check for the Python or pytest version, it assumes the environment is correctly set up as described). The script checks for the presence of the test name in the skipped tests output and uses that to determine if the issue is present.