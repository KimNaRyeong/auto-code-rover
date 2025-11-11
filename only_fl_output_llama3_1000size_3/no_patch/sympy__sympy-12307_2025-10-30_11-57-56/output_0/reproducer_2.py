import sympy as sp
from sympy.abc import x

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
    import sympy as sp
    from sympy.abc import x
    from sympy.utilities.codegen import write_c_code

    code = write_c_code(sp.sign(x), 'sign', 'f')
    with open('sign.c', 'w') as f:
        f.write(code)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
else:
    print("Issue not reproduced, exiting with code 0.")
    exit(0)
