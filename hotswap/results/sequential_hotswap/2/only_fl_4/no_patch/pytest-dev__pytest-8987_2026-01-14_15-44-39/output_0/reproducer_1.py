import subprocess
import traceback
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

def run_test():
    """
    This function attempts to reproduce the issue by running a pytest command
    with a test name that includes a backslash.
    """
    test_file_content = """
import pytest

@pytest.mark.parametrize("input,output", [("5\\n10\\n", "16\\n")])
def test_solution(input, output):
    assert input != output  # Dummy assertion for demonstration
"""
    filename = "test_reproducer.py"

    # Write the test content to a file
    with open(filename, "w") as f:
        f.write(test_file_content)
    
    # Build the command to run pytest with a pattern that includes an escaped character
    command = ["pytest", "-k", r"test_solution[5\\n10\\n-16\\n]", filename]
    
    try:
        # Execute the pytest command
        result = subprocess.run(command, text=True, capture_output=True)
        if "unexpected character \"\\" in result.stderr or result.returncode != 0:
            # If the specific error message is found, the issue is present
            error_msg = "Issue reproduced: pytest '-k' does not work with '\\'"
            print(error_msg)
            raise AssertionError(error_msg)
        else:
            print("Issue seems to be fixed or not reproduced.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    run_test()
