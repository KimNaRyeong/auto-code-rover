import math
from sympy.core.power import isqrt

def test_isqrt(n, expected):
    result = isqrt(n)
    assert result ** 2 <= n, f"Expected {expected} but got {result}"
    print(f"Test passed for input {n}")

def main():
    try:
        test_isqrt(4503599761588224, 67108864)
        test_isqrt(9999999999999999, 99999999)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
