Here is the standalone Python file `reproducer.py` to reproduce the issue:

```py
import sympy as sp

def main():
    try:
        poly = sp.Poly(1.2*sp.Symbol('x')*sp.Symbol('y')*sp.Symbol('z'), sp.Symbol('x'), domain='RR[y,z]')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected Poly to be created without raising an error")

if __name__ == "__main__":
    main()
```

To run the script, execute `python3 reproducer.py`. This should reproduce the issue and print a stack trace.