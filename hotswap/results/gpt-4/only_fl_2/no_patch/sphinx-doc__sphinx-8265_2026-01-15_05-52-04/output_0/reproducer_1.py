"""
reproducer.py
A script to detect if Sphinx correctly renders method signatures with default argument tuples.
"""

def reproducer_method(lines, color=(1, 1, 1), width=5, label=None, name=None):
    """
    Example method to reproduce Sphinx documentation issue.

    :param lines: A parameter.
    :param color: A tuple parameter with a default value. Expected to cause rendering issues.
    :param width: An integer parameter with a default value.
    :param label: A NoneType parameter with a default value, meant for labels.
    :param name: A NoneType parameter with a default value, meant for naming.
    """

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

def main():
    expected_signature = "reproducer_method(lines, color=(1, 1, 1), width=5, label=None, name=None)"
    actual_signature = reproducer_method.__doc__.split('\n')[3].strip()

    try:
        assert actual_signature == expected_signature, f"Signature mismatch.\nExpected: {expected_signature}\nGot: {actual_signature}"
        print("No issue detected. The method signature in the docstring is correctly rendered.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
