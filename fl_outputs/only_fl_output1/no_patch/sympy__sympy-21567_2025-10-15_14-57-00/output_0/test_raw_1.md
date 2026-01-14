Given the previous misunderstanding, I now recognize your exact need. Let's adjust the Python script to print an error traceback if it encounters the described issue and exit gracefully with code 0 if the script confirms the issue is present, to match your requirements closely:

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


def main():
    from sympy import symbols, expand_trig, csch, sech, sin, cos, tanh

    x, y = symbols('x y')

    try:
        # Confirm tanh expansion works as expected
        assert expand_trig(tanh(x + y)) == (tanh(x) + tanh(y)) / (1 + tanh(x) * tanh(y)), "tanh expansion did not work as expected"

        # Attempt to expand csch and sech should not return the unmodified input
        assert expand_trig(csch(x + y)) != csch(x + y), "csch expansion did not modify the input"
        assert expand_trig(sech(x + y)) != sech(x + y), "sech expansion did not modify the input"

        # This part of the script should not be reached if the above assertions fail
        print("Issue has been fixed.")
    except AssertionError as e:
        # An assertion error indicates the issue is present
        print_stacktrace(e)
        # Exit with zero to indicate successful reproduction of the issue (not a script error)
        exit(0)


if __name__ == "__main__":
    main()
```
This script uses the provided `print_stacktrace` function to display a detailed traceback when encountering an `AssertionError`, suggesting that the issue described is present. It specifically checks the functionality that should be affected by the issue (`expand_trig` for `csch` and `sech`) and compares it to an expected behavior (i.e., the expression is modified upon expansion, similar to how it works for `tanh`). The script exits with code 0 if the issue is confirmed, aligned with your specification for handling the reproduction of the issue.