import subprocess
import tempfile
import os

def create_test_files(test_directory):
    # Create a sample test file
    test_file_path = os.path.join(test_directory, "test_foo.py")
    with open(test_file_path, 'w') as f:
        f.write("""
def test_0(bar):
    assert 0
""")

    # Create a conftest.py with a fixture that skips
    conftest_path = os.path.join(test_directory, "conftest.py")
    with open(conftest_path, 'w') as f:
        f.write("""
import pytest

@pytest.fixture
def bar():
    pytest.skip("Skipping")
""")

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

def run_pytest_and_check_output(test_directory):
    try:
        result = subprocess.run(["pytest", test_directory, "-rs"], capture_output=True, text=True, check=True)
        output = result.stdout

        # Check if the output specifies which test was skipped
        if "test_foo.py::test_0 SKIPPED" not in output:
            raise AssertionError("Skipped test name is not shown in pytest summary.")

    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue is fixed, exiting with code 0.")
        exit(0)

def main():
    with tempfile.TemporaryDirectory() as test_directory:
        create_test_files(test_directory)
        run_pytest_and_check_output(test_directory)

if __name__ == "__main__":
    main()
