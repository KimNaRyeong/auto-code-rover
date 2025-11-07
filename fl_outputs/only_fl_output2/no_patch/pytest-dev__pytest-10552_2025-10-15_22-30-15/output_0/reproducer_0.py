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


def reproduce_issue():
    test_code = """
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
    
    with open("temp_test.py", "w") as test_file:
        test_file.write(test_code)

    try:
        result = subprocess.run(
            ["pytest", "temp_test.py", "-v"], capture_output=True, text=True
        )
        output = result.stdout + result.stderr
        
        if "cannot collect" in output:
            raise AssertionError("Found 'cannot collect' warning(s)")
        if "silently fails to run" in output:  # Placeholder example; adjust as needed
            raise AssertionError("Found silently failed to run tests")
        if result.returncode != 0:
            raise AssertionError("Pytest did not exit cleanly")

        print("No issues detected with pytest staticmethod or classmethod test collection.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        subprocess.run(["rm", "temp_test.py"])


if __name__ == "__main__":
    try:
        reproduce_issue()
        sys.exit(0)  # No errors occurred
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
