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

def setup_test_environment():
    current_path = os.getcwd()
    test_dir_path = os.path.join(current_path, "pytest")
    test_file_dir_path = os.path.join(current_path, "my_tests")
    test_file_path = os.path.join(test_file_dir_path, "test1.py")

    os.makedirs(test_dir_path, exist_ok=True)
    os.makedirs(test_file_dir_path, exist_ok=True)

    with open(test_file_path, "w") as test_file:
        test_file.write("""
import pytest

@pytest.mark.skip(reason="no way of currently testing this")
def test_example():
    assert True
""")

    return test_dir_path, test_file_dir_path, test_file_path

def run_pytest_and_check_output(invocation_dir, test_file_path):
    command = f"pytest -rs {test_file_path}"
    result = subprocess.run(command, cwd=invocation_dir, capture_output=True, text=True, shell=True)
    output = result.stdout

    expected_phrase = f"SKIPPED [1] {test_file_path}:3: no way of currently testing this"
    if expected_phrase not in output:
        raise AssertionError("The output does not contain the expected skip report path.")

def clean_up(test_dir_path, test_file_dir_path):
    subprocess.run(f"rm -rf {test_dir_path}", shell=True)
    subprocess.run(f"rm -rf {test_file_dir_path}", shell=True)

def main():
    try:
        test_dir_path, test_file_dir_path, test_file_path = setup_test_environment()
        run_pytest_and_check_output(test_dir_path, test_file_path)
        print("Issue not present. Relative path in skip report appears correctly.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 to indicate failure due to AssertionError.
    finally:
        clean_up(test_dir_path, test_file_dir_path)

if __name__ == "__main__":
    sys.exit(main())  # If no exception, exits with 0 indicating success.
