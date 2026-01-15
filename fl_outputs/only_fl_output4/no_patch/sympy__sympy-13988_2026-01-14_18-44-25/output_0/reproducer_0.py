# reproducer.py
import sympy as sm

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

def main():
    t, t0, tf = sm.symbols('t t0 tf')
    x = sm.Function('x')(t)
    y = sm.Function('y')(t)
    J = sm.Integral((x - y)**2, (t, t0, tf))
    sum_result = J.as_sum(20, 'trapezoid')

    try:
        assert isinstance(sum_result, sm.Sum), "Result is not a Sum object"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("The issue is fixed.")
        raise SystemExit(0)

if __name__ == "__main__":
    main()
