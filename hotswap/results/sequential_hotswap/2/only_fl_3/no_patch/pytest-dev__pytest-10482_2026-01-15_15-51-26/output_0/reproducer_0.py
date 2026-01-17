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

def run_pytest():
    # Write the test file.
    test_code = """\
import pytest

def test_0(bar):
    assert 0

@pytest.fixture
def bar():
    if True:  # Simulate the condition is met to skip the test.
        pytest.skip("Skipping")
"""
    test_file = "test_foo.py"
    with open(test_file, "w") as f:
        f.write(test_code)

    # Write the conftest.py file.
    conftest_code = """\
import pytest
"""
    conftest_file = "conftest.py"
    with open(conftest_file, "w") as f:
        f.write(conftest_code)

    # Run pytest
    result = subprocess.run(["pytest", ".", "-rs"], capture_output=True, text=True)
    print(result.stdout)
    if "test_0" not in result.stdout:
        raise AssertionError("Test name not shown in the pytest skip summary")

try:
    run_pytest()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue not present.")
    sys.exit(0)
