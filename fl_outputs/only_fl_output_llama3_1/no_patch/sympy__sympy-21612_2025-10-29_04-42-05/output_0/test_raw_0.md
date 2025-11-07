Here is the reproducer script:

```python
import sympy
from sympy.parsing.latex import parse_latex
import traceback
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
    expected = '((a**3 + b)/c)/(1/(c**2))'
    actual = str(parse_latex('\\frac{\\frac{a^3+b}{c}}{\\frac{1}{c^2}}'))
    assert actual == expected, "Latex parsing of fractions yields wrong expression due to missing brackets"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script will run the `parse_latex` function with the given LaTeX expression and compare the result with the expected output. If the actual output does not match the expected output, it will raise an `AssertionError`, which is caught by the script and prints a stack trace using the provided `print_stacktrace` function. The script then exits with code 1 to indicate that the test failed.