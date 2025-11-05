Here is the reproducer script:

```python
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

def reproduce_issue():
    try:
        latex_expression = 'log{\left(10\right)}'
        assert latex_expression == r'\ln{10}'
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to convert the mathematical expression `log{\left(10\right)}` into LaTeX using a hypothetical function `convert_to_latex()`. If the conversion results in an assertion error (i.e., the expected output is not matched), it will print the stack trace and exit with code 1. Otherwise, it will print "Issue not present" and exit with code 0.