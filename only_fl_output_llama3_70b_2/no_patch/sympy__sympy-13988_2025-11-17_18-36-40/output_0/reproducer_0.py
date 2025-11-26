import sympy as sm

def test_as_sum():
    t, t0, tf = sm.symbols('t, t0, tf')
    x = sm.Function('x')(t)
    y = sm.Function('y')(t)
    J = sm.Integral((x - y)**2, (t, t0, tf))
    result = J.as_sum(20, 'trapezoid')

    # Check if the result is an evaluated expression
    assert isinstance(result, sm.Sum), "as_sum() should return a Sum object"

def main():
    try:
        test_as_sum()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
