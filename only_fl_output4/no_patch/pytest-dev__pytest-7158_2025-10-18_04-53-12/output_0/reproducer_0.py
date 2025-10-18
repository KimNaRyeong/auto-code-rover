import os
import subprocess
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

def create_test_file(test_directory: str, test_file_name: str):
    if not os.path.exists(test_directory):
        os.makedirs(test_directory)
    test_file_path = os.path.join(test_directory, test_file_name)
    with open(test_file_path, "w") as file:
        file.write("""
import pytest

@pytest.mark.skip(reason="no way of currently testing this")
def test_sample():
    pass
""")
    return test_file_path

def run_pytest_on_file(test_file_path: str):
    invocation_directory = "pytest_invocation_dir"
    if not os.path.exists(invocation_directory):
        os.makedirs(invocation_directory)
    command = ["pytest", "-rs", test_file_path]
    result = subprocess.run(command, cwd=invocation_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def verify_skip_message(result, test_file_path):
    expected_message = f"SKIPPED [1] {test_file_path}:3: no way of currently testing this"
    if expected_message not in result.stderr:
        raise AssertionError(f"Expected message not found in pytest output: {expected_message}")

def main():
    try:
        test_directory = "../my_tests"
        test_file_name = "test1.py"
        test_file_path = create_test_file(test_directory, test_file_name)
        result = run_pytest_on_file(test_file_path)
        verify_skip_message(result, test_file_path)
        print("The issue has been fixed.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
