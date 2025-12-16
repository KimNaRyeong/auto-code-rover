import sys
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

def function_with_dict_param(dict_param: dict[str, str] = None):
    """
    :param dict(str, str) dict_param: (optional)
    """
    pass

def test_docstring():
    # Get the docstring of the function
    docstring = function_with_dict_param.__doc__

    # Check if the docstring contains the incorrect rendering
    if "dict(str," in docstring:
        raise AssertionError(f"Incorrect docstring rendering: {docstring}")

try:
    # Call the test function
    test_docstring()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

# If the script reaches this point, it means that the issue was not reproduced
sys.exit(0)
