 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
def sqf_list(poly):
    """Compute the square-free factorization of a polynomial."""
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def sqf_part(poly):
        """Return a tuple (coeffs, powers) where poly = product(coeffs**powers)."""
        coeffs, powers = [], []
        for fac in poly.factor():
            c = fac[0]
            exp = fac[1]
            while exp:
                if exp & 1:
                    coeffs.append(c)
                    powers.append(1)
              