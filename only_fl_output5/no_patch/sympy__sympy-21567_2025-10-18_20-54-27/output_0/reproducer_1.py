from sympy import symbols, expand_trig, csch, sech, csc, tanh, sin, cos
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

def verify_expansion():
    x, y = symbols('x y')
    # Testing expansion for tanh as a reference
    tanh_expansion = expand_trig(tanh(x + y))
    assert tanh_expansion == (tanh(x) + tanh(y))/(1 + tanh(x)*tanh(y)), "tanh expansion did not match"

    # Testing expansion for csc, which should work as referenced
    csc_expansion = expand_trig(csc(x + y))
    assert csc_expansion == 1/(sin(x)*cos(y) + sin(y)*cos(x)), "csc expansion did not match"

    # Testing csch and sech expansions, which are known to fail initially
    try:
        csch_expansion = expand_trig(csch(x + y))
        sech_expansion = expand_trig(sech(x + y))
        # The expected behavior is that the result should not be equal to the unexpanded form
        assert csch_expansion != csch(x + y), "csch did not expand"
        assert sech_expansion != sech(x + y), "sech did not expand"
        print("Issue is fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        # Re-raise to make sure we exit with a non-zero code if the issue is not fixed
        raise

if __name__ == "__main__":
    try:
        verify_expansion()
    except AssertionError:
        sys.exit(1)
    sys.exit(0)
