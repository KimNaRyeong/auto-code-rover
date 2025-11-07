```python
def main():
    from sympy import symbols, imageset, Lambda, I, S
    from sympy.abc import n

    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    print(f"S1: {S1}")
    
    try:
        # Check if 2 is in S1
        assert 2 not in S1, "2 should not be in S1, but it is found."
        print("Check 1 passed: 2 not in S1")

        # Check if 2 is in the intersection of S1 and Reals
        assert 2 not in S1.intersect(S.Reals), "2 should not be in the intersection of S1 and Reals, but it is found."
        print("Check 2 passed: 2 not in S1.intersect(Reals)")

        # Check the intersection of S1 and Reals
        intersection = S1.intersect(S.Reals)
        assert intersection == {-1, 1}, f"Intersection is wrong: expected {-1, 1}, got {intersection}"
        print("Check 3 passed: Intersection of S1 and Reals is correct")

    except AssertionError as e:
        print_stacktrace(e)
    
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

if __name__ == "__main__":
    main()
```
This script will raise an `AssertionError` if the issue described is present by checking whether the element `2` is incorrectly considered as part of set `S1` or its intersection with `Reals`. It also checks if the intersection of `S1` and `Reals` returns the correct set `{-1, 1}`. The script utilizes a custom `print_stacktrace` function to display the error trace clearly if an assertion fails.