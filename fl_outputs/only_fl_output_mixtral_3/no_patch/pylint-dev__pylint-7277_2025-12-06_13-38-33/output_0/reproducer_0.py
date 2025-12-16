import sys
import runpy
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

def test_pylint_run():
    sys.path.insert(0, "something")
    try:
        runpy.run_module('pylint', run_name="__main__", alter_sys=True)
    except Exception as e:
        assert False, "Pylint should not remove the first item from sys.path"
        print_stacktrace(e)

if __name__ == "__main__":
    test_pylint_run()
