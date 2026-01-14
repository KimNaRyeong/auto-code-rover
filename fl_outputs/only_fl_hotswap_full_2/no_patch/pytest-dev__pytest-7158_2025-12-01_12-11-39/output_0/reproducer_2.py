import sys
import subprocess
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_pytest(args):
    try:
        subprocess.check_call(["pytest"] + args)
    except subprocess.CalledProcessError as e:
        raise AssertionError(f"Pytest exited with non-zero exit code: {e.returncode}") from e

def test_skip():
    pytest.skip("no way of currently testing this")

if __name__ == "__main__":
    if "pytest" not in sys.modules:
        print("Installing pytest...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
        print("pytest installed.", file=sys.stderr)

    try:
        run_pytest(["-rs", "../my_tests/test1.py"])
    except AssertionError as e:
        assert e.args[0].startswith("SKIPPED [1] ../my_tests/test1.py"), "Incorrect skip message format"
        print_stacktrace(e)
        sys.exit(1)
