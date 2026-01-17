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
    from sympy import MatrixSymbol, pprint, latex

    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)

    str_output = str(A - A*B - B)
    pretty_output = repr(pprint(A - A*B - B, use_unicode=False))  # Using `repr` to capture the output of `pprint`.
    latex_output = latex(A - A*B - B)

    # Checking output against the expected format.
    try:
        assert str_output == "A - A*B - B", f"str output mismatch: {str_output}"
        assert "-B + -A*B + A" in pretty_output, f"pretty output mismatch: {pretty_output}"
        assert latex_output == "A - A B - B", f"latex output mismatch: {latex_output}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```