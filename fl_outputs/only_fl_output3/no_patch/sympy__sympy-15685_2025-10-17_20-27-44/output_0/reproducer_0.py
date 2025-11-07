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
    from sympy.physics.units import Quantity, voltage, current, ohm, convert_to

    try:
        # Setting up the quantities
        vs = Quantity('vs')
        vs.set_dimension(voltage)
        vs_i = Quantity('vs_i')
        vs_i.set_dimension(current)

        # Converting the result of division to ohms
        result = convert_to(vs/vs_i, ohm)

        # Assert that the result is exactly ohm, not ohm/1000
        assert result == ohm, f"Expected result to be 'ohm', but got '{result}' instead."
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # Re-raising the exception to allow for exit code handling

if __name__ == "__main__":
    main()
