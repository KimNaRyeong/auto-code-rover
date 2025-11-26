import sympy as sm

def test_as_sum_issue():
    t, t0, tf = sm.symbols('t, t0, tf')
    x = sm.Function('x')(t)
    y = sm.Function('y')(t)
    J = sm.Integral((x - y)**2, (t, t0, tf))
    result = J.as_sum(20, 'trapezoid')

    # Check if the result is an evaluated expression
    assert isinstance(result, sm.Add), "Integral.as_sum() should output a Sum object"
    assert not any(isinstance(arg, sm.Sum) for arg in result.args), "Integral.as_sum() should output a Sum object"

def main():
    try:
        test_as_sum_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == "__main__":
    main()
