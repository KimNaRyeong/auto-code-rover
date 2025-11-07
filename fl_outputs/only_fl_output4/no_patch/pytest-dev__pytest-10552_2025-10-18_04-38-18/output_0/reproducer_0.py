import subprocess
import tempfile
import os

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

def run_test_script():
    test_script = """
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

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "test_issue.py")
        with open(test_file, "w") as f:
            f.write(test_script)
        
        result = subprocess.run(["pytest", test_file, "-v"], capture_output=True, text=True)
        output = result.stdout + result.stderr

        # Checking if the problematic tests were not run or any unexpected warnings occurred.
        issues = [
            "cannot collect 'test_classmethod_inner' because it is not a function.",
            "cannot collect 'test_classmethod_outer' because it is not a function.",
            "cannot collect 'test_staticmethod_inner' because it is not a function."
        ]
        num_expected_tests = 6
        passed_tests = output.count("PASSED")

        if any(issue in output for issue in issues) or passed_tests != num_expected_tests:
            raise AssertionError("Pytest did not properly handle staticmethod or classmethod tests as expected.")
        else:
            print("All tests detected and executed as expected.")

try:
    run_test_script()
except Exception as e:
    print_stacktrace(e)
    exit(1)
else:
    exit(0)
