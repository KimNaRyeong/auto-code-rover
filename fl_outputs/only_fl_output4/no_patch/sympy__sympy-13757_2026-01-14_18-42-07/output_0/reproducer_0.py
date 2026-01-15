from sympy import Poly, symbols, S
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = symbols('x')
    
    try:
        # This should evaluate to Poly(x**2, x, domain='ZZ')
        result_1 = Poly(x) * x
        assert str(Poly(x) * x) == str(Poly(x**2, x, domain='ZZ')), "Multiplying Poly by symbol does not evaluate correctly"
        
        # Failing cases
        # This should also evaluate to Poly(x**2, x, domain='ZZ'), but it doesn't
        result_2 = x * Poly(x)
        assert str(x * Poly(x)) == str(Poly(x**2, x, domain='ZZ')), "Multiplying symbol by Poly does not evaluate correctly"
        
        result_3 = -2 * Poly(x)
        assert str(-2 * Poly(x)) == str(Poly(-2*x, x, domain='ZZ')), "Multiplying integer by Poly does not evaluate correctly"
        
        result_4 = S(-2) * Poly(x)
        assert str(S(-2) * Poly(x)) == str(Poly(-2*x, x, domain='ZZ')), "Multiplying SymPy Integer by Poly does not evaluate correctly"
        
        result_5 = Poly(x) * S(-2)
        assert str(Poly(x) * S(-2)) == str(Poly(-2*x, x, domain='ZZ')), "Multiplying Poly by SymPy Integer does not evaluate correctly"
    
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("All tests passed successfully!")

if __name__ == '__main__':
    main()
