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

try:
    from pylint import epylint as lint
except ImportError as e:
    print_stacktrace(e)
    sys.exit("Failed to import pylint modules necessary for running pyreverse.")

# Prepare arguments for the current cumbersome approach
name = "MyProject"
files = "example1.py example2.py"  # Assuming files are in the current working directory
pyreverse_cmd = f'pyreverse -o png -p {name} {files}'

# Try the current cumbersome approach
try:
    (pylint_stdout, pylint_stderr) = lint.py_run(pyreverse_cmd, return_std=True)
    output = pylint_stdout.getvalue()
    error = pylint_stderr.getvalue()
    if error:
        raise RuntimeError("Pyreverse encountered an error:\n" + error)
    if "no module named" in output.lower() or "error" in output.lower():
        raise AssertionError("Pyreverse did not execute as expected.")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

# Mock a desired solution API call - this will always fail because it doesn't exist
try:
    lint.pyreverse(output=lint.PNG, project=name, files=files.split())
except AttributeError as e:  # AttributeError used as a stand-in for any failure due to the call not existing
    print_stacktrace(e)
    raise AssertionError("The desired pyreverse API is not implemented.") from e
except Exception as e:
    print_stacktrace(e)
    sys.exit("Unexpected error while attempting the desired pyreverse API call.")
