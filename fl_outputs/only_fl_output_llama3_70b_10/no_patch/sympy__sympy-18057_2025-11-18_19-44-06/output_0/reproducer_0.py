import sympy

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

class C:
    def __repr__(self):
        return 'x.y'

try:
    _ = sympy.Symbol('x') == C()
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Sympy incorrectly attempts to eval reprs in its __eq__ method")

try:
    class C:
        def __repr__(self):
            return 'x'
    assert sympy.Symbol('x') != C()
except AssertionError:
    pass
else:
    raise AssertionError("Unknown object whose repr is `x` incorrectly compares as equal to a sympy symbol x")
