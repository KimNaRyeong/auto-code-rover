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
    try:
        from sympy import Symbol, S, oo, integrate
        x = Symbol('x')
        result = integrate(1 / (1 + x**4)**(S(1)/4), [x, 0, oo])
        print("Integration successful:", result)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced successfully.") from None

if __name__ == '__main__':
    main()
```