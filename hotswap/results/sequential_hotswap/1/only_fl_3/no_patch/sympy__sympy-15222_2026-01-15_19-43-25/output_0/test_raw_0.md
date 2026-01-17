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

def test_subs_hashing():
    from sympy import symbols, Subs

    x, y, a, z = symbols('x y a z')

    expr1 = Subs(x + y, (a,), (4,))
    expr2 = Subs(x + y, (a,), (a,)).subs(a, z)
    
    # Check if the result of the substitution matches the expected output
    assert expr1 == expr2, "Subs hashing problem detected"

if __name__ == "__main__":
    try:
        test_subs_hashing()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
```