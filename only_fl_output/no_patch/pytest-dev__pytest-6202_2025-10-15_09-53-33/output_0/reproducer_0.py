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

def run_pytest_check():
    test_content = """
        import pytest

        @pytest.mark.parametrize("a",["..["])
        def test_boo(a):
            assert 0
    """

    # Write test to a temporary file
    test_filename = 'temp_test.py'
    with open(test_filename, 'w') as f:
        f.write(test_content)
    
    # Run pytest with the test
    result = subprocess.run(['pytest', test_filename], capture_output=True, text=True)
    
    # Check for incorrectly formatted failure headline
    if '..[' in result.stdout or '..[' in result.stderr:
        print("Issue not present.")
        sys.exit(0)
    else:
        try:
            raise AssertionError("Failure headline incorrectly formatted.")
        except AssertionError as e:
            print_stacktrace(e)
            # Exiting with non-zero code to indicate failure for automation purposes.
            # Change to zero if you prefer it to exit cleanly after reporting.
            sys.exit(1)

if __name__ == "__main__":
    run_pytest_check()
