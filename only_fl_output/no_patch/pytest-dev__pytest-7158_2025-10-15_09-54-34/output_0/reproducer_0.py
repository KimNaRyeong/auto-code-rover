import os
import subprocess
import shutil

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

def setup_test_environment():
    # Create test directories and file
    os.makedirs("my_tests", exist_ok=True)
    os.makedirs("pytest", exist_ok=True)

    test_file_path = "my_tests/test1.py"
    with open(test_file_path, "w") as test_file:
        test_file.writelines([
            "import pytest\n",
            "@pytest.mark.skip(reason='no way of currently testing this')\n",
            "def test_example():\n",
            "    assert True\n"
        ])

def run_pytest_and_check_output():
    # Change working directory to pytest
    os.chdir("pytest")

    # Run pytest command
    result = subprocess.run(["pytest", "-rs", "../my_tests/test1.py"], capture_output=True, text=True)

    # Return to the root directory
    os.chdir("../")

    return result

def main():
    try:
        # Setup test environment
        setup_test_environment()

        # Invoke pytest and capture its output
        result = run_pytest_and_check_output()

        # Check if the output has the correct relative path in the skip report
        expected_output_fragment = "../my_tests/test1.py:3: no way of currently testing this"
        assert expected_output_fragment in result.stdout, "Skip report does not show the correct relative path."

        print("Issue not found: Skip report shows the correct relative path.")

    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with an error code
    finally:
        # Cleanup: Consider commenting out this during debugging, so you can inspect the files
        shutil.rmtree("my_tests")
        shutil.rmtree("pytest")

if __name__ == "__main__":
    main()
