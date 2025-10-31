import sympy
from sympy.core.power import isqrt

def main():
    n = 4503599761588224
    s = isqrt(n)
    assert s**2 <= n, "isqrt gives incorrect results"
    print_stacktrace(AssertionError("isqrt gives incorrect results"))

n = 9999999999999999
s = isqrt(n)
assert s**2 <= n, "isqrt gives incorrect results"
print_stacktrace(AssertionError("isqrt gives incorrect results"))

if __name__ == "__main__":
    main()
