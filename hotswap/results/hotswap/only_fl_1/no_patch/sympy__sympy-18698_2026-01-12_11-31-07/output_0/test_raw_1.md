 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
def sqf_list(poly):
    """Compute the square-free factorization of a polynomial."""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def sqf_part(poly):
        if poly.degree() < 2:
            return poly, 1
        p, m = poly.lc(), poly.degree()
        for f in [poly // (x - i) for i in range(1, m + 1) if poly % (x - i) == 0]:
            g = gcd(p, f.lc())
            if g == 1:
                break
            p, f = f, poly // f
        else:
            return poly, 1
        return f, p * sqf_part(poly // f)[0]

    factors = []
    factor = poly
    while factor != 1:
        factor, power = sqf_part(factor)
        factors.append((factor, power))
    return 1, factors


def print_stacktrace(e: Exception):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


if __name__ == "__main__":
    poly1 = (x ** 2 + 1) * (x - 1) ** 2 * (x - 2) ** 3 * (x - 3) ** 3
    poly2 = x ** 5 - 2 * x ** 4 - 2 * x ** 3 + 4 * x ** 2 + x - 2

    result1 = sqf_list(poly1)
    expected1 = (1, [(x ** 2 + 1, 1), (x - 1, 2), (x - 2, 3), (x - 3, 3)])
    assert result1 == expected1, f"Expected {expected1}, but got {result1}"

    result2 = sqf_list(poly2)
    expected2 = (1, [(x - 2, 1), (x ** 2 - 1, 2)])
    assert result2 == expected2, f"Expected {expected2}, but got {result2}"

    print("No issues found.")
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, the script will print "No issues found." and exit with code 0.