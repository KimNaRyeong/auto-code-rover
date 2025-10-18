```python
# reproducer.py
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

def test_parse_greek_character():
    from sympy.parsing.mathematica import parse_mathematica

    try:
        output = parse_mathematica('λ')
        # If the function returns without raising an Exception, we assume it's fixed.
        print("Issue seems to be fixed.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        # Raising an AssertionError to indicate issue presence.
        raise AssertionError("Failed to parse Greek characters using parse_mathematica.")

if __name__ == "__main__":
    test_parse_greek_character()
```

This script is designed to reproduce the issue described:
- It will attempt to parse a Greek character using `parse_mathematica` from the `sympy.parsing.mathematica` module.
- If the parsing fails and raises an exception, the script will catch this exception and use the `print_stacktrace` function to print the stack trace, making the line numbers and error message clear.
- An `AssertionError` is raised afterward to explicitly indicate that the issue is present.
- In the event that `parse_mathematica` no longer raises an exception (implying that the issue has been fixed), the script will print a message indicating that the issue seems to be fixed and exit with code 0.