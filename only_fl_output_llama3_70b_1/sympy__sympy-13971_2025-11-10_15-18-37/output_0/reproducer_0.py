import sympy as sp
import io
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

k, m, n = sp.symbols('k m n', integer=True)
sp.init_printing()

formula = sp.SeqFormula(n**2, (n,0,sp.oo))
output = io.StringIO()
print(formula, file=output)
result = output.getvalue().strip()

expected_output = "[0, 1, 4, 9, …]"
if result != expected_output:
    raise AssertionError(f"Expected '{expected_output}' but got '{result}'")

sys.exit(0)
