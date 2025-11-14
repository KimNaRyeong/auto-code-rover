Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy as sp

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

def reproduce_issue():
    try:
        mathml1 = sp.printing.mathml(sp.acoth(x))
        mathml2 = sp.printing.mathml(sp.acsc(x))
        mathml3 = sp.printing.mathml(sp.asec(x))
        assert mathml1 == '<apply><arccoth/><ci>x</ci></apply>'
        assert mathml2 == '<apply><arccsc/><ci>x</ci></apply>'
        assert mathml3 == '<apply><arcsec/><ci>x</ci></apply>'
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    x = sp.Symbol('x')
    reproduce_issue()
```

To run the script, execute `python3 reproducer.py` in the terminal. If the issue is present, it will raise an `AssertionError`, print a stack trace of the issue, and exit with code 1.