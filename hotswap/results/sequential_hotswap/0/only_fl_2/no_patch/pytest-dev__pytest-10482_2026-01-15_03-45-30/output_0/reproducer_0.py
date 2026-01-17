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
