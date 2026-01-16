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
    from sympy import symbols, Integral, sin, exp, oo, refine, Q, Piecewise, Abs, arg
    
    # Define symbols
    a, x = symbols('a x', real=True)

    # Define the integral
    J = Integral(sin(x) * exp(-a * x), (x, 0, oo))
    
    # Perform the integral
    result = J.doit()

    # Attempt to refine the result with the assumption that 'a' is positive
    refined_result = refine(result, Q.positive(a))
    
    # Check if refinement works as expected
    try:
        # The refinement should not return the original form if a is positive
        assert refined_result != result, "Refinement did not alter the result under the assumption that 'a' is positive."
        
        # Test specific assumptions
        test_abs_a = refine(abs(a), Q.positive(a))
        test_arg_a = refine(arg(a), Q.positive(a))
        
        # Assert correct refinements
        assert test_abs_a == a, f"Expected refine(abs(a), Q.positive(a)) to equal 'a', got {test_abs_a}"
        assert test_arg_a == 0, f"Expected refine(arg(a), Q.positive(a)) to equal '0', got {test_arg_a}"
    
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
