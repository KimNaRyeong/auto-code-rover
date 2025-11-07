import subprocess
import os
import sys

# Function to print the stack trace of an exception
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

def setup_test_environment():
    os.makedirs("my_tests", exist_ok=True)
    with open("my_tests/test1.py", "w") as f:
        f.write("""
import pytest

@pytest.mark.skip(reason="no way of currently testing this")
def test_example():
    assert True
""")

    if not os.path.exists("pytest"):
        os.mkdir("pytest")

def run_pytest_and_check_output():
    # Move to the pytest directory
    os.chdir("pytest")
    # Execute pytest and capture the output
    result = subprocess.run(["pytest", "-rs", "../my_tests/test1.py"], capture_output=True, text=True)
    os.chdir("..")  # Move back to the root directory
    
    # Check if the output contains the correct path
    if "SKIPPED [1] ../my_tests/test1.py:3" not in result.stdout:
        raise AssertionError("Pytest skip report does not show the correct relative path.")

def main():
    try:
        setup_test_environment()
        run_pytest_and_check_output()
        print("The issue is fixed.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
