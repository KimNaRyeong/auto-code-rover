import os
import subprocess
import sys

def setup_test_environment():
    # Create test directories and conftest.py files
    os.makedirs('unit_test', exist_ok=True)
    os.makedirs('test', exist_ok=True)
    conftest_content = """
import pytest

def pytest_addoption(parser):
    parser.addoption("--run-podman", action="store_true", default=False, help="run podman tests")
"""
    with open('unit_test/conftest.py', 'w') as f:
        f.write(conftest_content)
    with open('test/conftest.py', 'w') as f:
        f.write(conftest_content)
    
def clean_test_environment():
    subprocess.run(["rm", "-rf", "unit_test", "test"], check=True)

def run_pytest():
    # Attempt to run pytest on one of the test directories
    try:
        import pytest
        result = pytest.main(['unit_test', '--run-podman'])
        assert result == 0, "pytest run did not complete successfully."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An error occurred during pytest execution.") from e

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
    
if __name__ == "__main__":
    setup_test_environment()
    try:
        run_pytest()  # This should raise an AssertionError if the issue is present
        print("No issue detected. Exiting with code 0.")
    finally:
        clean_test_environment()
    sys.exit(0)
