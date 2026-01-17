import subprocess
import sys
import os
import tempfile

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

def check_issue_and_print_trace():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file_path = os.path.join(temp_dir, 'test_foo.py')
        conftest_file_path = os.path.join(temp_dir, 'conftest.py')

        # Create a test file
        with open(test_file_path, 'w') as test_file:
            test_file.write("""
def test_0(bar):
    assert 0
""")

        # Create a conftest.py file with a fixture
        with open(conftest_file_path, 'w') as conftest_file:
            conftest_file.write("""
import pytest

@pytest.fixture
def bar():
    some_condition = True
    if some_condition:
        pytest.skip("Skipping")
""")

        try:
            # Run Pytest and capture the output
            result = subprocess.run(['pytest', temp_dir, '-rs'], text=True, capture_output=True)
            output = result.stdout
            
            # Check if the test name appears next to the skip reason in the summary
            if not 'test_0' in output:
                raise AssertionError("Test name not shown in skip summary")

        except Exception as e:
            print_stacktrace(e)
            sys.exit(1)

    print("Issue not present. Exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    check_issue_and_print_trace()
