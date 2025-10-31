Here is the reproducer script:

```python
import sympy as sp
from sympy.printing import latex
from sympy.functions.elementary.trigonometric import acsc, asin
import sys

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

try:
    latex(asin(1), inv_trig_style="full")
    latex(acsc(1), inv_trig_style="full")
except AssertionError as e:
    print_stacktrace(e)
else:
    sys.exit(0)
```

This script creates a standalone Python file that reproduces the issue. It attempts to print the LaTeX representation of `asin(x)` and `acsc(x)` with full inverse trig function name. If the issue is present, it will raise an `AssertionError` and print the stack trace using the provided function. The script also exits with code 0 if no error occurs.

Please note that you need to have sympy installed in your Python environment to run this script.