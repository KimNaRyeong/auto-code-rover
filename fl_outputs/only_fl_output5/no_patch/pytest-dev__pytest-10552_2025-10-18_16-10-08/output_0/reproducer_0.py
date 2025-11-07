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

def run_pytest_on_file():
    # Create a temporary Python file with the pytest code.
    pytest_code = """
import pytest

class TestFoo:
    @staticmethod
    def test_staticmethod() -> None:
        foo = 0
        assert foo < 3

    @pytest.mark.parametrize("foo", [1, 2])
    @staticmethod
    def test_staticmethod_inner(foo: int) -> None:
        assert foo < 3

    @staticmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_staticmethod_outer(foo: int) -> None:
        assert foo < 3

    @classmethod
    def test_classmethod(cls) -> None:
        foo = 0
        assert foo < 3

    @pytest.mark.parametrize("foo", [1, 2])
    @classmethod
    def test_classmethod_inner(cls, foo: int) -> None:
        assert foo < 3

    @classmethod
    @pytest.mark.parametrize("foo", [1, 2])
    def test_classmethod_outer(cls, foo: int) -> None:
        assert foo < 3
"""
    with open("temp_test.py", "w") as f:
        f.write(pytest_code)

    # Run pytest on the created file and capture the output.
    result = subprocess.run(["pytest", "temp_test.py", "-v"], capture_output=True, text=True)

    # Check for the known issues in pytest output.
    if "cannot collect 'test_staticmethod_inner' because it is not a function." not in result.stderr:
        raise AssertionError("Expected warning about test_staticmethod_inner not being a function is missing")
    if "cannot collect 'test_classmethod_inner' because it is not a function." not in result.stderr:
        raise AssertionError("Expected warning about test_classmethod_inner not being a function is missing")
    if "TestFoo::test_classmethod " in result.stdout or "TestFoo::test_classmethod_outer" in result.stdout:
        raise AssertionError("Class method tests should either be run and visible or a clear error/warning should be displayed")

    # Clean up
    subprocess.run(["rm", "temp_test.py"])

try:
    run_pytest_on_file()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error status if the issue is present.
else:
    print("No issue detected, all tests are handled as expected.")
    sys.exit(0)
